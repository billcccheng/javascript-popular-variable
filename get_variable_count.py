import codecs
import json
import os
import re
import requests

from git import Repo

def fetch_popular_repo():
    popular_repo_urls = []
    api_url = 'https://api.github.com/search/repositories?q=stars:%3E1+language:javascript&sort=stars&order=desc&type=Repositories%27'
    res = requests.get(api_url).json()
    for repo in res['items']:
        popular_repo_urls.append(repo['clone_url'])
        if len(popular_repo_urls) == 10: break
    return popular_repo_urls

def clone_repo(url):
    find_repo_name = re.compile('(\w+\/[^\/]+).git$')
    repo_name = find_repo_name.findall(url)[0].replace('/','-')
    repo_dir = './repos/' + repo_name
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        Repo.clone_from(url, repo_dir)

    return repo_dir, repo_name

def read_files(repo_dir, var_counter):
    prog = re.compile('(?:const|var|let|function)\s+(\w+);?')
    directories = [repo_dir]
    while directories:
        parent_dir = directories.pop()
        all_dir = next(os.walk(parent_dir))[1]
        all_file = next(os.walk(parent_dir))[2]
        for _dir in all_dir:
            if _dir == '.git': continue
            directories.append(parent_dir + '/' + _dir)
        for _file in all_file:
            if not _file.endswith(".js"): continue
            curr_file = parent_dir + '/' + _file
            with codecs.open(curr_file , 'r', encoding='utf-8', errors='ignore') as content_file:
                get_variable_count(content_file.read(), prog, var_counter)

def get_variable_count(content, prog, var_counter):
    matches = prog.findall(content)
    if matches:
        for match in set(matches):
            var_counter[match] = var_counter[match] + 1 if match in var_counter and len(match) > 1 else 1

def write_to_file(data):
    with open('variable-dict.txt', 'w') as _file:
        json.dump(data, _file, indent=2, sort_keys=True)

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
        variable_dict[repo_name] = {}
        read_files(repo_dir, variable_dict[repo_name])
    write_to_file(variable_dict)
    # for key in variable_dict.keys():
        # variable_dict[key] = variable_dict[key].most_common(10)
    # print(json.dumps(variable_dict, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

