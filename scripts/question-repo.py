import openai
import os
import time
import glob
import re
import fnmatch
from typing import List, Dict, Any, Tuple, Set, Optional

# List of API keys for rotation
api_keys = ["API_KEYHERE",
    # Add additional API keys here
    # "sk-your-second-api-key",
    # "sk-your-third-api-key",
]

# Initialize with the first key
current_key_index = 0
os.environ["OPENAI_API_KEY"] = api_keys[current_key_index]
client = openai.OpenAI(api_key=api_keys[current_key_index])

# Updated system prompt to establish the expanded context and focus
system_prompt = """You are an expert code analyst and documentation processor specializing in JavaScript, web applications, and SvelteKit architecture mapping.
Your task is to help developers understand, navigate, and modify codebases more efficiently.

For each response:
1. Structure your explanations clearly, using headers and lists
2. Be specific about file locations and their purposes
3. When describing where to make changes, provide exact file paths and line numbers if possible
4. Explain both WHAT each component does and WHY it exists in the architecture
5. Reference relevant documentation from Dialogflow CX, SvelteKit, and Google Cloud Run when applicable
6. Include implementation guidance based on documentation and existing code patterns
7. For any follow-up questions, maintain context from previous answers"""

# Updated initial user message content with expanded focus
initial_prompt = """I need a comprehensive analysis of the Google Maps JS Solar Potential repository to understand the complete workflow and implementation options:

✅ Identify all functional pathways in the codebase
✅ Map data flow between components and modules
✅ Understand the dependency hierarchy between files
✅ Process technical documentation related to the codebase
✅ Provide implementation guidance with specific line numbers

### **🔍 What I Need:**  
1. **Identify all entry points** to the application (main files, routes, API endpoints).
2. **Map the component hierarchy** - parent-child relationships between Svelte components.
3. **Trace data flow paths** from user inputs through to displayed outputs and calculations.
4. **Document all key functions** that handle data transformation, API calls, or state changes.
5. **Create a dependency graph** showing which files import/require which other files.
6. **Identify event propagation chains** - how events from one component affect others.
7. **Categorize files by location and purpose** with precise line numbers for reference.
8. **Locate documentation references** for Dialogflow CX, SvelteKit, and Google Cloud Run components.
9. **Find insertion points** where new code should be added for specific features.

### **📂 Key Repository Paths to Analyze:**
- /workspaces/js-solar-potential/.svelte-kit
- /workspaces/js-solar-potential/build/server
- /workspaces/js-solar-potential/build/client
- /workspaces/js-solar-potential/build/prerendered
- /workspaces/js-solar-potential/build
- /workspaces/js-solar-potential/src
- /workspaces/js-solar-potential/src/routes
- /workspaces/js-solar-potential/src/routes/components
- /workspaces/js-solar-potential/src/routes/sections
- /workspaces/js-solar-potential/src/theme
- /workspaces/js-solar-potential/static
- /workspaces/js-solar-potential/tests
- .svelte-kit/adapter-node
- .svelte-kit/generated
- .svelte-kit/output
- .svelte-kit/types
- .svelte-kit/types/src/routes
- .svelte-kit/adapter-node/_app
- .svelte-kit/adapter-node/.vite
- .svelte-kit/adapter-node/nodes

This will help me understand the complete architecture, implement new features, and fix issues by seeing the full picture of how data and control flows through the system, with guidance from both code analysis and relevant documentation."""

def rotate_api_key() -> None:
    """Rotate to the next available API key in the list"""
    global current_key_index, client
    current_key_index = (current_key_index + 1) % len(api_keys)
    os.environ["OPENAI_API_KEY"] = api_keys[current_key_index]
    client = openai.OpenAI(api_key=api_keys[current_key_index])
    print(f"Switched to API key #{current_key_index + 1}")

def send_message_to_gpt(messages: List[Dict[str, Any]]) -> str:
    """Send messages to GPT and return the response, with automatic key rotation on failure"""
    global current_key_index
    
    # Try each API key up to the number of keys we have
    for attempt in range(len(api_keys)):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            
            if completion.choices:
                return completion.choices[0].message.content
            else:
                return "No response received."
                
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a rate limit or quota error
            if "rate limit" in error_str or "quota" in error_str or "capacity" in error_str:
                print(f"API key #{current_key_index + 1} hit rate limit. Rotating to next key...")
                rotate_api_key()
                # Short pause before retry
                time.sleep(1)
            else:
                # For other errors, just return the error message
                return f"Error occurred while calling OpenAI API: {str(e)}"
    
    # If we've tried all keys and still failed
    return "All available API keys have been exhausted or are rate limited. Please try again later."

def print_with_formatting(text):
    """Print response with nice formatting"""
    print("\n" + "="*80)
    print(text)
    print("="*80 + "\n")

def glob_to_regex(pattern: str) -> str:
    """
    Convert a glob pattern to a regular expression pattern
    
    Args:
        pattern: Glob pattern (e.g. "*.js")
    
    Returns:
        Regular expression pattern
    """
    # Escape all special regex characters, but keep * and ? special for glob matching
    pattern = re.escape(pattern)
    # Convert glob * to regex .*
    pattern = pattern.replace('\\*', '.*')
    # Convert glob ? to regex .
    pattern = pattern.replace('\\?', '.')
    # Add anchors to match the whole string
    return f'^{pattern}$'

def scan_directory(base_path: str, include_patterns: List[str] = None, exclude_patterns: List[str] = None) -> List[str]:
    """
    Scan directory recursively and return list of files matching include/exclude patterns
    
    Args:
        base_path: Base directory path to scan
        include_patterns: List of glob patterns to include (e.g. ["*.py", "*.js"])
        exclude_patterns: List of glob patterns to exclude (e.g. ["node_modules/*", "*.min.js"])
    
    Returns:
        List of matching file paths
    """
    if not os.path.exists(base_path):
        print(f"Warning: Path {base_path} does not exist")
        return []
        
    if include_patterns is None:
        include_patterns = ["*"]
    
    all_files = []
    
    # Find all matching files
    for pattern in include_patterns:
        pattern_path = os.path.join(base_path, "**", pattern)
        all_files.extend(glob.glob(pattern_path, recursive=True))
    
    # Apply exclusion patterns if specified
    if exclude_patterns:
        filtered_files = []
        for file_path in all_files:
            exclude_this_file = False
            for exclude in exclude_patterns:
                # Use fnmatch instead of regex for more reliable glob-style matching
                if fnmatch.fnmatch(file_path, "*" + exclude + "*"):
                    exclude_this_file = True
                    break
            if not exclude_this_file:
                filtered_files.append(file_path)
        all_files = filtered_files
    
    return sorted(all_files)

def read_file_content(file_path: str, max_chars: int = 10000) -> str:
    """
    Read file content safely with size limit
    
    Args:
        file_path: Path to the file
        max_chars: Maximum number of characters to read
    
    Returns:
        File content or error message
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read(max_chars)
            if len(content) >= max_chars:
                content += "\n... [content truncated due to size] ..."
            return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

def analyze_code_files(base_paths: List[str], files_per_path: int = 5, max_chars_per_file: int = 5000) -> Dict[str, Any]:
    """
    Analyze code files in specified paths
    
    Args:
        base_paths: List of base directories to scan
        files_per_path: Maximum number of files to include per path
        max_chars_per_file: Maximum characters to read per file
    
    Returns:
        Dictionary with analysis results
    """
    analysis_results = {
        "file_count": 0,
        "scanned_files": [],
        "file_contents": {}
    }
    
    # Define common code file extensions
    code_extensions = ["*.js", "*.jsx", "*.ts", "*.tsx", "*.svelte", "*.html", "*.css", "*.py", "*.json"]
    
    # Define directories to exclude
    exclude_dirs = ["*node_modules*", "*build/client*", "*__pycache__*", "*.git*"]
    
    for base_path in base_paths:
        # Get files in this path
        files = scan_directory(base_path, include_patterns=code_extensions, exclude_patterns=exclude_dirs)
        
        # Limit number of files per path
        path_files = files[:files_per_path]
        analysis_results["scanned_files"].extend(path_files)
        
        # Read content of each file
        for file_path in path_files:
            content = read_file_content(file_path, max_chars=max_chars_per_file)
            analysis_results["file_contents"][file_path] = content
            analysis_results["file_count"] += 1
    
    return analysis_results

def prepare_file_context(analysis_results: Dict[str, Any], max_tokens: int = 10000) -> str:
    """
    Prepare file context for sending to GPT
    
    Args:
        analysis_results: Results from analyze_code_files
        max_tokens: Approximate maximum tokens to include
    
    Returns:
        Formatted file context as string
    """
    context = f"Repository Analysis Results:\n\n"
    context += f"Total files scanned: {analysis_results['file_count']}\n\n"
    
    # Approximate character to token ratio (conservative estimate)
    chars_per_token = 3.5
    max_chars = int(max_tokens * chars_per_token)
    
    current_chars = len(context)
    
    # Add file contents up to max_chars
    for file_path, content in analysis_results["file_contents"].items():
        file_section = f"FILE: {file_path}\n```\n{content}\n```\n\n"
        
        if current_chars + len(file_section) > max_chars:
            context += "\n[Additional files omitted due to context length limitations]"
            break
            
        context += file_section
        current_chars += len(file_section)
    
    return context

def main():
    # Initialize paths to analyze
    base_paths = [
        "/workspaces/js-solar-potential/src",
        "/workspaces/js-solar-potential/src/routes",
        "/workspaces/js-solar-potential/.svelte-kit",
    ]
    
    print("Scanning repository and analyzing code files...")
    analysis_results = analyze_code_files(base_paths)
    
    print(f"Found {analysis_results['file_count']} relevant files to analyze.")
    
    # Prepare file context
    file_context = prepare_file_context(analysis_results)
    
    # Add file context to the initial prompt
    enhanced_prompt = initial_prompt + "\n\n### Code Analysis Context:\n" + file_context
    
    # Initialize conversation history
    conversation_history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": enhanced_prompt}
    ]
    
    print(f"Starting comprehensive codebase and documentation analysis using API key #{current_key_index + 1}.")
    print(f"Total available API keys: {len(api_keys)}")
    print("Please wait for initial results...")
    
    # Get initial analysis
    response = send_message_to_gpt(conversation_history)
    conversation_history.append({"role": "assistant", "content": response})
    
    print_with_formatting(response)
    
    print("\nYou can now ask follow-up questions about the codebase structure, specific files,")
    print("implementation details, or where to make changes for particular features.")
    print("Type 'exit' to quit.\n")
    
    # Interactive loop for follow-up questions
    while True:
        user_input = input("\n> What would you like to know about the codebase? ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting codebase analysis session.")
            break
        
        # Add new user message to conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        # Get response
        print("\nProcessing your question...")
        response = send_message_to_gpt(conversation_history)
        conversation_history.append({"role": "assistant", "content": response})
        
        print_with_formatting(response)

if __name__ == "__main__":
    main()
