# agentic/tools/git_tools.py
import git
import os


# Re-using the core logic from the original repo_manager.py
# The class structure is kept to easily manage state and dependencies.
class RepoManager:
    """
    Manages Git repository operations on a local repository.
    It now also extracts the full content of ALL text files in the codebase.
    """

    MAX_TOTAL_CODE_CONTEXT_LENGTH = 500000

    def _get_all_text_file_contents(self, repo_path: str) -> dict:
        """
        Recursively reads the content of all text files in the repository.
        """
        all_files_content = {}
        current_total_length = 0
        print("Collecting full codebase content (text files only)...")
        for root, _, files in os.walk(repo_path):
            if ".git" in root:
                continue
            for file in files:
                full_file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(full_file_path, repo_path)
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
                        if (
                            current_total_length + len(content)
                            > self.MAX_TOTAL_CODE_CONTEXT_LENGTH
                        ):
                            remaining_capacity = (
                                self.MAX_TOTAL_CODE_CONTEXT_LENGTH
                                - current_total_length
                            )
                            if remaining_capacity > 0:
                                all_files_content[relative_file_path] = (
                                    content[:remaining_capacity]
                                    + "\n... (content truncated)"
                                )
                            current_total_length = self.MAX_TOTAL_CODE_CONTEXT_LENGTH
                            break
                        else:
                            all_files_content[relative_file_path] = content
                            current_total_length += len(content)
                except Exception as e:
                    print(f"Error reading file {relative_file_path}: {e}")
            if current_total_length >= self.MAX_TOTAL_CODE_CONTEXT_LENGTH:
                break
        print(
            f"Collected {len(all_files_content)} files, total content length: {current_total_length} characters."
        )
        return all_files_content

    def get_last_diff_and_full_codebase(
        self, repo_path: str, branch_name: str = "main"
    ) -> tuple[str, str, dict, str]:
        """
        Opens a local Git repository, gets the last diff, and extracts the full content of all relevant text files.
        """
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            return "", "", {}, f"Error: '{repo_path}' is not a valid Git repository."
        try:
            repo = git.Repo(repo_path)
            if repo.head.is_valid() and repo.head.ref.name != branch_name:
                repo.git.checkout(branch_name)

            last_commit = repo.head.commit
            second_to_last_commit = repo.commit(f"{last_commit.hexsha}~1")
            diff_text = repo.git.diff(second_to_last_commit, last_commit)
            all_codebase_content = self._get_all_text_file_contents(repo_path)
            return (diff_text, last_commit.hexsha, all_codebase_content, "")
        except Exception as e:
            return "", "", {}, f"An unexpected error occurred during Git operation: {e}"


# Instantiate the manager to be used by the tool.
_repo_manager = RepoManager()


def get_repository_context(repo_path: str, branch: str) -> dict:
    """
    Provides the full context of the most recent changes in a Git repository.
    This includes the code diff from the last commit, the commit's unique identifier (SHA),
    and the complete content of all text files in the codebase.

    Args:
        repo_path: The local file system path to the Git repository.
        branch: The name of the branch to analyze (e.g., 'main', 'develop').

    Returns:
        A dictionary containing 'diff_text', 'commit_sha', 'codebase_content', and 'error'.
        The 'error' key will be empty on success.
    """
    print(
        f"Tool 'get_repository_context' called for repo: {repo_path} on branch: {branch}"
    )
    diff_text, commit_sha, all_codebase_content, error = (
        _repo_manager.get_last_diff_and_full_codebase(repo_path, branch)
    )
    return {
        "diff_text": diff_text,
        "commit_sha": commit_sha,
        "codebase_content": all_codebase_content,
        "error": error,
    }
