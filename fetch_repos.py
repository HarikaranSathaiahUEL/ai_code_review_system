import subprocess
import os
from github import Github

def fetch_github_repos(token, query, max_repos=5):
    g = Github(token)
    repos = g.search_repositories(query=query, sort='stars')
    repo_list = []
    for repo in repos[:max_repos]:
        repo_list.append(repo.clone_url)
    return repo_list

def clone_repo(repo_url, dest_dir):
    repo_name = repo_url.split("/")[-1].replace('.git', '')
    local_path = os.path.join(dest_dir, repo_name)

    if not os.path.exists(local_path):
        subprocess.run(['git', 'clone', repo_url, local_path])
    return local_path