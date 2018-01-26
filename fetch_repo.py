import json
import os
import re
import requests

from git import Repo

popular_variable_dict = {}

def fetch_popular_repo():
    git_url = 'https://github.com/billcccheng/ptt-search.git'
    repo_dir = './repos/ptt-search'
    prog = re.compile('(?:const|var|let)\s+(\w+);?')

    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        Repo.clone_from(git_url, repo_dir)

    directories = []
    for _file in os.listdir(repo_dir):
        if os.path.isdir(repo_dir + '/' + _file):
            directories.append(_file)
    # print(directories)
    with open('./repos/ptt-search/app/components/App.js', 'r') as content_file:
        content = content_file.read()
        match = prog.findall(content)
        # print(match)

def main():
    fetch_popular_repo()

if __name__ == "__main__":
    main()

