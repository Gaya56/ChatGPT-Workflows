import os
import openai
from github import Github

def main():
    # Grab secrets from env
    openai_api_key = os.getenv("OPENAI_API_KEY")
    gh_access_token = os.getenv("GH_ACCESS_TOKEN")

    # Authenticate OpenAI & GitHub
    openai.api_key = openai_api_key
    g = Github(gh_access_token)

    # IMPORTANT: replace with your actual repo name
    repo = g.get_repo("Gaya56/ChatGPT-Workflows")

    # (Optional) test reading or creating a file
    try:
        new_file_path = "some_folder/new_test_file.txt"
        new_file_content = "Hello from ChatGPT AI bot!"
        repo.create_file(
            new_file_path,
            "Create a new test file via AI bot",
            new_file_content
        )
        print(f"{new_file_path} created successfully.")
    except Exception as e:
        print(f"Could not create file {new_file_path}. Error: {e}")

    # Add more logic here if desired.
    # E.g., generate content using openai.Completion, etc.

if __name__ == "__main__":
    main()
