"""Git Worktree & Branch isolation manager for concurrent agents."""
import subprocess
import os
import shutil
from typing import Optional, Dict, Any, List


class GitWorktreeManager:
    def __init__(self, repo_root: str):
        self.repo_root = os.path.abspath(repo_root)

    def _run_git(self, args: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
        target_dir = cwd or self.repo_root
        cmd = ["git"] + args
        try:
            res = subprocess.run(
                cmd,
                cwd=target_dir,
                capture_output=True,
                text=True,
                check=False
            )
            return {
                "success": res.returncode == 0,
                "returncode": res.returncode,
                "stdout": res.stdout.strip(),
                "stderr": res.stderr.strip()
            }
        except Exception as ex:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(ex)
            }

    def create_feature_branch(self, branch_name: str, base_branch: str = "main") -> Dict[str, Any]:
        """Creates a new feature branch from base branch."""
        return self._run_git(["checkout", "-b", branch_name, base_branch])

    def create_worktree(self, branch_name: str, worktree_path: str) -> Dict[str, Any]:
        """Creates an isolated git worktree for a parallel agent task."""
        abs_path = os.path.abspath(worktree_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        return self._run_git(["worktree", "add", abs_path, branch_name])

    def remove_worktree(self, worktree_path: str, force: bool = False) -> Dict[str, Any]:
        """Removes a worktree after task completion."""
        abs_path = os.path.abspath(worktree_path)
        args = ["worktree", "remove", abs_path]
        if force:
            args.append("--force")
        res = self._run_git(args)
        if os.path.exists(abs_path):
            shutil.rmtree(abs_path, ignore_errors=True)
        self._run_git(["worktree", "prune"])
        return res

    def list_worktrees(self) -> List[Dict[str, str]]:
        """Lists all active worktrees."""
        res = self._run_git(["worktree", "list", "--porcelain"])
        if not res["success"]:
            return []
        
        worktrees = []
        current: Dict[str, str] = {}
        for line in res["stdout"].splitlines():
            line = line.strip()
            if not line:
                if current:
                    worktrees.append(current)
                    current = {}
                continue
            if line.startswith("worktree "):
                current["worktree"] = line.split(" ", 1)[1]
            elif line.startswith("HEAD "):
                current["head"] = line.split(" ", 1)[1]
            elif line.startswith("branch "):
                current["branch"] = line.split(" ", 1)[1]
        if current:
            worktrees.append(current)
        return worktrees

    def get_diff(self, cwd: Optional[str] = None, cached: bool = False) -> str:
        """Gets the uncommitted or cached diff."""
        args = ["diff"]
        if cached:
            args.append("--cached")
        res = self._run_git(args, cwd=cwd)
        return res["stdout"] if res["success"] else ""

    def commit_changes(self, message: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Stages and commits changes in specified worktree or root."""
        add_res = self._run_git(["add", "-A"], cwd=cwd)
        if not add_res["success"]:
            return add_res
        return self._run_git(["commit", "-m", message], cwd=cwd)
