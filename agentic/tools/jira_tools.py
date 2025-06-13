# agentic/tools/jira_tools.py
import os
from jira import JIRA


# The core logic from the original JiraIntegrator is preserved.
class JiraManager:
    """
    Integrates with Jira to fetch issue details.
    """

    def __init__(self, jira_server_url: str, jira_user_email: str, jira_api_token: str):
        self.jira_server_url = jira_server_url
        self.jira_user_email = jira_user_email
        self.jira_api_token = jira_api_token
        self.jira_client = self._authenticate_jira()

    def _authenticate_jira(self):
        try:
            options = {"server": self.jira_server_url}
            jira = JIRA(options, basic_auth=(self.jira_user_email, self.jira_api_token))
            print("Successfully authenticated with Jira.")
            return jira
        except Exception as e:
            print(f"Error authenticating with Jira: {e}")
            return None

    def get_jira_notes_by_project(
        self, project_key: str, max_results: int = 50
    ) -> list[dict]:
        if not self.jira_client:
            print("Jira client not initialized.")
            return []
        try:
            jql = f'project = "{project_key}" ORDER BY created DESC'
            issues = self.jira_client.search_issues(jql, maxResults=max_results)
            print(f"Found {len(issues)} issues for project {project_key}")
            jira_issues_data = [
                {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": issue.fields.status.name,
                    "issue_type": issue.fields.issuetype.name,
                }
                for issue in issues
            ]
            return jira_issues_data
        except Exception as e:
            print(f"Error fetching issues for project {project_key}: {e}")
            return []


# We will initialize this manager in main.py where we have credentials.
# This makes the tool function pure and testable.
def get_jira_tickets(
    project_key: str, jira_server_url: str, jira_user_email: str, jira_api_token: str
) -> list[dict]:
    """
    Fetches the most recent Jira tickets for a given project key.

    Args:
        project_key: The Jira project key (e.g., 'PROJ', 'TEST').
        jira_server_url: The URL of the Jira instance.
        jira_user_email: The email for Jira authentication.
        jira_api_token: The API token for Jira authentication.

    Returns:
        A list of dictionaries, where each dictionary represents a Jira ticket
        with its key, summary, status, and issue type.
    """
    print(f"Tool 'get_jira_tickets' called for project: {project_key}")
    jira_manager = JiraManager(jira_server_url, jira_user_email, jira_api_token)
    return jira_manager.get_jira_notes_by_project(project_key)
