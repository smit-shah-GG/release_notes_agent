Automated Release Note Generator - Project Plan
1. Project Goal
To develop a centralized Python service that, when manually triggered, performs the following steps for a specified code repository:

Fetches the last significant code diff.

Identifies and retrieves relevant Jira ticket details linked to the diff.

Generates comprehensive release notes using Google's google-genai library.

Saves the generated release notes to local timestamped Markdown files for easy review during development.

This service is intended to run on a Google Compute Engine VM and will be designed to support future automation and integration with platforms like Microsoft Teams.

2. Core Components
The service will be composed of the following modules:

main.py: The central script that orchestrates the entire process. It will take repository URL and branch as input.

repo_manager.py: Handles Git operations, specifically cloning a repository and extracting the latest diff.

jira_integrator.py: Connects to Jira, parses commit messages for Jira issue keys, and fetches detailed information for those issues.

release_note_generator.py: Utilizes the google-genai library to generate human-readable release notes from the diff content and Jira data.

output_writer.py: Manages saving the generated release notes to local files with timestamped names.

requirements.txt: Lists all Python dependencies for easy installation.

run_release_notes.sh: A simple shell script to manually execute the service.

3. Setup and Environment
The service will be designed to run on a Linux-based Google Compute Engine VM.

3.1. Google Cloud Project & VM Setup (Conceptual for LLM Agent)
Google Cloud Project: A Google Cloud project with billing enabled is required.

Compute Engine VM: A suitable VM instance should be provisioned.

Operating System: Debian, Ubuntu, or CentOS are recommended.

Software: Git client (git), Python 3 and pip must be installed on the VM.

Authentication:

Google AI API Key: The google-genai library requires an API key. This must be set as an environment variable GEMINI_API_KEY on the VM where the service runs.

Jira API Token: A Jira API token and the Jira server URL are required. These must be set as environment variables JIRA_API_TOKEN and JIRA_SERVER_URL respectively.

Repository Access: For private Git repositories, ensure SSH keys are configured on the VM for the user running the service, or provide appropriate personal access tokens via environment variables.

3.2. Project Directory Structure
The LLM agent should create the following directory and file structure:

release_notes_generator/
├── main.py
├── repo_manager.py
├── jira_integrator.py
├── release_note_generator.py
├── output_writer.py
├── requirements.txt
└── run_release_notes.sh

4. Core Modules Implementation
The LLM agent should create each file with the specified content.

4.1. requirements.txt
This file lists the necessary Python packages.

File: release_notes_generator/requirements.txt

google-generativeai==0.7.0
GitPython==3.1.43
jira==3.8.0
python-dotenv==1.0.1

