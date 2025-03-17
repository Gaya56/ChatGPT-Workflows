import os
import openai

def ai_describe(path, snippet):
    """
    Uses OpenAI's ChatCompletion to describe a file in 1-2 sentences.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. "
                        "Given a file path and snippet of its content, "
                        "provide a 1-2 sentence description focusing on the file's purpose."
                    )
                },
                {"role": "user", "content": f"Path: {path}\nSnippet: {snippet}"}
            ],
            max_tokens=60,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(No AI summary: {str(e)})"

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    use_ai = False
    if openai_api_key:
        openai.api_key = openai_api_key
        use_ai = True

    lines = [
        "# Repository Index\n\n",
        "Below is an automatically generated index of the files/folders in this repository.\n\n"
    ]

    # Root directory to scan
    root_dir = "."

    for root, dirs, files in os.walk(root_dir):
        # Skip hidden or special folders
        if any(skip in root for skip in [".git", ".github", "OpenAI"]):
            continue

        # Sort for consistency
        dirs.sort()
        files.sort()

        rel_root = os.path.relpath(root, start=".")
        if rel_root == ".":
            rel_root = ""

        # Add heading for each directory
        if rel_root:
            lines.append(f"## {rel_root}\n\n")
        else:
            lines.append("## Root\n\n")

        # List subdirectories
        if dirs:
            lines.append("**Directories:**\n\n")
            for d in dirs:
                sub_path = os.path.join(rel_root, d) if rel_root else d
                lines.append(f"- `{sub_path}/`\n")
            lines.append("\n")

        # List files
        if files:
            lines.append("**Files:**\n\n")
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.join(rel_root, f) if rel_root else f

                # Optionally read snippet
                snippet = ""
                if use_ai:
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as ff:
                            snippet = ff.read(200)
                    except:
                        snippet = "(Could not read file)"

                # Summarize if AI is enabled
                description = ""
                if use_ai:
                    description = ai_describe(rel_path, snippet)

                if description:
                    lines.append(f"- `{rel_path}`: {description}\n")
                else:
                    lines.append(f"- `{rel_path}`\n")

            lines.append("\n")

    # Write index.md
    with open("index.md", "w", encoding="utf-8") as output:
        output.writelines(lines)

    print("Created or updated index.md in the repo root.")

if __name__ == "__main__":
    main()
