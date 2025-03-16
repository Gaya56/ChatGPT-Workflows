import os
import openai
from github import Github

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    gh_token = os.getenv("GH_ACCESS_TOKEN")

    g = Github(gh_token)
    repo = g.get_repo("Gaya56/ChatGPT-Workflows")  # Example

    # Create or update a file
    file_path = "some_folder/new_test_file.txt"
    file_content = "Hello from the AI bot!"
    try:
        contents = repo.get_contents(file_path)
        repo.update_file(
            file_path, 
            "Update file via AI bot", 
            file_content, 
            contents.sha
        )
    except:
        repo.create_file(
            file_path, 
            "Create file via AI bot", 
            file_content
        )

if __name__ == "__main__":
    main()
