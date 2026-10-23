# 🎯 CareerGuide AI

A personal career guidance app for students. It learns your education, interests, skills and experience, recommends roles with a scikit-learn matcher, shows your skill gaps, builds a learning roadmap with certifications and project ideas, helps you find and track job and internship applications, and creates an ATS-friendly resume you can download as a PDF or Word file. A built-in chatbot answers questions about careers, the website and your skills.

Built by **Nithyasri Miriyala** as a personal project.

## 🌐 Live demo

- **App:** https://careerguide-x5mshkvwgjpa8veesm8yym.streamlit.app
- **API docs:** https://career-guide-bvsd.onrender.com/docs

The backend runs on a free Render instance, so the first request after a quiet period can take up to a minute to wake up.

---

## ✨ Features

| Page | What it does |
|---|---|
| 🔑 **Login** | Create an account or log in with email and password. Passwords are stored only as salted PBKDF2-SHA256 hashes, and five wrong attempts lock an account for five minutes. |
| 👤 **Profile** | Name, date of birth, graduation year, **education** (the interest choices change with it, for example ECE offers Embedded Systems & IoT, VLSI, Telecom), interests, career goal, experience level and experience notes, skills and a level for each skill. Saved to the database. |
| 🏠 **Home** | Summary cards and a chart of jobs applied versus skills completed, built from your real activity. A floating **Ask CareerGuide AI** chatbot sits at the bottom-right. |
| 💼 **Recommendations** | Ranks roles with a scikit-learn matcher (skills, skills found in your experience notes, interests, career goal) and explains each match. Below that, pick a role, a location and Jobs or Internships, and open ready-made searches on LinkedIn, Indeed, Naukri, Wellfound, Internshala, Glassdoor, Foundit and Google Jobs. Press **I applied ✅** to track an application. |
| 🧩 **Skill Gap** | Current level versus a target level for each skill, with a tick for skills you have completed. |
| 🗺️ **Learning Roadmap** | A top-to-bottom path from your current level to your target: topics, YouTube channels, certifications and project ideas at every stage. |
| 📄 **Resume Builder** | Requires the key fields (name, email, phone, skills, education, and experience or projects) before it scores anything. Then it gives an ATS score out of 100 with tips and downloads as **PDF**, **Word** or **text**. |
| 💬 **Chatbot** | Answers website questions, suggests roles from the skills you type or from your profile, runs a resume interview, and searches a career knowledge base. An optional Claude model makes answers conversational. |

The top menu turns into a slim, icon-only bar on the left when you scroll.

---

## 🧱 Tech stack

- **Frontend:** Streamlit (modular views, custom CSS, light-blue theme in `utils/theme.py`)
- **Backend:** FastAPI (REST API, business logic, CORS)
- **Database:** MongoDB Atlas with connection pooling and automatic retry (falls back to in-memory storage if no database is configured)
- **ML / AI:** scikit-learn (TF-IDF and cosine similarity) for role matching and knowledge retrieval, optional Anthropic Claude for conversational answers
- **Documents:** ReportLab (PDF) and python-docx (Word)
- **Jobs:** one-click search links for eight job portals, with application tracking
- **Tests:** pytest

```
Browser ──► Streamlit (app.py) ──► FastAPI (backend/) ──► MongoDB Atlas
                                        │
                                        ├─► scikit-learn (recommendations, retrieval)
                                        └─► Anthropic API (optional chatbot)
```

Streamlit calls the backend from the server side with `requests`, so the browser never talks to the API directly.

---

## 📁 Project structure

```
Career_Guide/
├── app.py                  # Streamlit entry point: login, top bar, profile dialog, routing
├── requirements.txt
├── .env                    # secrets (NOT committed)
├── backend/
│   ├── main.py             # FastAPI app, CORS, core endpoints, router wiring
│   ├── config.py           # settings from environment variables
│   ├── database.py         # MongoDB pooling + retry, in-memory fallback
│   ├── models.py           # pydantic request/response models
│   ├── auth.py             # password hashing, register/login, lockout
│   ├── auth_router.py      # POST /auth/register, POST /auth/login
│   ├── recommender.py      # scikit-learn role matching
│   ├── reco_router.py      # POST /recommend
│   ├── assistant.py        # rule-based chatbot answers (site help, skill-based roles)
│   ├── rag.py              # TF-IDF retrieval + optional LLM answers
│   ├── data.py             # knowledge base
│   └── jobs_router.py      # application tracking and skill progress
├── utils/
│   ├── api.py              # calls the backend from Streamlit
│   ├── theme.py            # CSS theme and navigation behaviour
│   ├── local_matcher.py    # roles, interests, education map (single source of roles)
│   ├── roadmap.py          # topics, channels, certifications, project ideas per skill
│   ├── ats.py              # ATS-friendly resume text + ATS score
│   └── resume_files.py     # PDF and Word export
├── views/                  # one file per page
│   ├── home.py
│   ├── recommendations.py
│   ├── skill_gap.py
│   ├── roadmap.py
│   ├── resume.py
│   └── chat_widget.py
└── tests/                  # pytest: recommender, assistant, education, auth
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

### Run the tests

```bash
python -m pytest -q
```

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
```

| Variable | Purpose |
|---|---|
| `MONGO_URI` | MongoDB Atlas connection string, all on one line. Empty means in-memory mode. |
| `MONGO_DB_NAME` | Database name. |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend URLs. Add your live frontend URL here. |
| `API_BASE_URL` | Where Streamlit finds the backend (your Render URL when deployed). |
| `ANTHROPIC_API_KEY` | Optional. Without it the chatbot uses rule-based answers and retrieved knowledge snippets. |

---

## 🔌 API overview

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Service, database and LLM status |
| POST | `/auth/register`, `/auth/login` | Create an account or log in (returns the user id) |
| PUT / GET | `/profiles`, `/profiles/{user_id}` | Save and load a profile |
| POST | `/recommend` | Rank roles with scikit-learn from skills, interests and career goal |
| POST / GET | `/resume`, `/resume/{user_id}` | Save and load a resume |
| POST / GET | `/chat`, `/chat/{user_id}` | Chatbot messages and history |
| POST / GET | `/applications`, `/applications/{user_id}` | Record "I applied" and read counts per skill and month |
| POST / GET | `/skill-progress`, `/skill-progress/{user_id}` | Tick skills as completed and read progress |

Full interactive docs: `/docs`.

---

## ☁️ Deployment

| Part | Where | Notes |
|---|---|---|
| Database | **MongoDB Atlas** (free M0) | In Network Access, allow `0.0.0.0/0` so Render can connect. |
| Backend | **Render** web service | Build: `pip install -r requirements.txt` · Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` · Health check path: `/health` · Add the env vars above in Render's Environment tab. |
| Frontend | **Streamlit Community Cloud** | Main file: `app.py` · Add `API_BASE_URL` (your Render URL) as a secret. |
| Keep-alive | **UptimeRobot** (optional) | An HTTP(s) monitor on `/health` every 5 minutes stops the free backend from sleeping. |

After the frontend is live, add its URL to `CORS_ORIGINS` on the backend. Every push to `main` redeploys both Render and Streamlit.

---

## 🗄️ Where is my data?

With MongoDB Atlas connected, everything is stored in the `careerguide` database (Atlas → Browse Collections):

- `users`: accounts (email, salted password hash, user id)
- `profiles`: saved profiles
- `resumes`: generated resumes
- `chats`: chatbot messages
- `applications`: jobs the user marked as applied
- `skill_progress`: skills the user ticked as completed

---

## 🛡️ Security notes

- Passwords are never stored in plain text. Each one is hashed with PBKDF2-SHA256 (200,000 rounds) and a random salt, and repeated wrong attempts lock the account for five minutes.
- New accounts get a random, unguessable user id. Accounts created before passwords existed keep their old id so their saved data stays available.
- **Known limitation:** the user id travels in the web address and the API does not check a session token on every request. Treat your full link like a key. Adding token-based sessions on every route is the next hardening step.

---

## 🧪 Tests

`tests/` covers the scikit-learn recommender, the chatbot's quick answers, the education-to-interests map and the password system (hashing, duplicate accounts, wrong passwords, lockout). Run them with `python -m pytest -q`.

---

## 🛠️ Status and ideas

- [x] Login with hashed passwords, profile with education, interests and experience
- [x] scikit-learn role recommender with reasons, and interests that follow the education
- [x] Job and internship search links for eight portals, with application tracking and a real Home graph
- [x] Skill Gap, Learning Roadmap with certifications and project ideas
- [x] Resume Builder with validation, ATS score, PDF and Word export
- [x] Chatbot with site help, skill-based role suggestions and a resume interview
- [x] MongoDB Atlas with pooling and retry, deployed on Render and Streamlit Cloud
- [x] Automated tests
---

## 📄 License

Personal project. All rights reserved unless a license file is added.