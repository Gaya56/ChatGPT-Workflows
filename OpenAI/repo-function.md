# Repository Functions Overview

This document combines data from `index.md` (file references), `find-path.txt` (short AI-based file summaries), and local/GPT-based function extraction.

## README.md

**Short Summary:** The file contains descriptions and configurations for different GitHub Actions workflows related to an AI-powered automation setup. It specifically includes details about the AI Bot Workflow named `ai-bot.yml` that has been created and tested as part of this project.

**AI-based Function Extraction:**

Functions or methods found in the code snippet:

1. **AI Bot Workflow**:
   - Purpose: Automate edits, commits, or file updates based on ChatGPT-generated logic.
   - Trigger: Automatically triggered (push, issue, etc.) to run a Python script that uses OpenAI’s API + GitHub API.

2. **ChatGPT Code Reviewer**:
   - Purpose: Provides AI-based feedback and suggestions to Pull Requests, helping catch errors or prompt improvements.
   - Trigger: Automatically runs on Pull Requests.

3. **List Repos Workflow**:
   - Purpose: Demonstrates how to fetch information from GitHub (like listing repos) and commit new or updated files back to the repo for tracking or documentation.
   - Trigger: Manually dispatch the workflow from the Actions tab or schedule/trigger as needed.

4. **OpenAI-Find-Paths**:
   - Purpose: Scans through the repository, lists all directories and files, and summarizes each file's role in the codebase using OpenAI's ChatCompletion API.
   - Trigger: Manually from the Actions tab (`workflow_dispatch`) to generate or refresh summaries as needed.
   - Output: Writes file paths and short descriptions to `OpenAI/find-path.txt`.

5. **Create Index Workflow**:
   - Purpose: Not fully described in the provided snippet.
Functions or methods found in the code snippet:
1. `create-index.yml`: A YAML file that likely contains configuration settings or instructions for the workflow to create an `index.md` file in the repository.
2. `create-index.py`: A Python script that automates the process of generating an `index.md` file by scanning all folders and files in the repository and optionally using OpenAI for short descriptions.
3. `workflow_dispatch`: A trigger that allows manual execution of the workflow from the Actions tab.
4. `install dependencies`: This step likely involves installing any required dependencies for the workflow to run successfully.
5. `pushes the newly generated index.md to the repository`: A step that commits and pushes the updated `index.md` file back to the repository.
6. `ai-bot.yml`: A workflow file that can be copied and adapted for use in other repositories, potentially for AI-assisted code editing or reviewing.
7. "find paths" workflow: A workflow that can be adapted to generate a dynamic index or documentation in any repository, using OpenAI to summarize new or changing files.

## scripts/ai_bot.py

**Short Summary:** This script defines a `main` function that retrieves sensitive information like OpenAI and GitHub tokens from environment variables. It appears to be a script designed to interact with OpenAI and GitHub APIs within a code repository for automation or integration purposes.

**Local Regex-Found Functions:**

- `main`

**AI-based Function Extraction:**

Functions found in ai_bot.py:
1. main(): This function serves as the main entry point of the script. It retrieves API keys for OpenAI and GitHub from environment variables, authenticates with both services, interacts with a GitHub repository (specifically creating a new file), and potentially includes additional logic for generating content using OpenAI's Completion API.

## scripts/create-index.py

**Short Summary:** (No summary found)

**Local Regex-Found Functions:**

- `ai_describe`
- `main`

**AI-based Function Extraction:**

Functions found in the code snippet:

1. `ai_describe(path, snippet)`: This function uses OpenAI's ChatCompletion to describe a file in 1-2 sentences. It takes a file path and a snippet of its content as input and returns a description of the file's purpose using AI.

2. `main()`: This function is the main entry point of the script. It sets up the OpenAI API key, scans the root directory for files and folders, generates an index of the repository's contents, and optionally uses the `ai_describe` function to provide descriptions of files if AI is enabled.
Functions found in the code snippet:
1. `main()`: This is the main function of the script. It calls other functions to create or update an `index.md` file in the repository root.
2. `get_files_in_directory(directory)`: This function takes a directory path as input and returns a list of files in that directory.
3. `generate_index(files)`: This function takes a list of files as input and generates the content for the `index.md` file based on the files list.
4. `write_index(lines)`: This function takes a list of lines as input and writes them to the `index.md` file.

## scripts/list_repos.py

**Short Summary:** This script imports necessary modules to access GitHub and retrieve an access token from environment variables for authentication. The main function is responsible for obtaining the GitHub access token and raising an error if the token is not found.

**Local Regex-Found Functions:**

- `main`

**AI-based Function Extraction:**

Functions/Methods found in the code snippet:

1. `main()`: This is the main function of the script. It retrieves a GitHub token from environment variables, authenticates to GitHub using PyGithub, fetches all repositories for a specific account, prepares an output text with the list of repositories, and writes this list to a file named "repoList.txt" under the "OpenAI" folder. Finally, it prints a message indicating the successful saving of the repository list.

2. `os.getenv("GH_ACCESS_TOKEN")`: This function is used to retrieve the GitHub access token from the environment variables.

3. `Github()`: This is a constructor method from the `github` library that is used to authenticate to GitHub using the provided access token.

4. `g.get_user("Gaya56")`: This method is used to get the user object for the specified GitHub username ("Gaya56" in this case).

5. `user.get_repos()`: This method is used to fetch all repositories for the specified user.

6. `os.makedirs("OpenAI", exist_ok=True)`: This function is used to create a directory named "OpenAI" if it does not already exist.

7. `open(file_path, "w", encoding="utf-8")`: This function is used to open a file named "repoList.txt" in write mode with UTF-8 encoding.

8. `f.writelines(output_lines)`: This method writes the lines of text

## scripts/openai-find-paths.py

**Short Summary:** This Python script utilizes the OpenAI API to generate a short summary of a file's content with a focus on its role within a code repository. The `summarize_content` function takes the content of a file as input and outputs a concise two

**Local Regex-Found Functions:**

- `summarize_content`
- `main`

**AI-based Function Extraction:**

Functions found in the code snippet:

1. `summarize_content(content)`: This function uses OpenAI's ChatCompletion to generate a short, two-sentence description focusing on the file's role in a code repository.

2. `main()`: This is the main function of the script. It sets up the OpenAI API key, walks through a target directory, reads snippets from files, summarizes the content using the `summarize_content` function, and writes the paths and summaries to a file.

