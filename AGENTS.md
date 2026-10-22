# AGENTS.md — CEA Brain Context Gateway & Directives

> **Operating Architecture:** Gravity HyperScale Thinking (iDirectory v3.0)  
> **Repository Role:** CEA Brain — Observability Kernel, Gateway & Session Governance  
> **Canonical Seed Reference:** `./01_seed/seed-cea-brain-master.md`  
> **Topological Map:** `./.context/tree.json`

---

## 1. Agente Bootloader & Preload Protocol

Cualquier modelo de IA o agente autónomo que opere en este repositorio debe respetar el siguiente protocolo de arranque jerárquico según lo declarado en `./.context/tree.json`:

- **Tier 1 (Contexto Mínimo de Ejecución):**
  1. `./AGENTS.md` (este archivo)
  2. `./.context/tree.json`
  3. `./[target_folder]/.context.yaml`
- **Tier 2 (Contexto Arquitectónico Completo):**
  1. `./AGENTS.md`
  2. `./.context/tree.json`
  3. `./01_seed/seed-cea-brain-master.md`
  4. `./[target_folder]/.context.yaml`

---

## 2. Invariantes de Ingeniería Obligatorios

- **[INV-01] Independencia del Core:** `src/context_auditor/models.py`, `signals.py`, `scoring.py` y `compactor.py` jamás deben importar SDKs de inferencia remota (`google.genai`, `openai`, `anthropic`).
- **[INV-02] Contrato Epistémico Absoluto:** Prohibición estricta de inferir estados físicos no observables (tensores de atención, hardware GPU/TPU, o invalidaciones de KV Cache sin telemetría explícita en `runtime_telemetry.previous_prefix_hash`). Toda métrica determinista se reporta como `EpistemicStatus.RUNTIME_MEASURED`.
- **[INV-03] Pureza Matemática e Inmutabilidad:** Las funciones de scoring, extracción de señales y compactación son funciones puras. `ContextCompactor` opera sobre copias profundas sin mutar objetos `AuditInput` in-place.
- **[INV-04] Bidireccionalidad de Esquemas:** Todo payload de entrada se valida contra `./schemas/audit-input.schema.json` y todo resultado se valida contra `./schemas/audit-result.schema.json`.
- **[INV-05] Presupuesto de Latencia Zero-Impact:** El gate determinista L1 (`extract_deterministic_signals` + `compute_l1_gate`) debe ejecutarse en $\le 15\text{ ms}$ sobre cargas de 128k tokens (~512 KB).

---

## 3. Pipeline de Evaluación en Dos Fases (L1 Fast Gate & L2 Semantic Router)

1. **L1 Heurístico Determinista (`<= 15ms`):**
   - Redundancia léxica via `zlib` `level=1` (Z_BEST_SPEED).
   - Distancia de Compresión Normalizada (`NCD`) selectiva entre documentos con pre-filtro de longitud ($\Delta L \le 20\%$).
   - Detección de sesgo posicional (*Lost-in-the-Middle*, zona degradada $0.35 \le p \le 0.75$).
   - Detección de volatilidad de prefijo ($p < 0.15$) y churn de KV Cache entre turnos.
   - Detección de deriva de estado de herramientas (*stale tool drift* y referencias a IDs fantasma).
2. **L2 Semántico Condicional:**
   - Invocado únicamente si `l1_verdict.route == GateRoute.FORCE_L2_AUDIT`, `force_semantic=True` o `task_requires_factual=True`.
   - Adaptadores soportados: `AntigravityAdapter` (`agy.exe`), `LocalEndpointAdapter` (Ollama, vLLM, OpenAI-compatible vía `urllib.request`) y `GeminiAdapter`.

---

## 4. Convenciones de Rutas y Seguridad

- **Prohibición de Rutas Absolutas:** Cita siempre rutas relativas a la raíz del repositorio (`./src/...`, `./config/...`) con separador Unix `/`.
- **Seguridad Zero-Trust:** Prohibido persistir o solicitar credenciales o claves de API (`GEMINI_API_KEY`). Utilizar marcadores `<REDACTED>`.
- **Comandos de Verificación:**
  - Suite completa: `python -m pytest -v`
  - Launcher Windows: `.\run_audit.ps1 [-File <path>] [-Model <model>] [-Effort <effort>] [-Interactive]`
  - Launcher POSIX: `./run_audit.sh [-f <path>] [-m <model>] [-e <effort>] [-i]`
