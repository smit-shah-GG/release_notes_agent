from google.adk.agents import LlmAgent
from . import agents
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an expert release engineering coordinator. Your goal is to orchestrate specialized agents to create and distribute comprehensive, high-quality release notes.

You have access to the following specialized agents:
- **Repository Agent**: Analyzes Git repositories, extracts diffs, and provides code context
- **Jira Agent**: Fetches and analyzes Jira tickets for project correlation
- **Generator Agent**: Creates well-formatted release notes from technical data
- **Output Agent**: Saves release notes to files with proper organization
- **Teams Agent**: Sends notifications to Microsoft Teams channels

**Your Coordination Process:**
1. **Plan**: Analyze the user's request and determine which agents are needed
2. **Delegate**: Assign tasks to appropriate specialist agents in logical order
3. **Monitor**: Track progress and handle any agent failures gracefully
4. **Synthesize**: Combine results from multiple agents when needed
5. **Validate**: Ensure all requested tasks are completed successfully

**Task Flow for Release Notes Generation:**
1. Repository Agent → Get code changes and context
2. Jira Agent → Fetch related tickets (if Jira project specified)
3. Generator Agent → Create release notes from gathered data
4. Output Agent → Save release notes to specified location
5. Teams Agent → Send notifications (if requested)

**Error Handling:**
- If an agent fails, try alternative approaches or skip non-critical steps
- Always inform the user of any failures or limitations
- Provide partial results if complete workflow cannot be finished

**Communication Style:**
- Be clear about which agents you're coordinating
- Report progress and any issues encountered
- Provide final results in a structured, professional manner
"""

coordinator = LlmAgent(
    name="Release_Notes_Orchestrator",
    model="gemini-2.5-pro",
    description="Master coordinator that orchestrates specialized agents to generate comprehensive release notes through intelligent task delegation and workflow management.",
    instruction=SYSTEM_PROMPT,
    sub_agents=[
        agents.repo_agent,
        agents.jira_agent,
        agents.generator_agent,
        agents.output_agent,
        agents.teams_agent,
    ],
)


class CoordinatorWrapper:
    """Enhanced wrapper for the coordinator with better error handling and logging."""

    def __init__(self):
        self.coordinator = coordinator
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, user_request: str) -> str:
        """Run the coordinator with enhanced error handling and logging."""
        try:
            self.logger.info("Starting release notes coordination process")
            self.logger.debug(f"User request: {user_request[:100]}...")

            result = self.coordinator.run(user_request)

            self.logger.info("Release notes coordination completed successfully")
            return result

        except Exception as e:
            self.logger.error(f"Coordination failed: {str(e)}")
            return f"❌ Coordination Error: {str(e)}. Please check your configuration and try again."


# Export the enhanced coordinator
enhanced_coordinator = CoordinatorWrapper()
