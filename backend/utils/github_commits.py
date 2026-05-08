from datetime import datetime, timezone

import requests
from flask import current_app


def get_today_commit_count():
    github_username = current_app.config.get("GITHUB_USERNAME", "")
    github_repos = current_app.config.get("GITHUB_REPOS", [])
    github_token = current_app.config.get("GITHUB_TOKEN", "")
    github_api_url = current_app.config.get("GITHUB_API_URL", "https://api.github.com")

    if not github_username or not github_repos:
        return 0

    headers = {"Accept": "application/vnd.github+json"}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    start_of_day = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    since_iso = start_of_day.isoformat().replace("+00:00", "Z")

    total_commits = 0
    for repo in github_repos:
        url = f"{github_api_url}/repos/{repo}/commits"
        params = {"author": github_username, "since": since_iso, "per_page": 100}

        while url:
            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)
            except requests.RequestException:
                break

            if response.status_code != 200:
                break

            commits = response.json()
            if isinstance(commits, list):
                total_commits += len(commits)

            next_url = None
            link_header = response.headers.get("Link", "")
            if 'rel="next"' in link_header:
                links = [part.strip() for part in link_header.split(",")]
                for link in links:
                    if 'rel="next"' in link:
                        next_url = link.split(";")[0].strip("<>")
                        break

            url = next_url
            params = None

    return total_commits
