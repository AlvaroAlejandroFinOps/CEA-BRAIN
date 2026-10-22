import json
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

from src.context_auditor.adapters.base import BaseLLMAdapter, AdapterExecutionError
from src.context_auditor.models import AuditInput


class AntigravityAdapter(BaseLLMAdapter):
    """
    Local inference adapter for Antigravity IDE / CLI toolchain.
    Delegates semantic context evaluation to the local `agy.exe` executable,
    enabling offline evaluation without requiring a remote API key.
    """

    SUPPORTED_MODELS = [
        "gemini-3.6-flash",
        "gemini-3.7-flash",
        "gemini-3.8-flash",
        "gemini-3.1-pro"
    ]

    def __init__(
        self,
        model: str = "gemini-3.7-flash",
        effort: Optional[str] = "medium",
        agy_path: str = "agy.exe",
        timeout: int = 120
    ):
        self.model = model
        self.effort = effort
        self.agy_path = agy_path
        self.timeout = timeout

    def evaluate_context(self, audit_input: AuditInput, signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes semantic context evaluation using local `agy.exe` CLI.
        """
        prompt = self._compile_prompt(audit_input, signals)
        cmd = [
            self.agy_path,
            "--model", self.model,
        ]
        if self.effort:
            cmd.extend(["--effort", self.effort])
        cmd.extend([
            "--input-format", "text",
            "--output-format", "json",
            "--dangerously-skip-permissions"
        ])

        try:
            result = subprocess.run(
                cmd,
                input=prompt,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout
            )
        except FileNotFoundError as fnf:
            raise AdapterExecutionError(
                f"Antigravity CLI executable '{self.agy_path}' was not found. "
                f"Please ensure agy.exe is installed and configured in your system PATH."
            ) from fnf
        except subprocess.TimeoutExpired as te:
            raise AdapterExecutionError(
                f"Antigravity CLI execution timed out after {self.timeout} seconds."
            ) from te
        except Exception as e:
            raise AdapterExecutionError(
                f"Unexpected error running Antigravity CLI: {str(e)}"
            ) from e

        if result.returncode != 0:
            err_msg = result.stderr.strip() if result.stderr else f"Process exited with code {result.returncode}"
            raise AdapterExecutionError(f"Antigravity CLI execution failed: {err_msg}")

        raw_output = result.stdout.strip()
        parsed_json = self._extract_json(raw_output)
        return parsed_json

    def _compile_prompt(self, audit_input: AuditInput, signals: Dict[str, Any]) -> str:
        """
        Builds the complete auditor prompt instructing the LLM to evaluate
        the conversation flow against the 6 CEA dimensions and return valid JSON.
        """
        prompt_path = Path("prompts/auditor-technical-en.md")
        system_instructions = ""
        if prompt_path.exists():
            system_instructions = prompt_path.read_text(encoding="utf-8")
        else:
            system_instructions = (
                "You are the Context Entropy Auditor (CEA). "
                "Evaluate the provided conversation and deterministic signals across the 6 dimensions: "
                "instruction_conflict, task_ambiguity, context_contamination, evidence_quality, "
                "state_integrity, redundancy_pressure (scores 0-100). "
                "Respond strictly with a valid JSON object."
            )

        payload = {
            "messages": [
                m.model_dump() if hasattr(m, "model_dump") else m
                for m in audit_input.messages
            ],
            "documents": [
                d.model_dump() if hasattr(d, "model_dump") else d
                for d in audit_input.documents
            ],
            "tool_events": [
                t.model_dump() if hasattr(t, "model_dump") else t
                for t in audit_input.tool_events
            ],
            "runtime_telemetry": audit_input.runtime_telemetry,
            "deterministic_signals": signals
        }

        return (
            f"{system_instructions}\n\n"
            f"## Audit Input Data:\n```json\n{json.dumps(payload, indent=2, default=str)}\n```\n\n"
            "Return JSON output matching the CEA audit schema strictly."
        )

    def _extract_json(self, raw_text: str) -> Dict[str, Any]:
        """
        Defensively parses JSON output, extracting agy CLI response envelope
        and markdown code fences if present.
        """
        cleaned = raw_text.strip()
        
        # Step 1: If raw_text is a top-level JSON envelope from agy (e.g. {"status": "SUCCESS", "response": "..."})
        try:
            top_parsed = json.loads(cleaned)
            if isinstance(top_parsed, dict):
                # If it contains dimension_scores directly, it's the raw audit output
                if "dimension_scores" in top_parsed or "risk_score" in top_parsed:
                    return self._ensure_schema_defaults(top_parsed)
                # If it's an agy envelope with 'response' field
                if "response" in top_parsed and isinstance(top_parsed["response"], str):
                    cleaned = top_parsed["response"].strip()
                elif "response" in top_parsed and isinstance(top_parsed["response"], dict):
                    return self._ensure_schema_defaults(top_parsed["response"])
        except json.JSONDecodeError:
            pass

        # Step 2: Strip markdown ```json ... ``` or ``` ... ```
        if "```" in cleaned:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
            if match:
                cleaned = match.group(1).strip()

        # Step 3: Parse cleaned JSON string
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict):
                return self._ensure_schema_defaults(parsed)
            raise AdapterExecutionError(f"Expected JSON object from Antigravity CLI, got: {type(parsed).__name__}")
        except json.JSONDecodeError:
            # Step 4: Fallback attempt with regex extraction of outer curly braces
            match = re.search(r"(\{[\s\S]*\})", cleaned)
            if match:
                try:
                    parsed = json.loads(match.group(1))
                    if isinstance(parsed, dict):
                        return self._ensure_schema_defaults(parsed)
                except json.JSONDecodeError:
                    pass

            raise AdapterExecutionError(
                f"Failed to decode JSON from Antigravity CLI output: {raw_text[:300]}"
            )

    def _ensure_schema_defaults(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures all expected keys for CEA scoring and models are present in the dictionary.
        """
        data.setdefault("confidence", 0.9)
        data.setdefault("evidence_coverage", 1.0)
        data.setdefault("dimension_scores", {})
        data.setdefault("findings", [])
        data.setdefault("recommended_actions", [])
        data.setdefault("limitations", [])

        dim_defaults = {
            "instruction_conflict": 0,
            "task_ambiguity": 0,
            "context_contamination": 0,
            "evidence_quality": 0,
            "state_integrity": 0,
            "redundancy_pressure": 0
        }
        for k, v in dim_defaults.items():
            data["dimension_scores"].setdefault(k, v)

        return data
