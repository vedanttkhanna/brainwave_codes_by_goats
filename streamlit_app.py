import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Hackathon Intelligence Platform",
    layout="wide"
)

st.title("Hackathon Intelligence Platform")

# =========================
# ROLE SELECTION
# =========================
role = st.sidebar.selectbox(
    "Select Role",
    ["User", "Host"]
)

# =====================================================
# HOST DASHBOARD
# =====================================================
if role == "Host":
    st.header("Host Dashboard")

    # ---------- FILE UPLOADS ----------
    st.subheader("Upload Knowledge Documents")

    col1, col2, col3 = st.columns(3)

    with col1:
        peer_doc = st.file_uploader("Upload Peer List", type=["txt"])
        if peer_doc:
            r = requests.post(
                f"{BACKEND_URL}/upload/peer",
                files={"file": peer_doc}
            )
            st.success("Peer document uploaded")

    with col2:
        rules_doc = st.file_uploader("Upload Rules / FAQs", type=["txt"])
        if rules_doc:
            r = requests.post(
                f"{BACKEND_URL}/upload/rules",
                files={"file": rules_doc}
            )
            st.success("Rules document uploaded")

    with col3:
        idea_doc = st.file_uploader("Upload Hackathon Tracks", type=["txt"])
        if idea_doc:
            r = requests.post(
                f"{BACKEND_URL}/upload/idea",
                files={"file": idea_doc}
            )
            st.success("Tracks document uploaded")

    st.divider()

    # ---------- GITHUB ACTIVITY ----------
    st.subheader("GitHub Activity Tracker")

    repo_url = st.text_input("GitHub Repository URL")
    team_id = st.text_input("Team ID (for tracking)")

    if st.button("Analyze GitHub Activity"):
        if repo_url and team_id:
            r = requests.post(
                f"{BACKEND_URL}/internal/github-activity",
                params={
                    "repo_url": repo_url,
                    "team_id": team_id
                }
            )
            st.subheader("GitHub Engagement Signal")
            st.write(r.json().get("response"))
        else:
            st.warning("Please provide both Repo URL and Team ID")

    st.divider()

    # ---------- ORCHESTRATION ----------
    st.subheader("Team Overview (Orchestration Agent)")

    orchestration_team = st.text_input(
        "Team ID for Overview",
        key="orchestration_team"
    )

    if st.button("Generate Team Overview"):
        if orchestration_team:
            r = requests.post(
                f"{BACKEND_URL}/internal/orchestration",
                params={"team_id": orchestration_team}
            )
            st.subheader("Team Overview")
            st.write(r.json().get("overview"))
        else:
            st.warning("Please enter a Team ID")

# =====================================================
# USER DASHBOARD
# =====================================================
else:
    st.header("Participant Dashboard")

    team_id = st.text_input("Enter your Team ID")

    st.divider()

    # ---------- PEER RECOMMENDATION ----------
    st.subheader("Peer Recommendation")

    peer_query = st.text_area(
        "Describe skills you are looking for",
        height=80
    )

    if st.button("Find Peers"):
        if peer_query and team_id:
            r = requests.post(
                f"{BACKEND_URL}/query/peer",
                params={
                    "query": peer_query,
                    "team_id": team_id
                }
            )
            st.write(r.json().get("response"))
        else:
            st.warning("Please enter query and Team ID")

    st.divider()

    # ---------- RULES / FAQ ----------
    st.subheader("Rules & FAQ Bot")

    rules_query = st.text_area(
        "Ask a question about rules or FAQs",
        height=80
    )

    if st.button("Ask Rules Bot"):
        if rules_query and team_id:
            r = requests.post(
                f"{BACKEND_URL}/query/rules",
                params={
                    "query": rules_query,
                    "team_id": team_id
                }
            )
            st.write(r.json().get("response"))
        else:
            st.warning("Please enter query and Team ID")

    st.divider()

    # ---------- IDEA EVALUATION ----------
    st.subheader("Idea Evaluation")

    idea_query = st.text_area(
        "Describe your hackathon idea",
        height=120
    )

    if st.button("Evaluate Idea"):
        if idea_query and team_id:
            r = requests.post(
                f"{BACKEND_URL}/query/idea",
                params={
                    "query": idea_query,
                    "team_id": team_id
                }
            )
            st.write(r.json().get("response"))
        else:
            st.warning("Please enter idea and Team ID")
