# Simplified Agentic AI Release Notes System - Plan

## Proposed File Structure

```
work/solvendo/release_notes_agent/agentic/
├── main.py                    # CLI interface + orchestrator agent
├── base_agent.py              # Simple base class for agents
├── config.py                  # Configuration management
├── agents/
│   ├── __init__.py
│   ├── repo_agent.py          # Git operations
│   ├── jira_agent.py          # Jira integration  
│   ├── generator_agent.py     # AI content generation
│   ├── output_agent.py        # File management
│   └── teams_agent.py         # Teams communication
├── tools/
│   ├── __init__.py
│   ├── git_tools.py           # Git utilities
│   ├── jira_tools.py          # Jira utilities
│   ├── ai_tools.py            # AI/LLM utilities
│   ├── file_tools.py          # File utilities
│   └── teams_tools.py         # Teams utilities
├── requirements.txt
└── README.md
```

## File Purposes

### Core System
- **main.py**: Entry point with CLI interface and orchestrator agent. Handles user conversations, parses commands, and coordinates subagents to accomplish tasks.

- **base_agent.py**: Simple base class that all agents inherit from. Provides common functionality like logging, error handling, and basic communication methods.

- **config.py**: Single configuration file for API keys, settings, and agent parameters. Loads from environment variables and .env files.

### Agents (Specialized Workers)
- **agents/repo_agent.py**: Handles all Git operations - cloning, diffing, branch management. Uses git_tools internally.

- **agents/jira_agent.py**: Manages Jira integration - fetching tickets, searching projects. Uses jira_tools internally.

- **agents/generator_agent.py**: AI-powered content generation using Google's Gemini. Creates release notes from provided context.

- **agents/output_agent.py**: Manages file operations - saving release notes, creating directories, file naming.

- **agents/teams_agent.py**: Handles Teams communication - sending messages via webhooks.

### Tools (Reusable Utilities)
- **tools/git_tools.py**: Low-level Git operations extracted from current repo_manager.py

- **tools/jira_tools.py**: Jira API calls extracted from current jira_integrator.py

- **tools/ai_tools.py**: AI/LLM interactions extracted from current release_note_generator.py

- **tools/file_tools.py**: File system operations extracted from current output_writer.py

- **tools/teams_tools.py**: Teams webhook operations extracted from current teams_integrator.py

## Key Features

### 1. Conversational CLI
Users can interact naturally:
- "Generate release notes for project ABC"
- "Send the last release notes to Teams"
- "Show me recent commits for main branch"

### 2. Agent Coordination
The orchestrator in main.py decides which agents to activate based on user requests and coordinates their work.

### 3. Simple Communication
Agents communicate through direct method calls coordinated by the orchestrator - no complex message bus needed.

### 4. Tool Reusability
Common operations are extracted into tools that multiple agents can use.

This structure accomplishes the agentic goals while keeping complexity minimal and maintainable.
