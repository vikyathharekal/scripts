import argparse
import requests
import os
import yaml
import re

yaml_content_template = """
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  tags:
    - java
    - harness
  name: {repo_name}
  annotations:
    backstage.io/source-location: url:{repo_path}
spec:
  type: service
  system: harness
  lifecycle: experimental
  owner: Harness_Account_All_Users
"""

def list_repositories(organization, token, repo_pattern=None):
    url = f"https://api.github.com/orgs/{organization}/repos"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(url, headers=headers)

    yaml_files_created = 0

    if response.status_code == 200:
        repos = response.json()
        print(f"Repositories in {organization}:")
        for repo in repos:
            repo_name = repo['name']
            repo_path = repo['html_url']
            if repo_pattern is None or re.match(repo_pattern, repo_name):
                print(repo_name)
                create_or_update_catalog_info(repo_name, repo_path)
                yaml_files_created += 1
        print("----------")
    else:
        print(f"Failed to fetch repositories. Status code: {response.status_code}")

    print(f"Total YAML files created or updated: {yaml_files_created}")

def create_or_update_catalog_info(repo_name, repo_path):
    directory = f"services/{repo_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    yaml_file_path = f"{directory}/catalog-info.yaml"

    if os.path.exists(yaml_file_path):
        # Update existing YAML file
        with open(yaml_file_path, "r") as file:
            existing_content = file.read()
        updated_content = yaml_content_template.format(repo_name=repo_name, repo_path=repo_path)
        with open(yaml_file_path, "w") as file:
            file.write(updated_content)
    else:
        # Create new YAML file
        with open(yaml_file_path, "w") as file:
            file.write(yaml_content_template.format(repo_name=repo_name, repo_path=repo_path))

def register_yamls():
    # Placeholder function for registering YAML files
    print("Registering YAML files...")

def run_all():
    # Placeholder function for running all
    print("Running all...")

def parse_arguments():
    parser = argparse.ArgumentParser(description="List repositories in a GitHub organization and manage catalog-info.yaml files")
    parser.add_argument("--org", help="GitHub organization name", required=True)
    parser.add_argument("--token", help="GitHub personal access token", required=True)
    parser.add_argument("--repo-pattern", help="Optional regex pattern to filter repositories")
    parser.add_argument("--create-yamls", action="store_true", help="Create or update catalog-info.yaml files")
    parser.add_argument("--register-yamls", action="store_true", help="Register existing catalog-info.yaml files")
    parser.add_argument("--run-all", action="store_true", help="Run all operations: create, register, and run")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if not (args.create_yamls or args.register_yamls or args.run_all):
        print("Error: One of --create-yamls, --register-yamls or --run_all must be used.")
        return
    
    if args.create_yamls:
        list_repositories(args.org, args.token, args.repo_pattern)
    elif args.register_yamls:
        register_yamls()
    
    if args.run_all:
        run_all()

if __name__ == "__main__":
    main()
