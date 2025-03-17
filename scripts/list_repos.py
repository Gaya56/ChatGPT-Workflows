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
    user = g.get_user("Gaya56")  # or just g.get_user() if the token belongs to Gaya56
    repos = user.get_repos()

    # 4. Prepare output text
    output_lines = ["Repositories under the account 'Gaya56':\n"]
    for repo in repos:
        output_lines.append(f"- {repo.full_name}\n")

    # 5. Write the repo list to OpenAI/repoList.txt
    # Ensure the 'OpenAI' folder exists (create if missing)
    os.makedirs("OpenAI", exist_ok=True)

    file_path = os.path.join("OpenAI", "repoList.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print(f"Repository list saved to {file_path}")

if __name__ == "__main__":
    main()
