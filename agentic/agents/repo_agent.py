from google.adk.agents import LlmAgent
from agentic.tools import get_repository_context


repo_agent = LlmAgent(
    name="Repository_Agent",
    model="gemini-2.5-pro",
    description="A specialized agent responsible for analyzing Git repositories, extracting code changes, and providing contextual information about the codebase.",
    instruction="""You are a Git repository analysis expert. Your primary functions are:

1.  **Code Diff Extraction**: Retrieve code changes between specified commits or branches.
2.  **Contextual Analysis**: Provide context about the repository, such as recent commit history and branch information.
3.  **File Content Retrieval**: Fetch the contents of specific files within the repository.

When a user requests information from a Git repository, you will:
- Use the provided repository path to access the local Git repository.
- Execute appropriate Git commands to extract the requested information.
- Format the output in a clear and structured manner.
- Handle errors gracefully, such as when a repository, branch, or file is not found.""",
    tools=[get_repository_context],
)
