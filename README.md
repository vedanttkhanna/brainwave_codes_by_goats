🚀 Hackathon Event Intelligence Platform

An end-to-end event intelligence and monitoring platform designed for hackathons.
The system helps participants, hosts, and organizers interact with rules, peers, ideas, and team activity in a structured, document-grounded, and auditable way.

✨ Key Features
👤 Participant Features

Peer Recommendation

Find suitable teammates based strictly on uploaded peer profiles

Skill matching is exact and document-bound (no hallucinations)

Rules & FAQ Assistant

Ask questions about hackathon rules and FAQs

Answers are generated only from the uploaded documents

Ambiguous cases are flagged for organizer clarification

Idea Evaluation

Get a structured 5-line evaluation of your hackathon idea:

Originality

Feasibility

Technical Depth

Track Alignment

Best Matching Track

Output is concise, consistent, and judge-friendly

🧑‍💼 Host / Organizer Features

Document Management

Upload:

Peer list

Rules & FAQs

Hackathon tracks

These documents power all RAG-based intelligence

GitHub Activity Tracker

Analyze public GitHub repositories

Track:

Recent commit activity (24h / 72h)

Last commit time

Contributor count

Converted into a structured engagement signal using an LLM agent

Team Orchestration (Overview Agent)

Aggregates:

Recent rules questions

GitHub activity history

Produces a high-level team status:

Team readiness

Technical momentum

Engagement pattern

Risk flags

Suggested host action

Hackathon Branding

Host can upload a hackathon logo

Logo is stored via a free media API (Imgur)

Displayed on the UI for both hosts and users (read-only for users)

🧠 Architecture Overview
Streamlit (Frontend UI)
        ↓
FastAPI (Backend API Layer)
        ↓
RAG Layer (Document Storage & Retrieval)
        ↓
LLM Agents (On-Demand Chat Sessions API)
        ↓
SQLite (Signals, Logs, History)

Core Design Principles

Document-grounded responses only

No assumptions or inferred permissions

Clear separation of concerns

Auditability for organizers

Fail-safe design (non-blocking features)

📁 Project Structure
final_app/
│
├── streamlit_app.py        # Frontend (User + Host dashboards)
├── main.py                 # FastAPI backend
├── ondemand.py             # LLM agent interface
├── rag.py                  # Document storage & retrieval
├── github_activity.py      # GitHub activity analysis
├── db.py                   # SQLite database layer
│
└── backend/
    └── storage/            # Uploaded documents (txt)

⚙️ Tech Stack

Frontend: Streamlit

Backend: FastAPI, Uvicorn

LLM API: On-Demand Chat Sessions API

RAG: Lightweight file-based retrieval

Database: SQLite

Media Storage: Imgur (free, anonymous uploads)

External Data: GitHub REST API

▶️ Running the Project
1. Install Dependencies
pip install fastapi uvicorn streamlit requests

2. Set Environment Variables
setx ONDEMAND_API_KEY "YOUR_ONDEMAND_API_KEY"
setx IMGUR_CLIENT_ID "YOUR_IMGUR_CLIENT_ID"


Restart the terminal after setting variables.

3. Start Backend
uvicorn main:app --reload

4. Start Frontend
streamlit run streamlit_app.py

🧪 Recommended Usage Flow
Host

Upload peer list, rules, and tracks

Upload hackathon logo (optional)

Monitor GitHub activity

Generate team overviews using orchestration

Participant

Enter team ID

Find peers

Ask rules/FAQ questions

Evaluate hackathon ideas

🔐 Safety & Compliance

No rule exploitation or bypass logic

All ambiguous cases are explicitly flagged

AI usage is transparent and bounded

No private GitHub data is accessed

Users cannot modify host-level assets

🎯 Use Cases

Hackathon organizers

University tech events

Student innovation challenges

Internal company hack days

AI-assisted event moderation

🚧 Future Enhancements

Authentication & role-based access

Judge dashboard

Analytics & charts for engagement

Track-specific evaluation weights

Multi-event support

