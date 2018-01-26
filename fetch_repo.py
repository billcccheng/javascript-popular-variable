import json
import os
import re
import requests

from git import Repo

popular_variable_dict = {}

def fetch_popular_repo():
    popular_repo_urls = []
    api_url = 'https://api.github.com/search/repositories?q=stars:%3E1+language:javascript&sort=stars&order=desc&type=Repositories%27'
    res = requests.get(api_url).json()
    for repo in res['items']:
        popular_repo_urls.append(repo['clone_url'])
        if len(popular_repo_urls) == 100: break
    return popular_repo_urls

def clone_repo(urls):
    prog = re.compile('(?:const|var|let|function)\s+(\w+);?')
    for url in urls:
        repo_name = re.findall('\/([^\/]+).git$', url)[0]
        repo_dir = './repos/' + repo_name
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)
            Repo.clone_from(url, repo_dir)

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
    popular_repo_urls = fetch_popular_repo()
    clone_repo(popular_repo_urls)

if __name__ == "__main__":
    main()

