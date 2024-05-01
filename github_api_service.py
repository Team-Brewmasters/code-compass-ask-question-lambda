import requests

ignore_list = [
    'node_modules', 'assets', 'favicon.ico', '.gitignore', 'package-lock.json', 
    'angular.json', 'tsconfig.app.json', 'package.json', 'yarn.lock', 'LICENSE', 
    'Dockerfile', 'docker-compose.yml', 'jest.config.js', 'tsconfig.json', 
    'tsconfig.build.json', 'tsconfig.spec.json', 'tslint.json', 'README.md', 
    'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'PULL_REQUEST_TEMPLATE.md', 
    'ISSUE_TEMPLATE.md', '.github', '.gitattributes', '.editorconfig', 
    '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', 
    '.gitlab-ci.yml', '.circleci'
]

def get_repo_file_contents(repo_url, path=''):
    # Extract the username and repository name from the URL
    parts = repo_url.rstrip('/').split('/')
    username = parts[-2]
    repo_name = parts[-1]
    
    # Construct the API URL to get the repository contents
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}"
    
    # Send a GET request to the GitHub API
    response = requests.get(api_url)
    file_contents = []

    if response.status_code == 200:
        # Iterate over each item in the repository
        for item in response.json():
            item_name = item['name']
            item_path = f"{path}/{item_name}".strip('/')
            
            if item['type'] == 'file' and item_name not in ignore_list:
                file_url = item['download_url']
                # Send a GET request to download the file contents
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    content = file_response.text
                    file_contents.append(f"{item_path}\n{content}")
                else:
                    print(f"Error downloading file '{item_name}': {file_response.status_code} - {file_response.text}")
            elif item['type'] == 'dir':
                if item_name not in ignore_list:
                    # Recursively get the contents of the directory if not in ignore list
                    dir_contents = get_repo_file_contents(repo_url, item_path)
                    file_contents.extend(dir_contents)

    else:
        print(f"Error: {response.status_code} - {response.text}")
    return file_contents

# # Example usage
# repo_link = "https://github.com/Team-Brewmasters/code-compass-webapp"
# file_contents_array = get_repo_file_contents(repo_link)

# # Print the file contents array
# for file_content in file_contents_array:
#     print(file_content)
#     print("---")