import git
import os


class RepoManager:
    """
    Manages Git repository operations on a local repository.
    This version does NOT perform a 'git pull' operation.
    It works with the current local state of the repository.
    """

    def __init__(self):
        """
        Initializes the RepoManager.
        """
        pass

    def get_last_diff(
        self, repo_path: str, branch_name: str = "main"
    ) -> tuple[str, str, str]:
        """
        Opens a local Git repository, ensures the correct branch is checked out,
        gets the last diff based on local commits, and returns the diff and commit SHA.
        This function does NOT pull latest changes from a remote.

        Args:
            repo_path (str): The local file system path to the Git repository.
            branch_name (str): The name of the branch to get the diff from (default: 'main').

        Returns:
            tuple[str, str, str]: A tuple containing:
                - The diff text as a string.
                - The SHA of the last commit.
                - An error message string (empty if no error).
        """
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            error_message = f"Error: '{repo_path}' is not a valid Git repository directory (missing .git folder)."
            print(error_message)
            return "", "", error_message

        try:
            print(f"Opening local repository at {repo_path}...")
            repo = git.Repo(repo_path)
            print("Repository opened successfully.")

            # Ensure we are on the correct branch
            if repo.head.is_valid() and repo.head.ref.name != branch_name:
                print(f"Switching to branch: {branch_name}")
                repo.git.checkout(branch_name)
            elif not repo.head.is_valid():
                error_message = f"Error: Repository head is invalid. Cannot checkout branch {branch_name}."
                print(error_message)
                return "", "", error_message

            # --- IMPORTANT CHANGE: Removed repo.remotes.origin.pull() ---
            print("Operating on local repository state only (no 'git pull' performed).")

            last_commit = repo.head.commit
            second_to_last_commit = None

            # Attempt to get the commit before the HEAD.
            # If this fails, it means there's only 0 or 1 commit in the repo.
            try:
                second_to_last_commit = repo.commit(f"{last_commit.hexsha}~1")
            except git.BadObject:
                print(
                    "Not enough commits to generate a diff (needs at least two local commits)."
                )
                return (
                    "",
                    last_commit.hexsha,
                    "Initial commit or single commit - no meaningful diff available.",
                )
            except Exception as e:
                # Catch any other unexpected errors during commit retrieval
                error_message = f"Error retrieving previous commit: {e}"
                print(error_message)
                return "", last_commit.hexsha, error_message

            diff_text = repo.git.diff(second_to_last_commit, last_commit)
            return diff_text, last_commit.hexsha, ""  # Return empty error if successful

        except git.InvalidGitRepositoryError:
            error_message = f"Error: '{repo_path}' is not a valid Git repository."
            print(error_message)
            return "", "", error_message
        except git.NoSuchPathError:
            error_message = f"Error: Repository path '{repo_path}' does not exist."
            print(error_message)
            return "", "", error_message
        except git.CommandError as e:
            error_message = f"Git command error: {e}"
            print(error_message)
            return "", "", error_message
        except Exception as e:
            error_message = f"An unexpected error occurred during Git operation: {e}"
            print(error_message)
            return "", "", error_message


if __name__ == "__main__":
    # Example usage (for testing this module independently)
    # IMPORTANT: Replace with an actual local path to a Git repository on your machine
    #            that has at least two commits.
    example_local_repo_path = "/home/smit/work/solvendo/strategies/"

    repo_manager = RepoManager()
    diff, commit_sha, error = repo_manager.get_last_diff(
        example_local_repo_path, branch_name="master"
    )  # Adjust branch if needed

    if not error:
        print(f"\n--- Last Diff for commit {commit_sha} ---")
        print(diff)
        # print(diff[:1000])  # Print first 1000 characters of diff
        print("\nDiff extracted successfully.")
    else:
        print(f"\nError extracting diff: {error}")
