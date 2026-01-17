import requests
from datetime import datetime, timezone

print("github_activity.py loaded")

GITHUB_API = "https://api.github.com"

GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json"
}

def parse_repo_url(repo_url: str):
    parts = repo_url.rstrip("/").split("/")
    return parts[-2], parts[-1]

def fetch_github_activity(repo_url: str):
    owner, repo = parse_repo_url(repo_url)

    repo_resp = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}",
        headers=GITHUB_HEADERS
    )

    if repo_resp.status_code != 200:
        return {"error": "Repository not accessible or not public"}

    repo_data = repo_resp.json()

    commits_resp = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}/commits",
        headers=GITHUB_HEADERS,
        params={"per_page": 30}
    )

    commits = commits_resp.json() if commits_resp.status_code == 200 else []

    now = datetime.now(timezone.utc)

    def hours_ago(commit):
        ts = commit["commit"]["committer"]["date"]
        commit_time = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return (now - commit_time).total_seconds() / 3600

    commits_24h = sum(1 for c in commits if hours_ago(c) <= 24)
    commits_72h = sum(1 for c in commits if hours_ago(c) <= 72)

    last_commit_time = commits[0]["commit"]["committer"]["date"] if commits else None

    contributors_resp = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}/contributors",
        headers=GITHUB_HEADERS
    )

    contributors = contributors_resp.json() if contributors_resp.status_code == 200 else []

    return {
        "public": not repo_data.get("private", True),
        "default_branch": repo_data.get("default_branch"),
        "total_commits_fetched": len(commits),
        "last_commit_time": last_commit_time,
        "commits_24h": commits_24h,
        "commits_72h": commits_72h,
        "contributors": len(contributors)
    }

