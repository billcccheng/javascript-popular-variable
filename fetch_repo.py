import base64
import json
import os
import requests

from git import Repo

popular_variable_dict = {}

def fetch_popular_repo():
    git_url = 'https://github.com/billcccheng/ptt-search.git'
    repo_dir = './repos/ptt-search'
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        Repo.clone_from(git_url, repo_dir)


    print(os.listdir(repo_dir))
    with open('./repos/ptt-search/app/index.js', 'r') as content_file:
        content = content_file.read()
        print(content)

def main():
    fetch_popular_repo()

if __name__ == "__main__":
    main()

