import json
import os
import re
import requests

from collections import Counter
from git import Repo

def fetch_popular_repo():
    popular_repo_urls = []
    api_url = 'https://api.github.com/search/repositories?q=stars:%3E1+language:javascript&sort=stars&order=desc&type=Repositories%27'
    res = requests.get(api_url).json()
    for repo in res['items']:
        popular_repo_urls.append(repo['clone_url'])
        if len(popular_repo_urls) == 6: break
    return popular_repo_urls

def clone_repo(url):
    find_repo_name = re.compile('\/([^\/]+).git$')
    repo_name = find_repo_name.findall(url)[0]
    repo_dir = './repos/' + repo_name
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        Repo.clone_from(url, repo_dir)

    return repo_dir

def read_files(repo_dir, var_counter):
    prog = re.compile('(?:const|var|let|function)\s+(\w+);?')
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
                analyze_content(content_file, prog, var_counter)

def analyze_content(contents, prog, var_counter):
    content = contents.read()
    matches = prog.findall(content)
    if matches:
        for match in set(matches):
            if len(match) < 2: continue
            var_counter[match] += 1
        # print(var_counter.most_common(10))

def main():
    # TODO:
    # Find all the variable names for each seperate projects and
    # intersect them and see the results
    # Should be {React: Counter(), Vue: Counter, ...}

    var_counter = Counter()
    popular_repo_urls = fetch_popular_repo()
    for url in popular_repo_urls:
        repo_dir = clone_repo(url)
        read_files(repo_dir, var_counter)
    print(var_counter.most_common(50))

if __name__ == "__main__":
    main()

