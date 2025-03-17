import os
import re
import openai

def ai_extract_functions(file_path, code_chunk):
    """
    Uses ChatCompletion to identify functions and their purposes in a code chunk.
    Returns a string describing them.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a code parsing assistant. "
                        "Given a code snippet, list all functions or methods you find, "
                        "briefly describing their purpose or usage."
                    )
                },
                {
                    "role": "user",
                    "content": f"File: {file_path}\nCode:\n{code_chunk}"
                }
            ],
            max_tokens=300,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(No AI analysis: {str(e)})"

def local_extract_functions(code_text):
    """
    Basic regex approach to find 'def function_name(...):' in Python code.
    Expand or adjust for other languages as needed.
    """
    pattern = r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    found = re.findall(pattern, code_text, flags=re.MULTILINE)
    return found

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    use_ai = False
    if openai_api_key:
        openai.api_key = openai_api_key
        use_ai = True
        print("AI-based function extraction is enabled.")
    else:
        print("No OPENAI_API_KEY found; defaulting to regex-based function extraction only.")

    # The two input files needed from previous workflows:
    index_path = os.path.join(".", "index.md") # from create-index.py
    find_paths_file = os.path.join("OpenAI", "find-path.txt") # from openai-find-paths.py

    # Check if they exist
    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found. Make sure create-index.py was run.")
        return
    if not os.path.exists(find_paths_file):
        print(f"Error: {find_paths_file} not found. Make sure openai-find-paths.py was run.")
        return

    # Read index.md
    with open(index_path, "r", encoding="utf-8") as idx:
        index_md = idx.read()

    # Read find-path.txt
    with open(find_paths_file, "r", encoding="utf-8") as fpf:
        find_paths_content = fpf.read()

    # 1) Collect file references from index.md (looking for lines with backticks that have .py, .yml, etc.)
    file_lines = []
    for line in index_md.splitlines():
        if '`' in line and (".py" in line or ".yml" in line):
            path = line.split('`')[1]
            file_lines.append(path)

    # 2) Create a dict for short summaries from find-path.txt
    summary_dict = {}
    lines = find_paths_content.splitlines()
    current_path = None
    for ln in lines:
        if ln.startswith("**Path**: "):
            current_path = ln.split(": ", 1)[1].strip()
        elif ln.startswith("**Summary**: ") and current_path:
            summary = ln.split(": ", 1)[1].strip()
            summary_dict[current_path] = summary
            current_path = None

    # Prepare output lines for the final doc
    output = [
        "# Repository Functions Overview\n\n",
        "This document combines data from `index.md` (file references), "
        "`find-path.txt` (short AI-based file summaries), and local/GPT-based function extraction.\n\n"
    ]

    # Make sure the OpenAI folder exists
    os.makedirs("OpenAI", exist_ok=True)

    # The path where we'll write the final results
    out_file = os.path.join("OpenAI", "repo-function.md")

    for file_path in file_lines:
        # if file doesn't exist, skip
        if not os.path.exists(file_path):
            continue

        # read file content
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as code_file:
                code_text = code_file.read()
        except:
            code_text = ""

        # 1) local parse
        local_funcs = local_extract_functions(code_text)

        # 2) AI parse if we have a key
        ai_results = []
        if use_ai and code_text:
            chunk_size = 3000
            chunks = [code_text[i:i+chunk_size] for i in range(0, len(code_text), chunk_size)]
            for chunk in chunks:
                ai_res = ai_extract_functions(file_path, chunk)
                ai_results.append(ai_res)
            ai_parse = "\n".join(ai_results)

        # get short summary from find-path.txt
        short_summary = summary_dict.get(file_path, "(No summary found)")

        # Build section
        output.append(f"## {file_path}\n\n")
        output.append(f"**Short Summary:** {short_summary}\n\n")

        if local_funcs:
            output.append("**Local Regex-Found Functions:**\n\n")
            for fn in local_funcs:
                output.append(f"- `{fn}`\n")
            output.append("\n")

        if ai_parse:
            output.append("**AI-based Function Extraction:**\n\n")
            output.append(ai_parse)
            output.append("\n\n")

    # Write out to OpenAI/repo-function.md
    with open(out_file, "w", encoding="utf-8") as outf:
        outf.writelines(output)

    print(f"{out_file} created with function details from each file!")

if __name__ == "__main__":
    main()