import git
import os
import io  # To handle potential encoding errors gracefully


class RepoManager:
    """
    Manages Git repository operations on a local repository.
    This version does NOT perform a 'git pull' operation.
    It works with the current local state of the repository.
    It now also extracts the full content of ALL text files in the codebase.
    """

    # Define a maximum total length for the codebase context to prevent
    # exceeding LLM context windows or incurring excessive costs.
    # 500,000 characters is a reasonable starting point, roughly 600K tokens.
    # Adjust as needed based on your LLM's context window and budget.
    MAX_TOTAL_CODE_CONTEXT_LENGTH = 500000

    def __init__(self):
        """
        Initializes the RepoManager.
        """
        pass

    def _get_all_text_file_contents(self, repo_path: str) -> dict:
        """
        Recursively reads the content of all text files in the repository.

        Args:
            repo_path (str): The local file system path to the Git repository.

        Returns:
            dict: A dictionary where keys are file paths (relative to repo root)
                  and values are their full content. Binary files are skipped.
                  Content will be truncated if MAX_TOTAL_CODE_CONTEXT_LENGTH is exceeded.
        """
        all_files_content = {}
        current_total_length = 0

        print("Collecting full codebase content (text files only)...")
        for root, _, files in os.walk(repo_path):
            # Skip the .git directory
            if ".git" in root:
                continue

            for file in files:
                full_file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(full_file_path, repo_path)

                # Skip common binary or unwanted files/directories
                if (
                    any(
                        ext in file.lower()
                        for ext in [
                            ".exe",
                            ".dll",
                            ".zip",
                            ".tar.gz",
                            ".bin",
                            ".jpg",
                            ".jpeg",
                            ".png",
                            ".gif",
                            ".bmp",
                            ".pdf",
                            ".docx",
                            ".xlsx",
                            ".pptx",
                            ".sqlite",
                            ".db",
                            ".pyc",
                            ".class",
                        ]
                    )
                    or "node_modules" in relative_file_path
                    or "venv" in relative_file_path
                    or "__pycache__" in relative_file_path
                ):
                    continue

                try:
                    with open(
                        full_file_path, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        content = f.read()

                        # Check if adding this file's content exceeds the limit
                        if (
                            current_total_length + len(content)
                            > self.MAX_TOTAL_CODE_CONTEXT_LENGTH
                        ):
                            remaining_capacity = (
                                self.MAX_TOTAL_CODE_CONTEXT_LENGTH
                                - current_total_length
                            )
                            if remaining_capacity > 0:
                                print(
                                    f"Warning: Truncating content for {relative_file_path} to fit within total limit."
                                )
                                all_files_content[relative_file_path] = (
                                    content[:remaining_capacity]
                                    + "\n... (content truncated)"
                                )
                            else:
                                print(
                                    f"Warning: Skipping {relative_file_path} as total context limit reached."
                                )
                            # Once limit is reached, stop adding more files
                            current_total_length = (
                                self.MAX_TOTAL_CODE_CONTEXT_LENGTH
                            )  # Mark as full
                            break  # Break from inner file loop, will exit outer loops too
                        else:
                            all_files_content[relative_file_path] = content
                            current_total_length += len(content)

                except UnicodeDecodeError:
                    print(f"Skipping binary or undecodable file: {relative_file_path}")
                except Exception as e:
                    print(f"Error reading file {relative_file_path}: {e}")
            if current_total_length >= self.MAX_TOTAL_CODE_CONTEXT_LENGTH:
                break  # Break from outer directory loop too

        if current_total_length >= self.MAX_TOTAL_CODE_CONTEXT_LENGTH:
            print(
                f"--- Full codebase context CONTEXT TRUNCATED at {self.MAX_TOTAL_CODE_CONTEXT_LENGTH} characters. ---"
            )
        else:
            print(
                f"Collected {len(all_files_content)} files, total content length: {current_total_length} characters."
            )

        return all_files_content

    def get_last_diff_and_full_codebase(
        self, repo_path: str, branch_name: str = "main"
    ) -> tuple[str, str, dict, str]:
        """
        Opens a local Git repository, ensures the correct branch is checked out,
        gets the last diff based on local commits, and extracts the full content
        of all relevant text files in the codebase.
        This function does NOT pull latest changes from a remote.

        Args:
            repo_path (str): The local file system path to the Git repository.
            branch_name (str): The name of the branch to get the diff from (default: 'main').

        Returns:
            tuple[str, str, dict, str]: A tuple containing:
                - The diff text as a string.
                - The SHA of the last commit.
                - A dictionary mapping all relevant text file paths (relative to repo root) to their content.
                - An error message string (empty if no error).
        """
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            error_message = f"Error: '{repo_path}' is not a valid Git repository directory (missing .git folder)."
            print(error_message)
            return "", "", {}, error_message

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
                return "", "", {}, error_message

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
                # For single commit repos, we can still provide codebase context
                all_codebase_content = self._get_all_text_file_contents(repo_path)
                return (
                    "",
                    last_commit.hexsha,
                    all_codebase_content,
                    "Initial commit or single commit - no meaningful diff available.",
                )
            except Exception as e:
                error_message = f"Error retrieving previous commit: {e}"
                print(error_message)
                return "", last_commit.hexsha, {}, error_message

            diff_text = repo.git.diff(second_to_last_commit, last_commit)

            # Get all text files in the entire codebase
            all_codebase_content = self._get_all_text_file_contents(repo_path)

            return (
                diff_text,
                last_commit.hexsha,
                all_codebase_content,
                "",
            )  # Return empty error if successful

        except git.InvalidGitRepositoryError:
            error_message = f"Error: '{repo_path}' is not a valid Git repository."
            print(error_message)
            return "", "", {}, error_message
        except git.NoSuchPathError:
            error_message = f"Error: Repository path '{repo_path}' does not exist."
            print(error_message)
            return "", "", {}, error_message
        except git.CommandError as e:
            error_message = f"Git command error: {e}"
            print(error_message)
            return "", "", {}, error_message
        except Exception as e:
            error_message = f"An unexpected error occurred during Git operation: {e}"
            print(error_message)
            return "", "", {}, error_message


if __name__ == "__main__":
    # Example usage (for testing this module independently)
    # IMPORTANT: Replace with an actual local path to a Git repository on your machine
    #            that has at least two commits.
    example_local_repo_path = "/path/to/your/local/repository"

    repo_manager = RepoManager()
    diff, commit_sha, all_codebase_content, error = (
        repo_manager.get_last_diff_and_full_codebase(
            example_local_repo_path, branch_name="master"
        )
    )  # Adjust branch if needed

    if not error:
        print(f"\n--- Last Diff for commit {commit_sha} ---")
        print(diff[:1000])  # Print first 1000 characters of diff

        print("\n--- Full Codebase Content Summary ---")
        for file_path, content in list(all_codebase_content.items())[
            :5
        ]:  # Print first 5 files
            print(f"File: {file_path}")
            print(f"  Content length: {len(content)} chars")
            print("-" * 20)
        if len(all_codebase_content) > 5:
            print(f"...and {len(all_codebase_content) - 5} more files.")

        print(f"\nTotal unique files collected: {len(all_codebase_content)}")
        total_chars = sum(
            len(c) for c in all_codebase_content.values() if isinstance(c, str)
        )
        print(f"Total character count of collected codebase: {total_chars}")
        print("\nDiff and full codebase content extracted successfully.")
    else:
        print(f"\nError extracting data: {error}")
