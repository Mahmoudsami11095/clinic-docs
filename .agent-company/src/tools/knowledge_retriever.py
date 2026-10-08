"""Domain Knowledge Base and Specification Search for ClinicCorp AI."""
import os
import re
from typing import List, Dict, Any


class KnowledgeRetriever:
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)
        self.docs_to_index = [
            "CUSTOMER_REQUIREMENTS_DOCUMENT.md",
            "SOFTWARE_REQUIREMENTS_SPECIFICATION.md",
            "CLINIC_USER_MANUAL_AND_SOP.md",
            "UAT_ACCEPTANCE_TEST_PLAN.md",
            "ENTERPRISE_FEATURE_ROADMAP_v3.1.0_v4.0.0.md",
            "AGENT_HANDOFF.md"
        ]

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Searches indexed documentation for sections relevant to query terms."""
        results = []
        tokens = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
        if not tokens:
            return []

        for doc_name in self.docs_to_index:
            doc_path = os.path.join(self.workspace_root, doc_name)
            if not os.path.isfile(doc_path):
                continue

            with open(doc_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Split by markdown headers (## or ###)
            sections = re.split(r"\n(?=##+\s)", content)
            for section in sections:
                section_lower = section.lower()
                score = sum(1 for token in tokens if token in section_lower)
                if score > 0:
                    lines = section.strip().splitlines()
                    title = lines[0] if lines else "Section"
                    snippet = "\n".join(lines[1:10]) if len(lines) > 1 else ""
                    results.append({
                        "doc_name": doc_name,
                        "title": title.strip("# "),
                        "score": score,
                        "snippet": snippet[:500]
                    })

        # Sort by match score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]
