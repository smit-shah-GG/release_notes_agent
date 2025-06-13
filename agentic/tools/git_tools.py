# agentic/tools/git_tools.py
import git
import os


# Re-using the core logic from the original repo_manager.py
# The class structure is kept to easily manage state and dependencies.
class RepoManager:
    """
    Manages Git repository operations on a local repository.
    Manages Git repository operations on a local repository.
    It primarily extracts the diff from the last commit.
    """

    def get_last_diff_and_commit_info(
        self, repo_path: str, branch_name: str = "main"
    ) -> tuple[str, str, str]:
        """
        Opens a local Git repository and gets the diff from the last commit and its SHA.
        """
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            return "", "", f"Error: '{repo_path}' is not a valid Git repository."
        try:
            repo = git.Repo(repo_path)
            if repo.is_dirty(untracked_files=True):
                # Handle or log dirty repository state if necessary, for now, we proceed
                print(f"Warning: Repository at {repo_path} is dirty. Proceeding with diff operation.")

            # Ensure the correct branch is checked out if specified and different from current
            if repo.head.is_valid() and repo.active_branch.name != branch_name:
                print(f"Checking out branch '{branch_name}'...")
                # Ensure there's a local branch corresponding to branch_name
                if branch_name in repo.heads:
                    repo.heads[branch_name].checkout()
                else: # Try to checkout remote branch if local doesn't exist
                    try:
                        repo.git.checkout(branch_name)
                    except git.exc.GitCommandError as e:
                         return "", "", f"Error checking out branch '{branch_name}': {e}. Ensure it exists locally or remotely."


            if not repo.head.is_valid():
                return "", "", "Error: Repository head is not valid."
            
            last_commit = repo.head.commit
            if not last_commit.parents:
                # This is the initial commit, no parent to diff against
                # We can return the state of the tree at this commit as a diff against an empty tree
                print("Initial commit detected. Diffing against an empty tree.")
                diff_text = repo.git.diff(git.NULL_TREE, last_commit)
            else:
                second_to_last_commit = last_commit.parents[0] # Diff against the first parent
                diff_text = repo.git.diff(second_to_last_commit, last_commit)
            
            return (diff_text, last_commit.hexsha, "")
        except git.exc.NoSuchPathError:
            return "", "", f"Error: Path '{repo_path}' does not exist or is not a Git repository."
        except git.exc.InvalidGitRepositoryError:
            return "", "", f"Error: '{repo_path}' is not a valid Git repository."
        except Exception as e:
            return "", "", f"An unexpected error occurred during Git operation: {e}"


# Instantiate the manager to be used by the tool.
_repo_manager = RepoManager()


def get_repository_context(repo_path: str, branch: str) -> dict:
    """
    Provides the diff from the last commit and the commit's SHA for a Git repository.

    Args:
        repo_path: The local file system path to the Git repository.
        branch: The name of the branch to analyze (e.g., 'main', 'develop').

    Returns:
        A dictionary containing 'diff_text', 'commit_sha', and 'error'.
        The 'error' key will be empty on success.
    """
    print(
        f"Tool 'get_repository_context' called for repo: {repo_path} on branch: {branch}"
    )
    diff_text, commit_sha, error = (
        _repo_manager.get_last_diff_and_commit_info(repo_path, branch)
    )
    return {
        "diff_text": diff_text,
        "commit_sha": commit_sha,
        "error": error,
    }
