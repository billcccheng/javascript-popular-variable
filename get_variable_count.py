import codecs
import json
import os
import re
import requests

from git import Repo

def fetch_popular_repo():
    popular_repo_urls, popular_html_urls = [], []
    api_url = 'https://api.github.com/search/repositories?q=stars:%3E1+language:javascript&sort=stars&order=desc&type=Repositories%27'
    res = requests.get(api_url).json()
    for repo in res['items']:
        popular_html_urls.append(repo['html_url'] + '/search/?q=')
        popular_repo_urls.append(repo['clone_url'])
        if len(popular_repo_urls) == 10: break
    return popular_repo_urls, popular_html_urls

def clone_repo(url):
    find_repo_name = re.compile('([^\/]+).git$')
    repo_name = find_repo_name.findall(url)[0]
    repo_dir = './repos/' + repo_name
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        Repo.clone_from(url, repo_dir)

    return repo_dir, repo_name

def read_files(repo_dir, var_counter, html_url):
    find_var_name = re.compile('(?:const|var|let|function)\s+(\w+);?')
    directories = [repo_dir]
    group_name = repo_dir.replace('./repos/', '')
    while directories:
        parent_dir = directories.pop()
        all_dir = next(os.walk(parent_dir))[1]
        all_file = next(os.walk(parent_dir))[2]
        for _dir in all_dir:
            if _dir == '.git': continue
            directories.append(parent_dir + '/' + _dir)
        for _file in all_file:
            if not _file.endswith(".js"): continue
            curr_file_path = parent_dir + '/' + _file
            with codecs.open(curr_file_path, 'r', encoding='utf-8', errors='ignore') as content_file:
                content = content_file.read()
                matches = find_var_name.findall(content)
                get_variable_count(matches, var_counter,  html_url)

def get_variable_count(matches, var_counter, url):
    if matches:
        for match in set(matches):
            if len(match) < 3:
                continue
            if match in var_counter:
                var_counter[match]["counter"] = var_counter[match]["counter"] + 1
            else:
                _url = url + match
                var_counter[match] = {"counter" : 1, "url": _url}

def write_to_file(data):
    with open('variable-dict-update', 'w') as _file:
        json.dump(data, _file, sort_keys=True)

def main():
    # TODO:
    # 1. Find all the variable names for each seperate projects and
    #    intersect them and see the results
    # 2. Normalize the variables: Maybe by file or project?
    # 3. Seperate out functions and variables
    # 4. Remove repo when finished parsing

    variable_dict = {}
    repo_urls, html_urls = fetch_popular_repo()
    for index, url in enumerate(repo_urls):
        repo_dir, repo_name = clone_repo(url)
        variable_dict[repo_name] = {}
        read_files(repo_dir, variable_dict[repo_name], html_urls[index])
    write_to_file(variable_dict)
    # for key in variable_dict.keys():
        # variable_dict[key] = variable_dict[key].most_common(10)
    # print(json.dumps(variable_dict, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

