"""Career chatbot: TF-IDF retrieval over a knowledge base + optional Claude answer (RAG)."""
import logging
from typing import Dict, List, Optional, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from . import config

log = logging.getLogger("careerguide.rag")

KNOWLEDGE_BASE: List[Dict[str, str]] = [
    {"title": "Resume: structure", "text": "A strong resume is one page for under ten years of experience. Order: header with contact links, 2-line summary, skills, projects or experience, education. Lead every bullet with a strong action verb and end with a measurable result."},
    {"title": "Resume: bullet formula", "text": "Use the formula: Accomplished X, as measured by Y, by doing Z. Example: Reduced API latency 35% by adding Redis caching to the recommendation endpoint. Avoid vague phrases like responsible for or worked on."},
    {"title": "Resume: projects for students", "text": "Without work experience, projects carry your resume. Include 2-3 projects with a link to the repository, the tech stack, the problem solved and one measurable outcome. Deploy at least one project so recruiters can click a live demo."},
    {"title": "ATS keywords", "text": "Applicant tracking systems scan for keywords from the job description. Mirror the exact skill names from the posting where truthful, use standard section headings, avoid tables and graphics, and submit as PDF or docx as requested."},
    {"title": "Interview preparation", "text": "Prepare for technical rounds with data structures and algorithms practice, then role-specific topics such as SQL queries for analysts or system design for backend roles. For behavioural rounds use the STAR method: situation, task, action, result."},
    {"title": "Building a portfolio", "text": "A portfolio of three focused projects beats ten tutorials. Pick problems you care about, write a clear README with screenshots, document trade-offs, and keep commit history clean. Writing short blog posts about what you learned improves visibility."},
    {"title": "Switching careers into AI", "text": "To move into AI, build strong Python and statistics foundations first, then machine learning with scikit-learn, then deep learning or LLM application development. Ship end-to-end projects: data, model, API, and a simple UI. Contribute to open source or Kaggle for proof of work."},
    {"title": "Data analyst path", "text": "Data analysts need SQL first, then spreadsheet fluency, then a BI tool such as Power BI or Tableau, then Python with pandas. Practise by analysing public datasets and publishing a dashboard with a written summary of findings."},
    {"title": "Improving a skill from intermediate to advanced", "text": "To move from intermediate to advanced, stop following tutorials and build something real. Learn the internals, performance and testing side of the skill, read other people's code, and teach or write about it. Advanced means you can design solutions and explain trade-offs."},
    {"title": "Networking and referrals", "text": "Referrals often outperform cold applications. Engage with engineers on LinkedIn, join local meetups and hackathons, and send short specific messages that mention a project of theirs. Ask for advice rather than a job."},
    {"title": "Internships and first job", "text": "For a first role, apply broadly to internships and junior positions, tailor the resume for each, and follow up after one week. Hackathons, open-source contributions and campus placement drives are high-yield channels for freshers."},
    {"title": "Certifications: when they help", "text": "Certifications help most when you lack experience or are moving into cloud, security or data roles. They complement but do not replace projects. Choose vendor certifications aligned with the tools in the job postings you target."},
    {"title": "Salary negotiation", "text": "Research the market range for the role and city, wait for an offer before discussing numbers when possible, and negotiate total compensation including bonus and learning budget. Be polite, specific and ready to justify your ask with evidence."},
    {"title": "Learning plan habits", "text": "Study in consistent short blocks, five to ten hours per week beats occasional marathons. Alternate learning with building: after each topic, apply it in a small project. Review progress monthly and adjust the roadmap."},
    {"title": "Cover letters", "text": "Keep cover letters under 250 words. Open with why this company, connect two of your achievements to the role's top requirements, and close with a clear call to action. Customise every letter; generic ones are ignored."},
]

_docs = [f"{d['title']}. {d['text']}" for d in KNOWLEDGE_BASE]
_vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
_mat = _vec.fit_transform(_docs)
_client = None


def _get_client():
    global _client
    if _client is None and config.ANTHROPIC_API_KEY:
        import anthropic
        _client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client


def retrieve(query: str, k: int = 3, min_score: float = 0.05) -> List[Dict[str, str]]:
    sims = cosine_similarity(_vec.transform([query]), _mat)[0]
    order = sims.argsort()[::-1][:k]
    return [KNOWLEDGE_BASE[i] for i in order if sims[i] >= min_score]


def _profile_summary(profile: Optional[Dict]) -> str:
    if not profile:
        return "No profile saved yet."
    levels = profile.get("levels", {})
    skills = profile.get("skills", []) + profile.get("extra_skills", [])
    skill_text = ", ".join(f"{s} ({levels.get(s, 'Beginner')})" for s in skills) or "none yet"
    return (f"Name: {profile.get('name') or 'n/a'}; Graduated: {profile.get('grad_year') or 'n/a'}; "
            f"Skills and levels: {skill_text}")


def answer(message: str, profile: Optional[Dict], history: List[Dict],
           mode: str = "career") -> Tuple[str, List[str], bool]:
    """Returns (reply, source_titles, llm_used)."""
    docs = retrieve(message)
    sources = [d["title"] for d in docs]
    context = "\n\n".join(f"[{d['title']}]\n{d['text']}" for d in docs) or "(no relevant notes)"

    client = _get_client()
    if client is not None:
        system = ("You are CareerGuide AI, a friendly, practical career coach. Ground your answers in the "
                "knowledge snippets and the user's profile. If they don't cover the question, say so and "
                "give honest general advice. Be concise and actionable.")
        if mode == "resume":
            system += (" The user wants resume help: give concrete rewrites with action verbs and "
                    "measurable results, and never invent experience they haven't stated.")
        msgs = [{"role": m["role"], "content": m["content"]}
                for m in history[-8:] if m["role"] in ("user", "assistant")]
        msgs.append({"role": "user", "content":
                    f"User profile:\n{_profile_summary(profile)}\n\nKnowledge snippets:\n{context}\n\nQuestion: {message}"})
        try:
            resp = client.messages.create(model=config.LLM_MODEL, max_tokens=800, system=system, messages=msgs)
            return resp.content[0].text, sources, True
        except Exception as exc:  # network, key, rate limit...
            log.error("LLM call failed: %s", exc)

    # No key (or the LLM call failed): answer from the retrieved notes directly
    if docs:
        body = "\n\n".join(f"**{d['title']}**: {d['text']}" for d in docs)
        return ("Here is what I found in the career knowledge base "
                "(add an ANTHROPIC_API_KEY to .env for conversational answers):\n\n" + body), sources, False
    return ("I don't have specific notes on that yet. Try asking about resumes, interviews, "
            "portfolios, certifications or learning plans."), sources, False