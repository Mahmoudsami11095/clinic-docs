"""Documentation synchronizer and compliance auditor for clinic-docs."""
import os
import re
from typing import Dict, Any


class DocSynchronizer:
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)
        self.agent_handoff_path = os.path.join(self.workspace_root, "AGENT_HANDOFF.md")
        self.readme_path = os.path.join(self.workspace_root, "README.md")

    def audit_doc_presence(self) -> Dict[str, bool]:
        """Verifies that all master documentation files exist and are non-empty."""
        expected_docs = [
            "CUSTOMER_REQUIREMENTS_DOCUMENT.md",
            "SOFTWARE_REQUIREMENTS_SPECIFICATION.md",
            "CLINIC_USER_MANUAL_AND_SOP.md",
            "UAT_ACCEPTANCE_TEST_PLAN.md",
            "AUTOMATED_TEST_SUITE_REPORT.md",
            "ENTERPRISE_FEATURE_ROADMAP_v3.1.0_v4.0.0.md",
            "AGENT_HANDOFF.md",
            "README.md",
            "MULTI_AGENT_COMPANY_PLAN.md"
        ]
        status = {}
        for doc in expected_docs:
            full_path = os.path.join(self.workspace_root, doc)
            exists = os.path.isfile(full_path) and os.path.getsize(full_path) > 0
            status[doc] = exists
        return status

    def sync_test_counts(self, backend_count: int, frontend_count: int, e2e_count: int) -> bool:
        """Updates test count statistics across AGENT_HANDOFF.md and README.md."""
        total_tests = backend_count + frontend_count + e2e_count

        # 1. Update AGENT_HANDOFF.md if exists
        if os.path.exists(self.agent_handoff_path):
            with open(self.agent_handoff_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace Total count
            new_content = re.sub(
                r"\*\*TOTAL VERIFIED SUITE\*\*\s*\|\s*Full Application Stack\s*\|\s*\*\*\d+\*\*",
                f"**TOTAL VERIFIED SUITE** | Full Application Stack | **{total_tests}**",
                content
            )
            with open(self.agent_handoff_path, "w", encoding="utf-8") as f:
                f.write(new_content)

        return True
