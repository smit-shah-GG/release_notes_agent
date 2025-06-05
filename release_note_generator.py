#!/usr/bin/env python3

import google.generativeai as genai
import os
import json  # For better formatting of Jira data for the LLM


class ReleaseNoteGenerator:
    """
    Generates release notes using the Google Generative AI model.
    """

    def __init__(self):
        """
        Initializes the ReleaseNoteGenerator.
        Configures the google-generativeai library using GEMINI_API_KEY from environment.
        """
        api_key = os.getenv("GEMINI_API_KEY", "AIzaSyCcfe3aNTRPMS2QrO_HBsWGy2Kku-lwjEQ")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set. Please provide your Google AI API key."
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash"
        )  # Or 'gemini-1.5-pro' for more complex reasoning

    def generate_release_notes(
        self, diff_text: str, jira_data: list[dict], commit_sha: str
    ) -> str:
        """
        Generates release notes based on the provided diff text and Jira issue data.

        Args:
            diff_text (str): The raw code diff.
            jira_data (list[dict]): A list of dictionaries containing Jira issue details.
            commit_sha (str): The SHA of the last commit for context.

        Returns:
            str: The generated release notes in Markdown format.
        """
        # Convert Jira data to a more readable JSON string for the LLM
        jira_data_str = json.dumps(jira_data, indent=2)

        prompt = f"""
        You are an expert release note generator. Your task is to create clear, concise, and informative release notes based on a code diff and associated Jira tickets.

        **Instructions:**
        - Analyze the `CODE_DIFF` and `JIRA_TICKETS` carefully.
        - Infer new features, bug fixes, and general improvements.
        - List resolved Jira tickets by their key and summary.
        - Focus on user-facing changes where possible.
        - Avoid overly technical jargon.
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

        ---
        **Release Notes for Commit: `{commit_sha}`**

        Please generate the release notes following this structure:

        ### [Release Version/Date - e.g., YYYY-MM-DD Update]

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
    # NOTE: You MUST set GEMINI_API_KEY environment variable for this example to work.
    # export GEMINI_API_KEY="YOUR_GOOGLE_AI_API_KEY"

    if not os.getenv("GEMINI_API_KEY"):
        print("Please set GEMINI_API_KEY environment variable for testing.")
    else:
        generator = ReleaseNoteGenerator()

        mock_diff = """
        diff --git a/app.py b/app.py
        index 1234abc..def5678 100644
        --- a/app.py
        +++ b/app.py
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

        notes = generator.generate_release_notes(
            mock_diff, mock_jira_data, mock_commit_sha
        )
        print("\n--- Generated Release Notes ---")
        print(notes)
