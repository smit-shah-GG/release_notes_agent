import os
import argparse
from dotenv import load_dotenv  # For loading environment variables from a .env file

from repo_manager import RepoManager
from jira_integrator import JiraIntegrator
from release_note_generator import ReleaseNoteGenerator
from output_writer import OutputWriter


def main():
    """
    Main function to orchestrate the release note generation process.
    """
    # Load environment variables from a .env file (if present)
    load_dotenv()

    # 1. Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate release notes from a local Git repository and Jira, with full codebase context."
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="Local file system path to the Git repository.",
    )
    parser.add_argument("--branch", default="main", help="Branch name (default: main).")
    parser.add_argument(
        "--output-dir",
        default="generated_release_notes",
        help="Directory to save release notes.",
    )

    args = parser.parse_args()

    # 2. Get environment variables for credentials
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    jira_server_url = os.getenv("JIRA_SERVER_URL")
    jira_user_email = os.getenv("JIRA_USER_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")

    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set your Google AI API key.")
        return
    if not all([jira_server_url, jira_user_email, jira_api_token]):
        print(
            "Error: JIRA_SERVER_URL, JIRA_USER_EMAIL, or JIRA_API_TOKEN environment variables not set."
        )
        print("Please set your Jira credentials.")
        return

    print("Starting release note generation process...")

    # 3. Initialize modules
    repo_manager = RepoManager()
    jira_integrator = JiraIntegrator(jira_server_url, jira_api_token, jira_user_email)
    release_note_generator = ReleaseNoteGenerator()
    output_writer = OutputWriter()

    # 4. Get last diff and full codebase content from local repository
    print(
        f"Fetching last diff and full codebase content for local repo at {args.repo_path} on branch {args.branch}..."
    )
    # Renamed the method call
    diff_text, commit_sha, all_codebase_content, repo_error = (
        repo_manager.get_last_diff_and_full_codebase(args.repo_path, args.branch)
    )

    if repo_error:
        print(f"Failed to get diff or codebase content: {repo_error}")
        return

    # Check if there's any diff, even if codebase content was collected
    if not diff_text:
        print(
            "No significant diff found. Generating notes based on full codebase and Jira if available."
        )
        # If no diff, still proceed if we have a codebase and Jira data might be relevant

    # 5. Get Jira notes for the diff
    print("Fetching Jira notes...")
    jira_data = jira_integrator.get_jira_notes_for_diff(diff_text)

    if not jira_data:
        print("No Jira issues found or accessible for this diff.")

    # 6. Generate release notes with enhanced context
    print(
        "Generating release notes using Google Generative AI (with full codebase context)..."
    )
    generated_notes = release_note_generator.generate_release_notes(
        diff_text, jira_data, commit_sha, all_codebase_content  # Pass the new context
    )

    if "Error: Could not generate release notes" in generated_notes:
        print(f"Failed to generate release notes:\n{generated_notes}")
        return

    # 7. Save release notes to file
    print("Saving generated release notes...")
    saved_filepath = output_writer.save_release_notes_to_file(
        generated_notes, args.output_dir
    )

    if saved_filepath:
        print(f"\nProcess completed. Release notes available at: {saved_filepath}")
    else:
        print("\nProcess completed with issues: Could not save release notes.")


if __name__ == "__main__":
    main()
