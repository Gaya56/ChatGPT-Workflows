###This Python script creates an interactive code analysis tool using OpenAI's GPT-4o to help developers 
understand and navigate the Google Maps JS Solar Potential repository. 
It scans specified directories in the codebase (avoiding node_modules and other noisy folders), 
extracts relevant code files, and feeds them to GPT-4o along with specialized prompts 
that establish context about the SvelteKit architecture. 

###The tool features API key rotation to handle rate limits, smart file content extraction with size limits, 
and maintains conversation history to allow developers to ask follow-up questions about specific implementation details, 
data flows, component hierarchies, and integration points. 

###It's essentially creating a smart assistant that can explain the codebase's architecture and help plan new feature 
implementations based on the existing code patterns.

# How to Edit a Variable Across All Repository Files

1. **Add a search and replace function** to Path_finder.py:
   ```python
   def replace_in_files(base_paths: List[str], old_value: str, new_value: str, file_patterns: List[str] = ["*.js", "*.ts", "*.svelte"]):
       modified_files = 0
       for base_path in base_paths:
           files = scan_directory(base_path, include_patterns=file_patterns, exclude_patterns=["*node_modules*", "*.git*"])
           for file_path in files:
               try:
                   with open(file_path, 'r', encoding='utf-8') as f:
                       content = f.read()
                   if old_value in content:
                       modified_content = content.replace(old_value, new_value)
                       with open(file_path, 'w', encoding='utf-8') as f:
                           f.write(modified_content)
                       modified_files += 1
                       print(f"Modified: {file_path}")
               except Exception as e:
                   print(f"Error processing {file_path}: {e}")
       print(f"Total files modified: {modified_files}")
   ```

2. **Call the function** with your variable:
   ```python
   # Example usage
   base_paths = ["/workspaces/js-solar-potential/src"]
   old_variable = "CLOUD_FUNCTION_URL"  # Variable to change
   new_variable = "NEW_CLOUD_FUNCTION_URL"  # New value
   replace_in_files(base_paths, old_variable, new_variable)
   ```

3. **For more precise matching** (optional), use regex:
   ```python
   # For more precise variable replacement
   import re
   def replace_variable_regex(base_paths, var_name, new_value, file_patterns=["*.js", "*.ts"]):
       pattern = rf"(const|let|var)\s+{var_name}\s*=\s*['\"]([^'\"]*)['\"]"
       replacement = f"\\1 {var_name} = \"{new_value}\""
       # Rest of function using re.sub(pattern, replacement, content)
   ```

Run the script with your specific variable name and new value to update it across all matching files.
