#!/usr/bin/env python3

import argparse
import sys
from .config import config
from .base_agent import enhanced_coordinator


def main():
    """
    Main entry point for the agentic release notes system.
    Provides CLI interface and coordinates the orchestrator agent.
    """
    print("🚀 Starting Agentic Release Notes Generator...")

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate release notes using an agentic AI system with specialized agents."
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="Local file system path to the Git repository",
    )
    parser.add_argument(
        "--branch", default="main", help="Branch name to analyze (default: main)"
    )
    parser.add_argument(
        "--jira-project-key",
        required=True,
        help="Jira project key to fetch tickets from (e.g., PROJ, DEV)",
    )
    parser.add_argument(
        "--output-dir",
        default="generated_release_notes",
        help="Directory to save release notes (default: generated_release_notes)",
    )
    parser.add_argument(
        "--send-to-teams",
        action="store_true",
        help="Flag to send generated release notes to Microsoft Teams",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode for conversational interface",
    )

    args = parser.parse_args()

    # Validate configuration
    is_valid, missing_vars = config.validate_required_credentials(
        require_teams=args.send_to_teams
    )
    if not is_valid:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these environment variables and try again.")
        sys.exit(1)

    print("✅ Configuration validated successfully")

    if args.interactive:
        run_interactive_mode(args)
    else:
        run_single_command(args)


def run_single_command(args):
    """Run a single release notes generation command."""
    print(f"📁 Repository: {args.repo_path}")
    print(f"🌿 Branch: {args.branch}")
    print(f"🎫 Jira Project: {args.jira_project_key}")
    print(f"📄 Output Directory: {args.output_dir}")
    if args.send_to_teams:
        print("📢 Will send to Teams after generation")

    # Create the prompt for the orchestrator with ALL needed information
    user_request = f"""
    Please generate comprehensive release notes with the following specifications:

    Repository Details:
    - Path: {args.repo_path}
    - Branch: {args.branch}

    Jira Integration:
    - Project Key: {args.jira_project_key}
    - Server URL: {config.jira_server_url}
    - User Email: {config.jira_user_email}
    - API Token: {config.jira_api_token}

    Output Requirements:
    - Save to directory: {args.output_dir}
    {"- Send to Microsoft Teams with webhook: " + config.teams_webhook_url if args.send_to_teams else ""}

    Please coordinate with your specialized agents to:
    1. Repository Agent: Use get_repository_context tool with repo_path="{args.repo_path}" and branch="{args.branch}"
    2. Jira Agent: Use get_jira_tickets tool with project_key="{args.jira_project_key}", jira_server_url="{config.jira_server_url}", jira_user_email="{config.jira_user_email}", jira_api_token="{config.jira_api_token}"
    3. Generator Agent: Create release notes from the collected data
    4. Output Agent: Save to directory "{args.output_dir}"
    {"5. Teams Agent: Send to webhook URL" if args.send_to_teams else ""}
    """

    print("\n🤖 Coordinating with specialized agents...")
    try:
        result = enhanced_coordinator.run(user_request)
        print("\n" + "=" * 50)
        print("✅ RELEASE NOTES GENERATION COMPLETE")
        print("=" * 50)
        print(result)
    except Exception as e:
        print(f"\n❌ Error during release notes generation: {e}")
        sys.exit(1)


def run_interactive_mode(args):
    """Run in interactive conversational mode."""
    print("\n🗣️  Interactive Mode - You can now chat with the release notes coordinator")
    print("Type 'quit', 'exit', or 'bye' to end the session")
    print("Type 'help' for available commands")
    print("-" * 60)

    # Set up context with the provided arguments
    context = f"""
    Current session context:
    - Repository: {args.repo_path} (branch: {args.branch})
    - Jira Project: {args.jira_project_key}
    - Output Directory: {args.output_dir}
    - Teams Integration: {'Enabled' if args.send_to_teams else 'Disabled'}
    """

    print(context)
    print("-" * 60)

    while True:
        try:
            user_input = input("\n💬 You: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == "help":
                show_help()
                continue
            elif user_input.lower() == "context":
                print(context)
                continue
            elif not user_input:
                continue

            # Add context to user input
            full_request = f"{context}\n\nUser request: {user_input}"

            print("\n🤖 Coordinator: Working on your request...")
            result = enhanced_coordinator.run(full_request)
            print(f"\n🤖 Coordinator: {result}")

        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def show_help():
    """Show available commands in interactive mode."""
    help_text = """
Available commands:
- 'generate release notes' - Generate release notes for the current repository
- 'send to teams' - Send the last generated release notes to Teams
- 'show recent commits' - Display recent commits from the repository
- 'list jira tickets' - Show recent Jira tickets for the project
- 'context' - Show current session context
- 'help' - Show this help message
- 'quit', 'exit', 'bye' - End the session

You can also ask natural language questions like:
- "What changed in the last commit?"
- "Generate release notes and send them to Teams"
- "Show me the Jira tickets for this project"
"""
    print(help_text)


if __name__ == "__main__":
    main()
