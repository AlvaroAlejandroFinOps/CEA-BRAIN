# Análisis del Plan Maestro CEA → Estrategia de Implementación Gradual

## Resumen Ejecutivo

El documento [INSTRUCCION_MAESTRA_CONTEXT_ENTROPY_AUDITOR.md](file:///d:/0001 HyperScale Thinking/PROYECTOS CLOUD/Research and Development/Context Entropy Auditor (CEA)/artifacts/plans/active/01 PLAN GPT 5.6 SOL THINKING/INSTRUCCION_MAESTRA_CONTEXT_ENTROPY_AUDITOR.md) es un plan exhaustivo de ~1150 líneas que define la evolución del proyecto desde un prompt inyectable hacia un framework abierto de confiabilidad contextual. El plan fue generado con GPT 5.6 SOL Thinking y es técnicamente sólido, pero necesita descomponerse en unidades de trabajo ejecutables.

---

## 1. Diagnóstico del Estado Actual del Repositorio

### Lo que existe

| Componente | Estado | Contenido |
|---|---|---|
| [Context Entropy Auditor.md](file:///d:/0001 HyperScale Thinking/PROYECTOS CLOUD/Research and Development/Context Entropy Auditor (CEA)/Context Entropy Auditor.md) | Prompt v0 funcional | 54 líneas, prompt inyectable con 7 dimensiones, formato tabular |
| [EngineReadme.md](file:///d:/0001 HyperScale Thinking/PROYECTOS CLOUD/Research and Development/Context Entropy Auditor (CEA)/Engine/EngineReadme.md) | Manifiesto de gobernanza | Estructura corporativa HyperScale estándar |
| `schemas/` | **Vacío** | Sin JSON Schemas |
| `tests/` | **Vacío** | Sin pruebas |
| `config/` | **Vacío** | Sin configuración |
| `src/data_generation/` | **Vacío** | Sin código de generación |
| `src/fabric_jobs/` | **Vacío** | Sin pipelines |
| `docs/*/` | **Vacíos** | Sin documentación técnica |
| `data/raw,processed,sandbox/` | **Vacíos** | Sin datasets |

### Conclusión: El proyecto consiste en el prompt original y la estructura de directorios. Todo lo demás está por construir.

---

## 2. Evaluación del Plan Maestro

### Fortalezas

1. **Disciplina epistémica rigurosa** — El contrato `observed/inferred/runtime_measured/unknown` es el diferenciador más fuerte del proyecto. Ningún framework similar lo tiene tan bien definido.

2. **Correcciones necesarias al prompt** — Identifica correctamente las afirmaciones no verificables del prompt original (cabezales de atención, KV Cache, "token exacto de inicio").

3. **Modelo de scoring bien diseñado** — Las 6 dimensiones del IRC con rúbrica discreta (0/25/50/75/100) y reglas de sobrescritura son pragmáticas y calibrables.

4. **Separación de responsabilidades clara** — Normalización → Señales → Evaluación → Scoring → Políticas → Presentación es una pipeline correcta.

5. **Pragmatismo en la publicación** — La estrategia de publicar rigor metodológico antes que amplitud funcional es acertada.

### Riesgos y Tensiones

> [!WARNING]
> **Riesgo 1: Scope Creep** — El plan contiene ~250 tareas implícitas en 21 secciones. Las secciones 9 (compactación), 11 (RAG), 12 (evaluación continua) son extensiones que no deberían estar en el horizonte de las primeras 3 fases.

> [!WARNING]  
> **Riesgo 2: Estructura actual vs. estructura objetivo** — El plan propone una estructura de repo (`context-entropy-auditor/`) diferente a la estructura HyperScale existente. Hay que decidir: ¿se migra o se adapta?

> [!IMPORTANT]
> **Riesgo 3: Dependencia de evaluación semántica** — El evaluador semántico (sección 4.3) requiere un LLM para funcionar. Esto crea una dependencia circular: se necesita un LLM para auditar LLMs. El plan lo reconoce implícitamente pero no lo resuelve explícitamente en el orden de trabajo.

> [!NOTE]
> **Tensión 4: Dataset antes de SDK** — El plan pide 80-120 casos etiquetados (Fase 3) antes del SDK (Fase 4). Esto es correcto metodológicamente pero lento operativamente. Un camino híbrido puede crear 20 casos con el SDK mínimo y crecer iterativamente.

---

## 3. Delta: Prompt Original vs. Plan Maestro

| Aspecto | Prompt Original (v0) | Plan Maestro (objetivo) |
|---|---|---|
| Nombre métrica | Puntuación 0-100 sin nombre formal | IRC (Índice de Riesgo Contextual) |
| Dimensiones | 7 dimensiones con términos mecánicos | 6 dimensiones redefinidas sin afirmaciones internas |
| Epistémico | Sin clasificación epistémica | 4 categorías obligatorias |
| `Lost-in-the-Middle` | Tratado como falla confirmada | Reclasificado como riesgo potencial |
| `Trajectory Lock-in` | Propagación autoregresiva (mecanicista) | `observable_error_propagation` (evidencial) |
| Salida | Markdown tabular, formato fijo | JSON Schema versionado + múltiples presentadores |
| Rúbrica | Nula/Baja/Media/Alta/Crítica (5 niveles) | 0/25/50/75/100 (5 valores discretos) |
| Confianza/Cobertura | No existe | Campos obligatorios separados del riesgo |
| Acciones | Plan textual libre | Acciones tipadas con `destructive` y `requires_approval` |

---

## 4. Propuesta de Implementación Gradual

### Filosofía: "Increments que producen valor demostrable"

Cada incremento debe dejar el proyecto en un estado usable y verificable. No hay incrementos puramente preparatorios.

---

### Incremento 0 — Fundación Epistémica (1-2 sesiones)

**Objetivo**: Documentar el "por qué" y "qué no" del proyecto. Sin código.

**Entregables**:
- `docs/methodology.md` — Contrato epistémico, glosario, capacidades vs. no-capacidades
- `docs/scoring.md` — 6 dimensiones con rúbricas completas (criterios por nivel)
- `docs/terminology.md` — Glosario bilingüe  
- `ROADMAP.md` — Plan público de fases
- Archivar prompt original como `prompts/v0-original.md` (copia histórica)

**Criterio de aceptación**: Una persona externa lee la documentación y entiende qué mide CEA y qué **no** mide.

---

### Incremento 1 — Prompt Core v0.1 (1-2 sesiones)

**Objetivo**: Producir un prompt corregido y usable manualmente.

**Entregables**:
- `prompts/auditor-simple-es.md` — Modo personal en español
- `prompts/auditor-simple-en.md` — Modo personal en inglés
- `prompts/auditor-technical-es.md` — Modo técnico en español
- `prompts/auditor-technical-en.md` — Modo técnico en inglés

**Cambios clave respecto al prompt v0**:
1. Eliminar "deja de responder normalmente"
2. Reemplazar "token exacto" por rangos observables
3. Sustituir `Trajectory Lock-in` → `observable_error_propagation`
4. Reclasificar `Lost-in-the-Middle` como riesgo potencial
5. Introducir IRC, confianza, cobertura
6. Añadir clasificación epistémica obligatoria en cada hallazgo
7. Añadir campo `limitations` en la salida

**Criterio de aceptación**: El prompt produce hallazgos con evidence_refs y reconoce falta de información.

---

### Incremento 2 — Esquemas y Modelos de Datos v0.2 (2-3 sesiones)

**Objetivo**: Convertir la salida del auditor en un contrato programático verificable.

**Entregables**:
- `schemas/audit-input.schema.json` — JSON Schema de entrada normalizada
- `schemas/audit-result.schema.json` — JSON Schema de resultado
- `examples/healthy-conversation.json` — Caso saludable
- `examples/ambiguous-task.json` — Ambigüedad de tarea
- `examples/contaminated-context.json` — Contaminación contextual
- `examples/instruction-conflict.json` — Conflicto de instrucciones
- `examples/tool-state-drift.json` — Deriva de herramientas
- `src/context_auditor/models.py` — Dataclasses/Pydantic tipados
- `src/context_auditor/validators.py` — Validación contra schema
- `tests/unit/test_validators.py` — Tests de validación positivos y negativos

**Criterio de aceptación**: Toda salida se valida determinísticamente. Un JSON inválido falla con error descriptivo.

---

### Incremento 3 — Scoring Engine v0.3 (2-3 sesiones)

**Objetivo**: Motor de puntuación reproducible, separado del LLM.

**Entregables**:
- `src/context_auditor/scoring.py` — Cálculo de IRC con pesos configurables
- `src/context_auditor/policies.py` — Motor de políticas (audit_only, recommend, human_review, dry_run)
- `config/scoring_defaults.yaml` — Pesos y umbrales provisionales
- `tests/unit/test_scoring.py` — Tests de scoring con fixtures
- `tests/unit/test_policies.py` — Tests de reglas de sobrescritura

**Fórmula implementada**:
```
IRC = 0.20*instruction_conflict + 0.20*task_ambiguity + 0.20*context_contamination 
    + 0.15*evidence_quality + 0.15*state_integrity + 0.10*redundancy_pressure
```

**Criterio de aceptación**: Dado un JSON de scores por dimensión, el motor calcula IRC, aplica sobrescrituras y produce un resultado reproducible sin LLM.

---

### Incremento 4 — Señales Deterministas + Normalizador v0.4 (3-4 sesiones)

**Objetivo**: Extraer métricas objetivas del contexto sin necesidad de LLM.

**Entregables**:
- `src/context_auditor/normalizers/` — Normalizadores de entrada (mensajes, documentos, tool_events)
- `src/context_auditor/signals.py` — Extractor de señales deterministas
- `tests/unit/test_normalizers.py`
- `tests/unit/test_signals.py`
- 10 fixtures de normalización en `tests/fixtures/`

**Señales deterministas iniciales**:
- Conteo de mensajes/turnos
- Tokens estimados (tiktoken o equivalente)
- Proporción de contexto utilizado
- Documentos/fuentes distintas
- Duplicación exacta de contenido
- IDs repetidos o ausentes
- Resultados de herramientas reemplazados
- Antigüedad del último objetivo explícito

**Criterio de aceptación**: Las señales se calculan sobre JSON normalizado y producen resultados idénticos en cada ejecución.

---

### Incremento 5 — SDK Mínimo + CLI v0.5 (3-4 sesiones)

**Objetivo**: Un desarrollador puede auditar un JSON desde código o terminal.

**Entregables**:
- `src/context_auditor/auditor.py` — Clase Auditor principal
- `src/context_auditor/cli.py` — CLI con Click/Typer
- `src/context_auditor/providers/` — Adaptador inicial (OpenAI o Gemini)
- `pyproject.toml` — Empaquetado
- `README.md` — Documentación pública
- `tests/integration/test_auditor.py`

**Comandos implementados**:
```bash
context-auditor inspect conversation.json
context-auditor validate audit-result.json
context-auditor compare baseline.json candidate.json
```

**Criterio de aceptación**: `pip install -e .` funciona, el CLI audita un JSON de ejemplo y produce un resultado válido.

---

### Incremento 6 — Dataset + Evaluación Inicial v0.6 (4-5 sesiones)

**Objetivo**: Demostrar que el scoring es evaluable y no solo un prompt.

**Entregables**:
- `datasets/context-regression/` — 30-50 casos etiquetados iniciales
- `evaluation/metrics.py` — Precisión, recall, error de severidad, concordancia
- `evaluation/reports/` — Informe de evaluación inicial
- `tests/adversarial/` — 10-15 casos adversariales
- Ajustes trazables de pesos/umbrales documentados en `CHANGELOG.md`

**Criterio de aceptación**: Se documenta precisión/recall por dimensión con al menos 30 casos. Los pesos se ajustan con justificación.

---

### Incremento 7 — Publicación Pública v0.7→v1.0 (2-3 sesiones)

**Objetivo**: Repositorio listo para contribuciones externas.

**Entregables**:
- `LICENSE` (Apache 2.0)
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`
- `CHANGELOG.md` completo
- CI/CD (lint, tests, validación de schemas)
- Release `v0.5-public` o similar según estado real

---

## 5. Mapeo Plan Maestro → Incrementos

| Sección del Plan | Incremento |
|---|---|
| §1 Visión, §2 Principios | Inc 0 |
| §14 Fase 0 (definición conceptual) | Inc 0 |
| §14 Fase 1 (Prompt Core) | Inc 1 |
| §4.1 Normalizador | Inc 4 |
| §4.2 Señales deterministas | Inc 4 |
| §4.3 Evaluador semántico | Inc 5 (parcial) |
| §4.4 Motor de puntuación | Inc 3 |
| §4.5 Motor de políticas | Inc 3 |
| §4.6 Presentadores | Inc 5 |
| §5 Modelo de puntuación | Inc 0 (diseño) + Inc 3 (código) |
| §6 Contrato de salida | Inc 2 |
| §7.1 Modo personal | Inc 1 |
| §7.2 Modo técnico | Inc 5 |
| §7.3 Modo organizacional | **Diferido** (post v1.0) |
| §8 SDK y API | Inc 5 |
| §9 Compactación/Routing | **Diferido** (post v1.0) |
| §10 Dataset/Evaluación | Inc 6 |
| §11 Auditoría RAG | **Diferido** (v0.8+) |
| §12 Evaluación continua | **Diferido** (v0.8+) |
| §13 Estructura del repo | Progresivo Inc 0-7 |
| §14 Fases 2-5 | Inc 2-7 |
| §15 Publicación temprana | Inc 7 |
| §16 README | Inc 5+7 |
| §17 Seguridad | Inc 5+7 |
| §18 Calidad | Transversal |
| §19 Reglas de decisión | Transversal |
| §20 Orden de trabajo | Mapeado a Inc 0-7 |

---

## 6. Lo que el plan difiere explícitamente (no olvidar)

Estas secciones están correctamente **fuera del alcance MVP** pero deben mantenerse visibles en el roadmap:

1. **§9 Compactación adaptativa** — Candidatos y planes de compactación (v0.8+)
2. **§9.2 Routing adaptativo** — Recomendaciones de escalamiento de modelo (v0.8+)
3. **§11 Auditoría RAG completa** — Pipeline de evaluación de retrieval (v0.8+)
4. **§12 Evaluación continua** — Regresiones sobre versiones de prompts/modelos (v1.0+)
5. **§7.3 Modo organizacional** — Políticas corporativas, tenancy, permisos (v1.0+)
6. **`auto_recover`** — Modo de política con recuperación automática (post v1.0)

---

## User Review Required

> [!IMPORTANT]
> **Decisión de estructura del repositorio**: El plan propone una estructura plana (`context-entropy-auditor/`) pero el repo actual usa la estructura HyperScale corporativa (`Engine/`, `Artefactos/`, `001_Seed/`). ¿Creamos el paquete Python dentro de la estructura existente (ej: `src/context_auditor/`) o reestructuramos hacia el modelo del plan?

> [!IMPORTANT]
> **Lenguaje primario del código**: El plan dice bilingüe (ES/EN). La convención estándar de open-source es código y API en inglés, documentación bilingüe. ¿Confirmamos inglés para código + español/inglés para docs y prompts?

> [!IMPORTANT]
> **Proveedor LLM inicial**: El evaluador semántico necesita un LLM. ¿Cuál es el proveedor prioritario para el primer adaptador? (OpenAI, Gemini, Anthropic, agnóstico con LiteLLM?)

## Verification Plan

### Automated Tests
- Cada incremento incluye sus propios tests unitarios
- `pytest` como runner principal
- Validación de JSON Schemas con `jsonschema`
- Linting con `ruff`

### Manual Verification
- Incremento 1: Ejecutar prompts manualmente en al menos 2 LLMs y verificar que la salida cumple el contrato epistémico
- Incremento 5: `pip install -e .` + `context-auditor inspect examples/contaminated-context.json`
- Incremento 6: Revisar informe de evaluación con métricas documentadas
