import os
import argparse
from dotenv import load_dotenv  # For loading environment variables from a .env file

from repo_manager import RepoManager
from jira_integrator import JiraIntegrator
from release_note_generator import ReleaseNoteGenerator
from output_writer import OutputWriter
from teams_integrator import TeamsIntegrator  # <-- IMPORT THE NEW CLASS


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
    parser.add_argument(
        "--jira-project-key",
        required=True,
        help="Jira project key to fetch tickets from",
    )
    # Add new argument for sending to Teams
    parser.add_argument(
        "--send-to-teams",
        action="store_true",  # Makes this a flag, e.g., --send-to-teams
        help="Send the generated release notes to a Microsoft Teams channel.",
    )

    args = parser.parse_args()

    # 2. Get environment variables for credentials
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    jira_server_url = os.getenv("JIRA_SERVER_URL")
    jira_user_email = os.getenv("JIRA_USER_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    teams_webhook_url = os.getenv("TEAMS_WEBHOOK_URL")  # <-- GET TEAMS WEBHOOK

    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return
    if not all([jira_server_url, jira_user_email, jira_api_token]):
        print(
            "Error: JIRA_SERVER_URL, JIRA_USER_EMAIL, or JIRA_API_TOKEN environment variables not set."
        )
        return

    # Validate Teams webhook URL if the flag is set
    if args.send_to_teams and not teams_webhook_url:
        print(
            "Error: --send-to-teams flag is set, but TEAMS_WEBHOOK_URL environment variable is not."
        )
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
    diff_text, commit_sha, all_codebase_content, repo_error = (
        repo_manager.get_last_diff_and_full_codebase(args.repo_path, args.branch)
    )

    if repo_error:
        print(f"Failed to get diff or codebase content: {repo_error}")
        return

    if not diff_text:
        print(
            "No significant diff found. Generating notes based on full codebase and Jira if available."
        )

    # 5. Get Jira notes for the project
    print(f"Fetching Jira notes for project: {args.jira_project_key}...")
    jira_data = jira_integrator.get_jira_notes_by_project(args.jira_project_key)

    if not jira_data:
        print("No Jira issues found or accessible for this project.")

    # 6. Generate release notes
    print(
        "Generating release notes using Google Generative AI (with full codebase context)..."
    )
    generated_notes = release_note_generator.generate_release_notes(
        diff_text, jira_data, commit_sha, all_codebase_content
    )

    if "Error: Could not generate release notes" in generated_notes:
        print(f"Failed to generate release notes:\n{generated_notes}")
        return

    # 7. Save release notes to file
    print("Saving generated release notes...")
    saved_filepath = output_writer.save_release_notes_to_file(
        generated_notes, args.output_dir
    )

    # 8. Send release notes to Teams if the flag is set
    if args.send_to_teams and saved_filepath:
        teams_integrator = TeamsIntegrator(teams_webhook_url)
        teams_integrator.send_release_notes(generated_notes, commit_sha)

    if saved_filepath:
        print(f"\nProcess completed. Release notes available at: {saved_filepath}")
    else:
        print("\nProcess completed with issues: Could not save release notes.")


if __name__ == "__main__":
    main()
