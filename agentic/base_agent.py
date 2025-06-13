from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from . import agents
import logging
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an expert release engineering coordinator. Your goal is to orchestrate specialized agents to create and distribute comprehensive, high-quality release notes.

You have access to the following specialized agents:
- **Repository Agent**: Analyzes Git repositories, extracts diffs and commit SHAs from the last commit.
- **Jira Agent**: Fetches and analyzes Jira tickets for project correlation
- **Generator Agent**: Creates well-formatted release notes from technical data
- **Output Agent**: Saves release notes to files with proper organization
- **Teams Agent**: Sends notifications to Microsoft Teams channels

**IMPORTANT: You must EXECUTE the workflow, not just describe it.**

**Task Flow for Release Notes Generation:**
When a user requests release notes generation, immediately start by transferring to the Repository Agent to get code changes.

**Execution Steps:**
1. IMMEDIATELY call transfer_to_agent with "Repository_Agent" to get repository context
2. DO NOT describe the plan - EXECUTE it by calling the transfer function
3. Let each agent complete their task and return results
4. Use the accumulated results to coordinate the next steps

**You must start by calling transfer_to_agent function RIGHT NOW - do not explain what you will do, just do it.**

**Error Handling:**
- If an agent fails, try alternative approaches or skip non-critical steps
- Always inform the user of any failures or limitations
- Provide partial results if complete workflow cannot be finished
"""

coordinator = LlmAgent(
    name="Release_Notes_Orchestrator",
    model="gemini-2.5-flash-preview-05-20",
    description="Master coordinator that orchestrates specialized agents to generate comprehensive release notes through intelligent task delegation and workflow management.",
    instruction=SYSTEM_PROMPT,
    sub_agents=[
        agents.repo_agent,
        agents.jira_agent,
        agents.generator_agent,
        agents.output_agent,
        agents.teams_agent,
    ],
    output_key="release_notes_result",
)


class CoordinatorWrapper:
    """Enhanced wrapper for the coordinator with proper Google ADK integration."""

    def __init__(self):
        self.coordinator = coordinator
        self.logger = logging.getLogger(self.__class__.__name__)

        # Set up session management
        self.session_service = InMemorySessionService()
        self.app_name = "release_notes_agent"
        self.user_id = "release_notes_user"
        self.session_id = "release_notes_session"

        # Initialize session and runner (will be set up in first run)
        self.runner = None
        self._initialized = False

    async def _initialize_async(self):
        """Initialize session and runner asynchronously."""
        if not self._initialized:
            # Create session asynchronously
            await self.session_service.create_session(
                app_name=self.app_name, user_id=self.user_id, session_id=self.session_id
            )

            # Create runner
            self.runner = Runner(
                agent=self.coordinator,
                app_name=self.app_name,
                session_service=self.session_service,
            )

            self._initialized = True

    def run(self, user_request: str) -> str:
        """Run the coordinator with proper Google ADK integration."""
        try:
            self.logger.info("Starting release notes coordination process")
            self.logger.debug(f"User request: {user_request[:100]}...")

            # Run the async coordination
            result = asyncio.run(self._run_async(user_request))

            self.logger.info("Release notes coordination completed successfully")
            return result

        except Exception as e:
            self.logger.error(f"Coordination failed: {str(e)}")
            return f"❌ Coordination Error: {str(e)}. Please check your configuration and try again."

    async def _run_async(self, user_request: str) -> str:
        """Async method to run the coordinator using Google ADK Runner."""
        # Initialize if not already done
        await self._initialize_async()

        user_content = types.Content(role="user", parts=[types.Part(text=user_request)])

        final_response_content = "No response received from coordinator."

        async for event in self.runner.run_async(
            user_id=self.user_id, session_id=self.session_id, new_message=user_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_content = event.content.parts[0].text
                break

        return final_response_content


# Export the enhanced coordinator
enhanced_coordinator = CoordinatorWrapper()
