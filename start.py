import json
import os
import re
import requests

from collections import Counter, OrderedDict
from git import Repo

def fetch_popular_repo():
    popular_repo_urls = []
    api_url = 'https://api.github.com/search/repositories?q=stars:%3E1+language:javascript&sort=stars&order=desc&type=Repositories%27'
    res = requests.get(api_url).json()
    for repo in res['items']:
        popular_repo_urls.append(repo['clone_url'])
        if len(popular_repo_urls) == 7: break
    return popular_repo_urls

def clone_repo(url):
    find_repo_name = re.compile('(\w+\/[^\/]+).git$')
    repo_name = find_repo_name.findall(url)[0].replace('/','-')
    repo_dir = './repos/' + repo_name
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        Repo.clone_from(url, repo_dir)

    return repo_dir, repo_name

def read_files(repo_dir, repo_var_counter):
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
                analyze_content(content_file, prog, repo_var_counter)

def analyze_content(contents, prog, repo_var_counter):
    content = contents.read()
    matches = prog.findall(content)
    if matches:
        for match in set(matches):
            if len(match) > 1:
                repo_var_counter[match] += 1
        # print(variable_dict.most_common(10))

def main():
    # TODO:
    # 1. Find all the variable names for each seperate projects and
    # intersect them and see the results
    #
    # 2. Normalize the variables: Maybe by file or project?
    # 3. Seperate out functions and variables

    variable_dict = {}
    popular_repo_urls = fetch_popular_repo()
    for url in popular_repo_urls:
        repo_dir, repo_name = clone_repo(url)
        variable_dict[repo_name] = Counter()
        read_files(repo_dir, variable_dict[repo_name])
    for key in variable_dict.keys():
        variable_dict[key] = variable_dict[key].most_common(10)
    print(json.dumps(variable_dict, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

