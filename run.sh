#!/bin/bash

# This script is for manually running the release notes generator.
# Ensure you have set the following environment variables in your shell
# or in a `.env` file that main.py can load:
export GEMINI_API_KEY="AIzaSyBfdlA9vIDy698izYeygOfP9ZR-vzBcqso"
export JIRA_SERVER_URL="https://smitshah.atlassian.net"
export JIRA_USER_EMAIL="johannschmidt045@gmail.com"
export JIRA_API_TOKEN="ATATT3xFfGF0vF3U2TqGO4Vl81M5EYSKBjpVpX2ghZE_PWhpZ8TQ5lqWiu8_ziIybDGn6SkuTy_aZnI0US__ZdbsXWWTdLAI2V_U68prALWb1HaumIyxPZqjfvASoSXC2CWHhDsrLaSf0BPYWvcUVaaNxlHgB-KyswQmaxZV8pKTVwUSeJNC2Jo=16937040"

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

python3 main.py --repo-path "$LOCAL_REPO_PATH" --branch "$BRANCH_NAME" --output-dir "$OUTPUT_DIRECTORY"

echo "--- Release Notes Generation Finished ---"
