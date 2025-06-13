import datetime
import os
import pymsteams


def save_release_notes_to_file(release_notes_content: str, output_dir: str) -> str:
    """
    Saves the release notes content to a Markdown file with a timestamped name.

    Args:
        release_notes_content: The Markdown content of the release notes to save.
        output_dir: The directory where the file will be saved.

    Returns:
        The full path to the saved file, or an error message if saving failed.
    """
    print(
        f"Tool 'save_release_notes_to_file' called for output directory: {output_dir}"
    )
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"release_notes_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(release_notes_content)
        success_message = f"Release notes saved successfully to: {filepath}"
        print(success_message)
        return success_message
    except Exception as e:
        error_message = f"Error saving release notes to file '{filepath}': {e}"
        print(error_message)
        return error_message
