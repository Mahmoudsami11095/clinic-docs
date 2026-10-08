"""Interactive CLI tool for ClinicCorp AI multi-agent software company."""
import os
import sys
import argparse
import json

# Setup sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_company_root = os.path.abspath(os.path.join(current_dir, ".."))
clinic_docs_root = os.path.abspath(os.path.join(agent_company_root, ".."))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

if agent_company_root not in sys.path:
    sys.path.insert(0, agent_company_root)

from src.tools.knowledge_retriever import KnowledgeRetriever
from src.tools.azure_health_checker import AzureHealthChecker
from src.tools.doc_synchronizer import DocSynchronizer
from src.orchestrator.state_graph import ClinicCorpOrchestrator
from src.orchestrator.self_healing import SelfHealingEngine


def cmd_list_agents(args):
    prompts_dir = os.path.join(agent_company_root, "prompts")
    files = [f for f in os.listdir(prompts_dir) if f.endswith(".md")]
    print("\n--- ClinicCorp AI Registered Squads & Agents ---")
    for f in sorted(files):
        role_name = f.replace(".md", "")
        with open(os.path.join(prompts_dir, f), "r", encoding="utf-8") as file:
            first_line = file.readline().strip("# \r\n")
        print(f"• {role_name:<25} | {first_line}")
    print()


def cmd_query_kb(args):
    retriever = KnowledgeRetriever(clinic_docs_root)
    query = " ".join(args.query)
    print(f"\n[Searching Knowledge Base for: '{query}']")
    results = retriever.search(query, max_results=args.limit)
    if not results:
        print("No matching documentation sections found.")
        return

    for idx, r in enumerate(results, 1):
        print(f"\n[{idx}] {r['doc_name']} -> {r['title']} (Score: {r['score']})")
        print("-" * 60)
        print(r['snippet'])


def cmd_check_health(args):
    checker = AzureHealthChecker()
    print("\n[Probing Live Azure & Vercel Cloud Endpoints]")
    report = checker.check_all_endpoints()
    print(f"Availability: {report['healthy_count']}/{report['total_endpoints']} Endpoints Healthy\n")
    for p in report["probes"]:
        status_icon = "🟢" if p["healthy"] else "🔴"
        print(f"{status_icon} {p['name']:<25} | {p['latency_ms']:>6.1f}ms | HTTP {p['status_code']} | {p['url']}")
        if p["error"]:
            print(f"   └── Error: {p['error']}")


def cmd_audit_docs(args):
    sync = DocSynchronizer(clinic_docs_root)
    audit = sync.audit_doc_presence()
    print("\n[Auditing Master Specification Documents]")
    for doc, exists in audit.items():
        icon = "🟢" if exists else "🔴"
        print(f"{icon} {doc:<45} : {'Present' if exists else 'Missing'}")


def cmd_run_sprint(args):
    orchestrator = ClinicCorpOrchestrator(clinic_docs_root)
    orchestrator.run_sprint_cycle(args.feature, dry_run=not args.live_tests)


def main():
    parser = argparse.ArgumentParser(description="ClinicCorp AI — Interactive CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # list-agents
    subparsers.add_parser("list-agents", help="List all registered agent personas")

    # query-kb
    kb_parser = subparsers.add_parser("query-kb", help="Query domain documentation & rules")
    kb_parser.add_argument("query", nargs="+", help="Keywords or phrase to search")
    kb_parser.add_argument("--limit", type=int, default=3, help="Max results")

    # check-health
    subparsers.add_parser("check-health", help="Probe live production endpoints")

    # audit-docs
    subparsers.add_parser("audit-docs", help="Audit presence of master specifications")

    # sprint
    sprint_parser = subparsers.add_parser("sprint", help="Execute an autonomous SDLC sprint")
    sprint_parser.add_argument("--feature", type=str, default="v3.2.0-telehealth-webrtc", help="Feature ID")
    sprint_parser.add_argument("--live-tests", action="store_true", help="Run actual test suites")

    args = parser.parse_args()
    if args.command == "list-agents":
        cmd_list_agents(args)
    elif args.command == "query-kb":
        cmd_query_kb(args)
    elif args.command == "check-health":
        cmd_check_health(args)
    elif args.command == "audit-docs":
        cmd_audit_docs(args)
    elif args.command == "sprint":
        cmd_run_sprint(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
