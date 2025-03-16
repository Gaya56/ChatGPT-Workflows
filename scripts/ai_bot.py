import os
import openai
from github import Github

def main():
    # 1. Retrieve secrets from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    gh_access_token = os.getenv("GH_ACCESS_TOKEN")
    
    # 2. Authenticate with OpenAI (if you want ChatGPT-based text generation)
    openai.api_key = openai_api_key

    # 3. Authenticate with GitHub
    g = Github(gh_access_token)
    
    # Replace 'owner/repo-name' with your actual GitHub repo, e.g. 'my-org/my-repo'
    repo = g.get_repo("owner/repo-name")

    # --------------------------------------------------------------------------
    # EXAMPLE: Reading, updating, creating, and deleting files
    # --------------------------------------------------------------------------

    # Reading file contents
    file_path = "some_folder/hello_world.txt"
    try:
        contents = repo.get_contents(file_path)
        print("Current file content:", contents.decoded_content.decode())
    except Exception as e:
        print(f"Could not read file {file_path}. Error: {e}")

    # Updating a file
    new_content = "Hello from our AI bot!\n"
    try:
        repo.update_file(
            file_path,
            "Update file via AI bot",
            new_content,
            contents.sha
        )
        print(f"{file_path} updated successfully.")
    except Exception as e:
        print(f"Could not update file {file_path}. Error: {e}")

    # Creating a new file
    new_file_path = "some_folder/newfile.txt"
    new_file_content = "Some new content here"
    try:
        repo.create_file(
            new_file_path,
            "Create new file via AI bot",
            new_file_content
        )
        print(f"{new_file_path} created successfully.")
    except Exception as e:
        print(f"Could not create file {new_file_path}. Error: {e}")

    # Deleting a file
    delete_file_path = "some_folder/deletable_file.txt"
    try:
        delete_contents = repo.get_contents(delete_file_path)
        repo.delete_file(
            delete_file_path,
            "Delete file via AI bot",
            delete_contents.sha
        )
        print(f"{delete_file_path} deleted successfully.")
    except Exception as e:
        print(f"Could not delete file {delete_file_path}. Error: {e}")

    # --------------------------------------------------------------------------
    # EXAMPLE: Using ChatGPT (OpenAI) to generate file content or interpret instructions
    # --------------------------------------------------------------------------

    user_prompt = "Provide a short greeting message in Markdown"
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",  # or your model of choice
            prompt=user_prompt,
            max_tokens=50,
            temperature=0.7
        )
        generated_text = completion.choices[0].text.strip()
        print("Generated content:", generated_text)
    except Exception as e:
        print(f"OpenAI API call failed. Error: {e}")

    # You could take this 'generated_text' and use it to create or update a file in the repo.
    # For example, we could commit it to 'generated_text.md' as new content.

if __name__ == "__main__":
    main()
