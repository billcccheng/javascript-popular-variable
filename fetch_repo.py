import json
import os
import re
import requests

from git import Repo

popular_variable_dict = {}

def fetch_popular_repo():
    git_url = 'https://github.com/facebook/react.git'
    repo_dir = './repos/react'
    prog = re.compile('(?:const|var|let|function)\s+(\w+);?')

    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        Repo.clone_from(git_url, repo_dir)

    directories = [repo_dir]
    while directories:
        parent_dir = directories.pop()
        all_dir = next(os.walk(parent_dir))[1]
        for _dir in all_dir:
            if _dir == '.git': continue
            directories.append(parent_dir + '/' + _dir)
        for _file in os.listdir(parent_dir):
            if not _file.endswith(".js"): continue
            curr_file = parent_dir + '/' + _file
            with open(curr_file , 'r') as content_file:
                analyze_content(content_file, prog)

def analyze_content(contents, prog):
    content = contents.read()
    match = prog.findall(content)
    # TODO:
    # Plug the matches into the dictionary
    if match:
        match.sort()
        print(match)

def main():
    fetch_popular_repo()

if __name__ == "__main__":
    main()

