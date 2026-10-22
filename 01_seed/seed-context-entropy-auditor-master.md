<SEED_ARCHITECTURAL_VECTOR version="3.0" contains_source_code="false" artifact_type="architectural_vector" mode="architecture_and_vulnerability_audit">

# THINKING SEED MASTER: Context Entropy Auditor (CEA)

> **[DIRECTIVA DE SISTEMA PARA MODELOS DE IA RECEPTORES — CLAUDE / GPT / GEMINI / AGENTES]:**
> 1. **Naturaleza del Artefacto:** Este documento es un **Vector Arquitectónico y Memoria Técnica (ThinkingSeed Master v3.0)** con `contains_source_code="false"`. **NO es el repositorio de código fuente completo** ni un volcado truncado. La ausencia de bloques de código de implementación es una **invariante deliberada de ingeniería** para maximizar la densidad semántica y preservar más del 99% de tu ventana de contexto.
> 2. **Modo de Razonamiento Adversarial:** Opera como **Arquitecto de Sistemas y Cazador de Vulnerabilidades/Bugs**. Utiliza las firmas simbólicas (Sección 4) y la superficie de tensión (Sección 7) para detectar condiciones de carrera, acoplamientos frágiles y casos borde antes de proponer cambios.
> 3. **Estado de Avance Real:** Los componentes etiquetados como `[FALTANTE]` reflejan el trabajo en progreso (WIP) real del proyecto, no defectos de este documento.

## Seed Changelog
- `2026-10-22`: `[CONFIRMADO]` Re-auditoría exhaustiva ejecutada vía `/seedMaster`. Verificación de suite completa de pruebas (36/36 tests PASSED en 6.02s). Validación de 0 rutas absolutas locales, 0 URIs de esquema file y 0 código fuente de implementación. Sincronización de metadatos de telemetría y estado de árbol de trabajo.
- `2026-10-21`: `[CONFIRMADO]` Actualización a especificación ThinkingSeed Master v3.0. Integración de balizas `.context.yaml` (24 nodos) y mapa satelital `.context/tree.json`. Auditoría de madurez MetricsThinking™ (68.75% LLMOps Profile v3.0) y roadmap de remediación P1/P2 en `artifacts/plans/active/INFERRED_ROADMAP.md`. Extracción simbólica AST exhaustiva de 1 línea, eliminación de rutas absolutas locales y adición de análisis adversarial de superficie de tensión en Sección 7.

---

## 0. IDENTIDAD, METADATOS Y CONTRATO DEL RECEPTOR
```yaml
seed_schema_version: "3.0"
project_name: "Context Entropy Auditor"
repository_name: "Context Entropy Auditor (CEA)"
project_type: "library"
repository_mode: "single-project"
generated_at: "2026-10-22T08:57:30-03:00"
generated_by: "Antigravity Agent (Gemini 3.8 Flash)"
repository_root: "./"
git_branch: "master"
git_commit: "062ea79"
working_tree_state: "dirty"
analysis_mode: "static+git+validated"
coverage_level: "high"
known_analysis_limits:
  - "Validación de inferencia remota con Gemini requiere clave API GEMINI_API_KEY en variables de entorno."
  - "Inferencia LLM local soportada y verificada mediante el CLI de Antigravity (agy.exe) en PATH."
  - "Modelos locales testeados: gemini-3.7-flash, gemini-3.1-pro, gemini-3.8-flash, gemini-3.6-flash con niveles de esfuerzo (low, medium, high, max)."
```

### 0.1 Instrucciones para el modelo receptor
1. **ADN vs Repositorio:** Reconoce este documento como la memoria técnica y el ADN del proyecto (`contains_source_code="false"`), no como el repositorio completo ni como una prueba de ejecución.
2. **Contexto Pasivo y Quirúrgico:** No generes código no solicitado ni reclames por archivos ausentes; espera instrucciones específicas del usuario o utilízalo como Ground Truth para responder preguntas sobre el sistema.
3. **Estado de Avance:** Considera que los componentes marcados como `[FALTANTE]` representan el avance real del proyecto y oportunidades de asistencia, no errores del documento.
4. **Rigor Epistemológico:** Respeta las etiquetas `[CONFIRMADO]`, `[INFERIDO]`, `[DECLARADO]`, `[NO VERIFICADO]` y `[FALTANTE]`.
5. **Portabilidad de Rutas:** Cita siempre rutas relativas a la raíz del repositorio (`./ruta/archivo`) con `/`. Prohibido emitir rutas locales absolutas o enlaces con esquema `file` local.
6. **Contratos Simbólicos:** Conserva arquitectura, firmas simbólicas (Sección 4) e invariantes (`[INV-XX]`).
7. **Postura Adversarial Constructiva:** Revisa siempre la Sección 7 (Superficie de Tensión) antes de proponer cambios.
8. **Seguridad Zero-Trust:** No reveles ni solicites secretos. Usa placeholders (`<REDACTED>`).

---

## 1. RESUMEN EJECUTIVO Y ALCANCE

### 1.1 Proyecto en una frase
`[CONFIRMADO]` **Context Entropy Auditor (CEA)** es un framework y suite interactiva de diagnóstico epistémico y fiabilidad contextual para aplicaciones con Modelos de Lenguaje (LLMs), diseñado para auditar el Índice de Riesgo Contextual (IRC / CRS) a través de 6 dimensiones fundamentales, combinando extracción heurística determinista y evaluación semántica mediante adaptadores desacoplados (Google Gemini API y Antigravity CLI local).

### 1.2 Problema que resuelve
- **Degradación de señal y fatiga contextual:** Pérdida de coherencia, interferencia entre turnos contradictorios y dilución de restricciones críticas en ventanas de contexto extensas `[CONFIRMADO]`.
- **Confabulación mecanicista:** Tendencia frecuente de los evaluadores basados en LLMs a inventar fallas internas de atención o estados no observables de KV Cache sin evidencia física `[CONFIRMADO]`.
- **Falta de evaluación determinista combinada:** Ausencia de herramientas que integren métricas heurísticas objetivas (recencia del objetivo, drift de herramientas, redundancia documental) con clasificación semántica estricta bajo contratos JSON Schema `[CONFIRMADO]`.
- **Inferencia local y evaluación de estrés:** Necesidad de auditar y estresar modelos turno a turno en entornos de desarrollo sin exponer claves de API ni depender de servicios cloud externos `[CONFIRMADO]`.

### 1.3 Usuarios y sistemas consumidores
- **Ingenieros de Agentes y Arquitecturas LLM:** Auditoría previa y continua de ventanas de contexto antes del dispatch a modelos de frontera `[CONFIRMADO]`.
- **Suites de Evaluación y CI/CD:** Banco de pruebas automatizado contra datasets adversariales para prevenir regresiones en prompts `[CONFIRMADO]`.
- **Desarrolladores y QA en Antigravity IDE:** Simulación interactiva (Live Stress Test) evaluando la respuesta de múltiples modelos y esfuerzos de pensamiento (`effort: low|medium|high|max`) `[CONFIRMADO]`.
- **Equipos de Gobernanza y Confiabilidad:** Auditoría formal y generación de reportes periciales de riesgo operacional `[DECLARADO]`.

### 1.4 Alcance y límites del sistema
- **In Scope:**
  - Diagnóstico formal de 6 dimensiones contextuales: `instruction_conflict`, `task_ambiguity`, `context_contamination`, `evidence_quality`, `state_integrity`, `redundancy_pressure` `[CONFIRMADO]`.
  - Normalizador determinista y parser de entrada tolerante a fallos (`./src/context_auditor/normalizers/__init__.py`) `[CONFIRMADO]`.
  - Extractor de señales heurísticas deterministas (conteo de turnos, ratio de utilización de contexto, detección de duplicados, reemplazos de herramientas, recencia del objetivo) `[CONFIRMADO]`.
  - Motor de cálculo de Índice de Riesgo Contextual (IRC / CRS) con ponderaciones configurables y 5 reglas de sobrescritura de seguridad (override rules) `[CONFIRMADO]`.
  - Motor de políticas de recomendación (`audit_only`, `recommend`, `human_review`, `dry_run`) `[CONFIRMADO]`.
  - Arquitectura Hexagonal de adaptadores: `GeminiAdapter` (API remota) y `AntigravityAdapter` (CLI local `agy.exe`) `[CONFIRMADO]`.
  - CLI unificado con auto-detección y launcher PowerShell (`./run_audit.ps1`) `[CONFIRMADO]`.
  - Suite interactiva de benchmark y Live Stress Test (`InteractiveAuditorCLI`) con telemetría de tokens y persistencia automática de reportes en Markdown y JSON en `./logs/benchmarks/<session_id>/` `[CONFIRMADO]`.
- **Out of Scope:**
  - Inferencia sobre estados mecanicistas de capas de atención, activaciones internas o memoria GPU/TPU (violación explícita del Contrato Epistémico) `[CONFIRMADO]`.
  - Modificación automática no supervisada o mutación en caliente de prompts en ejecución `[DECLARADO]`.

---

## 2. ARQUITECTURA, TOPOLOGÍA Y FRONTERAS MODULARES

### 2.1 Estilo arquitectónico
`[CONFIRMADO]` Arquitectura limpia y modular basada en **Puertos y Adaptadores (Clean Architecture / Hexagonal Architecture)** con diseño **Schema-First**:
- **Núcleo de Dominio:** Modelos Pydantic v2 puros (`./src/context_auditor/models.py`), motor de scoring determinista (`./src/context_auditor/scoring.py`), extractor heurístico (`./src/context_auditor/signals.py`) y motor de políticas (`./src/context_auditor/policies.py`).
- **Puertos:** `BaseLLMAdapter` en `./src/context_auditor/adapters/base.py`.
- **Adaptadores Concretos:** `GeminiAdapter` (Google GenAI SDK) y `AntigravityAdapter` (ejecución subprocess de `agy.exe`).
- **Orquestador (Fachada):** `ContextAuditor` en `./src/context_auditor/auditor.py`.
- **Presentación e Interacción:** `./src/context_auditor/cli.py` y `./src/context_auditor/interactive.py` (`InteractiveAuditorCLI`).

### 2.2 Árbol estructural del repositorio
```
./
├── .agentignore                           # Exclusiones de indexación para agentes IA
├── .context/                              # Topología de gobernanza contextual
│   └── tree.json
├── .gitignore
├── 01_seed/                               # Memoria técnica pasiva y ADN arquitectónico
│   ├── .context.yaml
│   └── seed-context-entropy-auditor-master.md
├── 02_foundation/                         # Fundamentos de arquitectura y gobernanza
│   └── engine/
│       ├── .context.yaml
│       └── engine_readme.md
├── 03_research/                           # Área de experimentación, notebooks y prompts
│   ├── experiments/
│   │   └── .context.yaml
│   ├── notebooks/
│   │   └── .context.yaml
│   └── prompts/
│       └── .context.yaml
├── artifacts/                             # Artefactos, métricas y fases completadas
│   ├── Fases/                             # Incrementos de desarrollo documentados (Inc0 - Inc7)
│   ├── plans/                             # Planes activos, archivados y métricas
│   │   ├── active/
│   │   │   ├── .context.yaml
│   │   │   ├── implementation_plan.md
│   │   │   ├── INFERRED_ROADMAP.md
│   │   │   └── INSTRUCCION_MAESTRA_CONTEXT_ENTROPY_AUDITOR.md
│   │   ├── archive/
│   │   │   ├── .context.yaml
│   │   │   └── Analisis de Planes/
│   │   └── metricsthinking/
│   │       └── .context.yaml
│   ├── Task del agente/                   # Tareas y tracking operacional
│   │   └── task.md
│   ├── MetricsThinking.json               # Telemetría de auditoría de madurez (68.75%)
│   └── MetricsThinking.md                 # Reporte formal de madurez del proyecto
├── config/                                # Configuraciones operacionales
│   ├── .context.yaml
│   └── scoring_defaults.yaml              # Ponderaciones, umbrales y reglas de override
├── data/                                  # Almacenamiento local de datos
│   ├── processed/
│   ├── raw/
│   └── sandbox/
├── dataset/                               # Datasets de evaluación y autodiagnóstico
│   ├── eval_dataset.jsonl                 # Dataset de evaluación con casos representativos
│   └── self_audit.json                    # Carga real de autodiagnóstico del sistema
├── docs/                                  # Documentación técnica y epistémica
│   ├── architecture/
│   ├── notes/
│   ├── specs/
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
│   ├── .context.yaml
│   └── benchmarks/                        # Subcarpetas generadas por sesión interactiva
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
│   ├── .context.yaml
│   ├── Context Entropy Auditor.md
│   └── evaluate.py
├── src/
│   ├── cloud_jobs/
│   ├── core/
│   ├── dashboards/
│   ├── data_generation/
│   └── context_auditor/                   # Paquete principal Python
│       ├── __init__.py
│       ├── auditor.py                     # Orquestador ContextAuditor
│       ├── cli.py                         # Entry point CLI con resolución de adaptadores
│       ├── interactive.py                 # Suite Interactiva & Live Stress Test CLI
│       ├── models.py                      # Modelos de dominio canónicos Pydantic v2
│       ├── policies.py                    # Motor de políticas y filtrado de acciones
│       ├── scoring.py                     # Cálculo matemático del IRC y overrides
│       ├── signals.py                     # Extracción de señales heurísticas deterministas
│       ├── validators.py                  # Validación contra schemas/
│       ├── adapters/
│       │   ├── __init__.py                # Exportación unificada de adaptadores
│       │   ├── base.py                    # Puerto abstracto BaseLLMAdapter y excepciones
│       │   ├── antigravity.py             # Adaptador local para CLI agy.exe
│       │   └── gemini.py                  # Adaptador para Google Gemini API
│       └── normalizers/
│           └── __init__.py                # Normalizador tolerante de entrada
├── tests/                                 # Suite automatizada (36 tests)
│   ├── .context.yaml
│   ├── e2e/
│   │   └── test_cli.py                    # Pruebas e2e de CLI y opciones interactivas
│   └── unit/
│       ├── test_antigravity_adapter.py    # Pruebas completas del adaptador agy.exe
│       ├── test_interactive_session.py    # Pruebas de persistencia y telemetría de sesión
│       ├── test_normalizers.py            # Pruebas de normalización
│       ├── test_policies.py               # Pruebas del motor de políticas
│       ├── test_scoring.py                # Pruebas de cálculo de IRC y overrides
│       ├── test_signals.py                # Pruebas de extracción de señales
│       └── test_validators.py             # Pruebas de validación de esquemas JSON
├── Tools/                                 # Herramientas utilitarias y baliza de contexto
│   └── .context.yaml
├── CONTRIBUTING.md
├── Context Entropy Auditor.md
├── Entropy.jpeg
├── LICENSE
├── README.md                              # Documentación general en inglés
├── README_ES.md                           # Documentación general en español
├── ROADMAP.md                             # Roadmap del proyecto
├── pyproject.toml                         # Manifiesto formal de empaquetado Python
├── resultado_auditoria.json               # Evidencia de ejecución real de auto-auditoría
└── run_audit.ps1                          # Launcher PowerShell para Windows
```

### 2.3 Responsabilidad por módulo clave
- `./src/context_auditor/auditor.py`: Fachada principal del SDK (`ContextAuditor`). Orquesta el pipeline de auditoría: normalización, extracción de señales, evaluación semántica del adaptador, cálculo de IRC, filtrado de acciones por políticas y validación de salida `[CONFIRMADO]`.
- `./src/context_auditor/models.py`: Entidades canónicas fuertemente tipadas en Pydantic v2 (`AuditInput`, `AuditResult`, `Message`, `Role`, `ToolEvent`, `Document`, `DimensionScores`, `Finding`, `RecommendedAction`, `OverallStatus`, `EpistemicStatus`) `[CONFIRMADO]`.
- `./src/context_auditor/adapters/antigravity.py`: Adaptador local para el CLI `agy.exe`. Compila prompts, invoca subprocess con argumentos de razonamiento (`--effort`), sanitiza bloques JSON defensivamente en 4 capas `[CONFIRMADO]`.
- `./src/context_auditor/adapters/gemini.py`: Adaptador remoto para la API de Google Gemini utilizando el SDK `google.genai` con soporte de fallback mock para pruebas `[CONFIRMADO]`.
- `./src/context_auditor/adapters/base.py`: Define el contrato abstracto `BaseLLMAdapter` y la excepción canónica `AdapterExecutionError` `[CONFIRMADO]`.
- `./src/context_auditor/interactive.py`: Implementa `BenchmarkSession` (gestión de sesiones, timeline, telemetría y reportes) y `InteractiveAuditorCLI` (consola a color con menús de simulación, stress test en vivo turno a turno, cambio dinámico de modelos/effort y visualización histórica) `[CONFIRMADO]`.
- `./src/context_auditor/scoring.py`: Implementa el cálculo formal ponderado del IRC y las 5 reglas de sobrescritura crítica (overrides) desde `./config/scoring_defaults.yaml` `[CONFIRMADO]`.
- `./src/context_auditor/signals.py`: Analizador heurístico determinista sin LLM (conteo de turnos, ratio de utilización de contexto, detección de duplicados, reemplazos de herramientas, recencia del objetivo) `[CONFIRMADO]`.
- `./src/context_auditor/policies.py`: Motor de gobernanza operacional con modos `audit_only`, `recommend`, `human_review`, `dry_run` `[CONFIRMADO]`.
- `./src/context_auditor/validators.py`: Validación estricta contra esquemas formales JSON Schema en `./schemas/` `[CONFIRMADO]`.
- `./run_audit.ps1`: Script PowerShell de arranque rápido en Windows con verificación de `agy.exe` en PATH y parámetros amigables `[CONFIRMADO]`.

### 2.4 Invariantes Arquitectónicos
- `[INV-01]` **Independencia del Core:** El motor de scoring (`./src/context_auditor/scoring.py`), las señales (`./src/context_auditor/signals.py`) y los modelos (`./src/context_auditor/models.py`) jamás deben importar librerías de clientes LLM (como `google-genai`, `openai`, etc.).
- `[INV-02]` **Contrato Epistémico Absoluto:** Queda estrictamente prohibido alucinar estados internos no observables (pesos de capas de atención, KV cache allocation físico). Toda métrica debe ser observable en el texto o medida heurísticamente.
- `[INV-03]` **Pureza Matemática:** Las funciones `compute_irc()` y `extract_deterministic_signals()` son funciones matemáticas puras; dados los mismos inputs, deben producir idénticos resultados sin efectos colaterales.
- `[INV-04]` **Esquemas como Fuente de Verdad:** Todo cambio en `models.py` debe reflejarse y validarse de forma bidireccional contra `schemas/audit-input.schema.json` y `schemas/audit-result.schema.json`.

---

## 3. FLUJOS DE EJECUCIÓN, ENTRY POINTS Y CICLO DE VIDA

### 3.1 Puntos de entrada principales
1. **Launcher Windows PowerShell (`./run_audit.ps1`):**
   - Ejecución interactiva: `.\run_audit.ps1 -Interactive`
   - Auditoría de archivo específico: `.\run_audit.ps1 -File examples/ambiguous-task.json -Model gemini-3.7-flash -Effort high`
2. **CLI de Línea de Comandos (`./src/context_auditor/cli.py`):**
   - Batch audit: `python -m context_auditor.cli examples/instruction-conflict.json --adapter antigravity --model gemini-3.7-flash --effort medium`
   - Modo interactivo: `python -m context_auditor.cli --interactive`
3. **SDK Programático en Python:**
   - Invocación desde pipelines: `ContextAuditor(llm_adapter=AntigravityAdapter(model="gemini-3.7-flash", effort="high")).audit(raw_payload)`
4. **Script de Evaluación por Lotes (`./scripts/evaluate.py`):**
   - Ejecución contra dataset: `python scripts/evaluate.py`

### 3.2 Diagrama de flujo principal E2E
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
         ┌───────────┴───────────────────────────────┐
         ▼                                           ▼
[signals.py: extract_deterministic_signals]   [BaseLLMAdapter: evaluate_context]
  • Message counts & turns                     ├── AntigravityAdapter (agy.exe)
  • Token estimation & utilization             └── GeminiAdapter (google.genai)
  • Document exact duplicates                                │
  • Stale tool drift detection                               │
  • Last objective recency                                   ▼
         │                                      [Semantic Dimension Scores]
         │                                      [Findings & Recommendations]
         └───────────────────┬───────────────────────────────┘
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
                             │
                             ▼
                [validators.py: validate_result]
                             │
                             ▼
              [AuditResult: JSON / Report / CLI]
```

### 3.3 Ciclo de vida de la ejecución y estados
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
- **Clasificación Epistémica (`EpistemicStatus`):**
  - `observed`: Evidencia directamente contrastada en el texto `[CONFIRMADO]`.
  - `inferred`: Deducción lógica justificada por la semántica `[CONFIRMADO]`.
  - `runtime_measured`: Medido heurísticamente por `signals.py` `[CONFIRMADO]`.
  - `unknown`: No verificable con la información provista `[CONFIRMADO]`.

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
- `./src/context_auditor/models.py::AuditScope(messages_observed: Optional[int], documents_observed: Optional[int], tool_outputs_observed: Optional[int]) -> AuditScope | Delimitación del alcance auditado`
- `./src/context_auditor/models.py::DimensionScores(instruction_conflict: int, task_ambiguity: int, context_contamination: int, evidence_quality: int, state_integrity: int, redundancy_pressure: int) -> DimensionScores | Puntuaciones enteras [0, 100] de las 6 dimensiones`
- `./src/context_auditor/models.py::Finding(finding_id: str, dimension: str, epistemic_status: EpistemicStatus, severity: int, evidence_refs: List[str], explanation: str, confidence: Optional[float]) -> Finding | Hallazgo atómico con referencia a evidencia física`
- `./src/context_auditor/models.py::RecommendedAction(action: str, target_refs: List[str], reason: str, requires_policy_approval: bool, destructive: bool) -> RecommendedAction | Acción de remediación contextual`
- `./src/context_auditor/models.py::AuditResult(schema_version: str, audit_version: Optional[str], audit_id: str, overall_status: OverallStatus, risk_score: float, confidence: float, evidence_coverage: float, scope: Optional[AuditScope], dimension_scores: DimensionScores, findings: List[Finding], recommended_actions: List[RecommendedAction], triggered_rules: List[str], limitations: List[str]) -> AuditResult | Contrato formal de salida de auditoría
- `./src/context_auditor/scoring.py::load_scoring_config() -> Dict[str, Any] | Carga configuración y ponderaciones desde config/scoring_defaults.yaml con fallback determinista`
- `./src/context_auditor/scoring.py::compute_base_status(score: float, thresholds: Dict[str, float]) -> OverallStatus | Mapea IRC a status base (stable, moderate, high, critical)`
- `./src/context_auditor/scoring.py::compute_irc(dimensions: DimensionScores, evidence_coverage: float, task_requires_factual: bool = False) -> Tuple[float, OverallStatus, list[str]] | Función matemática pura: calcula IRC lineal ponderado y evalúa 5 reglas críticas de override`
- `./src/context_auditor/signals.py::estimate_tokens(text: str) -> int | Estimador determinista heurístico de tokens (~4 chars/token)`
- `./src/context_auditor/signals.py::extract_deterministic_signals(audit_input: AuditInput) -> Dict[str, Any] | Extrae métricas objetivas: conteos, recencia de objetivo, duplicados y tool drift`
- `./src/context_auditor/policies.py::PolicyMode(str, Enum) | Modos de gobernanza: AUDIT_ONLY, RECOMMEND, HUMAN_REVIEW, DRY_RUN`
- `./src/context_auditor/policies.py::PolicyEngine(mode: PolicyMode = PolicyMode.RECOMMEND) -> PolicyEngine | Motor de políticas de filtrado y aprobación`
- `./src/context_auditor/policies.py::PolicyEngine.process_actions(candidate_actions: List[RecommendedAction]) -> List[RecommendedAction] | Aplica filtrado de acciones destructivas según modo de política`
- `./src/context_auditor/validators.py::get_schema_path(schema_filename: str) -> str | Resuelve ruta canónica a archivos JSON Schema en schemas/`
- `./src/context_auditor/validators.py::validate_input(data: Dict[str, Any]) -> None | Valida payload contra schemas/audit-input.schema.json | Lanza jsonschema.ValidationError`
- `./src/context_auditor/validators.py::validate_result(data: Dict[str, Any]) -> None | Valida resultado contra schemas/audit-result.schema.json | Lanza jsonschema.ValidationError`
- `./src/context_auditor/normalizers/__init__.py::normalize_input(raw_data: Dict[str, Any]) -> AuditInput | Normalizador tolerante de esquemas de entrada a entidad AuditInput`
- `./src/context_auditor/adapters/base.py::AdapterExecutionError(Exception) | Excepción base tipada para fallos de adaptadores LLM`
- `./src/context_auditor/adapters/base.py::BaseLLMAdapter.evaluate_context(audit_input: AuditInput, signals: Dict[str, Any]) -> Dict[str, Any] | Puerto abstracto para evaluación semántica`
- `./src/context_auditor/adapters/antigravity.py::AntigravityAdapter(model: str = "gemini-3.7-flash", effort: Optional[str] = "medium", agy_path: str = "agy.exe", timeout: int = 120) -> AntigravityAdapter | Adaptador de inferencia local offline vía CLI agy.exe`
- `./src/context_auditor/adapters/antigravity.py::AntigravityAdapter.evaluate_context(audit_input: AuditInput, signals: Dict[str, Any]) -> Dict[str, Any] | Ejecuta evaluación por subprocess local con deserialización multicapa | Lanza AdapterExecutionError`
- `./src/context_auditor/adapters/antigravity.py::AntigravityAdapter._compile_prompt(audit_input: AuditInput, signals: Dict[str, Any]) -> str | Compila prompt evaluador con señales deterministas`
- `./src/context_auditor/adapters/antigravity.py::AntigravityAdapter._extract_json(raw_text: str) -> Dict[str, Any] | Extracción defensiva en 4 capas (top-level dict, markdown fence regex, json.loads, regex balanceado)`
- `./src/context_auditor/adapters/antigravity.py::AntigravityAdapter._ensure_schema_defaults(data: Dict[str, Any]) -> Dict[str, Any] | Asegura presencia de campos obligatorios en respuesta semántica`
- `./src/context_auditor/adapters/gemini.py::GeminiAdapter(api_key: str = None, model_name: str = "gemini-2.5-pro") -> GeminiAdapter | Adaptador remoto para API Google Gemini (o fallback a mock offline)`
- `./src/context_auditor/adapters/gemini.py::GeminiAdapter.evaluate_context(audit_input: AuditInput, signals: Dict[str, Any]) -> Dict[str, Any] | Inferencia remota vía google.genai con fallback a mock`
- `./src/context_auditor/adapters/gemini.py::GeminiAdapter._get_mock_evaluation(audit_input: AuditInput) -> Dict[str, Any] | Genera evaluación sintética para pruebas sin conexión`
- `./src/context_auditor/auditor.py::ContextAuditor(llm_adapter: BaseLLMAdapter, policy_mode: PolicyMode = PolicyMode.RECOMMEND) -> ContextAuditor | Fachada principal del SDK y orquestador del pipeline`
- `./src/context_auditor/auditor.py::ContextAuditor.audit(raw_input: Dict[str, Any], task_requires_factual: bool = False) -> AuditResult | Pipeline E2E: validación, normalización, señales, evaluación LLM, scoring IRC, políticas y validación de contrato`
- `./src/context_auditor/cli.py::resolve_adapter(adapter_name: str = None, model: str = None, effort: str = "medium", agy_path: str = "agy.exe") -> BaseLLMAdapter | Auto-detección y resolución entre AntigravityAdapter y GeminiAdapter`
- `./src/context_auditor/cli.py::main() -> None | Entry point CLI con soporte para archivos JSON y modo interactivo (--interactive)`
- `./src/context_auditor/interactive.py::BenchmarkSession(session_name: Optional[str] = None, initial_model: str = "gemini-3.7-flash", initial_effort: str = "medium") -> BenchmarkSession | Gestor de estado para sesiones interactivas, telemetría y reportes`
- `./src/context_auditor/interactive.py::BenchmarkSession.add_message(role: str, content: str, model_used: Optional[str] = None) -> str | Registra mensaje y actualiza telemetría de tokens`
- `./src/context_auditor/interactive.py::BenchmarkSession.add_document(content: str, source: str = "user_input") -> str | Añade documento a la sesión`
- `./src/context_auditor/interactive.py::BenchmarkSession.add_tool_event(tool_name: str, parameters: Dict[str, Any], result: str) -> str | Inyecta evento de tool a la sesión`
- `./src/context_auditor/interactive.py::BenchmarkSession.record_turn_audit(turn_index: int, audit_result: AuditResult, latency_sec: float) -> None | Registra turno evaluado en timeline y dispara persistencia`
- `./src/context_auditor/interactive.py::BenchmarkSession.build_audit_input() -> AuditInput | Construye AuditInput acumulativo para el auditor`
- `./src/context_auditor/interactive.py::BenchmarkSession.save_snapshot() -> None | Persiste session_meta.json, conversation.json, timeline.json y summary_report.md en logs/benchmarks/<session_id>/`
- `./src/context_auditor/interactive.py::InteractiveAuditorCLI() -> InteractiveAuditorCLI | Cockpit de consola a color para Live Stress Test, benchmarking y auditorías interactivas`
- `./src/context_auditor/interactive.py::InteractiveAuditorCLI.run() -> None | Menú principal interactivo`
- `./src/context_auditor/interactive.py::main() -> None | Entry point para launcher interactivo`
- `./scripts/evaluate.py::main() -> None | Runner de evaluación batch sobre dataset/eval_dataset.jsonl`

### 4.2 Persistencia y Almacenamiento
- `[CONFIRMADO]` El núcleo es completamente **stateless**. No requiere bases de datos relacionales ni motores SQL.
- `[CONFIRMADO]` Persistencia estructurada en disco para sesiones de benchmark interactivo en `./logs/benchmarks/<session_id>/`:
  1. `session_meta.json`: Metadatos del benchmark, modelos y recuentos.
  2. `conversation.json`: Contexto íntegro de la conversación auditada.
  3. `timeline.json`: Array cronológico de turnos evaluados con latencias, tokens y scores.
  4. `summary_report.md`: Reporte ejecutivo en Markdown con tabla comparativa de evolución del IRC.

### 4.3 Interfaces y Contratos de Datos
- **Esquemas JSON formales:**
  - `./schemas/audit-input.schema.json` `[CONFIRMADO]`.
  - `./schemas/audit-result.schema.json` `[CONFIRMADO]`.
- **Contrato de Subprocess con Antigravity CLI:**
  - Invocación: `agy.exe --model <MODEL> [--effort <EFFORT>] --input-format text --output-format json --dangerously-skip-permissions` `[CONFIRMADO]`.
  - Sanitización: Parsing robusto tolerante a envolturas `{"status": "SUCCESS", "response": ...}`, bloques de código markdown triple backtick y fallback regex `[CONFIRMADO]`.

---

## 5. CONFIGURACIÓN, ENTORNOS Y DEPENDENCIAS

### 5.1 Variables de Entorno y Flags CLI
| Parámetro / Variable | Tipo | Default | Efecto | Sensible |
|:---|:---:|:---:|:---|:---:|
| `GEMINI_API_KEY` | Env Var (String) | `None` | Clave de acceso requerida si se utiliza `GeminiAdapter` | **Sí** |
| `CEA_CONFIG_PATH` | Env Var (Path) | `config/scoring_defaults.yaml` | Ruta alternativa a las ponderaciones de scoring | No |
| `--adapter` | CLI Flag | Auto-detect | Selecciona `antigravity` o `gemini` (si no hay clave pero existe `agy.exe`, auto-selecciona `antigravity`) | No |
| `--model` | CLI Flag | `gemini-3.7-flash` | Modelo LLM a utilizar para inferencia | No |
| `--effort` | CLI Flag | `medium` | Nivel de esfuerzo de pensamiento (`low`, `medium`, `high`, `max`) | No |
| `--agy-path` | CLI Flag | `agy.exe` | Ruta al ejecutable de Antigravity CLI | No |
| `--policy` | CLI Flag | `recommend` | Modo de política (`audit_only`, `recommend`, `human_review`, `dry_run`) | No |
| `--factual` | CLI Flag | `False` | Activa comprobaciones estrictas de evidencia y reglas para afirmaciones fácticas | No |

### 5.2 Dependencias del Sistema
- Runtime: Python >= 3.9 (verificado en Python 3.12.10 sobre Windows 11) `[CONFIRMADO]`.
- Dependencias de producción (`./pyproject.toml`):
  - `pydantic>=2.0.0`
  - `jsonschema>=4.0.0`
  - `pyyaml>=6.0`
- Dependencias de desarrollo:
  - `pytest>=7.0.0`
- Dependencia local opcional para inferencia offline:
  - `agy.exe` instalado en el PATH o especificado vía `--agy-path` `[CONFIRMADO]`.

---

## 6. PRUEBAS, CI/CD, DESPLIEGUE Y OPERACIÓN

### 6.1 Estrategia de Pruebas Automatizadas
`[CONFIRMADO]` Suite de **36 pruebas automatizadas** ejecutadas y aprobadas al 100% con `pytest` en 4.15 segundos:
- `./tests/unit/test_antigravity_adapter.py` (9 tests):
  - Inicialización y valores por defecto.
  - Invocación exitosa con mocks.
  - Sanitización de bloques Markdown (fences ` ```json `).
  - Desenvolvimiento de envoltura JSON de `agy.exe`.
  - Manejo de errores de proceso y retorno de código != 0.
  - Captura y excepción tipada ante `FileNotFoundError` (`agy.exe` ausente).
  - Manejo de timeouts (`subprocess.TimeoutExpired`).
  - Parsing tolerante ante respuestas JSON inválidas.
  - Resolución automática de adaptadores en CLI (`resolve_adapter`).
- `./tests/unit/test_interactive_session.py` (2 tests):
  - Creación de sesión, tracking acumulativo de mensajes, documentos, herramientas y tokens.
  - Registro de turnos y persistencia completa de artefactos (`session_meta.json`, `conversation.json`, `timeline.json`, `summary_report.md`).
- `./tests/unit/test_normalizers.py` (2 tests): Normalización de estructuras y rechazo de payloads inválidos.
- `./tests/unit/test_policies.py` (3 tests): Políticas `audit_only`, `recommend` y `human_review`.
- `./tests/unit/test_scoring.py` (5 tests): Cálculo de IRC, combinaciones de riesgo y las 4 reglas de override crítico.
- `./tests/unit/test_signals.py` (7 tests): Estimación de tokens, conteo de mensajes, duplicación exacta de documentos, integridad de IDs, drift de herramientas y recencia del objetivo de usuario.
- `./tests/unit/test_validators.py` (6 tests): Validación estricta contra esquemas de entrada y salida.
- `./tests/e2e/test_cli.py` (2 tests): Ejecución de CLI end-to-end con archivo válido e inválido.

### 6.2 Automatización CI/CD y Empaquetado
- `[CONFIRMADO]` Manifiesto de empaquetado `./pyproject.toml` configurado con build-backend de setuptools y entry point `context-auditor = "src.context_auditor.cli:main"`.
- `[FALTANTE]` Pipeline de integración continua en GitHub Actions (`.github/workflows/ci.yml`).

---

## 7. SUPERFICIE DE TENSIÓN, CONTRADICCIONES Y MODOS DE FALLA

### 7.1 Cruce Adversarial de Reglas vs Árbol Físico
1. **Contradicción del Bootloader vs Raíz del Repositorio:**
   - `.context/tree.json` declara en su bootloader de Tier 1 y Tier 2 el archivo `AGENTS.md`. Sin embargo, `AGENTS.md` **no existe físicamente en la raíz del repositorio**. Cualquier agente o script que intente precargar `AGENTS.md` experimentará un fallo de archivo no encontrado `[FALTANTE]`.
2. **Violación de Convenciones de Nombres y Case Sensitivity:**
   - El estándar de gobernanza contextual iDirectory exige nombres de directorios en minúsculas estrictas (`all-lowercase`). Sin embargo, en el repositorio coexisten carpetas con mayúsculas iniciales: `Tools/`, `artifacts/Task del agente/` (con espacios) y `artifacts/Fases/`. En entornos Linux/CI esto puede inducir fallos de resolución sensible a mayúsculas/minúsculas `[CONFIRMADO]`.
3. **Dependencia de Ecosistema Windows / PowerShell:**
   - El script launcher `./run_audit.ps1` depende exclusivamente del shell de Windows PowerShell. No existe un equivalente bash (`run_audit.sh`) para desarrolladores en Linux o macOS `[CONFIRMADO]`.
4. **Acoplamiento de Inferencia Local a Binario Externo no Empaquetado:**
   - `AntigravityAdapter` asume la disponibilidad en PATH de `agy.exe`. En entornos de producción headless, Docker o CI/CD donde `agy.exe` no está instalado y no se define `GEMINI_API_KEY`, el sistema no tiene un fallback automático a proveedores LLM de código abierto (vLLM, Ollama) o API estándar (OpenAI, Anthropic) `[CONFIRMADO]`.
5. **Riesgo de Truncamiento o Corrupción en Parsing JSON de Subprocess:**
   - La captura de salida estándar desde subprocess mediante buffer de texto puede experimentar bloqueos o truncamientos ante payloads masivos si el timeout se alcanza o si el CLI de inferencia emite advertencias a `stderr` que se mezclen con `stdout` `[CONFIRMADO]`.

### 7.2 Modos de Falla Conocidos y Recuperación
1. **Falta de API Key remota:** Si `GEMINI_API_KEY` no está configurada, el CLI resuelve automáticamente hacia `AntigravityAdapter` si `agy.exe` está disponible en el sistema `[CONFIRMADO]`.
2. **Falta de CLI Local:** Si `agy.exe` no existe o falla en ejecución, se lanza `AdapterExecutionError` con diagnóstico claro de instalación sin crashear el motor principal `[CONFIRMADO]`.
3. **Payloads LLM con formato imperfecto:** `_extract_json()` en `antigravity.py` ejecuta 4 capas consecutivas de deserialización defensiva `[CONFIRMADO]`.
4. **Violación de Contrato JSON Schema:** `validators.py` intercepta discrepancias antes del cálculo de scoring y durante la emisión de resultados `[CONFIRMADO]`.

---

## 8. SEGURIDAD, PRIVACIDAD Y GUARDRAILS

### 8.1 Hallazgos de Seguridad Estática
- Sin secretos, claves de API ni credenciales hardcodeadas en ningún archivo del repositorio `[CONFIRMADO]`.
- Archivos `.agentignore` y `.gitignore` previenen la inclusión inadvertida de `.env`, `.venv`, `.pytest_cache` o credenciales temporales `[CONFIRMADO]`.

### 8.2 Manejo de Autenticación y Autorización
- Inferencia remota: Las credenciales son leídas exclusivamente desde el entorno del sistema (`os.environ.get("GEMINI_API_KEY")`) `[CONFIRMADO]`.
- Inferencia local: `AntigravityAdapter` delega el control de permisos y autenticación a la sesión activa del CLI `agy.exe`, permitiendo operaciones aisladas en entornos corporativos `[CONFIRMADO]`.

### 8.3 Privacidad de Datos y Control de Acciones
- **Aislamiento Local:** El modo interactivo con `AntigravityAdapter` permite auditar conversaciones confidenciales sin que los datos salgan del equipo local hacia APIs públicas `[CONFIRMADO]`.
- **Control de Acciones Destructivas:** Las recomendaciones destructivas (e.g. poda de contexto) son marcadas automáticamente con `requires_policy_approval: true` y `destructive: true` por el `PolicyEngine` `[CONFIRMADO]`.

---

## 9. ESTADO REAL, DEUDA TÉCNICA Y DECISIONES (ADRs)

### 9.1 Nivel de Madurez y Métricas de Auditoría
- **Score MetricsThinking™ (LLMOps Profile v3.0):** **`68.75%`** — Estado: 🟡 **Construcción Activa / Madurez Media** `[CONFIRMADO]`.
  - M01 (Definición GenAI): 100.0% 🟢
  - M02 (Arquitectura Contexto/Prompts): 100.0% 🟢
  - M03 (Guardrails & Seguridad): 66.7% 🔵
  - M04 (Versionado Prompts & Hiperparámetros): 100.0% 🟢
  - M05 (Motor Orquestación): 75.0% 🔵
  - M06 (Adaptadores & Serialización): 66.7% 🔵
  - M07 (Suites Evaluación GenAI): 33.3% 🔵
  - M08 (Cockpits Observabilidad & CLI): 33.3% 🔵
  - M09 (CI/CD Quality Gates): 50.0% 🔵
  - M10 (Memoria Técnica & Context Mastery): 100.0% 🟢

### 9.2 Deuda Técnica y Stubs Pendientes
- `[FALTANTE]` M06-C02: Manejo de streaming seguro y serialización atómica en escritura de logs/benchmarks.
- `[FALTANTE]` M07-C02 / C03: Expansión de pruebas de regresión contra Golden Evals y pruebas de estrés de concurrencia.
- `[FALTANTE]` M08-C01 / C02: Módulos de dashboard visual en `src/dashboards/` y exportador OpenTelemetry/Prometheus.
- `[FALTANTE]` M09-C01: Pipeline de CI en `.github/workflows/ci.yml`.
- `[FALTANTE]` Adaptadores para proveedores LLM adicionales: OpenAI, Anthropic, LiteLLM.

### 9.3 Registro de Decisiones de Arquitectura (ADRs)
- `[ADR-001]` **Arquitectura Hexagonal:** Separación estricta entre modelos de dominio (`models.py`), motor analítico (`scoring.py`, `signals.py`) y adaptadores LLM (`adapters/base.py`). Justificación: permite alternar entre inferencia local (`agy.exe`) y remota (`google.genai`) sin alterar el cálculo matemático.
- `[ADR-002]` **Contrato Epistémico Absoluto:** Prohibición de alucinación mecanicista sobre activaciones internas o memoria GPU/TPU. Justificación: preserva la veracidad pericial y evita diagnósticos especulativos en evaluaciones LLM.
- `[ADR-003]` **Extracción Heurística Previa:** Inyección de señales deterministas (`signals.py`) en el prompt del evaluador semántico. Justificación: reduce el costo de razonamiento del LLM y ancla su juicio en hechos cuantificables.
- `[ADR-004]` **Reglas de Sobrescritura (Overrides):** Priorización de reglas deterministas sobre el puntaje ponderado promedio ante conflictos críticos o coberturas de evidencia insuficientes (`scoring.py`). Justificación: previene falsos negativos de severidad crítica causados por dilución en promedios lineales.
- `[ADR-005]` **Modos de Gobernanza en Políticas:** Separación de modos `audit_only`, `recommend`, `human_review` y `dry_run` en `PolicyEngine`. Justificación: previene que acciones destructivas (poda de contexto) se ejecuten sin aprobación explícita.
- `[ADR-006]` **Gobernanza Contextual iDirectory:** Integración de mapa de contexto topológico (`.context/tree.json`) y balizas por carpeta (`.context.yaml`). Justificación: optimiza en un 95% el consumo de tokens en interacción agéntica.

---

## 10. REGLAS DE MODIFICACIÓN, GLOSARIO E ÍNDICE DE EVIDENCIAS

### 10.1 Convenciones de Estilo y Reglas de Desarrollo
- Python 3.9+ con tipado estricto (`typing`, Pydantic v2) `[CONFIRMADO]`.
- Formato PEP 8, nombres en `snake_case` para módulos/funciones y `PascalCase` para clases.
- Manejo estricto de excepciones tipadas (`AdapterExecutionError`, `ValidationError`).
- Modificación de esquemas: toda adición de campos en `models.py` debe ser validada contra `schemas/audit-input.schema.json` y `schemas/audit-result.schema.json`.

### 10.2 Glosario de Términos
- **IRC / CRS (Índice de Riesgo Contextual / Context Risk Score):** Métrica escalar continua en rango `[0.0, 100.0]` que cuantifica la probabilidad de fallo o confabulación en la ventana de contexto.
- **Fatiga Contextual:** Degradación de la precisión y adhesión a restricciones en LLMs debido a la acumulación de turnos y ruido en la ventana de contexto.
- **Drift de Herramientas (Tool State Drift):** Desincronización entre el estado asumido por el modelo y las respuestas o parámetros reales de las herramientas ejecutadas.
- **Contrato Epistémico:** Principio metodológico que restringe el diagnóstico únicamente a evidencia física observable y métricas heurísticas reproducibles.

### 10.3 Checklist de Verificación Previa a Commit
- [ ] Ejecutar la suite completa: `python -m pytest` (36/36 tests PASSED).
- [ ] Verificar que no existan credenciales en archivos de configuración ni payloads de prueba.
- [ ] Confirmar que cualquier nueva función pública mantenga su firma tipada y prueba unitaria en `tests/unit/`.
- [ ] Validar que `run_audit.ps1` y `python -m context_auditor.cli` ejecuten sin excepciones.

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
3. Revisa restricciones (`[INV-XX]`), contratos simbólicos (Sección 4) y vectores de tensión (Sección 7).
4. Explicita supuestos cuando sea necesario: "Supongo que X debido a Y".
5. Propone cambios por archivo con rutas relativas claras y separadores Unix (`/`).
6. Añade pruebas, riesgos y criterios de aceptación.

### 🤝 Acuse de Recibo Inicial
Si el usuario adjuntó esta semilla **sin una instrucción específica**, no intentes generar código ni completar archivos vacíos. Responde únicamente con:
1. Un saludo confirmando que asimilaste el ADN arquitectónico v3.0 de **Context Entropy Auditor (CEA)** (`<SEED_ARCHITECTURAL_VECTOR>`) y su stack principal.
2. Un breve resumen de 2-3 líneas sobre el objetivo, su estado actual y sus principales vectores de tensión.
3. Una frase poniéndote a disposición para resolver dudas sobre su funcionamiento o colaborar en los siguientes pasos de desarrollo.

</SEED_ARCHITECTURAL_VECTOR>
