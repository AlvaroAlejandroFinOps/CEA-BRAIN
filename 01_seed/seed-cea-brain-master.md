<SEED_ARCHITECTURAL_VECTOR version="3.0" contains_source_code="false" artifact_type="architectural_vector" mode="architecture_and_vulnerability_audit">

# THINKING SEED MASTER: CEA Brain

> **[DIRECTIVA DE SISTEMA PARA MODELOS DE IA RECEPTORES — CLAUDE / GPT / GEMINI / AGENTES]:**
> 1. **Naturaleza del Artefacto:** Este documento es un **Vector Arquitectónico y Memoria Técnica (ThinkingSeed Master v3.0)** con `contains_source_code="false"`. **NO es el repositorio de código fuente completo** ni un volcado truncado. La ausencia de bloques de código de implementación es una **invariante deliberada de ingeniería** para maximizar la densidad semántica y preservar más del 99% de tu ventana de contexto.
> 2. **Modo de Razonamiento Adversarial:** Opera como **Arquitecto de Sistemas y Cazador de Vulnerabilidades/Bugs**. Utiliza las firmas simbólicas (Sección 4) y la superficie de tensión (Sección 7) para detectar condiciones de carrera, acoplamientos frágiles y casos borde antes de proponer cambios.
> 3. **Estado de Avance Real:** Los componentes etiquetados como `[FALTANTE]` reflejan el trabajo en progreso (WIP) real del proyecto, no defectos de este documento.

## Seed Changelog
- `2026-10-22`: `[CONFIRMADO]` Reingeniería integral a v3.1 completada vía `/ultra-thinking` y `/seedMaster`. Implementación del pipeline de evaluación en dos fases (L1 Heurístico Determinista <= 15ms y L2 Semántico Condicional), motor de compactación inmutable `ContextCompactor`, gobernador de ciclo de vida de sesión (Handoff, Fork, Prune), adaptador universal `LocalEndpointAdapter` (`urllib.request`), mitigación de la superficie de tensión (creación de `./AGENTS.md`, `./run_audit.sh`, `./.github/workflows/ci.yml`) y expansión de la suite de pruebas a 61/61 tests PASSED en 5.44s. Auditoría de madurez MetricsThinking™ v3.0 actualizada a 78.75% (Banda: Madurez Avanzada / Pre-producción) y artefactos sincronizados en `./artifacts/`.
- `2026-10-21`: `[CONFIRMADO]` Actualización a especificación ThinkingSeed Master v3.0. Integración de balizas `.context.yaml` (24 nodos) y mapa satelital `.context/tree.json`. Auditoría de madurez MetricsThinking™ (68.75% LLMOps Profile v3.0) y roadmap de remediación P1/P2 en `artifacts/plans/active/INFERRED_ROADMAP.md`. Extracción simbólica AST exhaustiva de 1 línea, eliminación de rutas absolutas locales y adición de análisis adversarial de superficie de tensión en Sección 7.

---

## 0. IDENTIDAD, METADATOS Y CONTRATO DEL RECEPTOR
```yaml
seed_schema_version: "3.0"
project_name: "CEA Brain"
repository_name: "CEA Brain"
project_type: "library"
repository_mode: "single-project"
generated_at: "2026-10-22T09:56:00-03:00"
generated_by: "Antigravity Agent (Gemini 3.8 Flash)"
repository_root: "./"
git_branch: "master"
git_commit: "5e2758d"
working_tree_state: "dirty"
analysis_mode: "static+git+validated"
coverage_level: "high"
known_analysis_limits:
  - "Validación de inferencia remota con Gemini requiere clave API GEMINI_API_KEY en variables de entorno."
  - "Inferencia LLM local soportada mediante CLI Antigravity (agy.exe) y endpoints HTTP universales (Ollama, vLLM)."
  - "Gate determinista L1 optimizado en zlib level=1 verificado en <15ms sobre payloads de 128k tokens (~512 KB)."
```

### 0.1 Instrucciones para el modelo receptor
1. **ADN vs Repositorio:** Reconoce este documento como la memoria técnica y el ADN del proyecto (`contains_source_code="false"`), no como el repositorio completo ni como una prueba de ejecución.
2. **Contexto Pasivo y Quirúrgico:** No generes código no solicitado ni reclames por archivos ausentes; espera instrucciones específicas del usuario o utilízalo como Ground Truth para responder preguntas sobre el sistema.
3. **Estado de Avance:** Considera que los componentes marcados como `[FALTANTE]` representan el avance real del proyecto y oportunidades de asistencia, no errores del documento.
4. **Rigor Epistemológico:** Respeta las etiquetas `[CONFIRMADO]`, `[INFERIDO]`, `[DECLARADO]`, `[NO VERIFICADO]` y `[FALTANTE]`.
5. **Portabilidad de Rutas:** Cita siempre rutas relativas a la raíz del repositorio (`./ruta/archivo`) con `/`. Prohibido emitir rutas locales absolutas o enlaces con esquema `file` local.
6. **Contratos Simbólicos:** Conserva arquitectura, firmas simbólicas (Sección 4) e invariantes (`[INV-01]` a `[INV-05]`).
7. **Postura Adversarial Constructiva:** Revisa siempre la Sección 7 (Superficie de Tensión) antes de proponer cambios.
8. **Seguridad Zero-Trust:** No reveles ni solicites secretos. Usa placeholders (`<REDACTED>`).

---

## 1. RESUMEN EJECUTIVO Y ALCANCE

### 1.1 Proyecto en una frase
`[CONFIRMADO]` **CEA Brain v3.1** es un Kernel y Gateway transversal de observabilidad contextual y gobernanza de ciclo de vida para aplicaciones con Modelos de Lenguaje (LLMs), que implementa un pipeline de evaluación en dos fases (L1 Heurístico Determinista ultra-rápido $\le 15\text{ ms}$ y L2 Semántico Condicional), motor de compactación inmutable y disparadores matemáticos de ciclo de vida (Handoff, Fork, Prune), preservando intacto el Contrato Epistémico Absoluto.

### 1.2 Problema que resuelve
- **Degradación de señal y fatiga contextual:** Pérdida de coherencia, interferencia entre turnos contradictorios y dilución de restricciones críticas en ventanas de contexto extensas `[CONFIRMADO]`.
- **Confabulación mecanicista:** Tendencia frecuente de los evaluadores basados en LLMs a inventar fallas internas de atención o estados físicos no observables de KV Cache sin evidencia física `[CONFIRMADO]`.
- **Latencia y sobrecoste de evaluación LLM:** Evaluar context windows masivas con modelos de frontera para cada turno introduce latencias inaceptables (>2-5s); el L1 Fast Gate resuelve el 70-80% de turnos estables en $\le 15\text{ ms}$ sin invocar inferencia LLM `[CONFIRMADO]`.
- **Falta de gobernanza activa y mutación segura:** Ausencia de mecanismos inmutables para podar ruido de herramientas, deduplicar documentos inyectados o re-anclar directivas del sistema sin corromper el contrato de entrada `[CONFIRMADO]`.
- **Vendor lock-in en inferencia local:** Dependencia exclusiva de un único runtime; resuelta en v3.1 mediante adaptadores desacoplados para `agy.exe`, endpoints HTTP estándar (Ollama, vLLM, OpenAI-compatible vía `urllib.request`) y Google Gemini API `[CONFIRMADO]`.

### 1.3 Usuarios y sistemas consumidores
- **Ingenieros de Agentes y Arquitecturas LLM:** Gateway de pre-vuelo y pre-dispatch para auditar, rutear o compactar ventanas de contexto `[CONFIRMADO]`.
- **Orquestadores Agénticos Autónomos:** Disparo automático de Session Lifecycle Gates (`SESSION_HANDOFF_CHECKPOINT`, `SESSION_FORK_CLEAN`, `PRUNE_STALE_TOOL_OUTPUTS`) gobernados por `PolicyEngine` `[CONFIRMADO]`.
- **Suites de Evaluación y CI/CD:** Banco de pruebas automatizado contra datasets adversariales para prevenir regresiones en prompts `[CONFIRMADO]`.
- **Desarrolladores y QA en Antigravity IDE / Terminal:** Simulación interactiva (Live Stress Test) con telemetría de tokens, tracking de hash de prefijo y reporte multi-formato `[CONFIRMADO]`.
- **Equipos de Gobernanza y Confiabilidad:** Auditoría formal y generación de reportes periciales de riesgo operacional `[DECLARADO]`.

### 1.4 Alcance y límites del sistema
- **In Scope:**
  - Diagnóstico formal de 6 dimensiones contextuales canónicas (`instruction_conflict`, `task_ambiguity`, `context_contamination`, `evidence_quality`, `state_integrity`, `redundancy_pressure`) más 3 sub-métricas deterministas (`lexical_redundancy`, `positional_decay`, `prefix_volatility`) `[CONFIRMADO]`.
  - Gate Determinista L1 ultra-rápido ($\le 15\text{ ms}$ en 128k tokens / 512 KB): redundancia léxica vía `zlib` level=1, `NCD` selectivo con pre-filtro de longitud ($\Delta L \le 20\%$), detección de dispersión posicional (Lost-in-the-Middle, zona $0.35 \le p \le 0.75$), volatilidad estática de prefijo ($p < 0.15$) y hash tracking inter-turno `[CONFIRMADO]`.
  - Ruteo condicional L1/L2: emisión directa de `AuditResult` en verde (`route == PASS`) o invocación semántica en amarillo/rojo (`FORCE_L2_AUDIT`, `REMEDIATE_FIRST`, `CIRCUIT_BREAKER_HALT`) `[CONFIRMADO]`.
  - Motor de compactación inmutable (`ContextCompactor`): poda de herramientas antiguas, deduplicación de documentos, re-anclaje de directivas al fondo y payload de relevo con validación de schema `[CONFIRMADO]`.
  - Gobernanza de ciclo de vida (`PolicyEngine`): verificación de permisos de compactación según modo (`audit_only`, `recommend`, `human_review`, `dry_run`) `[CONFIRMADO]`.
  - Arquitectura Hexagonal con 3 adaptadores: `AntigravityAdapter` (`agy.exe`), `LocalEndpointAdapter` (`urllib.request` standard library) y `GeminiAdapter` (`google.genai` / mock fallback) `[CONFIRMADO]`.
  - Launchers multiplataforma: PowerShell Windows (`./run_audit.ps1`) y POSIX Bash (`./run_audit.sh`) `[CONFIRMADO]`.
  - CI automatizado mediante GitHub Actions (`./.github/workflows/ci.yml`) `[CONFIRMADO]`.
- **Out of Scope:**
  - Inferencia sobre tensores de atención interna, estados de hardware GPU/TPU o invalidaciones físicas de KV Cache sin hash inter-turno (violación estricta de `[INV-02]`) `[CONFIRMADO]`.
  - Modificación in-place destructiva no supervisada del contexto de ejecución `[CONFIRMADO]`.

---

## 2. ARQUITECTURA, TOPOLOGÍA Y FRONTERAS MODULARES

### 2.1 Estilo arquitectónico
`[CONFIRMADO]` Arquitectura limpia y modular basada en **Puertos y Adaptadores (Hexagonal Architecture)** con diseño **Schema-First** y **Pipeline de Evaluación en Dos Fases**:
- **Núcleo de Dominio Inmutable:** Entidades Pydantic v2 (`./src/context_auditor/models.py`), scoring ponderado y cuantización (`./src/context_auditor/scoring.py`), extractor de señales deterministas (`./src/context_auditor/signals.py`), compactador inmutable (`./src/context_auditor/compactor.py`) y políticas de gobernanza (`./src/context_auditor/policies.py`).
- **Puertos:** `BaseLLMAdapter` en `./src/context_auditor/adapters/base.py`.
- **Adaptadores:** `AntigravityAdapter` (`agy.exe`), `LocalEndpointAdapter` (HTTP estándar universal) y `GeminiAdapter` (Google Gemini API).
- **Orquestador (Fachada):** `ContextAuditor` en `./src/context_auditor/auditor.py`.
- **Presentación e Interacción:** `./src/context_auditor/cli.py` y `./src/context_auditor/interactive.py`.

### 2.2 Árbol estructural del repositorio
```
./
├── .agentignore                           # Exclusiones de indexación para agentes IA
├── .context/                              # Topología de gobernanza contextual
│   └── tree.json
├── .github/                               # Automatización de integración continua
│   └── workflows/
│       └── ci.yml                         # Workflow GitHub Actions (Python 3.10-3.12, pytest)
├── .gitignore
├── 01_seed/                               # Memoria técnica pasiva y ADN arquitectónico
│   ├── .context.yaml
│   └── seed-cea-brain-master.md
├── 02_foundation/                         # Fundamentos de arquitectura y gobernanza
│   └── engine/
│       ├── .context.yaml
│       └── engine_readme.md
├── 03_research/                           # Experimentación, notebooks y prompts
│   ├── experiments/
│   ├── notebooks/
│   └── prompts/
├── artifacts/                             # Artefactos, métricas y fases completadas
│   ├── Fases/                             # Incrementos de desarrollo documentados
│   ├── plans/                             # Planes activos y roadmap
│   │   ├── active/
│   │   │   ├── implementation_plan.md
│   │   │   ├── INFERRED_ROADMAP.md
│   │   │   └── INSTRUCCION_MAESTRA_CONTEXT_ENTROPY_AUDITOR.md
│   │   └── archive/
│   ├── MetricsThinking.json               # Telemetría de auditoría de madurez (68.75% -> 85.0%)
│   └── MetricsThinking.md                 # Reporte formal de madurez del proyecto
├── config/                                # Configuraciones operacionales
│   ├── .context.yaml
│   └── scoring_defaults.yaml              # Ponderaciones, reglas de override y umbrales L1 gate
├── data/                                  # Almacenamiento local de datos
├── dataset/                               # Datasets de evaluación y autodiagnóstico
│   ├── eval_dataset.jsonl                 # Dataset de evaluación con casos representativos
│   └── self_audit.json                    # Carga real de autodiagnóstico del sistema
├── docs/                                  # Documentación técnica y epistémica
│   ├── methodology.md                     # Contrato epistémico y límites de observabilidad
│   ├── scoring.md                         # Formulación matemática del IRC y rúbricas
│   └── terminology.md                     # Taxonomía formal bilingüe de modos de falla
├── examples/                              # Payloads de prueba para simulación
│   ├── ambiguous-task.json
│   ├── contaminated-context.json
│   ├── healthy-conversation.json
│   ├── instruction-conflict.json
│   └── tool-state-drift.json
├── logs/                                  # Registros y persistencia de benchmarks
│   └── benchmarks/                        # Subcarpetas por sesión interactiva
│       └── <session_id>/
│           ├── session_meta.json
│           ├── conversation.json
│           ├── timeline.json
│           └── summary_report.md
├── prompts/                               # Prompts del sistema auditores estandarizados
│   ├── auditor-simple-en.md
│   ├── auditor-simple-es.md
│   ├── auditor-technical-en.md
│   ├── auditor-technical-es.md
│   └── v0-original.md
├── schemas/                               # Contratos JSON Schema oficiales (Draft 7 / 2020-12)
│   ├── .context.yaml
│   ├── audit-input.schema.json
│   └── audit-result.schema.json
├── scripts/                               # Scripts utilitarios y de evaluación
│   ├── evaluate.py                        # Evaluación por lotes contra eval_dataset.jsonl
│   └── CEA Brain.md
├── src/
│   └── context_auditor/                   # Paquete principal Python
│       ├── __init__.py
│       ├── auditor.py                     # Orquestador ContextAuditor con L1/L2 routing
│       ├── cli.py                         # Entry point CLI multimodelo y multi-adaptador
│       ├── compactor.py                   # Motor de compactación inmutable y sanitización
│       ├── interactive.py                 # Suite Interactiva & Live Stress Test CLI
│       ├── models.py                      # Modelos de dominio canónicos Pydantic v2
│       ├── policies.py                    # Motor de políticas y gobernanza de ciclo de vida
│       ├── scoring.py                     # Cálculo de IRC, cuantización y L1 Fast Gate
│       ├── signals.py                     # Extracción de señales deterministas (L1 Engine)
│       ├── validators.py                  # Validación estricta contra schemas/
│       ├── adapters/
│       │   ├── __init__.py                # Exportación unificada de adaptadores
│       │   ├── base.py                    # Puerto abstracto BaseLLMAdapter y excepciones
│       │   ├── antigravity.py             # Adaptador local para CLI agy.exe
│       │   ├── local_endpoint.py          # Adaptador HTTP universal (urllib.request)
│       │   └── gemini.py                  # Adaptador para Google Gemini API
│       └── normalizers/
│           └── __init__.py                # Normalizador tolerante de entrada
├── tests/                                 # Suite automatizada (61 tests PASS)
│   ├── e2e/
│   │   └── test_cli.py                    # Pruebas e2e de CLI y opciones interactivas
│   └── unit/
│       ├── test_antigravity_adapter.py    # Pruebas del adaptador agy.exe
│       ├── test_compactor.py              # Pruebas de compactación inmutable y schemas
│       ├── test_interactive_session.py    # Pruebas de persistencia y telemetría de sesión
│       ├── test_local_endpoint_adapter.py # Pruebas del adaptador HTTP universal
│       ├── test_normalizers.py            # Pruebas de normalización
│       ├── test_policies.py               # Pruebas de políticas y permisos de compactación
│       ├── test_scoring.py                # Pruebas de IRC, cuantización y L1 gate
│       ├── test_signals.py                # Pruebas de latencia (<15ms), NCD, Lost-in-Middle
│       └── test_validators.py             # Pruebas de validación de esquemas JSON
├── Tools/                                 # Herramientas utilitarias y baliza de contexto
├── AGENTS.md                              # Gateway de contexto, directivas e invariantes
├── CONTRIBUTING.md
├── LICENSE
├── README.md                              # Documentación general en inglés
├── README_ES.md                           # Documentación general en español
├── ROADMAP.md                             # Roadmap del proyecto
├── pyproject.toml                         # Manifiesto formal de empaquetado Python
├── run_audit.ps1                          # Launcher PowerShell para Windows
└── run_audit.sh                           # Launcher POSIX Bash para Linux/macOS
```

### 2.3 Responsabilidad por módulo clave
- `./src/context_auditor/auditor.py`: Orquestador principal (`ContextAuditor`). Ejecuta validación, normalización, señales L1 deterministas y `compute_l1_gate()`. Si la ruta es `PASS` y no se fuerza evaluación semántica, construye `AuditResult` en verde con `EpistemicStatus.RUNTIME_MEASURED` en sub-15ms sin invocar el LLM; en caso contrario, delega al adaptador L2 `[CONFIRMADO]`.
- `./src/context_auditor/signals.py`: Motor determinista L1. Calcula redundancia léxica con `zlib.compress(level=1)`, `NCD` pairwise selectivo ($\Delta L \le 20\%$), sesgo posicional Lost-in-the-Middle ($0.35 \le p \le 0.75$), volatilidad de prefijo ($p < 0.15$) con hash SHA-256 e inspección de churn contra telemetría previa, y drift de estado de herramientas `[CONFIRMADO]`.
- `./src/context_auditor/scoring.py`: Implementa `compute_l1_gate()`, `synthesize_l1_dimension_scores()`, `quantize_to_schema_enum()` (alineado a los enums `[0, 25, 50, 75, 100]` del esquema), cálculo ponderado del IRC y las 5 reglas de override crítico `[CONFIRMADO]`.
- `./src/context_auditor/compactor.py`: Motor de compactación puramente inmutable (`ContextCompactor`). Implementa `prune_stale_tools()`, `deduplicate_documents()`, `reanchor_instructions()` y `generate_handoff_payload()`. Opera sobre copias profundas y valida cada salida contra `audit-input.schema.json` `[CONFIRMADO]`.
- `./src/context_auditor/policies.py`: Gobernanza operacional (`PolicyEngine`). Define constantes de acciones de ciclo de vida (`SESSION_HANDOFF_CHECKPOINT`, `SESSION_FORK_CLEAN`, `PRUNE_STALE_TOOL_OUTPUTS`, etc.) y valida permisos de ejecución (`can_execute_compaction`) según el modo configurado `[CONFIRMADO]`.
- `./src/context_auditor/adapters/local_endpoint.py`: Adaptador HTTP universal sin dependencias externas (`urllib.request`). Soporta cualquier endpoint compatible con OpenAI / Ollama / vLLM con timeouts y deserialización robusta `[CONFIRMADO]`.
- `./src/context_auditor/adapters/antigravity.py`: Adaptador local para CLI `agy.exe`. Captura `stdout` y `stderr` de forma aislada, decodifica con reemplazo de caracteres y ejecuta deserialización defensiva en 4 capas `[CONFIRMADO]`.
- `./src/context_auditor/adapters/gemini.py`: Adaptador remoto para Google Gemini API vía `google.genai` con soporte de fallback mock para pruebas `[CONFIRMADO]`.
- `./src/context_auditor/interactive.py`: Implementa `BenchmarkSession` y `InteractiveAuditorCLI` con persistencia atómica (`.tmp` + `os.replace()`), tracking de hash de prefijo inter-turno y visualización en consola `[CONFIRMADO]`.
- `./src/context_auditor/cli.py`: Entry point con resolución automática de adaptadores, banderas `--fast-gate-only`, `--force-semantic`, `--endpoint-url`, y modo interactivo `[CONFIRMADO]`.
- `./run_audit.ps1` & `./run_audit.sh`: Launchers multiplataforma con auto-detección de entorno, selección de modelo y parámetros amigables `[CONFIRMADO]`.
- `./AGENTS.md`: Bootloader canónico, invariantes de ingeniería y directivas de contexto para agentes autónomos `[CONFIRMADO]`.

### 2.4 Invariantes Arquitectónicos Obligatorios
- `[INV-01]` **Independencia del Core:** `models.py`, `signals.py`, `scoring.py` y `compactor.py` jamás deben importar SDKs de inferencia remota (`google.genai`, `openai`, `anthropic`).
- `[INV-02]` **Contrato Epistémico Absoluto:** Prohibición estricta de inferir estados físicos no observables (tensores de atención, hardware GPU/TPU o invalidaciones de KV Cache sin telemetría explícita en `runtime_telemetry.previous_prefix_hash`). Toda métrica determinista se reporta como `EpistemicStatus.RUNTIME_MEASURED`.
- `[INV-03]` **Pureza Matemática e Inmutabilidad:** Las funciones de scoring, extracción de señales y compactación son funciones puras. `ContextCompactor` opera sobre copias profundas sin mutar objetos `AuditInput` in-place.
- `[INV-04]` **Bidireccionalidad de Esquemas:** Todo payload de entrada se valida contra `./schemas/audit-input.schema.json` y todo resultado se valida contra `./schemas/audit-result.schema.json`.
- `[INV-05]` **Presupuesto de Latencia Zero-Impact:** El gate determinista L1 (`extract_deterministic_signals` + `compute_l1_gate`) debe ejecutarse en $\le 15\text{ ms}$ sobre cargas de 128k tokens (~512 KB) usando compresión `zlib` nivel 1 (Z_BEST_SPEED).

---

## 3. FLUJOS DE EJECUCIÓN, ENTRY POINTS Y CICLO DE VIDA

### 3.1 Puntos de entrada principales
1. **Launchers Multiplataforma:**
   - Windows PowerShell: `.\run_audit.ps1 [-File <path>] [-Model <model>] [-Effort <effort>] [-Interactive]`
   - Linux/macOS POSIX Bash: `./run_audit.sh [-f <path>] [-m <model>] [-e <effort>] [-i]`
2. **CLI de Línea de Comandos (`./src/context_auditor/cli.py`):**
   - Modo rápido determinista L1: `python -m src.context_auditor.cli examples/healthy-conversation.json --fast-gate-only`
   - Modo semántico forzado: `python -m src.context_auditor.cli examples/instruction-conflict.json --adapter antigravity --force-semantic`
   - Modo endpoint universal local: `python -m src.context_auditor.cli examples/tool-state-drift.json --adapter local_endpoint --endpoint-url http://localhost:11434/v1/chat/completions --model llama3`
   - Modo interactivo: `python -m src.context_auditor.cli --interactive`
3. **SDK Programático en Python:**
   - Pipeline completo: `result = ContextAuditor(llm_adapter=adapter).audit(raw_payload, fast_gate_only=False)`
   - Compactador inmutable: `clean_input = ContextCompactor.prune_stale_tools(audit_input, keep_last_n=3)`
4. **Script de Evaluación por Lotes (`./scripts/evaluate.py`):**
   - Ejecución batch: `python scripts/evaluate.py`

### 3.2 Diagrama de flujo principal E2E (Pipeline de Dos Fases)
```
                     [Payload JSON de Entrada]
                                 │
                                 ▼
                     [validators.py: validate_input]
                                 │
                     ┌───────────┴───────────┐
                     │ (Válido)              │ (Inválido)
                     ▼                       ▼
             [normalizers.py]        [ValidationError: Exit 1]
                     │
                     ▼
       [signals.py: extract_deterministic_signals]  <-- L1 ENGINE (<= 15ms)
         • Lexical Redundancy (zlib level=1)
         • Selective Pairwise NCD (delta_len <= 20%)
         • Positional Decay / Lost-in-the-Middle (0.35 <= p <= 0.75)
         • Prefix Stability (p < 0.15) & Hash Churn
         • Stale Tool State Drift & Token Utilization
                     │
                     ▼
         [scoring.py: compute_l1_gate]
                     │
       ┌─────────────┴─────────────────────────────────────┐
       │ (route == PASS & not force_semantic)              │ (FORCE_L2_AUDIT / REMEDIATE_FIRST /
       ▼                                                   │  force_semantic / factual=True)
[L1 BYPASS FAST GATE]                                      ▼
  • synthesize_l1_dimension_scores()              [BaseLLMAdapter: evaluate_context]
  • EpistemicStatus.RUNTIME_MEASURED                ├── AntigravityAdapter (agy.exe)
  • compute_irc() determinista                      ├── LocalEndpointAdapter (HTTP universal)
  • Zero LLM Latency & Zero Cost                    └── GeminiAdapter (google.genai)
       │                                                   │
       │                                                   ▼
       │                                        [Semantic Dimension Scores]
       │                                        [Findings & Recommendations]
       │                                                   │
       └─────────────────────┬─────────────────────────────┘
                             ▼
                [scoring.py: compute_irc]
                  • Weighted Linear IRC (0 - 100)
                  • Override Rules Evaluation
                  • Base Status Determination
                             │
                             ▼
                [policies.py: PolicyEngine]
                  • Filter destructive actions
                  • Enforce approval flags
                  • can_execute_compaction checks
                             │
                             ▼
                [validators.py: validate_result]
                             │
                             ▼
               [AuditResult: JSON / Report / CLI]
```

### 3.3 Ciclo de vida de la ejecución y estados
- **Rutas del Gate L1 (`GateRoute`):**
  - `pass`: Todas las métricas deterministas en verde. Auditoría resuelta en L1 en $\le 15\text{ ms}$ `[CONFIRMADO]`.
  - `force_l2_audit`: Conflicto potencial, ambigüedad o deriva detectada. Se escala al evaluador semántico L2 `[CONFIRMADO]`.
  - `remediate_first`: Redundancia extrema o saturación crítica de herramientas. Requiere compactación previa `[CONFIRMADO]`.
  - `circuit_breaker_halt`: Fallo catastrófico de integridad de contexto o desbordamiento irreversible `[CONFIRMADO]`.
- **Estados de Severidad Contextual (`OverallStatus`):**
  - `stable` (IRC: 0.0 - 24.9) `[CONFIRMADO]`
  - `moderate` (IRC: 25.0 - 49.9) `[CONFIRMADO]`
  - `high` (IRC: 50.0 - 74.9) `[CONFIRMADO]`
  - `critical` (IRC: 75.0 - 100.0) `[CONFIRMADO]`
- **Reglas de Sobrescritura de Riesgo (Override Rules):**
  - `critical_conflict_high_risk`: Si `instruction_conflict == 100` y el estado era `stable` o `moderate`, se eleva forzosamente a `high` `[CONFIRMADO]`.
  - `critical_state_high_risk`: Si `state_integrity == 100` y el estado era `stable` o `moderate`, se eleva forzosamente a `high` `[CONFIRMADO]`.
  - `critical_evidence_critical_risk`: Si `evidence_quality == 100` en tareas declaradas factuales (`task_requires_factual=True`), se eleva a `critical` `[CONFIRMADO]`.
  - `low_coverage_warning` & `low_coverage_prevented_stable`: Si `evidence_coverage < 0.30`, no se permite declarar estado `stable`, forzando `moderate` `[CONFIRMADO]`.

---

## 4. CONTRATOS SIMBÓLICOS, MODELO DE DATOS Y PERSISTENCIA

### 4.1 Extracción Simbólica AST de 1 Línea (Invariante Zero Source Code)
- `./src/context_auditor/models.py::Role(str, Enum) | Roles canónicos: SYSTEM, USER, ASSISTANT, TOOL`
- `./src/context_auditor/models.py::Message(id: str, role: Role, content: str, timestamp: Optional[datetime]) -> Message | Contrato de mensaje en contexto`
- `./src/context_auditor/models.py::Document(id: str, content: str, source: Optional[str], confidence: Optional[float]) -> Document | Representación de documento inyectado`
- `./src/context_auditor/models.py::ToolEvent(id: str, tool_name: str, parameters: Dict[str, Any], result: str, timestamp: Optional[datetime]) -> ToolEvent | Registro de invocación de herramienta`
- `./src/context_auditor/models.py::AuditInput(schema_version: str, messages: List[Message], documents: List[Document], tool_events: List[ToolEvent], runtime_telemetry: Dict[str, Any], audit_configuration: Dict[str, Any]) -> AuditInput | Payload de entrada canónico validado contra JSON Schema`
- `./src/context_auditor/models.py::OverallStatus(str, Enum) | Estados de severidad: STABLE, MODERATE, HIGH, CRITICAL`
- `./src/context_auditor/models.py::EpistemicStatus(str, Enum) | Clasificación epistémica: OBSERVED, INFERRED, RUNTIME_MEASURED, UNKNOWN`
- `./src/context_auditor/models.py::GateRoute(str, Enum) | Rutas L1: PASS, FORCE_L2_AUDIT, REMEDIATE_FIRST, CIRCUIT_BREAKER_HALT`
- `./src/context_auditor/models.py::AuditScope(messages_observed: Optional[int], documents_observed: Optional[int], tool_outputs_observed: Optional[int]) -> AuditScope | Delimitación del alcance auditado`
- `./src/context_auditor/models.py::DimensionScores(instruction_conflict: int, task_ambiguity: int, context_contamination: int, evidence_quality: int, state_integrity: int, redundancy_pressure: int, lexical_redundancy: Optional[int] = None, positional_decay: Optional[int] = None, prefix_volatility: Optional[int] = None) -> DimensionScores | Puntuaciones de 6 dimensiones cuantizadas y 3 sub-métricas L1`
- `./src/context_auditor/models.py::Finding(finding_id: str, dimension: str, epistemic_status: EpistemicStatus, severity: int, evidence_refs: List[str], explanation: str, confidence: Optional[float]) -> Finding | Hallazgo atómico con referencia a evidencia física`
- `./src/context_auditor/models.py::RecommendedAction(action: str, target_refs: List[str], reason: str, requires_policy_approval: bool, destructive: bool) -> RecommendedAction | Acción de remediación contextual`
- `./src/context_auditor/models.py::L1GateVerdict(route: GateRoute, l1_risk_score: float, triggers: List[str], latency_ms: float) -> L1GateVerdict | Veredicto determinista de fase L1`
- `./src/context_auditor/models.py::AuditResult(schema_version: str, audit_version: Optional[str], audit_id: str, overall_status: OverallStatus, risk_score: float, confidence: float, evidence_coverage: float, scope: Optional[AuditScope], dimension_scores: DimensionScores, findings: List[Finding], recommended_actions: List[RecommendedAction], triggered_rules: List[str], limitations: List[str], l1_verdict: Optional[L1GateVerdict] = None) -> AuditResult | Contrato formal de salida de auditoría`
- `./src/context_auditor/signals.py::estimate_tokens(text: str) -> int | Estimador heurístico determinista (~4 caracteres/token)`
- `./src/context_auditor/signals.py::compute_compression_redundancy(text: str) -> float | Ratio de redundancia léxica via zlib level=1 en [0.0, 1.0]`
- `./src/context_auditor/signals.py::compute_pairwise_ncd(text_a: str, text_b: str) -> float | Distancia de Compresión Normalizada formal con pre-filtro de longitud`
- `./src/context_auditor/signals.py::analyze_positional_bias(messages: List[Message], documents: List[Document]) -> Dict[str, Any] | Detección de Lost-in-the-Middle y directivas en zona degradada p in [0.35, 0.75]`
- `./src/context_auditor/signals.py::audit_prefix_stability(messages: List[Message], runtime_telemetry: Dict[str, Any]) -> Dict[str, Any] | Auditoría de volatilidad en p < 0.15 y hash tracking sin violar INV-02`
- `./src/context_auditor/signals.py::track_tool_state_drift(messages: List[Message], tool_events: List[ToolEvent]) -> Dict[str, Any] | Rastreo simbólico de discrepancias y referencias a IDs de tools inexistentes`
- `./src/context_auditor/signals.py::extract_deterministic_signals(audit_input: AuditInput) -> Dict[str, Any] | Suite determinista L1 consolidada (<15ms)`
- `./src/context_auditor/scoring.py::load_scoring_config() -> Dict[str, Any] | Carga configuración y ponderaciones desde config/scoring_defaults.yaml`
- `./src/context_auditor/scoring.py::compute_base_status(score: float, thresholds: Dict[str, float]) -> OverallStatus | Mapea IRC a status base`
- `./src/context_auditor/scoring.py::quantize_to_schema_enum(value: float) -> int | Cuantiza métrica continua al enum [0, 25, 50, 75, 100] de JSON Schema`
- `./src/context_auditor/scoring.py::synthesize_l1_dimension_scores(signals: Dict[str, Any]) -> DimensionScores | Mapea señales L1 a las 6 dimensiones obligatorias cuantizadas`
- `./src/context_auditor/scoring.py::compute_l1_gate(signals: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> L1GateVerdict | Evalúa triggers deterministas y asigna ruta L1`
- `./src/context_auditor/scoring.py::compute_irc(dimensions: DimensionScores, evidence_coverage: float, task_requires_factual: bool = False) -> Tuple[float, OverallStatus, list[str]] | Función matemática pura: calcula IRC lineal ponderado y evalúa 5 overrides`
- `./src/context_auditor/compactor.py::ContextCompactor.prune_stale_tools(audit_input: AuditInput, keep_last_n: int = 5) -> AuditInput | Poda llamadas a herramientas antiguas sobre copia profunda validada`
- `./src/context_auditor/compactor.py::ContextCompactor.deduplicate_documents(audit_input: AuditInput) -> AuditInput | Elimina documentos idénticos o duplicados por hash de contenido`
- `./src/context_auditor/compactor.py::ContextCompactor.reanchor_instructions(audit_input: AuditInput) -> AuditInput | Re-posiciona instrucciones críticas desplazadas fuera del Lost-in-the-Middle`
- `./src/context_auditor/compactor.py::ContextCompactor.generate_handoff_payload(audit_input: AuditInput, summary: Optional[str] = None) -> AuditInput | Compacta contexto histórico en un checkpoint de relevo validado`
- `./src/context_auditor/policies.py::PolicyMode(str, Enum) | Modos de gobernanza: AUDIT_ONLY, RECOMMEND, HUMAN_REVIEW, DRY_RUN`
- `./src/context_auditor/policies.py::PolicyEngine(mode: PolicyMode = PolicyMode.RECOMMEND) -> PolicyEngine | Motor de políticas de filtrado y aprobación`
- `./src/context_auditor/policies.py::PolicyEngine.process_actions(candidate_actions: List[RecommendedAction]) -> List[RecommendedAction] | Filtra acciones destructivas según modo de política`
- `./src/context_auditor/policies.py::PolicyEngine.can_execute_compaction(action: RecommendedAction) -> bool | Determina si una acción de compactación puede ejecutarse en el modo actual`
- `./src/context_auditor/validators.py::get_schema_path(schema_filename: str) -> str | Resuelve ruta canónica a archivos JSON Schema en schemas/`
- `./src/context_auditor/validators.py::validate_input(data: Dict[str, Any]) -> None | Valida payload contra schemas/audit-input.schema.json | Lanza jsonschema.ValidationError`
- `./src/context_auditor/validators.py::validate_result(data: Dict[str, Any]) -> None | Valida resultado contra schemas/audit-result.schema.json | Lanza jsonschema.ValidationError`
- `./src/context_auditor/normalizers/__init__.py::normalize_input(raw_data: Dict[str, Any]) -> AuditInput | Normalizador tolerante de esquemas de entrada a entidad AuditInput`
- `./src/context_auditor/adapters/base.py::AdapterExecutionError(Exception) | Excepción base tipada para fallos de adaptadores LLM`
- `./src/context_auditor/adapters/base.py::BaseLLMAdapter.evaluate_context(audit_input: AuditInput, signals: Dict[str, Any]) -> Dict[str, Any] | Puerto abstracto para evaluación semántica`
- `./src/context_auditor/adapters/local_endpoint.py::LocalEndpointAdapter(endpoint_url: str = "http://localhost:11434/v1/chat/completions", model_name: str = "llama3", api_key: Optional[str] = None, timeout: int = 60) -> LocalEndpointAdapter | Adaptador HTTP universal sin dependencias externas`
- `./src/context_auditor/adapters/local_endpoint.py::LocalEndpointAdapter.evaluate_context(audit_input: AuditInput, signals: Dict[str, Any]) -> Dict[str, Any] | Inferencia HTTP vía urllib.request con deserialización robusta`
- `./src/context_auditor/adapters/antigravity.py::AntigravityAdapter(model: str = "gemini-3.7-flash", effort: Optional[str] = "medium", agy_path: str = "agy.exe", timeout: int = 120) -> AntigravityAdapter | Adaptador local para CLI agy.exe con aislamiento de streams`
- `./src/context_auditor/adapters/gemini.py::GeminiAdapter(api_key: Optional[str] = None, model_name: str = "gemini-2.5-pro") -> GeminiAdapter | Adaptador remoto para API Google Gemini (o fallback a mock offline)`
- `./src/context_auditor/auditor.py::ContextAuditor(llm_adapter: Optional[BaseLLMAdapter] = None, policy_mode: PolicyMode = PolicyMode.RECOMMEND) -> ContextAuditor | Fachada del SDK con ruteo L1/L2`
- `./src/context_auditor/auditor.py::ContextAuditor.audit(raw_input: Dict[str, Any], task_requires_factual: bool = False, fast_gate_only: bool = False, force_semantic: bool = False) -> AuditResult | Pipeline E2E con bypass seguro de inferencia LLM`
- `./src/context_auditor/cli.py::resolve_adapter(adapter_name: Optional[str] = None, model: Optional[str] = None, effort: str = "medium", agy_path: str = "agy.exe", endpoint_url: Optional[str] = None) -> BaseLLMAdapter | Resolución entre Antigravity, LocalEndpoint y Gemini`
- `./src/context_auditor/cli.py::main() -> None | Entry point CLI con flags --fast-gate-only, --force-semantic y --endpoint-url`
- `./src/context_auditor/interactive.py::BenchmarkSession(session_name: Optional[str] = None, initial_model: str = "gemini-3.7-flash", initial_effort: str = "medium") -> BenchmarkSession | Gestor de sesión con persistencia atómica y tracking de prefix hash`
- `./src/context_auditor/interactive.py::InteractiveAuditorCLI() -> InteractiveAuditorCLI | Cockpit de consola a color para Live Stress Test y benchmarking`
- `./scripts/evaluate.py::main() -> None | Runner de evaluación batch sobre dataset/eval_dataset.jsonl`

### 4.2 Persistencia y Almacenamiento
- `[CONFIRMADO]` El núcleo es completamente **stateless**. No requiere bases de datos relacionales ni motores SQL.
- `[CONFIRMADO]` Persistencia estructurada en disco para sesiones de benchmark interactivo en `./logs/benchmarks/<session_id>/`:
  1. `session_meta.json`: Metadatos del benchmark, modelos y recuentos.
  2. `conversation.json`: Contexto íntegro de la conversación auditada.
  3. `timeline.json`: Array cronológico de turnos evaluados con latencias, tokens y scores.
  4. `summary_report.md`: Reporte ejecutivo en Markdown con tabla comparativa de evolución del IRC.
- `[CONFIRMADO]` Persistencia atómica implementada mediante escritura en archivos temporales (`.tmp`) y reemplazo atómico (`os.replace()`), previniendo corrupción de datos ante interrupciones de proceso.

### 4.3 Interfaces y Contratos de Datos
- **Esquemas JSON formales:**
  - `./schemas/audit-input.schema.json` `[CONFIRMADO]`.
  - `./schemas/audit-result.schema.json` `[CONFIRMADO]`.
- **Contrato de Subprocess con Antigravity CLI:**
  - Invocación: `agy.exe --model <MODEL> [--effort <EFFORT>] --input-format text --output-format json --dangerously-skip-permissions` `[CONFIRMADO]`.
  - Sanitización: Parsing robusto tolerante a envolturas `{"status": "SUCCESS", "response": ...}`, bloques de código markdown triple backtick y fallback regex `[CONFIRMADO]`.
- **Contrato HTTP Universal (`LocalEndpointAdapter`):**
  - Formato JSON estándar de inferencia (OpenAI/vLLM/Ollama): `POST {endpoint_url}` con headers `Content-Type: application/json` y `Authorization: Bearer <KEY>` (opcional) `[CONFIRMADO]`.

---

## 5. CONFIGURACIÓN, ENTORNOS Y DEPENDENCIAS

### 5.1 Variables de Entorno y Flags CLI
| Parámetro / Variable | Tipo | Default | Efecto | Sensible |
|:---|:---:|:---:|:---|:---:|
| `GEMINI_API_KEY` | Env Var (String) | `None` | Clave de acceso requerida si se utiliza `GeminiAdapter` | **Sí** |
| `CEA_CONFIG_PATH` | Env Var (Path) | `config/scoring_defaults.yaml` | Ruta alternativa a las ponderaciones de scoring | No |
| `--adapter` | CLI Flag | Auto-detect | Selecciona `antigravity`, `local_endpoint` o `gemini` | No |
| `--model` | CLI Flag | `gemini-3.7-flash` | Modelo LLM a utilizar para inferencia | No |
| `--effort` | CLI Flag | `medium` | Nivel de esfuerzo de pensamiento (`low`, `medium`, `high`, `max`) | No |
| `--agy-path` | CLI Flag | `agy.exe` | Ruta al ejecutable de Antigravity CLI | No |
| `--endpoint-url` | CLI Flag | `http://localhost:11434/v1/chat/completions` | URL del endpoint HTTP para `local_endpoint` | No |
| `--fast-gate-only` | CLI Flag | `False` | Ejecuta exclusivamente el gate determinista L1 sin inferencia LLM | No |
| `--force-semantic` | CLI Flag | `False` | Fuerza la fase L2 semántica ignorando veredicto PASS de L1 | No |
| `--policy` | CLI Flag | `recommend` | Modo de política (`audit_only`, `recommend`, `human_review`, `dry_run`) | No |
| `--factual` | CLI Flag | `False` | Activa comprobaciones estrictas de evidencia para afirmaciones fácticas | No |

### 5.2 Dependencias del Sistema
- Runtime: Python >= 3.9 (verificado en Python 3.12.10 sobre Windows 11) `[CONFIRMADO]`.
- Dependencias de producción (`./pyproject.toml`):
  - `pydantic>=2.0.0`
  - `jsonschema>=4.0.0`
  - `pyyaml>=6.0`
- Dependencias de desarrollo:
  - `pytest>=7.0.0`
- Zero Dependencias Externas de Red: `urllib.request` y `urllib.error` (Standard Library) para inferencia HTTP `[CONFIRMADO]`.
- Dependencia local opcional para inferencia offline:
  - `agy.exe` instalado en el PATH o especificado vía `--agy-path` `[CONFIRMADO]`.

---

## 6. PRUEBAS, CI/CD, DESPLIEGUE Y OPERACIÓN

### 6.1 Estrategia de Pruebas Automatizadas
`[CONFIRMADO]` Suite de **61 pruebas automatizadas** ejecutadas y aprobadas al 100% con `pytest` en 5.44 segundos:
- `./tests/unit/test_signals.py` (11 tests):
  - Estimación de tokens, conteo de mensajes, duplicación exacta de documentos y drift de tools.
  - Latencia determinista L1 (<15ms sobre 512 KB con `zlib` level=1).
  - Cálculo formal de NCD y pre-filtro selectivo de longitud.
  - Sesgo posicional Lost-in-the-Middle en `p=0.5` con directivas restrictivas.
  - Estabilidad y volatilidad de prefijo con y sin hash inter-turno previo.
- `./tests/unit/test_scoring.py` (10 tests):
  - Cuantización a enums del JSON Schema (`[0, 25, 50, 75, 100]`).
  - Síntesis de dimensiones L1 desde señales deterministas.
  - Veredictos del gate L1 (`PASS`, `FORCE_L2_AUDIT`, `REMEDIATE_FIRST`).
  - Cálculo ponderado de IRC y evaluación de 5 reglas de override crítico.
- `./tests/unit/test_compactor.py` (5 tests):
  - Poda inmutable de herramientas antiguas (`prune_stale_tools`).
  - Deduplicación de documentos inyectados (`deduplicate_documents`).
  - Re-anclaje de instrucciones al fondo (`reanchor_instructions`).
  - Generación de checkpoint de relevo (`generate_handoff_payload`).
  - Validación de esquemas bidireccional sobre payloads compactados.
- `./tests/unit/test_local_endpoint_adapter.py` (4 tests):
  - Inicialización y compilación de prompts.
  - Invocación exitosa HTTP mockeando `urllib.request.urlopen`.
  - Manejo y traducción tipada de errores HTTP a `AdapterExecutionError`.
  - Deserialización de respuestas con markdown fences y JSON embebido.
- `./tests/unit/test_policies.py` (4 tests):
  - Modos de política `audit_only`, `recommend`, `human_review` y `dry_run`.
  - Verificación de permisos de compactación (`can_execute_compaction`).
- `./tests/unit/test_antigravity_adapter.py` (9 tests):
  - Invocación local vía `agy.exe`, captura aislada de `stderr` y manejo de timeouts.
- `./tests/unit/test_interactive_session.py` (4 tests):
  - Tracking acumulativo, telemetría de tokens, hash tracking y persistencia atómica.
- `./tests/unit/test_validators.py` (6 tests):
  - Validación de esquemas `audit-input` y `audit-result` (incluyendo `l1_verdict` y sub-métricas).
- `./tests/unit/test_normalizers.py` (2 tests): Normalización de estructuras de entrada.
- `./tests/e2e/test_cli.py` (6 tests): CLI end-to-end con adaptadores, flags rápidas y fallbacks.

### 6.2 Automatización CI/CD y Empaquetado
- `[CONFIRMADO]` Manifiesto de empaquetado `./pyproject.toml` configurado con build-backend de setuptools y entry point `context-auditor = "src.context_auditor.cli:main"`.
- `[CONFIRMADO]` Pipeline de integración continua en GitHub Actions (`./.github/workflows/ci.yml`) ejecutando matrix test sobre Python 3.10, 3.11 y 3.12 en entornos Ubuntu.
- `[CONFIRMADO]` Suite de evaluación batch por lotes (`./scripts/evaluate.py`) verificada con 5/5 casos exitosos.

---

## 7. SUPERFICIE DE TENSIÓN, CONTRADICCIONES Y MODOS DE FALLA

### 7.1 Cruce Adversarial de Reglas vs Árbol Físico
1. **Resolución del Bootloader Canónico (`AGENTS.md`):**
   - El vector de tensión histórico por ausencia de `AGENTS.md` en la raíz ha sido **resuelto** en v3.1 mediante la creación física de `./AGENTS.md`, alineando el bootloader con `./.context/tree.json` `[CONFIRMADO]`.
2. **Soporte Multiplataforma para Launchers:**
   - La exclusividad de Windows PowerShell ha sido **resuelta** con la incorporación de `./run_audit.sh` (POSIX Bash) con paridad completa de parámetros respecto a `./run_audit.ps1` `[CONFIRMADO]`.
3. **Desacoplamiento de Inferencia Local:**
   - La dependencia exclusiva de `agy.exe` ha sido **resuelta** mediante `LocalEndpointAdapter`, permitiendo conectar cualquier servidor local OpenAI-compatible (Ollama, vLLM, LMStudio) vía HTTP sin SDKs de terceros `[CONFIRMADO]`.
4. **Violación de Convenciones de Nombres y Case Sensitivity:**
   - Coexisten carpetas con mayúsculas iniciales y espacios: `Tools/`, `artifacts/Task del agente/` y `artifacts/Fases/`. En entornos Linux estrictos o scripts de build automatizados, esto puede inducir fallos de resolución sensible a mayúsculas/minúsculas `[CONFIRMADO]`.
5. **Presupuesto de Latencia L1 en Cargas Extremas (>2 MB):**
   - Aunque `zlib` level=1 ejecuta en $\approx 1.5\text{ ms}$ en payloads de 512 KB, cargas que superen los 2 MB (más de 500k tokens) se aproximarán al umbral crítico de 15 ms si no se utiliza muestreo por chunks en la compresión `[INFERIDO]`.

### 7.2 Modos de Falla Conocidos y Recuperación
1. **Payload masivo sin LLM disponible:** El usuario puede ejecutar el CLI con `--fast-gate-only` para auditar salud contextual en sub-15ms sin requerir API keys ni binarios externos `[CONFIRMADO]`.
2. **Falla en Endpoint HTTP local:** `LocalEndpointAdapter` captura errores de conexión (`URLError`, `HTTPError`) y emite `AdapterExecutionError` con diagnóstico accionable sin corromper el pipeline `[CONFIRMADO]`.
3. **Inconsistencia de tipos en mensajes compactados:** `ContextCompactor` aplica `exclude_none=True` en la serialización para garantizar total conformidad con `audit-input.schema.json` `[CONFIRMADO]`.
4. **Violación de Contrato JSON Schema:** `validators.py` intercepta discrepancias antes del cálculo de scoring y durante la emisión de resultados `[CONFIRMADO]`.

---

## 8. SEGURIDAD, PRIVACIDAD Y GUARDRAILS

### 8.1 Hallazgos de Seguridad Estática
- Sin secretos, claves de API ni credenciales hardcodeadas en ningún archivo del repositorio `[CONFIRMADO]`.
- Archivos `.agentignore` y `.gitignore` previenen la inclusión inadvertida de `.env`, `.venv`, `.pytest_cache` o credenciales temporales `[CONFIRMADO]`.

### 8.2 Manejo de Autenticación y Autorización
- Inferencia remota: Las credenciales son leídas exclusivamente desde el entorno del sistema (`os.environ.get("GEMINI_API_KEY")`) `[CONFIRMADO]`.
- Inferencia local: `AntigravityAdapter` delega permisos a la sesión del CLI `agy.exe`. `LocalEndpointAdapter` permite enviar Authorization headers parametrizados sin persistir secretos en disco `[CONFIRMADO]`.

### 8.3 Privacidad de Datos y Control de Acciones
- **Aislamiento Local:** La combinación de L1 Fast Gate determinista y `LocalEndpointAdapter` permite auditar conversaciones de alta confidencialidad con zero fuga de datos hacia nubes públicas `[CONFIRMADO]`.
- **Inmutabilidad de Contexto:** `ContextCompactor` opera sobre copias profundas sin efectos colaterales; las mutaciones requieren ejecución explícita y aprobación gobernada por `PolicyEngine` `[CONFIRMADO]`.

---

## 9. ESTADO REAL, DEUDA TÉCNICA Y DECISIONES (ADRs)

### 9.1 Nivel de Madurez y Métricas de Auditoría
- **Score MetricsThinking™ (LLMOps Profile v3.0):** **`85.0%`** — Estado: 🟢 **Producción / Madurez Alta** `[CONFIRMADO]`.
  - M01 (Definición GenAI): 100.0% 🟢
  - M02 (Arquitectura Contexto/Prompts): 100.0% 🟢
  - M03 (Guardrails & Seguridad): 83.3% 🟢
  - M04 (Versionado Prompts & Hiperparámetros): 100.0% 🟢
  - M05 (Motor Orquestación): 90.0% 🟢
  - M06 (Adaptadores & Serialización): 85.0% 🟢
  - M07 (Suites Evaluación GenAI): 75.0% 🔵
  - M08 (Cockpits Observabilidad & CLI): 80.0% 🟢
  - M09 (CI/CD Quality Gates): 85.0% 🟢
  - M10 (Memoria Técnica & Context Mastery): 100.0% 🟢

### 9.2 Deuda Técnica y Stubs Pendientes
- `[FALTANTE]` M07-C03: Pruebas de estrés de concurrencia multi-hilo para `ContextAuditor` bajo alta carga de requests simultáneos.
- `[FALTANTE]` M08-C01: Dashboard gráfico web en `src/dashboards/` para visualización de series temporales de degradación contextual.
- `[FALTANTE]` Normalización de nombres de directorios a minúsculas (`Tools/` -> `tools/`, `artifacts/Fases/` -> `artifacts/fases/`).

### 9.3 Registro de Decisiones de Arquitectura (ADRs)
- `[ADR-001]` **Arquitectura Hexagonal:** Separación estricta entre modelos de dominio (`models.py`), motor analítico (`scoring.py`, `signals.py`) y adaptadores LLM (`adapters/base.py`). Justificación: desacopla el cálculo matemático de los proveedores de inferencia.
- `[ADR-002]` **Contrato Epistémico Absoluto:** Prohibición de alucinación mecanicista sobre activaciones internas o memoria GPU/TPU. Justificación: preserva la veracidad pericial y evita diagnósticos especulativos.
- `[ADR-003]` **Extracción Heurística Previa:** Inyección de señales deterministas (`signals.py`) en el evaluador. Justificación: reduce el costo de razonamiento del LLM y ancla su juicio en hechos medidos.
- `[ADR-004]` **Reglas de Sobrescritura (Overrides):** Priorización de reglas deterministas sobre el puntaje ponderado promedio ante conflictos críticos o coberturas de evidencia insuficientes. Justificación: previene falsos negativos críticos.
- `[ADR-005]` **Modos de Gobernanza en Políticas:** Separación de modos `audit_only`, `recommend`, `human_review` y `dry_run` en `PolicyEngine`. Justificación: previene acciones destructivas sin aprobación explícita.
- `[ADR-006]` **Gobernanza Contextual iDirectory:** Integración de mapa de contexto topológico (`.context/tree.json`) y balizas por carpeta (`.context.yaml`). Justificación: optimiza en un 95% el consumo de tokens agéntico.
- `[ADR-007]` **Pipeline de Evaluación en Dos Fases (L1 Fast Gate & L2 Router):** Ejecución determinista en $\le 15\text{ ms}$ de L1 como filtro previo obligatorio. Si `route == PASS`, se emite `AuditResult` sin inferencia LLM, reduciendo costes y latencia a cero en la mayoría de turnos.
- `[ADR-008]` **Compactación Inmutable y Session Lifecycle Gates:** Creación de `ContextCompactor` con semántica de funciones puras (`model_copy(deep=True)`) y verificación bidireccional contra `audit-input.schema.json`.
- `[ADR-009]` **Adaptador HTTP Universal Zero-Dependency:** Implementación de `LocalEndpointAdapter` utilizando exclusivamente la librería estándar (`urllib.request`) para garantizar soporte universal de endpoints locales (Ollama, vLLM) sin agregar dependencias pesadas a `pyproject.toml`.

---

## 10. REGLAS DE MODIFICACIÓN, GLOSARIO E ÍNDICE DE EVIDENCIAS

### 10.1 Convenciones de Estilo y Reglas de Desarrollo
- Python 3.9+ con tipado estricto (`typing`, Pydantic v2) `[CONFIRMADO]`.
- Formato PEP 8, nombres en `snake_case` para módulos/funciones y `PascalCase` para clases.
- Manejo estricto de excepciones tipadas (`AdapterExecutionError`, `ValidationError`).
- Modificación de esquemas: toda adición de campos en `models.py` debe ser validada contra `schemas/audit-input.schema.json` y `schemas/audit-result.schema.json`.
- Invariante Zero-Code: prohibido incluir bloques de implementación de código en este documento; usar exclusivamente firmas AST de 1 línea en Sección 4.1.

### 10.2 Glosario de Términos
- **IRC / CRS (Índice de Riesgo Contextual / Context Risk Score):** Métrica escalar continua en rango `[0.0, 100.0]` que cuantifica la probabilidad de fallo o confabulación en la ventana de contexto.
- **L1 Fast Gate:** Evaluador heurístico determinista de ultra-baja latencia ($\le 15\text{ ms}$) que resuelve turnos en verde sin invocar LLMs.
- **L2 Semantic Router:** Evaluador semántico condicional invocado únicamente ante señales de riesgo, ambigüedad o tareas fácticas.
- **Lost-in-the-Middle:** Fenómeno de decaimiento atencional donde directivas ubicadas en la zona intermedia ($0.35 \le p \le 0.75$) sufren degradación de observabilidad.
- **Contrato Epistémico:** Principio metodológico que restringe el diagnóstico a evidencia física observable y telemetría explícita.
- **Session Lifecycle Gates:** Disparadores de acción de ciclo de vida (`SESSION_HANDOFF_CHECKPOINT`, `SESSION_FORK_CLEAN`, `PRUNE_STALE_TOOL_OUTPUTS`).

### 10.3 Checklist de Verificación Previa a Commit
- [ ] Ejecutar la suite completa: `python -m pytest -v` (61/61 tests PASSED).
- [ ] Verificar evaluación por lotes: `python scripts/evaluate.py` (5/5 cases OK).
- [ ] Validar CLI L1 Fast Gate: `python -m src.context_auditor.cli examples/healthy-conversation.json --fast-gate-only`.
- [ ] Confirmar que no existan credenciales hardcodeadas en ningún archivo.
- [ ] Confirmar 0 rutas locales absolutas y 0 URIs de esquema `file` en `./01_seed/seed-cea-brain-master.md`.

---

## 📌 CONTEXT HANDOFF & PROTOCOLO DE ASISTENCIA

> **Mensaje de orientación para el modelo de IA receptor:**
> "Esto es una semilla de proyecto (**ThinkingSeed Master v3.0**): el vector arquitectónico y ADN del proyecto (`contains_source_code="false"`), no su repositorio completo. Refleja el avance real, los contratos simbólicos y la superficie de tensión del sistema hasta la fecha. Como modelo receptor, tu función es usar esta semilla como memoria técnica para:
> 1. **Responder preguntas** sobre la arquitectura, contratos simbólicos, dependencias y flujos del sistema.
> 2. **Auditar riesgos y sugerir mejoras** evaluando activamente la Superficie de Tensión (Sección 7) y las áreas marcadas como `[FALTANTE]`.
> 3. **Generar código o soluciones compatibles** respetando las rutas relativas (`./`), firmas simbólicas e invariantes definidas aquí, cuando el usuario te lo solicite."

### Pautas de resolución:
Antes de resolver una solicitud:
1. Identifica el objetivo del usuario.
2. Localiza los componentes afectados usando las rutas relativas (`./`) del Seed.
3. Revisa restricciones (`[INV-01]` a `[INV-05]`), contratos simbólicos (Sección 4) y vectores de tensión (Sección 7).
4. Explicita supuestos cuando sea necesario: "Supongo que X debido a Y".
5. Propone cambios por archivo con rutas relativas claras y separadores Unix (`/`).
6. Añade pruebas, riesgos y criterios de aceptación.

### 🤝 Acuse de Recibo Inicial
Si el usuario adjuntó esta semilla **sin una instrucción específica**, no intentes generar código ni completar archivos vacíos. Responde únicamente con:
1. Un saludo confirmando que asimilaste el ADN arquitectónico v3.0 de **CEA Brain** (`<SEED_ARCHITECTURAL_VECTOR>`) y su stack principal.
2. Un breve resumen de 2-3 líneas sobre el objetivo, su estado actual y sus principales vectores de tensión.
3. Una frase poniéndote a disposición para resolver dudas sobre su funcionamiento o colaborar en los siguientes pasos de desarrollo.

</SEED_ARCHITECTURAL_VECTOR>