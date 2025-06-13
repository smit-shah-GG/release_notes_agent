import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration management for the agentic release notes system."""

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.jira_server_url = os.getenv("JIRA_SERVER_URL")
        self.jira_user_email = os.getenv("JIRA_USER_EMAIL")
        self.jira_api_token = os.getenv("JIRA_API_TOKEN")
        self.teams_webhook_url = os.getenv("TEAMS_WEBHOOK_URL")

    def validate_required_credentials(
        self, require_teams: bool = False
    ) -> tuple[bool, list[str]]:
        """
        Validate that required environment variables are set.

        Args:
            require_teams: Whether Teams webhook URL is required

        Returns:
            Tuple of (is_valid, list_of_missing_vars)
        """
        missing = []

        if not self.gemini_api_key:
            missing.append("GEMINI_API_KEY")
        if not self.jira_server_url:
            missing.append("JIRA_SERVER_URL")
        if not self.jira_user_email:
            missing.append("JIRA_USER_EMAIL")
        if not self.jira_api_token:
            missing.append("JIRA_API_TOKEN")
        if require_teams and not self.teams_webhook_url:
            missing.append("TEAMS_WEBHOOK_URL")

        return len(missing) == 0, missing

    def get_jira_credentials(self) -> dict:
        """Get Jira credentials as a dictionary."""
        return {
            "jira_server_url": self.jira_server_url,
            "jira_user_email": self.jira_user_email,
            "jira_api_token": self.jira_api_token,
        }


# Global config instance
config = Config()
