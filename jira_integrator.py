#!/usr/bin/env python3

import os
import re
from jira import JIRA


class JiraIntegrator:
    """
    Integrates with Jira to fetch issue details.
    """

    def __init__(self, jira_server_url: str, jira_api_token: str, jira_user_email: str):
        """
        Initializes the JiraIntegrator with Jira server URL and API token.

        Args:
            jira_server_url (str): The URL of your Jira instance.
            jira_api_token (str): The API token for Jira authentication.
            jira_user_email (str): The email of the user associated with the API token.
        """
        self.jira_server_url = jira_server_url
        self.jira_api_token = jira_api_token
        self.jira_user_email = jira_user_email
        self.jira_client = self._authenticate_jira()

    def _authenticate_jira(self):
        """
        Authenticates with Jira using the provided API token.
        """
        try:
            options = {"server": self.jira_server_url}
            # Use basic_auth with email and API token
            jira = JIRA(options, basic_auth=(self.jira_user_email, self.jira_api_token))
            print("Successfully authenticated with Jira.")
            return jira
        except Exception as e:
            print(f"Error authenticating with Jira: {e}")
            return None

    def _extract_jira_keys(self, text: str) -> set[str]:
        """
        Extracts potential Jira issue keys from a given text (e.g., commit messages).
        Matches patterns like 'PROJ-123', 'ABC-456'.

        Args:
            text (str): The text to search for Jira keys.

        Returns:
            set[str]: A set of unique Jira issue keys found.
        """
        # Regex to find common Jira key patterns (e.g., PROJ-123, DEV-456)
        # Assumes project keys are 2+ uppercase letters, followed by a hyphen and numbers.
        jira_key_pattern = r"\b[A-Z]{2,}-\d+\b"
        matches = re.findall(jira_key_pattern, text)
        return set(matches)

    def get_jira_notes_by_project(
        self, project_key: str, max_results: int = 50
    ) -> list[dict]:
        """
        Fetches all Jira issues for a specific project.

        Args:
            project_key (str): The project key to fetch issues for
            max_results (int): Maximum number of issues to return

        Returns:
            list[dict]: A list of Jira issue details
        """
        if not self.jira_client:
            print("Jira client not initialized. Cannot fetch issues.")
            return []

        try:
            # Search for all issues in the project
            jql = f'project = "{project_key}" ORDER BY created DESC'
            issues = self.jira_client.search_issues(jql, maxResults=max_results)
            print(f"Found {len(issues)} issues for project {project_key}")

            jira_issues_data = []
            for issue in issues:
                jira_issues_data.append(
                    {
                        "key": issue.key,
                        "summary": issue.fields.summary,
                        "status": issue.fields.status.name,
                        "issue_type": issue.fields.issuetype.name,
                        "description": (
                            issue.fields.description
                            if issue.fields.description
                            else "No description provided."
                        ),
                        "assignee": (
                            issue.fields.assignee.displayName
                            if issue.fields.assignee
                            else "Unassigned"
                        ),
                        "reporter": (
                            issue.fields.reporter.displayName
                            if issue.fields.reporter
                            else "Unknown"
                        ),
                        "priority": (
                            issue.fields.priority.name
                            if issue.fields.priority
                            else "None"
                        ),
                        "resolution": (
                            issue.fields.resolution.name
                            if issue.fields.resolution
                            else "Unresolved"
                        ),
                        "created": issue.fields.created,
                        "updated": issue.fields.updated,
                    }
                )
            return jira_issues_data
        except Exception as e:
            print(f"Error fetching issues for project {project_key}: {e}")
            return []


if __name__ == "__main__":
    # Example usage (for testing this module independently)
    # NOTE: You MUST set these environment variables for this example to work.
    # export JIRA_SERVER_URL="https://your-jira-instance.atlassian.net"
    # export JIRA_USER_EMAIL="your_jira_email@example.com"
    # export JIRA_API_TOKEN="your_jira_api_token"

    jira_server = os.getenv("JIRA_SERVER_URL")
    jira_user = os.getenv("JIRA_USER_EMAIL")
    jira_token = os.getenv("JIRA_API_TOKEN")

    if not all([jira_server, jira_user, jira_token]):
        print(
            "Please set JIRA_SERVER_URL, JIRA_USER_EMAIL, and JIRA_API_TOKEN environment variables for testing."
        )
    else:
        integrator = JiraIntegrator(jira_server, jira_token, jira_user)

        # Example diff text containing a mock Jira key
        mock_diff_text = """
        diff --git a/src/feature.py b/src/feature.py
        index abcdef1..1234567 100644
        --- a/src/feature.py
        +++ b/src/feature.py
        @@ -1,5 +1,6 @@
         def new_function():
             pass
        -
        +SCRUM-1: Added a new feature.
         def old_function():
             pass
        """

        # This will attempt to fetch PROJ-123. Ensure it exists in your Jira instance
        # and your token has permission to view it.
        jira_data = integrator.get_jira_notes_for_diff(mock_diff_text)
        if jira_data:
            print("\n--- Fetched Jira Data ---")
            for issue in jira_data:
                print(
                    f"Key: {issue['key']}, Summary: {issue['summary']}, Type: {issue['issue_type']}"
                )
        else:
            print("\nNo Jira data fetched or an error occurred.")
