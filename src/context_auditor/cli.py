import argparse
import json
import os
import shutil
import sys
from typing import Optional
from src.context_auditor.auditor import ContextAuditor
from src.context_auditor.adapters.base import BaseLLMAdapter
from src.context_auditor.adapters.gemini import GeminiAdapter
from src.context_auditor.adapters.antigravity import AntigravityAdapter
from src.context_auditor.adapters.local_endpoint import LocalEndpointAdapter
from src.context_auditor.policies import PolicyMode


def resolve_adapter(
    adapter_name: Optional[str] = None,
    model: Optional[str] = None,
    effort: str = "medium",
    agy_path: str = "agy.exe",
    endpoint_url: Optional[str] = None,
) -> BaseLLMAdapter:
    """
    Resolves the appropriate LLM adapter based on CLI options and environment availability.
    Full backward compatibility with existing callers.
    """
    if adapter_name == "antigravity":
        return AntigravityAdapter(model=model or "gemini-3.7-flash", effort=effort, agy_path=agy_path)
    elif adapter_name == "gemini":
        return GeminiAdapter(model_name=model or "gemini-2.5-pro")
    elif adapter_name == "local_endpoint":
        return LocalEndpointAdapter(
            base_url=endpoint_url or "http://localhost:11434/v1",
            model=model or "qwen2.5:7b",
        )

    # Auto-detection logic:
    # If GEMINI_API_KEY is not set but agy is available in system PATH, default to AntigravityAdapter
    if not os.environ.get("GEMINI_API_KEY") and (shutil.which("agy") or shutil.which(agy_path)):
        return AntigravityAdapter(model=model or "gemini-3.7-flash", effort=effort, agy_path=agy_path)

    return GeminiAdapter(model_name=model or "gemini-2.5-pro")


def main():
    parser = argparse.ArgumentParser(description="Context Entropy Auditor (CEA) CLI")
    parser.add_argument("input_file", nargs="?", default=None, help="Path to the JSON input file matching audit-input.schema.json")
    parser.add_argument("-i", "--interactive", action="store_true", help="Launch interactive benchmark and live stress testing menu")
    parser.add_argument("--adapter", choices=["gemini", "antigravity", "local_endpoint"], default=None, help="Inference adapter to use (default: auto-detected)")
    parser.add_argument("--endpoint-url", default="http://localhost:11434/v1", help="Base URL for local_endpoint adapter (default: http://localhost:11434/v1)")
    parser.add_argument("--model", default=None, help="LLM model name (e.g. gemini-3.7-flash, qwen2.5:7b)")
    parser.add_argument("--effort", default="medium", choices=["low", "medium", "high", "max"], help="Reasoning effort level for Antigravity models (default: medium)")
    parser.add_argument("--agy-path", default="agy.exe", help="Path to Antigravity CLI executable (default: agy.exe)")
    parser.add_argument("--policy", choices=[m.value for m in PolicyMode], default=PolicyMode.RECOMMEND.value, help="Policy mode for recommendations")
    parser.add_argument("--factual", action="store_true", help="Set to true if the task requires factual claims (stricter evidence checks)")
    parser.add_argument("--fast-gate-only", action="store_true", help="Execute deterministic L1 fast gate only without invoking an LLM")
    parser.add_argument("--force-semantic", action="store_true", help="Force L2 LLM evaluation even if L1 gate verdict is PASS")

    args = parser.parse_args()

    # If --interactive or no input_file provided, launch interactive menu
    if args.interactive or not args.input_file:
        from src.context_auditor.interactive import InteractiveAuditorCLI
        cli_app = InteractiveAuditorCLI()
        if args.model:
            cli_app.selected_model = args.model
        if args.effort:
            cli_app.selected_effort = args.effort
        cli_app.run()
        return

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            raw_input = json.load(f)

        adapter = resolve_adapter(
            adapter_name=args.adapter,
            model=args.model,
            effort=args.effort,
            agy_path=args.agy_path,
            endpoint_url=args.endpoint_url,
        )
        auditor = ContextAuditor(llm_adapter=adapter, policy_mode=PolicyMode(args.policy))

        result = auditor.audit(
            raw_input,
            task_requires_factual=args.factual,
            fast_gate_only=args.fast_gate_only,
            force_semantic=args.force_semantic,
        )

        # Print valid JSON to stdout
        print(json.dumps(result.model_dump(), indent=2))

    except Exception as e:
        print(f"Error during audit: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
