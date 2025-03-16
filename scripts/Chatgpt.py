import os
import openai
from github import Github

def main():
    # 1. Get secrets from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    gh_access_token = os.getenv("GH_ACCESS_TOKEN")

    # 2. Authenticate with OpenAI
    openai.api_key = openai_api_key

    # 3. Authenticate with GitHub
    g = Github(gh_access_token)

    # Replace "Gaya56/ChatGPT-Workflows" with your "owner/repo"
    repo = g.get_repo("YourGitHubUsername/YourRepo")

    # Example operation: create or update a file
    file_path = "some_folder/example_file.txt"
    new_content = "Hello from ChatGPT workflow!"
    commit_msg = "Update example_file via chatgpt.py"

    try:
        existing_file = repo.get_contents(file_path)
        repo.update_file(file_path, commit_msg, new_content, existing_file.sha)
        print(f"Updated '{file_path}'.")
    except Exception:
        repo.create_file(file_path, commit_msg, new_content)
        print(f"Created '{file_path}'.")

if __name__ == "__main__":
    main()
