import requests
import json
import uuid
import os

ONDEMAND_API_KEY = "VkBa1g7e3EsD2WAmyrSuMjNqPZ8s3OFI"
BASE_URL = "https://api.on-demand.io/chat/v1"

ENDPOINT_ID = "predefined-xai-grok4.1-fast"
REASONING_MODE = "grok-4-fast"

FULFILLMENT_PROMPTS = {
    "peer": """
You are a Knowledge-Base–Bound Peer Recommendation Engine.
Use ONLY provided context.
""",

    "rules": """
You are an Event Information Assistant.
Answer ONLY from provided rules/FAQ context.
""",

    "idea": """
You are an Idea Validation Assistant.
Output exactly 5 lines:
1. Originality score (0–10)
2. Feasibility score (0–10)
3. Technical depth score (0–10)
4. Alignment score (0–10)
5. Best matching track
""",

    "sentiment_internal": """
You are a Sentiment Signal Agent.

Analyze the text and output ONLY:
Sentiment: <Positive | Neutral | Negative>
Confidence Level: <High | Medium | Low>
Engagement Tone: <Curious | Confused | Confident | Stressed>
""",

    "engagement_activity": """
You are an Engagement Activity Tracker Agent.

Use ONLY structured GitHub activity data provided.

Output EXACTLY:
Activity Status: <Active | Low Activity | Inactive>
Last Commit: <timestamp or None>
Recent Commits (24h): <number>
Recent Commits (72h): <number>
Contributors: <number>
""",

    # ✅ ORCHESTRATION AGENT
    "orchestration": """
You are a Hackathon Team Orchestration Agent.

You receive historical signals for ONE team:
- Rules questions & answers
- GitHub engagement snapshots

Rules:
- Use ONLY provided context
- Do NOT infer missing data
- Do NOT speculate

Output EXACTLY:

Team Readiness: <High | Medium | Low>
Technical Momentum: <Active | Slowing | Inactive>
Engagement Pattern: <Concise phrase>
Risk Flags: <None or comma-separated list>
Suggested Host Action: <One short sentence>
"""
}

def call_agent(agent_type: str, context: str, query: str) -> str:
    if agent_type not in FULFILLMENT_PROMPTS:
        return f"Unknown agent type: {agent_type}"

    session_url = f"{BASE_URL}/sessions"
    headers = {
        "apikey": ONDEMAND_API_KEY,
        "Content-Type": "application/json"
    }

    session_payload = {
        "externalUserId": str(uuid.uuid4()),
        "agentIds": [],
        "contextMetadata": []
    }

    session_resp = requests.post(
        session_url,
        headers=headers,
        json=session_payload
    )

    if session_resp.status_code != 201:
        return "Failed to create session"

    session_id = session_resp.json()["data"]["id"]

    query_url = f"{BASE_URL}/sessions/{session_id}/query"

    payload = {
        "endpointId": ENDPOINT_ID,
        "query": f"Context:\n{context}\n\nUser Query:\n{query}",
        "responseMode": "sync",
        "reasoningMode": REASONING_MODE,
        "modelConfigs": {
            "fulfillmentPrompt": FULFILLMENT_PROMPTS[agent_type],
            "temperature": 0.2,
            "maxTokens": 500
        }
    }

    resp = requests.post(
        query_url,
        headers=headers,
        json=payload
    )

    if resp.status_code != 200:
        return "Agent execution failed"

    return resp.json()["data"]["answer"]

