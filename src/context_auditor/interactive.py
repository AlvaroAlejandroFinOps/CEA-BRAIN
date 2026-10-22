import json
import os
import shutil
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.context_auditor.adapters.antigravity import AntigravityAdapter
from src.context_auditor.adapters.base import AdapterExecutionError
from src.context_auditor.adapters.gemini import GeminiAdapter
from src.context_auditor.auditor import ContextAuditor
from src.context_auditor.models import AuditInput, Message, Role, ToolEvent, Document, AuditResult
from src.context_auditor.policies import PolicyMode
from src.context_auditor.signals import estimate_tokens


# --- ANSI Color Utilities ---
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def print_banner():
    banner = f"""{Colors.CYAN}{Colors.BOLD}
================================================================================
    🔍 CONTEXT ENTROPY AUDITOR (CEA) — INTERACTIVE BENCHMARK & STRESS SUITE    
================================================================================{Colors.RESET}
 {Colors.DIM}Inferencia Local: Antigravity CLI (agy.exe) | Contrato Epistémico | Diagnóstico IRC{Colors.RESET}
"""
    print(banner)


# --- Benchmark & Session Logging ---
class BenchmarkSession:
    """Manages grouped session logs, timeline audits, and token telemetry."""

    def __init__(self, session_name: Optional[str] = None, initial_model: str = "gemini-3.7-flash", initial_effort: str = "medium"):
        self.session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
        self.session_name = session_name or f"Live_Audit_{datetime.now().strftime('%H%M%S')}"
        self.created_at = datetime.now().isoformat()
        self.current_model = initial_model
        self.current_effort = initial_effort
        self.models_used = {initial_model}
        
        self.messages: List[Dict[str, Any]] = []
        self.documents: List[Dict[str, Any]] = []
        self.tool_events: List[Dict[str, Any]] = []
        self.timeline: List[Dict[str, Any]] = []
        self.token_telemetry: List[Dict[str, Any]] = []
        self.last_prefix_hash: Optional[str] = None
        
        self.logs_dir = Path("logs") / "benchmarks" / self.session_id
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def add_message(self, role: str, content: str, model_used: Optional[str] = None) -> str:
        msg_id = f"msg-{len(self.messages) + 1}"
        msg_data = {
            "id": msg_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "model": model_used or self.current_model,
            "effort": self.current_effort,
            "estimated_tokens": estimate_tokens(content)
        }
        self.messages.append(msg_data)
        if model_used:
            self.models_used.add(model_used)
        return msg_id

    def add_document(self, content: str, source: str = "user_input") -> str:
        doc_id = f"doc-{len(self.documents) + 1}"
        doc_data = {
            "id": doc_id,
            "content": content,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "estimated_tokens": estimate_tokens(content)
        }
        self.documents.append(doc_data)
        return doc_id

    def add_tool_event(self, tool_name: str, parameters: Dict[str, Any], result: str) -> str:
        tool_id = f"tool-{len(self.tool_events) + 1}"
        tool_data = {
            "id": tool_id,
            "tool_name": tool_name,
            "parameters": parameters,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "estimated_tokens": estimate_tokens(result)
        }
        self.tool_events.append(tool_data)
        return tool_id

    def record_turn_audit(self, turn_index: int, audit_result: AuditResult, latency_sec: float):
        total_tokens = sum(m["estimated_tokens"] for m in self.messages)
        total_tokens += sum(d["estimated_tokens"] for d in self.documents)
        total_tokens += sum(t["estimated_tokens"] for t in self.tool_events)

        turn_entry = {
            "turn_index": turn_index,
            "timestamp": datetime.now().isoformat(),
            "model": self.current_model,
            "effort": self.current_effort,
            "risk_score": audit_result.risk_score,
            "overall_status": audit_result.overall_status.value if hasattr(audit_result.overall_status, "value") else str(audit_result.overall_status),
            "confidence": audit_result.confidence,
            "evidence_coverage": audit_result.evidence_coverage,
            "dimensions": audit_result.dimension_scores.model_dump(),
            "findings_count": len(audit_result.findings),
            "triggered_rules": audit_result.triggered_rules,
            "latency_seconds": round(latency_sec, 2),
            "total_estimated_tokens": total_tokens
        }
        self.timeline.append(turn_entry)
        self.save_snapshot()

    def build_audit_input(self) -> AuditInput:
        telemetry = {}
        if self.last_prefix_hash:
            telemetry["previous_prefix_hash"] = self.last_prefix_hash

        return AuditInput(
            messages=[
                Message(id=m["id"], role=Role(m["role"]), content=m["content"])
                for m in self.messages
            ],
            documents=[
                Document(id=d["id"], content=d["content"], source=d.get("source"))
                for d in self.documents
            ],
            tool_events=[
                ToolEvent(id=t["id"], tool_name=t["tool_name"], parameters=t["parameters"], result=t["result"])
                for t in self.tool_events
            ],
            runtime_telemetry=telemetry
        )

    def _atomic_write_text(self, target_path: Path, content: str) -> None:
        """Writes content to a temporary file and atomically replaces the target path."""
        tmp_path = target_path.with_suffix(target_path.suffix + ".tmp")
        tmp_path.write_text(content, encoding="utf-8")
        os.replace(str(tmp_path), str(target_path))

    def save_snapshot(self):
        # 1. session_meta.json
        meta = {
            "session_id": self.session_id,
            "session_name": self.session_name,
            "created_at": self.created_at,
            "updated_at": datetime.now().isoformat(),
            "current_model": self.current_model,
            "current_effort": self.current_effort,
            "models_used": list(self.models_used),
            "turns_count": len(self.timeline),
            "messages_count": len(self.messages),
            "documents_count": len(self.documents),
            "tool_events_count": len(self.tool_events)
        }
        self._atomic_write_text(self.logs_dir / "session_meta.json", json.dumps(meta, indent=2, ensure_ascii=False))

        # 2. conversation.json
        conv_payload = {
            "messages": self.messages,
            "documents": self.documents,
            "tool_events": self.tool_events
        }
        self._atomic_write_text(self.logs_dir / "conversation.json", json.dumps(conv_payload, indent=2, ensure_ascii=False))

        # 3. timeline.json
        self._atomic_write_text(self.logs_dir / "timeline.json", json.dumps(self.timeline, indent=2, ensure_ascii=False))

        # 4. summary_report.md
        self._write_markdown_summary()

    def _write_markdown_summary(self):
        lines = [
            f"# Benchmark Report: {self.session_name}",
            "",
            f"- **Session ID:** `{self.session_id}`",
            f"- **Fecha:** `{self.created_at}`",
            f"- **Modelos Utilizados:** `{', '.join(self.models_used)}`",
            f"- **Esfuerzo de Pensamiento Actual:** `{self.current_effort}`",
            f"- **Total de Turnos Evaluados:** `{len(self.timeline)}`",
            "",
            "## Evolución del Índice de Riesgo Contextual (IRC / CRS)",
            "",
            "| Turno | Modelo | Esfuerzo | Tokens Est. | Score IRC | Estado | Confianza | Latencia | Reglas Override |",
            "|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|"
        ]

        for t in self.timeline:
            status_badge = t["overall_status"].upper()
            rules_str = ", ".join(t["triggered_rules"]) if t["triggered_rules"] else "—"
            lines.append(
                f"| `{t['turn_index']}` | `{t['model']}` | `{t['effort']}` | `{t['total_estimated_tokens']}` | **`{t['risk_score']:.1f}`** | **`{status_badge}`** | `{t['confidence']:.2f}` | `{t['latency_seconds']}s` | {rules_str} |"
            )

        lines.extend([
            "",
            "---",
            f"> *Archivo de benchmark guardado en `{self.logs_dir}`.*"
        ])
        self._atomic_write_text(self.logs_dir / "summary_report.md", "\n".join(lines))


# --- Interactive CLI Application ---
class InteractiveAuditorCLI:
    AVAILABLE_MODELS = [
        ("gemini-3.7-flash", "Gemini 3.7 Flash (Recomendado / Alta velocidad y razonamiento)"),
        ("gemini-3.1-pro", "Gemini 3.1 Pro (Máxima profundidad analítica)"),
        ("gemini-3.8-flash", "Gemini 3.8 Flash (Vanguardia / Próxima generación)"),
        ("gemini-3.6-flash", "Gemini 3.6 Flash (Modelo ultraligero)"),
        ("claude-sonnet-4-6", "Claude Sonnet 4.6 Thinking"),
        ("gpt-oss-120b-medium", "GPT-OSS 120B Open Weights")
    ]

    EFFORT_LEVELS = ["low", "medium", "high", "max"]

    def __init__(self):
        self.selected_model = "gemini-3.7-flash"
        self.selected_effort = "medium"
        self.adapter_mode = "antigravity" if (shutil.which("agy") or shutil.which("agy.exe")) else "gemini"

    def run(self):
        while True:
            print_banner()
            self._print_current_config()
            print(f"{Colors.BOLD}MENÚ PRINCIPAL:{Colors.RESET}")
            print(f"  {Colors.GREEN}[1]{Colors.RESET} 📂 Ejecutar Caso de Simulación (de examples/)")
            print(f"  {Colors.GREEN}[2]{Colors.RESET} 📄 Auditar Archivo JSON Personalizado")
            print(f"  {Colors.GREEN}[3]{Colors.RESET} ⚡ {Colors.BOLD}Live Stress Test (Chat Interactivo en Vivo + Auditoría Turno a Turno){Colors.RESET}")
            print(f"  {Colors.GREEN}[4]{Colors.RESET} ⚙️ Cambiar Modelo ({self.selected_model}) y Nivel de Pensamiento ({self.selected_effort})")
            print(f"  {Colors.GREEN}[5]{Colors.RESET} 📊 Ver Historial de Benchmarks y Sesiones Guardadas")
            print(f"  {Colors.RED}[0]{Colors.RESET} 🚪 Salir\n")

            choice = input(f"{Colors.YELLOW}Selecciona una opción [0-5]: {Colors.RESET}").strip()

            if choice == "1":
                self.run_simulation_menu()
            elif choice == "2":
                self.run_custom_file_audit()
            elif choice == "3":
                self.run_live_stress_chat()
            elif choice == "4":
                self.configure_model_menu()
            elif choice == "5":
                self.view_benchmarks_history()
            elif choice == "0":
                print(f"\n{Colors.CYAN}¡Hasta pronto!{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}Opción inválida.{Colors.RESET}")
                time.sleep(1)

    def _print_current_config(self):
        print(f"  {Colors.DIM}Configuración Activa:{Colors.RESET} Adaptador: {Colors.CYAN}{self.adapter_mode.upper()}{Colors.RESET} | Modelo: {Colors.GREEN}{self.selected_model}{Colors.RESET} | Effort: {Colors.YELLOW}{self.selected_effort}{Colors.RESET}\n")

    def configure_model_menu(self):
        print(f"\n{Colors.BOLD}=== SELECCIÓN DE MODELO ==={Colors.RESET}")
        for i, (m_id, desc) in enumerate(self.AVAILABLE_MODELS, 1):
            marker = f"{Colors.GREEN}●{Colors.RESET}" if m_id == self.selected_model else " "
            print(f"  [{i}] {marker} {m_id:<22} ({desc})")
        print("  [C] Nombre personalizado...")

        choice = input(f"\n{Colors.YELLOW}Selecciona modelo [1-{len(self.AVAILABLE_MODELS)} o Enter para mantener]: {Colors.RESET}").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.AVAILABLE_MODELS):
            self.selected_model = self.AVAILABLE_MODELS[int(choice) - 1][0]
        elif choice.upper() == "C":
            custom = input(f"{Colors.YELLOW}Escribe el identificador del modelo: {Colors.RESET}").strip()
            if custom:
                self.selected_model = custom

        print(f"\n{Colors.BOLD}=== NIVEL DE RAZONAMIENTO (EFFORT) ==={Colors.RESET}")
        for i, eff in enumerate(self.EFFORT_LEVELS, 1):
            marker = f"{Colors.GREEN}●{Colors.RESET}" if eff == self.selected_effort else " "
            print(f"  [{i}] {marker} {eff}")
        eff_choice = input(f"\n{Colors.YELLOW}Selecciona nivel [1-4 o Enter para mantener]: {Colors.RESET}").strip()
        if eff_choice.isdigit() and 1 <= int(eff_choice) <= len(self.EFFORT_LEVELS):
            self.selected_effort = self.EFFORT_LEVELS[int(eff_choice) - 1]

        print(f"\n{Colors.GREEN}✓ Configuración actualizada:{Colors.RESET} Modelo: {self.selected_model}, Effort: {self.selected_effort}")
        input(f"\n{Colors.DIM}Presiona Enter para continuar...{Colors.RESET}")

    def run_simulation_menu(self):
        examples_dir = Path("examples")
        if not examples_dir.exists():
            print(f"{Colors.RED}No se encontró la carpeta 'examples/'.{Colors.RESET}")
            time.sleep(1)
            return

        example_files = list(examples_dir.glob("*.json"))
        if not example_files:
            print(f"{Colors.RED}No hay archivos JSON en 'examples/'.{Colors.RESET}")
            time.sleep(1)
            return

        print(f"\n{Colors.BOLD}=== CASOS DE SIMULACIÓN DISPONIBLES ==={Colors.RESET}")
        for i, file in enumerate(example_files, 1):
            print(f"  [{i}] {file.name}")

        choice = input(f"\n{Colors.YELLOW}Selecciona caso [1-{len(example_files)}]: {Colors.RESET}").strip()
        if not (choice.isdigit() and 1 <= int(choice) <= len(example_files)):
            print(f"{Colors.RED}Opción inválida.{Colors.RESET}")
            time.sleep(1)
            return

        selected_file = example_files[int(choice) - 1]
        self._execute_file_audit(selected_file)

    def run_custom_file_audit(self):
        path_str = input(f"\n{Colors.YELLOW}Introduce la ruta del archivo JSON a auditar: {Colors.RESET}").strip().strip('"').strip("'")
        target_path = Path(path_str)
        if not target_path.exists():
            print(f"{Colors.RED}El archivo '{target_path}' no existe.{Colors.RESET}")
            input(f"\n{Colors.DIM}Presiona Enter para volver...{Colors.RESET}")
            return

        self._execute_file_audit(target_path)

    def _execute_file_audit(self, file_path: Path):
        print(f"\n{Colors.CYAN}Cargando y auditando {file_path.name}...{Colors.RESET}")
        try:
            raw_data = json.loads(file_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"{Colors.RED}Error al leer JSON: {e}{Colors.RESET}")
            input(f"\n{Colors.DIM}Presiona Enter para continuar...{Colors.RESET}")
            return

        session = BenchmarkSession(session_name=f"Audit_{file_path.stem}", initial_model=self.selected_model, initial_effort=self.selected_effort)
        adapter = AntigravityAdapter(model=self.selected_model, effort=self.selected_effort) if self.adapter_mode == "antigravity" else GeminiAdapter()
        auditor = ContextAuditor(llm_adapter=adapter, policy_mode=PolicyMode.RECOMMEND)

        start_time = time.time()
        try:
            result = auditor.audit(raw_data)
            latency = time.time() - start_time
            
            # Record in session
            session.messages = raw_data.get("messages", [])
            session.documents = raw_data.get("documents", [])
            session.tool_events = raw_data.get("tool_events", [])
            session.record_turn_audit(1, result, latency)

            self._display_audit_card(result, latency, self.selected_model, self.selected_effort)
            print(f"\n{Colors.GREEN}✓ Benchmark y logs guardados en:{Colors.RESET} `{session.logs_dir}`")
        except Exception as e:
            print(f"\n{Colors.RED}Error durante la auditoría: {e}{Colors.RESET}")

        input(f"\n{Colors.DIM}Presiona Enter para continuar...{Colors.RESET}")

    def run_live_stress_chat(self):
        print_banner()
        print(f"{Colors.BOLD}{Colors.GREEN}⚡ LIVE STRESS TEST — CHAT INTERACTIVO CON AUDITORÍA EN TIEMPO REAL{Colors.RESET}")
        print(f"{Colors.DIM}Escribe mensajes turno a turno. El auditor evaluará la entropía y recalculará el IRC.{Colors.RESET}")
        print(f"{Colors.DIM}Comandos especiales: /model (cambiar modelo), /effort, /tool, /doc, /report, /save, /exit{Colors.RESET}\n")

        session_name = input(f"{Colors.YELLOW}Nombre para esta sesión de Benchmark (o Enter para automático): {Colors.RESET}").strip()
        session = BenchmarkSession(
            session_name=session_name if session_name else None,
            initial_model=self.selected_model,
            initial_effort=self.selected_effort
        )

        turn = 0
        while True:
            turn += 1
            print(f"\n{Colors.CYAN}{'-'*70}{Colors.RESET}")
            print(f"{Colors.BOLD}[TURNO {turn}] Modelo Activo: {Colors.GREEN}{session.current_model}{Colors.RESET} ({session.current_effort}) | Mensajes: {len(session.messages)}{Colors.RESET}")
            
            user_input = input(f"{Colors.YELLOW}Usuario > {Colors.RESET}").strip()

            if not user_input:
                continue

            # Command Handlers
            if user_input.lower() in ["/exit", "/quit", "exit", "quit"]:
                print(f"\n{Colors.GREEN}✓ Sesión finalizada. Todos los logs y timeline están guardados en:{Colors.RESET}")
                print(f"  📁 `{session.logs_dir}`")
                input(f"\n{Colors.DIM}Presiona Enter para volver al menú principal...{Colors.RESET}")
                break

            if user_input.lower() == "/model":
                self._switch_model_in_session(session)
                continue

            if user_input.lower() == "/effort":
                self._switch_effort_in_session(session)
                continue

            if user_input.lower() == "/tool":
                self._inject_tool_event(session)
                continue

            if user_input.lower() == "/doc":
                self._inject_document(session)
                continue

            if user_input.lower() == "/report":
                session.save_snapshot()
                print(f"{Colors.GREEN}Reporte guardado en {session.logs_dir}/summary_report.md{Colors.RESET}")
                continue

            # 1. Add User Message
            session.add_message(role="user", content=user_input)

            # 2. Add Simulated Assistant Response (or ask user for it)
            asst_resp = input(f"{Colors.BLUE}Respuesta Asistente (o Enter para respuesta concisa estándar): {Colors.RESET}").strip()
            if not asst_resp:
                asst_resp = f"Entendido. Procedo con la solicitud: '{user_input[:50]}...'"
            session.add_message(role="assistant", content=asst_resp)

            # 3. Perform Live Turn Audit
            print(f"{Colors.DIM}⏳ Auditando contexto en tiempo real con {session.current_model}...{Colors.RESET}")
            audit_input = session.build_audit_input()
            
            adapter = AntigravityAdapter(model=session.current_model, effort=session.current_effort) if self.adapter_mode == "antigravity" else GeminiAdapter()
            auditor = ContextAuditor(llm_adapter=adapter, policy_mode=PolicyMode.RECOMMEND)

            start_t = time.time()
            try:
                result = auditor.audit(audit_input.model_dump())
                latency = time.time() - start_t
                session.record_turn_audit(turn, result, latency)
                self._display_turn_summary(turn, result, latency, session)
            except Exception as e:
                print(f"{Colors.RED}Error al auditar turno: {e}{Colors.RESET}")

    def _switch_model_in_session(self, session: BenchmarkSession):
        print(f"\n{Colors.BOLD}--- CAMBIAR MODELO EN CALIENTE ---{Colors.RESET}")
        for i, (m_id, desc) in enumerate(self.AVAILABLE_MODELS, 1):
            marker = f"{Colors.GREEN}●{Colors.RESET}" if m_id == session.current_model else " "
            print(f"  [{i}] {marker} {m_id:<20} ({desc})")
        choice = input(f"{Colors.YELLOW}Selecciona nuevo modelo: {Colors.RESET}").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.AVAILABLE_MODELS):
            new_model = self.AVAILABLE_MODELS[int(choice) - 1][0]
            session.current_model = new_model
            session.models_used.add(new_model)
            print(f"{Colors.GREEN}✓ Modelo cambiado a: {new_model}{Colors.RESET}")

    def _switch_effort_in_session(self, session: BenchmarkSession):
        print(f"\n{Colors.BOLD}--- CAMBIAR NIVEL DE EFFORT ---{Colors.RESET}")
        for i, eff in enumerate(self.EFFORT_LEVELS, 1):
            marker = f"{Colors.GREEN}●{Colors.RESET}" if eff == session.current_effort else " "
            print(f"  [{i}] {marker} {eff}")
        choice = input(f"{Colors.YELLOW}Selecciona nivel: {Colors.RESET}").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.EFFORT_LEVELS):
            session.current_effort = self.EFFORT_LEVELS[int(choice) - 1]
            print(f"{Colors.GREEN}✓ Effort cambiado a: {session.current_effort}{Colors.RESET}")

    def _inject_tool_event(self, session: BenchmarkSession):
        print(f"\n{Colors.BOLD}--- INYECTAR LLAMADA A HERRAMIENTA ---{Colors.RESET}")
        name = input("Nombre de la herramienta (ej: search_db): ").strip() or "tool_call"
        params_str = input("Parámetros JSON (ej: {\"query\": \"test\"}): ").strip() or "{}"
        result = input("Resultado de la herramienta: ").strip() or "OK"
        try:
            params = json.loads(params_str)
        except Exception:
            params = {"raw": params_str}
        session.add_tool_event(tool_name=name, parameters=params, result=result)
        print(f"{Colors.GREEN}✓ Herramienta inyectada.{Colors.RESET}")

    def _inject_document(self, session: BenchmarkSession):
        print(f"\n{Colors.BOLD}--- INYECTAR DOCUMENTO / CONTEXTO EXTERNO ---{Colors.RESET}")
        source = input("Fuente / URI del documento: ").strip() or "user_doc"
        content = input("Contenido del documento: ").strip()
        if content:
            session.add_document(content=content, source=source)
            print(f"{Colors.GREEN}✓ Documento inyectado ({estimate_tokens(content)} tokens est.).{Colors.RESET}")

    def _display_turn_summary(self, turn: int, result: AuditResult, latency: float, session: BenchmarkSession):
        status_color = Colors.GREEN if result.risk_score < 25 else (
            Colors.YELLOW if result.risk_score < 50 else (
                Colors.RED if result.risk_score < 75 else f"{Colors.BOLD}{Colors.RED}"
            )
        )
        total_tokens = sum(m["estimated_tokens"] for m in session.messages)

        print(f"\n  📊 {Colors.BOLD}Métricas Turno {turn}:{Colors.RESET}")
        print(f"     • Índice de Riesgo (IRC): {status_color}{result.risk_score:.1f}/100 ({result.overall_status.value.upper()}){Colors.RESET}")
        print(f"     • Tokens Acumulados: {Colors.CYAN}{total_tokens}{Colors.RESET} | Latencia: {latency:.2f}s | Confianza: {result.confidence:.2f}")
        
        # Dimensions bar
        print(f"     • Dimensiones:")
        for dim, score in result.dimension_scores.model_dump().items():
            bar_color = Colors.GREEN if score == 0 else (Colors.YELLOW if score <= 50 else Colors.RED)
            print(f"       - {dim:<22}: {bar_color}{score:>3}/100{Colors.RESET}")

        if result.triggered_rules:
            print(f"     • {Colors.RED}⚠️ Reglas Override Activadas: {', '.join(result.triggered_rules)}{Colors.RESET}")

        if result.findings:
            print(f"     • {Colors.YELLOW}Hallazgos ({len(result.findings)}):{Colors.RESET}")
            for f in result.findings[:2]:
                print(f"       - [{f.epistemic_status.upper()}] {f.explanation[:120]}...")

    def _display_audit_card(self, result: AuditResult, latency: float, model: str, effort: str):
        status_color = Colors.GREEN if result.risk_score < 25 else (
            Colors.YELLOW if result.risk_score < 50 else Colors.RED
        )
        print(f"\n{Colors.BOLD}=================== REPORTE DE AUDITORÍA ==================={Colors.RESET}")
        print(f"  Modelo: {Colors.GREEN}{model}{Colors.RESET} (Effort: {effort}) | Latencia: {latency:.2f}s")
        print(f"  Estado General: {status_color}{result.overall_status.value.upper()}{Colors.RESET}")
        print(f"  Índice de Riesgo Contextual (IRC): {status_color}{result.risk_score:.1f} / 100.0{Colors.RESET}")
        print(f"  Confianza: {result.confidence:.2f} | Cobertura: {result.evidence_coverage:.2f}")
        print(f"------------------------------------------------------------")
        print(f"  {'Dimensión':<25} {'Puntaje':<10}")
        print(f"------------------------------------------------------------")
        for dim, score in result.dimension_scores.model_dump().items():
            d_col = Colors.GREEN if score == 0 else (Colors.YELLOW if score <= 50 else Colors.RED)
            print(f"  {dim:<25} {d_col}{score:>3} / 100{Colors.RESET}")
        print(f"------------------------------------------------------------")
        if result.triggered_rules:
            print(f"  {Colors.RED}Reglas Override: {', '.join(result.triggered_rules)}{Colors.RESET}")
        if result.findings:
            print(f"\n  {Colors.BOLD}Hallazgos Prioritarios:{Colors.RESET}")
            for f in result.findings:
                print(f"  - [{f.dimension.upper()} - {f.epistemic_status}]: {f.explanation}")
                if getattr(f, "remediation", None):
                    print(f"    {Colors.CYAN}Acción:{Colors.RESET} {f.remediation}")
        print(f"============================================================\n")

    def view_benchmarks_history(self):
        benchmarks_dir = Path("logs") / "benchmarks"
        if not benchmarks_dir.exists():
            print(f"\n{Colors.YELLOW}No hay benchmarks guardados aún.{Colors.RESET}")
            input(f"\n{Colors.DIM}Presiona Enter para continuar...{Colors.RESET}")
            return

        sessions = sorted(list(benchmarks_dir.iterdir()), key=lambda x: x.stat().st_mtime, reverse=True)
        if not sessions:
            print(f"\n{Colors.YELLOW}No hay sesiones guardadas en logs/benchmarks/.{Colors.RESET}")
            input(f"\n{Colors.DIM}Presiona Enter para continuar...{Colors.RESET}")
            return

        print(f"\n{Colors.BOLD}=== HISTORIAL DE SESIONES Y BENCHMARKS ==={Colors.RESET}")
        for i, s_dir in enumerate(sessions[:15], 1):
            meta_file = s_dir / "session_meta.json"
            meta_name = s_dir.name
            turns_str = ""
            if meta_file.exists():
                try:
                    meta_data = json.loads(meta_file.read_text(encoding="utf-8"))
                    meta_name = meta_data.get("session_name", s_dir.name)
                    turns_str = f"({meta_data.get('turns_count', 0)} turnos - {', '.join(meta_data.get('models_used', []))})"
                except Exception:
                    pass
            print(f"  [{i}] {meta_name:<30} {turns_str:<35} -> `{s_dir.name}`")

        choice = input(f"\n{Colors.YELLOW}Selecciona sesión para ver detalle [1-{len(sessions[:15])} o Enter]: {Colors.RESET}").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(sessions[:15]):
            selected_s = sessions[int(choice) - 1]
            report_md = selected_s / "summary_report.md"
            if report_md.exists():
                print(f"\n{report_md.read_text(encoding='utf-8')}")
            else:
                print(f"{Colors.YELLOW}No se encontró summary_report.md para esta sesión.{Colors.RESET}")
            input(f"\n{Colors.DIM}Presiona Enter para volver...{Colors.RESET}")


def main():
    cli = InteractiveAuditorCLI()
    cli.run()


if __name__ == "__main__":
    main()
