from fastapi import FastAPI, UploadFile
from rag import store_doc, retrieve_context
from ondemand import call_agent
from github_activity import fetch_github_activity
from db import init_db, get_conn
from datetime import datetime
import json

app = FastAPI()
init_db()

@app.post("/upload/{doc_type}")
async def upload_doc(doc_type: str, file: UploadFile):
    text = (await file.read()).decode("utf-8", errors="ignore")
    store_doc(doc_type, text)
    return {"status": "uploaded"}

@app.post("/query/{agent_type}")
def query(agent_type: str, query: str, team_id: str):
    context = retrieve_context(agent_type, query)
    response = call_agent(agent_type, context, query)

    if agent_type == "rules":
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO rules_queries
            (team_id, question, answer, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (team_id, query, response, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()

    return {"response": response}

@app.post("/internal/sentiment")
def internal_sentiment(text: str):
    response = call_agent(
        agent_type="sentiment_internal",
        context="",
        query=text
    )
    return {"sentiment_signal": response}

@app.post("/internal/github-activity")
def github_activity(repo_url: str, team_id: str):
    activity_data = fetch_github_activity(repo_url)

    if "error" in activity_data:
        return {"response": activity_data["error"]}

    engagement = call_agent(
        agent_type="engagement_activity",
        context=json.dumps(activity_data, indent=2),
        query="Analyze repository activity"
    )

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO github_activity
        (team_id, repo_url, activity_status,
         commits_24h, commits_72h,
         contributors, last_commit_time, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            team_id,
            repo_url,
            engagement,
            activity_data.get("commits_24h"),
            activity_data.get("commits_72h"),
            activity_data.get("contributors"),
            activity_data.get("last_commit_time"),
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
    conn.close()

    return {"response": engagement}

# ✅ ORCHESTRATION ENDPOINT
@app.post("/internal/orchestration")
def orchestration(team_id: str):
    conn = get_conn()
    cur = conn.cursor()

    rules = cur.execute(
        """
        SELECT question, answer
        FROM rules_queries
        WHERE team_id = ?
        ORDER BY timestamp DESC
        LIMIT 5
        """,
        (team_id,)
    ).fetchall()

    github = cur.execute(
        """
        SELECT activity_status, commits_24h, commits_72h, contributors
        FROM github_activity
        WHERE team_id = ?
        ORDER BY timestamp DESC
        LIMIT 5
        """,
        (team_id,)
    ).fetchall()

    conn.close()

    context = {
        "recent_rules_queries": rules,
        "recent_github_activity": github
    }

    overview = call_agent(
        agent_type="orchestration",
        context=json.dumps(context, indent=2),
        query="Generate team overview"
    )

    return {"overview": overview}

