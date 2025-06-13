# agentic/tools/notification_tools.py
import datetime
import os
import pymsteams


def send_notes_to_teams(
    release_notes_content: str, commit_sha: str, webhook_url: str
) -> str:
    """
    Sends the generated release notes to a Microsoft Teams channel via a webhook.

    Args:
        release_notes_content: The Markdown content of the release notes.
        commit_sha: The SHA of the commit the notes are for, used in the message title.
        webhook_url: The Incoming Webhook URL for the Microsoft Teams channel.

    Returns:
        A confirmation message indicating success or failure.
    """
    print("Tool 'send_notes_to_teams' called.")
    if not webhook_url:
        return "Error: Microsoft Teams webhook URL is not configured."

    try:
        teams_message = pymsteams.connectorcard(webhook_url)
        teams_message.title(f"Release Notes for Commit: {commit_sha[:7]}")
        teams_message.text(release_notes_content)
        teams_message.send()
        message = "Successfully sent release notes to Teams."
        print(message)
        return message
    except Exception as e:
        message = f"Error sending message to Microsoft Teams: {e}"
        print(message)
        return message
