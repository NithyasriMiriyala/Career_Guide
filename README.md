# Career_Guide

A personal career guidance app: it learns your skills, recommends roles, shows your skill gaps, builds a learning roadmap, and creates an ATS-friendly resume you can download as a PDF or Word file.

Built by **Nithyasri Miriyala** as a personal project.

---

## ✨ Features

| Page | What it does |
|---|---|
| 🏠 **Home** | Summary cards and a bar chart of jobs applied vs. skills. A floating **Ask CareerGuide AI** chatbot sits at the bottom-right. |
| 💼 **Recommendations** | Suggests job roles that match your skills, with a match score and direct links to apply. |
| 🧩 **Skill Gap** | Shows which skills you already know and which to improve, with a target level (Beginner, Intermediate, Advanced) for each. |
| 🗺️ **Learning Roadmap** | A top-to-bottom path of topics and subtopics from your current level to your target level. |
| 📄 **Resume Builder** | Builds a one-column, ATS-friendly resume, gives an ATS score with tips, suggests matching jobs, and downloads as **PDF**, **Word** or **text**. |
| 👤 **Profile** | Name, date of birth, graduation year, skills and a level for each skill. Saved to the database. |
| 💬 **Chatbot** | Answers career questions (RAG over a career knowledge base, optional Claude model) and can interview you to build a resume. |

The top menu turns into a slim, icon-only bar on the left when you scroll.

---

## 🧱 Tech stack

- **Frontend:** Streamlit (modular views, custom CSS, light-blue theme in `utils/theme.py`)
- **Backend:** FastAPI (REST API, business logic, CORS)
- **Database:** MongoDB Atlas with connection pooling and automatic retry (falls back to in-memory storage if no database is configured)
- **ML / AI:** scikit-learn (TF-IDF + cosine similarity) for matching and retrieval, optional Anthropic Claude for conversational answers
- **Documents:** ReportLab (PDF) and python-docx (Word)
- **Jobs:** Adzuna API for real listings, with LinkedIn / Naukri / Indeed search links as a fallback

```
Browser ──► Streamlit (app.py) ──► FastAPI (backend/) ──► MongoDB Atlas
                                        │
                                        ├─► scikit-learn (recommendations, retrieval)
                                        ├─► Adzuna API (real jobs)
                                        └─► Anthropic API (optional chatbot)
```

Streamlit calls the backend from the server side with `requests`, so the browser never talks to the API directly.

---

## 📁 Project structure

```
Career_Guide/
├── app.py                  # Streamlit entry point: top bar, navigation, routing
├── requirements.txt
├── .env                    # secrets (NOT committed)
├── backend/
│   ├── main.py             # FastAPI app, CORS, endpoints
│   ├── config.py           # settings from environment variables
│   ├── database.py         # MongoDB pooling + retry, in-memory fallback
│   ├── models.py           # pydantic request/response models
│   ├── rag.py              # TF-IDF retrieval + optional LLM answers
│   ├── recommender.py      # scikit-learn role matching
│   ├── data.py             # knowledge base and role data
│   └── jobs_router.py      # real job listings + application tracking
├── utils/
│   ├── api.py              # calls the backend from Streamlit
│   ├── theme.py            # CSS theme and navigation behaviour
│   ├── ats.py              # ATS-friendly resume text + ATS score
│   ├── resume_files.py     # PDF and Word export
│   ├── roadmap.py          # topics per skill and level
│   └── local_matcher.py    # local role matching
└── views/                  # one file per page
    ├── home.py
    ├── recommendations.py
    ├── skill_gap.py
    ├── roadmap.py
    ├── resume.py
    ├── profile.py
    └── chat_widget.py
```

---

## 🚀 Run it locally

**Requirements:** Python 3.11+ and (optionally) a free MongoDB Atlas cluster.

```bash
# 1. Clone and enter the project
git clone https://github.com/NithyasriMiriyala/Career_Guide.git
cd Career_Guide

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. Create your .env file (see the table below)
```

Start the two servers in **two terminals**, both with the virtual environment active:

```bash
# Terminal 1: backend
python -m uvicorn backend.main:app --reload --port 8000

# Terminal 2: frontend
streamlit run app.py
```

Then open <http://localhost:8501>. The API docs are at <http://127.0.0.1:8000/docs> and a health check is at <http://127.0.0.1:8000/health>.

> If `MONGO_URI` is empty, the backend uses in-memory storage and everything is lost when it restarts. `/health` shows `"database":"memory"` or `"database":"mongodb"`.

---

## 🔐 Environment variables

Create a `.env` file in the project root. **Never commit it** (it is in `.gitignore`).

```env
MONGO_URI=                      # mongodb+srv://user:password@cluster.mongodb.net/?appName=Cluster0
MONGO_DB_NAME=careerguide
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501,http://localhost:3000
API_BASE_URL=http://127.0.0.1:8000
ANTHROPIC_API_KEY=              # optional: conversational chatbot answers
LLM_MODEL=claude-sonnet-5-5
ADZUNA_APP_ID=                  # optional: live job listings
ADZUNA_APP_KEY=
ADZUNA_COUNTRY=in
```

| Variable | Purpose |
|---|---|
| `MONGO_URI` | MongoDB Atlas connection string. Empty means in-memory mode. |
| `MONGO_DB_NAME` | Database name. |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend URLs. Add your live frontend URL here. |
| `API_BASE_URL` | Where Streamlit finds the backend (your Render URL when deployed). |
| `ANTHROPIC_API_KEY` | Optional. Without it the chatbot returns the retrieved knowledge snippets. |
| `ADZUNA_*` | Optional. Without them, job cards link to LinkedIn, Naukri and Indeed searches. |

---

## 🔌 API overview

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Service, database and LLM status |
| GET | `/roles` | Available roles |
| PUT / GET | `/profiles`, `/profiles/{user_id}` | Save and load a profile |
| GET | `/recommendations/{user_id}` | Role recommendations |
| GET | `/skill-gap/{user_id}` | Skill gap for a role |
| GET | `/roadmap/{user_id}` | Learning roadmap |
| POST / GET | `/resume`, `/resume/{user_id}` | Save and load a resume |
| PUT / GET | `/progress` | Progress data |
| POST / GET | `/chat`, `/chat/{user_id}` | Chatbot messages and history |
| GET | `/jobs` | Real job listings (or search links) for given skills |
| POST / GET | `/applications`, `/applications/{user_id}` | Record "I applied" and read counts per skill and month |

Full interactive docs: `/docs`.

---

## ☁️ Deployment

| Part | Where | Notes |
|---|---|---|
| Database | **MongoDB Atlas** (free M0) | In Network Access, allow the host's IP (or `0.0.0.0/0` for simplicity). |
| Backend | **Render** web service | Build: `pip install -r requirements.txt` · Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` · Health check path: `/health` · Add the env vars above in Render's dashboard. |
| Frontend | **Streamlit Community Cloud** | Main file: `app.py` · Add `API_BASE_URL` (your Render URL) as a secret. |

After the frontend is live, add its URL to `CORS_ORIGINS` on the backend.

Free hosting tiers sleep when idle, so the first request after a quiet period can take about a minute.

---

## 🗄️ Where is my data?

With MongoDB Atlas connected, everything is stored in the `careerguide` database:

- `profiles`: saved profiles
- `resumes`: generated resumes
- `chats`: chatbot messages
- `applications`: jobs the user marked as applied

View it in Atlas under **Browse Collections**, or with MongoDB Compass using the same connection string.

---

## 🛠️ Status and ideas

- [x] Profile, Skill Gap, Roadmap, Resume Builder (PDF / Word), chatbot with resume interview
- [x] MongoDB Atlas with pooling and retry
- [x] Backend endpoints for real jobs and application tracking
- [x] Recommendations page: real job cards with Apply buttons
- [x] Home graph driven by real applications
- [x] Production deployment
- [x] Automated tests

---
