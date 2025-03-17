# ChatGPT-Workflows
**Summary (Two Paragraphs)**  
We’ve created and tested three different GitHub Actions workflows for an AI-powered automation setup. First, the **AI Bot Workflow (`ai-bot.yml`)** pairs with `ai_bot.py` to fetch secrets (like an OpenAI key and GitHub token), allowing you to automate code edits or file operations via a Python script. Second, the **ChatGPT Code Reviewer (`chatgpt-code-reviewer.yml`)** workflow automatically posts GPT-based review comments on pull requests, providing near-instant code feedback. Finally, the **List Repos Workflow (`list_repos.yml`)** demonstrates how to run a Python script (`list_repos.py`) that fetches a list of repositories and writes them to a local file—then commits that file back to the repo for persistence.

In short, these workflows illustrate how to securely manage secrets, configure permissions for read/write operations, and leverage Python scripts (PyGithub + OpenAI) to extend GitHub’s capabilities. By combining these examples, you can automate repetitive tasks, incorporate AI-driven code reviews, and generate or manipulate files in a variety of ways—without ever leaving GitHub.

---

**Key Usage Scenarios (Bullet Points)**  
- **AI Bot Workflow**:  
  - *When to Use*: Triggered automatically (push, issue, etc.) to run a Python script that uses OpenAI’s API + GitHub API.  
  - *Purpose*: Automate edits, commits, or file updates based on ChatGPT-generated logic.  

- **ChatGPT Code Reviewer**:  
  - *When to Use*: Automatically on Pull Requests.  
  - *Purpose*: Provides AI-based feedback and suggestions to your PRs, helping catch errors or prompt improvements.  

- **List Repos Workflow**:  
  - *When to Use*: Manually dispatch the workflow from the Actions tab (or schedule/trigger as needed).  
  - *Purpose*: Demonstrates how to fetch information from GitHub (like listing repos) and commit new or updated files back to the repo for tracking or documentation.  

These workflows can be reused, adapted, or expanded (for example, adding more complex AI logic in your Python scripts) any time you need GitHub-based automations, code reviews, or integration with third-party services like OpenAI.
