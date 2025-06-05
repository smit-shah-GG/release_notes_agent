#!/usr/bin/env python3
import google.generativeai as genai
import os
import json


class ReleaseNoteGenerator:
    """
    Generates release notes using the Google Generative AI model,
    now with added context from the full content of the entire codebase.
    """

    def __init__(self):
        """
        Initializes the ReleaseNoteGenerator.
        Configures the google-generativeai library using GEMINI_API_KEY from environment.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set. Please provide your Google AI API key."
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash"
        )  # Or 'gemini-1.5-pro' for more complex reasoning

    def generate_release_notes(
        self,
        diff_text: str,
        jira_data: list[dict],
        commit_sha: str,
        all_codebase_content: dict,
    ) -> str:
        """
        Generates release notes based on the provided diff text, Jira issue data,
        and the full content of the entire codebase.

        Args:
            diff_text (str): The raw code diff.
            jira_data (list[dict]): A list of dictionaries containing Jira issue details.
            commit_sha (str): The SHA of the last commit for context.
            all_codebase_content (dict): A dictionary where keys are relative file paths
                                         and values are their full content.

        Returns:
            str: The generated release notes in Markdown format.
        """
        jira_data_str = json.dumps(jira_data, indent=2)

        # Format full codebase content for the prompt
        full_codebase_context_str = ""
        if all_codebase_content:
            full_codebase_context_str = "\n--- Entire Codebase Context ---\n"
            # Sort files by path for consistent ordering
            sorted_file_paths = sorted(all_codebase_content.keys())

            for file_path in sorted_file_paths:
                content = all_codebase_content[file_path]
                full_codebase_context_str += f"### File: {file_path}\n"
                full_codebase_context_str += "```\n"
                full_codebase_context_str += (
                    content  # Content is already potentially truncated by RepoManager
                )
                full_codebase_context_str += "\n```\n\n"
            full_codebase_context_str += "----------------------------------\n"

        prompt = f"""
        You are an expert release note generator. Your task is to create clear, concise, and informative release notes based on a code diff, associated Jira tickets, and the full context of the entire codebase provided.

        **Instructions:**
        - Analyze the `CODE_DIFF`, `JIRA_TICKETS`, and the `ENTIRE_CODEBASE_CONTEXT` carefully.
        - Use the `ENTIRE_CODEBASE_CONTEXT` to understand the broader architecture, dependencies, and implications of the changes described in the `CODE_DIFF` and linked to `JIRA_TICKETS`.
        - Infer new features, bug fixes, and general improvements by examining the actual code changes within the provided files, leveraging the full codebase context for deeper understanding.
        - List resolved Jira tickets by their key and summary.
        - Focus on user-facing changes where possible.
        - Avoid overly technical jargon, but feel free to reference specific code changes or architectural impacts if it clarifies a feature/fix.
        - Generate notes in Markdown format.
        - If no significant features or bug fixes are apparent, mention general changes or maintenance updates.

        ---
        **CODE_DIFF:**
        ```diff
        {diff_text}
        ```

        ---
        **JIRA_TICKETS:**
        ```json
        {jira_data_str}
        ```

        {full_codebase_context_str}

        ---
        **Release Notes for Commit: `{commit_sha}`**

        Please generate the release notes following this structure:

        ### [Release Version/Date - e.g., YMCA-MM-DD Update]

        #### New Features
        - [List new features, referencing Jira issues if applicable (e.g., `New Dashboard Widget (JIRA-123)`)]
        - ...

        #### Bug Fixes
        - [List bug fixes, referencing Jira issues (e.g., `Fixed login issue (JIRA-456)`)]
        - ...

        #### Resolved Issues
        - [JIRA-XXX: Summary of issue]
        - [JIRA-YYY: Another issue summary]
        - ...

        #### Improvements & General Changes
        - [List any other significant changes or performance improvements.]
        - ...

        ---
        """

        print("Sending prompt to Google Generative AI model...")
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content with Gemini: {e}")
            return f"Error: Could not generate release notes. {e}"


if __name__ == "__main__":
    # Example usage (for testing this module independently)
    if not os.getenv("GEMINI_API_KEY"):
        print("Please set GEMINI_API_KEY environment variable for testing.")
    else:
        generator = ReleaseNoteGenerator()

        mock_diff = """
        diff --git a/src/app.py b/src/app.py
        index 1234abc..def5678 100644
        --- a/src/app.py
        +++ b/src/app.py
        @@ -10,6 +10,10 @@
         def process_data(data):
             # Existing logic
             pass
        +
        +# FEAT-789: Add support for new data format
        +def convert_new_format(input_data):
        +    return f"Converted: {input_data}"
        +
         # BUG-456: Fix pagination error
         def get_paginated_results(items, page_size, page_num):
             if page_num < 1:
        -        return [] # Incorrect handling for page_num < 1
        +        raise ValueError("Page number cannot be less than 1.")
             start_index = (page_num - 1) * page_size
             end_index = start_index + page_size
             return items[start_index:end_index]
        """

        mock_jira_data = [
            {
                "key": "FEAT-789",
                "summary": "Implement new data format converter",
                "status": "Done",
                "issue_type": "Story",
                "description": "A new converter function to handle the new XYZ data format.",
            },
            {
                "key": "BUG-456",
                "summary": "Pagination throws error on first page",
                "status": "Done",
                "issue_type": "Bug",
                "description": "The pagination logic was incorrectly handling page_num less than 1, causing an empty list instead of an error.",
            },
        ]
        mock_commit_sha = "abcdef1234567890"

        # Mock full codebase content (simplified for example)
        mock_full_codebase_content = {
            "src/app.py": """
import json
# This is a mock example of the full app.py file
# It contains the new functions from the diff as well as old ones.

def init_app():
    print("App initialized.")

def process_data(data):
    # Existing logic
    return data # Simplified

# FEAT-789: Add support for new data format
def convert_new_format(input_data):
    # More complex conversion logic would go here
    return f"Converted and processed: {input_data}"

# BUG-456: Fix pagination error
def get_paginated_results(items, page_size, page_num):
    if page_num < 1:
        raise ValueError("Page number cannot be less than 1.")
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    return items[start_index:end_index]

def run_server():
    print("Server running.")
""",
            "src/config.py": """
# This is a mock example of a config file
API_KEY = "my_api_key_123"
DEBUG_MODE = True
""",
            "tests/test_app.py": """
import unittest
from src.app import convert_new_format, get_paginated_results

class TestApp(unittest.TestCase):
    def test_convert_new_format(self):
        self.assertEqual(convert_new_format("test"), "Converted and processed: test")

    def test_pagination_error(self):
        with self.assertRaises(ValueError):
            get_paginated_results([], 10, 0)
""",
        }

        notes = generator.generate_release_notes(
            mock_diff,
            mock_jira_data,
            mock_commit_sha,
            mock_full_codebase_content,  # Pass the mock full codebase content
        )
        print("\n--- Generated Release Notes ---")
        print(notes)
