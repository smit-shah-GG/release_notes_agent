# smit-shah-gg/release_notes_agent/release_notes_agent-0523db1cd64bf44c8e903fcc57f6d9a0a577e74e/teams_integrator.py
#!/usr/bin/env python3

import pymsteams


class TeamsIntegrator:
    """
    Handles sending messages to a Microsoft Teams channel via an Incoming Webhook.
    """

    def __init__(self, webhook_url: str):
        """
        Initializes the TeamsIntegrator.

        Args:
            webhook_url (str): The Incoming Webhook URL for the Microsoft Teams channel.
        """
        if not webhook_url:
            raise ValueError("Microsoft Teams webhook URL cannot be empty.")
        self.webhook_url = webhook_url

    def send_release_notes(self, release_notes_content: str, commit_sha: str) -> bool:
        """
        Sends the generated release notes to a Microsoft Teams channel.

        Args:
            release_notes_content (str): The Markdown content of the release notes.
            commit_sha (str): The SHA of the commit the notes are for.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        try:
            # Create a new connector card
            teams_message = pymsteams.connectorcard(self.webhook_url)

            # Set the title of the card
            teams_message.title(f"Release Notes for Commit: {commit_sha[:7]}")

            # Set the main text of the card to the release notes content
            # The text property supports Markdown
            teams_message.text(release_notes_content)

            # Send the message
            print("Sending release notes to Microsoft Teams channel...")
            teams_message.send()
            print("Successfully sent release notes to Teams.")
            return True
        except Exception as e:
            print(f"Error sending message to Microsoft Teams: {e}")
            return False
