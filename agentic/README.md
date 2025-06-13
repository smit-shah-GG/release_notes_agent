# Agentic Release Notes Generator

An intelligent, agent-based system for automatically generating comprehensive release notes from Git repositories and Jira tickets using specialized AI agents.

## 🤖 Architecture

The system uses a hierarchical agent architecture with specialized agents:

- **Orchestrator Agent**: Coordinates all other agents and manages workflow
- **Repository Agent**: Analyzes Git repositories and extracts code changes
- **Jira Agent**: Fetches and correlates Jira tickets with code changes
- **Generator Agent**: Creates well-formatted release notes using AI
- **Output Agent**: Manages file operations and saves release notes
- **Teams Agent**: Sends notifications to Microsoft Teams channels

## 🚀 Features

- **Intelligent Coordination**: AI orchestrator that delegates tasks to specialized agents
- **Multi-source Integration**: Combines Git diffs, full codebase context, and Jira tickets
- **Conversational Interface**: Interactive CLI for natural language interactions
- **Flexible Output**: Saves timestamped Markdown files and sends Teams notifications
- **Comprehensive Analysis**: Analyzes entire codebase for better context understanding
- **Error Recovery**: Graceful handling of failures with partial results

## 📋 Prerequisites

- Python 3.8+
- Git repository access
- Google AI API key (Gemini)
- Jira account with API access
- Microsoft Teams webhook (optional)

## 🛠️ Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd release_notes_agent/agentic
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Required
export GEMINI_API_KEY="your_gemini_api_key"
export JIRA_SERVER_URL="https://your-jira-instance.atlassian.net"
export JIRA_USER_EMAIL="your_email@example.com"
export JIRA_API_TOKEN="your_jira_api_token"

# Optional (for Teams integration)
export TEAMS_WEBHOOK_URL="your_teams_webhook_url"
```

Or create a `.env` file with these variables.

## 🎯 Usage

### Single Command Mode

Generate release notes with a single command:

```bash
python main.py --repo-path /path/to/repo --jira-project-key PROJ
```

With additional options:
```bash
python main.py \
  --repo-path /path/to/repo \
  --branch develop \
  --jira-project-key PROJ \
  --output-dir ./release_notes \
  --send-to-teams
```

### Interactive Mode

Start a conversational session:

```bash
python main.py --repo-path /path/to/repo --jira-project-key PROJ --interactive
```

Then interact naturally:
```
💬 You: Generate release notes for the latest changes
💬 You: What Jira tickets are related to this release?
💬 You: Send the release notes to Teams
```

### Command Line Options

- `--repo-path`: Local path to Git repository (required)
- `--branch`: Git branch to analyze (default: main)
- `--jira-project-key`: Jira project key (required)
- `--output-dir`: Directory for saving release notes (default: generated_release_notes)
- `--send-to-teams`: Send release notes to Teams channel
- `--interactive`: Enable conversational mode

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google AI API key for Gemini | Yes |
| `JIRA_SERVER_URL` | Jira instance URL | Yes |
| `JIRA_USER_EMAIL` | Jira user email | Yes |
| `JIRA_API_TOKEN` | Jira API token | Yes |
| `TEAMS_WEBHOOK_URL` | Teams webhook URL | No |

### Obtaining API Keys

#### Google AI API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set as `GEMINI_API_KEY` environment variable

#### Jira API Token
1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Create API token
3. Use your email and token for authentication

#### Teams Webhook
1. In Teams, go to the channel where you want notifications
2. Click "..." → "Connectors" → "Incoming Webhook"
3. Configure and copy the webhook URL

## 📁 Project Structure

```
agentic/
├── main.py                    # CLI interface and entry point
├── base_agent.py              # Orchestrator agent
├── config.py                  # Configuration management
├── agents/                    # Specialized agents
│   ├── repo_agent.py          # Git operations
│   ├── jira_agent.py          # Jira integration  
│   ├── generator_agent.py     # AI content generation
│   ├── output_agent.py        # File management
│   └── teams_agent.py         # Teams communication
├── tools/                     # Reusable utilities
│   ├── git_tools.py           # Git utilities
│   ├── jira_tools.py          # Jira utilities
│   ├── file_tools.py          # File utilities
│   └── teams_tools.py         # Teams utilities
└── utils/                     # Helper utilities
    ├── error_handling.py      # Error management
    └── logging_config.py      # Logging setup
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 📊 Output Format

Generated release notes follow this structure:

```markdown
### [Release Date] - Release Notes

#### New Features
- Feature description (JIRA-123)
- Another feature (JIRA-456)

#### Bug Fixes
- Bug fix description (JIRA-789)
- Another fix (JIRA-012)

#### Resolved Issues
- JIRA-123: Issue summary
- JIRA-456: Another issue summary

#### Improvements & General Changes
- Performance improvements
- Code refactoring
```

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify all environment variables are set correctly
   - Check API key permissions and expiration

2. **Repository Access**
   - Ensure the repository path exists and is a valid Git repository
   - Check branch name spelling

3. **Jira Connection**
   - Verify Jira server URL format
   - Ensure API token has proper permissions

4. **Teams Integration**
   - Confirm webhook URL is correct and active
   - Check Teams channel permissions

### Logging

Logs are saved in the `logs/` directory with timestamps. Use these for debugging:

```bash
tail -f logs/release_notes_agent_*.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Open an issue with detailed information
