import os
import openai

def summarize_content(content):
    """
    Sends a short snippet of the file content to OpenAI
    and returns a brief two-sentence description.
    """
    try:
        # Feel free to adjust model, max_tokens, temperature, etc.
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(
                f"Summarize this file content in two sentences, focusing on its role in a code repository:\n\n{content}\n\n"
            ),
            max_tokens=50,
            temperature=0.7
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        return f"Could not summarize: {str(e)}"

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    # The directory you want to walk through. By default, the repo root.
    target_directory = "."

    output_lines = ["Repository Paths and Summaries:\n\n"]

    for root, dirs, files in os.walk(target_directory):
        # Skip the .git folder or any other folder you don't want to process
        if '.git' in root:
            continue

        for filename in files:
            # Build the full path
            full_path = os.path.join(root, filename)
            # Relativize the path for easier readability
            display_path = os.path.relpath(full_path, start=".")

            # Read a small snippet from each file
            snippet = ""
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    snippet = f.read(200)  # Read the first 200 chars
            except:
                snippet = "Non-text or unreadable file."

            # Summarize via OpenAI
            summary = summarize_content(snippet)

            output_lines.append(f"**Path**: {display_path}\n")
            output_lines.append(f"**Summary**: {summary}\n\n")

    # Ensure the 'OpenAI' folder exists
    os.makedirs("OpenAI", exist_ok=True)
    file_path = os.path.join("OpenAI", "find-path.txt")

    # Write everything to a single file
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print(f"Paths and summaries saved to {file_path}")

if __name__ == "__main__":
    main()

