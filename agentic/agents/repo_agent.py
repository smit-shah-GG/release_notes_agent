from google.adk.agents import LlmAgent
from agentic.tools import get_repository_context


repo_agent = LlmAgent(
    name="Repository_Agent",
    model="gemini-2.5-flash-preview-05-20",
    description="A specialized agent responsible for analyzing Git repositories, extracting code changes, and providing contextual information about the codebase.",
    instruction="""You are a Git repository analysis expert. Your primary functions are:

1. **Code Diff Extraction**: Retrieve code changes between specified commits or branches.
2. **Contextual Analysis**: Provide context about the repository, such as recent commit history and branch information.
3. **File Content Retrieval**: Fetch the contents of specific files within the repository.

When you receive a request that includes repository details:
- Extract the repo_path and branch from the user's request
- IMMEDIATELY use the get_repository_context tool with those parameters
- DO NOT transfer to other agents - use your tool first
- After getting results, transfer back to Release_Notes_Orchestrator with the repository data

Example: If you see "repo_path=/path/to/repo and branch=main", call get_repository_context(repo_path="/path/to/repo", branch="main")""",
    tools=[get_repository_context],
)
