import os
from github import Github

def main():
    # 1. Retrieve GitHub token from environment variables
    gh_token = os.getenv("GH_ACCESS_TOKEN")
    if not gh_token:
        raise ValueError("GH_ACCESS_TOKEN environment variable is not set.")

    # 2. Authenticate to GitHub via PyGithub
    g = Github(gh_token)

    # 3. Fetch all repositories for your account
    # If it's a personal account, 'get_user()' will be your user. 
    # If it's an org, you'd do 'get_organization("YourOrgName")'.
    user = g.get_user("Gaya56")  # or just g.get_user() if the token belongs to Gaya56
    repos = user.get_repos()

    # 4. Print each repository name
    print("Repositories under the account 'Gaya56':")
    for repo in repos:
        print(f"- {repo.full_name}")

if __name__ == "__main__":
    main()
