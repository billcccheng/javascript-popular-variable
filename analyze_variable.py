import json

def load_file(_file):
    with open(_file, 'r') as _file:
        return json.load(_file)

def main():
    file_path = './variable-dict.txt'
    var_dict = load_file(file_path)
    repo_names = list(var_dict.keys())
    # airbnb_js_var_name = list(var_dict[repo_names[0]].keys())
    # angularjs_var_name = list(var_dict[repo_names[3]].keys())
    # print(repo_names)
    print(var_dict[repo_names[-1]].keys() & var_dict[repo_names[0]].keys())

if __name__ == "__main__":
    main()
