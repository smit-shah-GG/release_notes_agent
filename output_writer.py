#!/usr/bin/env python3

import datetime
import os


class OutputWriter:
    """
    Manages saving generated content to local files.
    """

    def __init__(self):
        """
        Initializes the OutputWriter.
        """
        pass

    def save_release_notes_to_file(
        self, release_notes_content: str, output_dir: str = "release_notes"
    ) -> str:
        """
        Saves the release notes content to a Markdown file with a timestamped name.

        Args:
            release_notes_content (str): The Markdown content of the release notes.
            output_dir (str): The directory where the file will be saved.
                              Defaults to 'release_notes' in the current working directory.

        Returns:
            str: The full path to the saved file, or an empty string if saving failed.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"release_notes_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)

        try:
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(release_notes_content)
            print(f"Release notes saved successfully to: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving release notes to file '{filepath}': {e}")
            return ""


if __name__ == "__main__":
    # Example usage (for testing this module independently)
    writer = OutputWriter()
    mock_notes = """
### 2024-01-01 Release
#### New Features
- Implemented user profiles (FEAT-100).
#### Bug Fixes
- Fixed login redirection (BUG-200).
"""
    saved_path = writer.save_release_notes_to_file(mock_notes, "dev_release_notes")
    if saved_path:
        print(f"Mock notes saved to: {saved_path}")
