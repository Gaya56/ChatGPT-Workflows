# ChatGPT-Workflows

**Summary (Two Paragraphs)**  
We’ve created and tested several different GitHub Actions workflows for an AI-powered automation setup. First, the **AI Bot Workflow (`ai-bot.yml`)** pairs with `ai_bot.py` to fetch secrets (like an OpenAI key and GitHub token), allowing you to automate code edits or file operations via a Python script. Second, the **ChatGPT Code Reviewer (`chatgpt-code-reviewer.yml`)** workflow automatically posts GPT-based review comments on pull requests, providing near-instant code feedback. Next, the **List Repos Workflow (`list_repos.yml`)** demonstrates how to run a Python script (`list_repos.py`) that fetches a list of repositories and writes them to a local file—then commits that file back to the repo for persistence.

Most recently, we tested and confirmed the **OpenAI-Find-Paths** workflow (`openai-find-paths.yml`) works successfully: it scans the repository, briefly summarizes each file’s content, and writes the collected data to `OpenAI/find-path.txt`. By combining these examples, you can securely manage secrets, configure permissions for read/write operations, and leverage Python scripts (PyGithub + OpenAI) to automate repetitive tasks, incorporate AI-driven code reviews, and generate or manipulate files—without ever leaving GitHub.

---

## Key Usage Scenarios

### 1. AI Bot Workflow
- **When to Use**: Triggered automatically (push, issue, etc.) to run a Python script that uses OpenAI’s API + GitHub API.  
- **Purpose**: Automate edits, commits, or file updates based on ChatGPT-generated logic.

### 2. ChatGPT Code Reviewer
- **When to Use**: Automatically on Pull Requests.  
- **Purpose**: Provides AI-based feedback and suggestions to your PRs, helping catch errors or prompt improvements.

### 3. List Repos Workflow
- **When to Use**: Manually dispatch the workflow from the Actions tab (or schedule/trigger as needed).  
- **Purpose**: Demonstrates how to fetch information from GitHub (like listing repos) and commit new or updated files back to the repo for tracking or documentation.

### 4. OpenAI-Find-Paths
**What It Does (Two Sentences)**  
The **OpenAI-Find-Paths** workflow (`openai-find-paths.yml`) and its companion script (`openai-find-paths.py`) scan through your repository, listing all directories and files. Using OpenAI’s ChatCompletion API, they briefly summarize each file’s role in the codebase, creating a concise inventory of paths in a single text file (`OpenAI/find-path.txt`).

**When & How to Use**  
- **Use Case**: When you need a quick, AI-generated overview of the repo’s file structure and each file’s purpose.  
- **Trigger**: Manually from the Actions tab (`workflow_dispatch`) so you can generate or refresh these summaries as needed.  
- **Output**: Writes file paths and short descriptions to `OpenAI/find-path.txt`, giving you a bird’s-eye view of the repository’s contents.

---

These workflows can be reused, adapted, or expanded (for example, adding more complex AI logic in your Python scripts) any time you need GitHub-based automations, code reviews, or integration with third-party services like OpenAI.
