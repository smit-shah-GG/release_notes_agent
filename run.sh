#!/bin/bash

# This script is for manually running the release notes generator.
# Ensure you have set the following environment variables in your shell
# or in a `.env` file that main.py can load:
export GEMINI_API_KEY="AIzaSyBfdlA9vIDy698izYeygOfP9ZR-vzBcqso"
export JIRA_SERVER_URL="https://smitshah.atlassian.net"
export JIRA_USER_EMAIL="johannschmidt045@gmail.com"
export JIRA_API_TOKEN="ATATT3xFfGF0ikVCxEfO4FzXzu_1GMa7wIgrBOcNt_pSHlvfAp3UUJdICfktinaaWqhv2UKqFDCeyHg6tMiY57crpyvqUtI15lU8c1ZOb_1l3niip-XAqdeqvDsg23b2EWovk89_66fRwQ74JxAzsvWRlh8oVktUZQOgSHkTuSoeRWagRI1rml0=9294B579"
export TEAMS_WEBHOOK_URL="https://netorgft7210864.webhook.office.com/webhookb2/ffb3974f-22c8-40e8-a9de-588905d8b944@1808c860-1a96-4640-8ce1-635eca00c108/IncomingWebhook/4d6d34d510c64ca8a139dc87f53cfd07/2adf894c-c9f4-41db-bb3f-4635b01e7498/V2tcgQ1F9yeHkInjVwZm6P8NbbL7Q3VNUmCkxzL_r6wm81"

# Navigate to the script's directory
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR" || exit

# --- Configuration ---
# IMPORTANT: Replace with the actual LOCAL FILE SYSTEM PATH to your Git repository
# Example: /home/youruser/my-project-repo
LOCAL_REPO_PATH="/home/smit/work/solvendo/release_notes_agent/"
# Replace with the branch you want to get the diff from
BRANCH_NAME="master" # Example: 'main' or 'develop'
# Output directory for the generated release notes
OUTPUT_DIRECTORY="generated_release_notes"
# --- End Configuration ---
JIRA_PROJECT="SCRUM"

echo "--- Starting Release Notes Generation ---"
echo "Local Repository Path: $LOCAL_REPO_PATH"
echo "Branch: $BRANCH_NAME"
echo "Output Directory: $OUTPUT_DIRECTORY"
echo "-----------------------------------------"

# Run the Python script
# It's recommended to run this in a Python virtual environment.
# Example:
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# python3 main.py --repo-path "$LOCAL_REPO_PATH" --branch "$BRANCH_NAME" --output-dir "$OUTPUT_DIRECTORY"

python3 main.py --repo-path "$LOCAL_REPO_PATH" --branch "$BRANCH_NAME" --output-dir "$OUTPUT_DIRECTORY" --jira-project-key "$JIRA_PROJECT" --send-to-teams

echo "--- Release Notes Generation Finished ---"
