import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Any, Optional

from src.context_auditor.adapters.base import BaseLLMAdapter, AdapterExecutionError
from src.context_auditor.models import AuditInput


class LocalEndpointAdapter(BaseLLMAdapter):
    """
    Universal local HTTP adapter compatible with OpenAI-style endpoints
    (Ollama, vLLM, LM Studio, LocalAI) using strictly Python stdlib urllib.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434/v1",
        model: str = "qwen2.5:7b",
        api_key: str = "not-needed",
        timeout: int = 60,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout

    def evaluate_context(self, audit_input: AuditInput, signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes semantic context evaluation by sending an HTTP POST request
        to the local endpoint's /chat/completions route.
        """
        prompt = self._compile_prompt(audit_input, signals)
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                resp_bytes = response.read()
                resp_text = resp_bytes.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as he:
            err_body = he.read().decode("utf-8", errors="replace") if hasattr(he, "read") else ""
            raise AdapterExecutionError(
                f"Local endpoint HTTP error {he.code}: {he.reason} - {err_body[:200]}"
            ) from he
        except urllib.error.URLError as ue:
            raise AdapterExecutionError(
                f"Failed to connect to local endpoint at '{url}': {ue.reason}"
            ) from ue
        except (TimeoutError, Exception) as e:
            raise AdapterExecutionError(
                f"Error communicating with local endpoint at '{url}': {str(e)}"
            ) from e

        # Extract content from OpenAI-compatible response format
        try:
            resp_json = json.loads(resp_text)
            choices = resp_json.get("choices", [])
            if not choices:
                raise AdapterExecutionError(f"No choices returned by endpoint: {resp_text[:200]}")
            raw_content = choices[0].get("message", {}).get("content", "")
        except json.JSONDecodeError as je:
            raise AdapterExecutionError(f"Invalid JSON from endpoint: {resp_text[:200]}") from je

        return self._extract_json(raw_content)

    def _compile_prompt(self, audit_input: AuditInput, signals: Dict[str, Any]) -> str:
        prompt_path = Path("prompts/auditor-technical-en.md")
        if prompt_path.exists():
            system_instructions = prompt_path.read_text(encoding="utf-8")
        else:
            system_instructions = (
                "You are the Context Entropy Auditor (CEA). "
                "Evaluate the provided conversation and deterministic signals across the 6 dimensions: "
                "instruction_conflict, task_ambiguity, context_contamination, evidence_quality, "
                "state_integrity, redundancy_pressure (scores 0-100, quantized to 0, 25, 50, 75, 100). "
                "Respond strictly with a valid JSON object."
            )

        payload = {
            "messages": [
                m.model_dump(mode="json", exclude_none=True) if hasattr(m, "model_dump") else m
                for m in audit_input.messages
            ],
            "documents": [
                d.model_dump(mode="json", exclude_none=True) if hasattr(d, "model_dump") else d
                for d in audit_input.documents
            ],
            "tool_events": [
                t.model_dump(mode="json", exclude_none=True) if hasattr(t, "model_dump") else t
                for t in audit_input.tool_events
            ],
            "runtime_telemetry": audit_input.runtime_telemetry,
            "deterministic_signals": signals,
        }

        return (
            f"{system_instructions}\n\n"
            f"## Audit Input Data:\n```json\n{json.dumps(payload, indent=2, default=str)}\n```\n\n"
            "Return JSON output matching the CEA audit schema strictly."
        )

    def _extract_json(self, raw_text: str) -> Dict[str, Any]:
        cleaned = raw_text.strip()

        # Step 1: Direct JSON parsing
        try:
            top_parsed = json.loads(cleaned)
            if isinstance(top_parsed, dict):
                return self._ensure_schema_defaults(top_parsed)
        except json.JSONDecodeError:
            pass

        # Step 2: Strip markdown ```json ... ```
        if "```" in cleaned:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
            if match:
                cleaned = match.group(1).strip()

        # Step 3: Parse cleaned JSON string
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict):
                return self._ensure_schema_defaults(parsed)
        except json.JSONDecodeError:
            pass

        # Step 4: Fallback regex extraction of outer curly braces
        match = re.search(r"(\{[\s\S]*\})", cleaned)
        if match:
            try:
                parsed = json.loads(match.group(1))
                if isinstance(parsed, dict):
                    return self._ensure_schema_defaults(parsed)
            except json.JSONDecodeError:
                pass

        raise AdapterExecutionError(
            f"Failed to decode JSON from local endpoint output: {raw_text[:300]}"
        )

    def _ensure_schema_defaults(self, data: Dict[str, Any]) -> Dict[str, Any]:
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
            "redundancy_pressure": 0,
        }
        for k, v in dim_defaults.items():
            data["dimension_scores"].setdefault(k, v)

        return data
