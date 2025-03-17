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

### 5. Create Index Workflow
**What It Does**  
The **Create Index Workflow** (`create-index.yml`) and its companion script (`create-index.py`) automate the process of generating an `index.md` at the root of your repo. By scanning all folders and files (optionally using OpenAI for short descriptions), it produces a structured outline of the entire repository, then commits `index.md` back to the repo so it’s always up to date.

**When & How to Use**
- **Use Case**: Ideal when you want a dynamic table of contents for your project, complete with optional AI-generated summaries of each file.
- **Trigger**: Manually from the Actions tab (`workflow_dispatch`). It installs dependencies, runs `create-index.py`, and pushes the newly generated `index.md` to the repository.
- **Result**: A fresh `index.md` at the repo root, listing directories and files, along with any AI-based descriptions.

### 6. Gather Functions & question-repo Scripts
**Gather Functions (`gather-functions.yml`, `gather-functions.py`)**  
- **What It Does**: This workflow and script collect file references from `index.md` and `OpenAI/find-path.txt`, then scan each file (optionally with GPT) to extract and list functions in a new file, `repo-function.md`.  
- **When & How to Use**: Manually trigger the “Gather Functions” workflow after you’ve generated `index.md` and `find-path.txt`. Great for a deeper dive into function definitions and code structure.

**question-repo (`question-repo.py`)**  
- **What It Does**: An interactive Python script that references `index.md`, `OpenAI/find-path.txt`, and optionally scanned code files for context. It rotates through multiple GPT API keys if rate-limited.  
- **When & How to Use**: Run locally via `python question-repo.py`. Then ask architecture or code questions about your repository, and ChatGPT will respond with file references, line numbers, and recommended changes.

---

These workflows and scripts can be reused, adapted, or expanded (for example, adding more complex AI logic in your Python scripts) any time you need GitHub-based automations, code reviews, or integration with third-party services like OpenAI.

---

## Future Integration in Other Repositories
You can easily apply these same patterns to other projects. For example, simply copy a workflow file (like `ai-bot.yml`) and its paired Python script into another repo, adjust the tokens and secrets, and you’ll have AI-assisted code editing or reviewing up and running. Similarly, you can adapt the “find paths” workflow to generate a dynamic index or documentation in any repository, or the “gather functions” and “question-repo” scripts for deeper architecture analysis. By combining these workflows with various triggers (push, pull_request, cron schedules), you can orchestrate advanced automation in multiple codebases, drastically streamlining your CI/CD and documentation processes.