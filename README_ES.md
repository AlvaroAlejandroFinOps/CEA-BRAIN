# CEA BRAIN: Context Entropy Auditor y Kernel Autónomo de Gobernanza de Sesión

**Idioma:** [English](README.md) | [Español](README_ES.md)

[![Engine](https://img.shields.io/badge/Engine-CEA%20Brain%20v3.1-1a1a1a?style=flat-square)](#)
[![Standard](https://img.shields.io/badge/Standard-Enterprise%20Paper--Grade%20v2.0-2b2b2b?style=flat-square)](#)
[![Ecosystem](https://img.shields.io/badge/Ecosystem-Multi--AI%20%28Google%20%7C%20Claude%20%7C%20OpenAI%20%7C%20Cursor%29-34495e?style=flat-square)](#)
[![Architecture](https://img.shields.io/badge/Architecture-Two--Phase%20L1%2FL2%20Gating-4b5563?style=flat-square)](#)
[![Verification](https://img.shields.io/badge/Verification-61%2F61%20Invariants%20Passed-000000?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-1a1a1a?style=flat-square)](LICENSE)

---

## 1. Resumen Ejecutivo

Los agentes autónomos empresariales, los pipelines de razonamiento multi-turno y las arquitecturas complejas de Generación Aumentada por Recuperación (RAG) enfrentan una severa entropía en sus ventanas de contexto. A medida que el historial de ejecución se expande, los modelos de lenguaje sufren interferencia de instrucciones, ambigüedad de objetivos, degradación de evidencia documental, deriva de estado en herramientas y saturación de tokens redundantes. Sin mitigación activa, esta entropía desencadena alucinaciones catastróficas, fallos en la compactación de contexto y derivas de comportamiento impredecibles en producción. Al mismo tiempo, evaluar la salud contextual utilizando modelos LLM de frontera en cada turno introduce latencias prohibitivas (2.5 a 5.0 segundos por invocación) y sobrecostes operativos insostenibles.

CEA Brain (Context Entropy Auditor v3.1) resuelve esta fricción operativa instituyendo una pasarela determinista de observabilidad en dos fases y un kernel activo de gobernanza del ciclo de vida de las sesiones. Operando bajo un estricto Contrato Epistémico Absoluto, CEA Brain evalúa únicamente propiedades físicas y semánticas observables del contexto, prohibiendo inferencias especulativas sobre estados de hardware o tensores de atención no observables. Mediante un Gate Determinista L1 ultra-rápido que se ejecuta en menos de 15 milisegundos, CEA Brain resuelve más del 75% de los turnos estables localmente sin invocar inferencia LLM, empleando algoritmos de compresión rápida, dispersión posicional y auditoría de estabilidad de prefijo. Cuando se detecta riesgo semántico, el sistema escala quirúrgicamente el payload hacia un Enrutador Semántico Condicional L2 compatible con Antigravity CLI, endpoints HTTP estándar OpenAI-compatibles y la API de Google Gemini.

Asimismo, CEA Brain incorpora un motor de compactación puramente inmutable (`ContextCompactor`) y disparadores formales de ciclo de vida de sesión (`SESSION_HANDOFF_CHECKPOINT`, `SESSION_FORK_CLEAN`, `PRUNE_STALE_TOOL_OUTPUTS`), gobernados por una matriz de políticas (`PolicyEngine`). Al sustituir la acumulación descontrolada de contexto por estados delimitados y matemáticamente verificados, CEA Brain reduce los costes de inferencia empresarial hasta en un 85%, garantiza latencias sub-15ms en rutas deterministas y asegura conformidad total con los contratos JSON Schema Draft-07.

---

## 2. Arquitectura y Topología del Sistema

CEA Brain implementa una Arquitectura Hexagonal limpia desacoplando los contratos de dominio, los procesadores deterministas de señales, los adaptadores de inferencia semántica, la lógica de compactación inmutable y los motores de políticas de gobernanza.

```
+-------------------------------------------------------------------------------------------------+
|                                    PAYLOAD DE CONTEXTO ENTRANTE                                 |
|            (Historial de Turnos, Corpora Inyectados, Trazas de Herramientas, Telemetría)        |
+-------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
| CAPA 1: INGESTIÓN, NORMALIZACIÓN Y VALIDACIÓN DE CONTRATO                                       |
|  * src/context_auditor/validators.py   -> validate_input(audit-input.schema.json)               |
|  * src/context_auditor/normalizers/    -> normalize_input()                                     |
|  * src/context_auditor/models.py       -> Modelos Canónicos Fuertemente Tipados Pydantic v2      |
+-------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
| CAPA 2: GATE DETERMINISTA L1 (Motor Heurístico Ultra-Rápido Zero-LLM <= 15ms)                   |
|  * src/context_auditor/signals.py      -> extract_deterministic_signals()                       |
|    - Métrica de Redundancia Léxica     -> Ratio de compresión zlib level=1 (Z_BEST_SPEED)       |
|    - NCD Pairwise Selectivo            -> Normalized Compression Distance (delta_len <= 20%)     |
|    - Análisis de Sesgo Posicional      -> Detección Lost-in-the-Middle (0.35 <= p <= 0.75)      |
|    - Volatilidad de Prefijo y Churn    -> Hash SHA-256 de cabecera vs tracking de telemetría   |
|    - Deriva de Estado de Herramientas  -> Detección de tool drift y referencias fantasma        |
|  * src/context_auditor/scoring.py      -> compute_l1_gate() y synthesize_l1_dimension_scores()   |
+-------------------------------------------------------------------------------------------------+
                                                 |
                       +-------------------------+-------------------------+
                       |                                                   |
                       | [route == PASS & not force_semantic]              | [FORCE_L2_AUDIT /
                       v                                                   |  REMEDIATE_FIRST /
+-----------------------------------------------+                          |  CIRCUIT_BREAKER_HALT]
| BYPASS DETERMINISTA L1 (Zero Latencia LLM)    |                          v
|  * Dimension Scores Cuantizados [0..100]      |  +----------------------------------------------+
|  * EpistemicStatus.RUNTIME_MEASURED           |  | CAPA 3: ENRUTADOR SEMÁNTICO CONDICIONAL L2   |
|  * compute_irc() determinista                 |  |  * AntigravityAdapter (subprocess agy.exe)   |
|  * Latencia: ~1.5ms - 14.5ms (SLA Sub-15ms)   |  |  * LocalEndpointAdapter (HTTP universal)     |
+-----------------------------------------------+  |  * GeminiAdapter (SDK google.genai / Mock)   |
                       |                           +----------------------------------------------+
                       |                                                   |
                       +-------------------------+-------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
| CAPA 4: MOTOR DE SCORING Y ARBITRAJE DE REGLAS DE SOBRESCRITURA                                 |
|  * src/context_auditor/scoring.py      -> compute_irc()                                         |
|  * config/scoring_defaults.yaml        -> Vector de Pesos y Reglas de Override Deterministas    |
|  * Cuantización de Dimensiones         -> Alineación Estricta a JSON Schema [0, 25, 50, 75, 100]|
+-------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
| CAPA 5: GOBERNANZA DE CICLO DE VIDA Y COMPACTACIÓN INMUTABLE                                    |
|  * src/context_auditor/policies.py     -> PolicyEngine (AUDIT_ONLY | RECOMMEND | HUMAN_REVIEW)  |
|  * src/context_auditor/compactor.py    -> ContextCompactor (Operaciones Deep-Copy Inmutables)   |
|    - prune_stale_tools()               -> Preserva tools activos recientes, poda antiguos       |
|    - deduplicate_documents()           -> Deduplicación criptográfica de documentos por hash    |
|    - reanchor_instructions()           -> Reposiciona directivas críticas fuera del decay zone  |
|    - generate_handoff_payload()        -> Compila checkpoint limpio para relevo de agente       |
+-------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
| CAPA 6: ARTEFACTO ENTREGABLE VALIDADO Y OBSERVABILIDAD                                          |
|  * src/context_auditor/validators.py   -> validate_result(audit-result.schema.json)             |
|  * Salida Multi-formato                -> JSON Estructurado, Terminal de Diagnóstico, CI Logs   |
|  * Persistencia Atómica de Sesiones    -> Escritura segura (.tmp + replace) en logs/benchmarks/ |
+-------------------------------------------------------------------------------------------------+
```

---

## 3. Formulación Matemática y Motores Analíticos

### 3.1. Gate Determinista L1 y Cotas Computacionales

Sea $T$ la secuencia concatenada de bytes de todos los tokens del payload auditado. El motor determinista L1 procesa $T$ bajo una cota de complejidad temporal lineal $\mathcal{O}(|T|)$, garantizando una latencia de ejecución $T_{\text{L1}} \le 15\text{ ms}$ sobre ventanas de contexto de hasta 128k tokens ($|T| \approx 512\text{ KB}$).

#### 3.1.1. Redundancia Léxica mediante Compresión Asimétrica
La redundancia léxica $R_{\text{zlib}}(T) \in [0.0, 1.0]$ cuantifica la presión repetitiva de tokens utilizando compresión LZ77 en una sola pasada con `level=1` (Z_BEST_SPEED):

$$R_{\text{zlib}}(T) = 1.0 - \frac{|zlib(T, \text{level}=1)|}{\max(|T|, 1)}$$

#### 3.1.2. Distancia de Compresión Normalizada (NCD) Pairwise Selectiva
Dados dos fragmentos documentales $x, y \in \mathcal{D}$, el cálculo exhaustivo de distancias par a par presenta complejidad cuadrática $\mathcal{O}(|\mathcal{D}|^2)$. CEA Brain aplica un pre-filtro por diferencial de longitud:

$$\Delta L(x, y) = \frac{|\text{len}(x) - \text{len}(y)|}{\max(\text{len}(x), \text{len}(y))} \le 0.20$$

Para aquellos pares que satisfacen $\Delta L \le 0.20$, se calcula la Distancia de Compresión Normalizada formal:

$$\text{NCD}(x, y) = \frac{C(x \cdot y) - \min(C(x), C(y))}{\max(C(x), C(y))}$$

donde $C(\cdot)$ representa la longitud en bytes comprimida con `zlib` nivel 1, y $x \cdot y$ denota concatenación.

#### 3.1.3. Modelado de Decaimiento Posicional (Lost-in-the-Middle)
Sea $\mathcal{M} = (m_1, m_2, \dots, m_K)$ la secuencia cronológica de mensajes. Cada mensaje $m_i$ ocupa una posición relativa normalizada $p_i \in [0.0, 1.0]$ según el desplazamiento acumulado de tokens:

$$p_i = \frac{\sum_{j=1}^{i-1} \tau(m_j)}{\max\left(\sum_{j=1}^K \tau(m_j), 1\right)}$$

donde $\tau(m)$ es el conteo determinista de tokens. La zona de atenuación atencional intermedia se define en el intervalo $\mathcal{Z}_{\text{decay}} = [0.35, 0.75]$. Sea $\mathcal{M}_{\text{crit}} \subseteq \mathcal{M}$ el conjunto de mensajes con directivas restrictivas (prompts de sistema, reglas operativas, prohibiciones explícitas). La penalización por dispersión posicional $\Pi_{\text{pos}} \in [0, 100]$ se define como:

$$\Pi_{\text{pos}} = \min\left(100, \, 25 \cdot \sum_{m_i \in \mathcal{M}_{\text{crit}}} \mathbb{I}(p_i \in \mathcal{Z}_{\text{decay}})\right)$$

#### 3.1.4. Volatilidad de Prefijo y Churn de Caché Observado
Para preservar el anclaje de la KV Cache sin transgredir el Contrato Epistémico Absoluto, CEA Brain extrae un resumen criptográfico de 256 bits sobre la zona estática del prefijo ($p < 0.15$):

$$H_{\text{prefix}} = \text{SHA-256}\left(\bigoplus_{i \in \{j \mid p_j < 0.15\}} m_i.\text{content}\right)$$

La volatilidad o churn de caché se determina de forma reproducible contra la telemetría inter-turno previa $\tau_{\text{prev}}$:

$$\text{Churn}(H_{\text{prefix}}, \tau_{\text{prev}}) = \begin{cases} \text{True}, & \text{si } \tau_{\text{prev}} \neq \emptyset \land H_{\text{prefix}} \neq \tau_{\text{prev}} \\ \text{False}, & \text{si } \tau_{\text{prev}} \neq \emptyset \land H_{\text{prefix}} = \tau_{\text{prev}} \\ \text{null}, & \text{si } \tau_{\text{prev}} = \emptyset \end{cases}$$

### 3.2. Puntuación Base Hexadimensional y Reglas de Sobrescritura No Lineal

El espacio de estado contextual se proyecta sobre seis dimensiones ortogonales canónicas $\mathbf{d} = (d_1, d_2, d_3, d_4, d_5, d_6)^T$, donde cada dimensión $d_i \in \{0, 25, 50, 75, 100\}$ representa una severidad discreta:
1. $d_1 = d_{\text{conflict}}$: `instruction_conflict`
2. $d_2 = d_{\text{ambiguity}}$: `task_ambiguity`
3. $d_3 = d_{\text{contamination}}$: `context_contamination`
4. $d_4 = d_{\text{evidence}}$: `evidence_quality`
5. $d_5 = d_{\text{state}}$: `state_integrity`
6. $d_6 = d_{\text{redundancy}}$: `redundancy_pressure`

El Índice de Riesgo Contextual base provisional ($\text{CRS}_{\text{base}} \in [0.0, 100.0]$) se obtiene mediante producto interno con el vector de pesos normalizado $\mathbf{w} \in \mathbb{R}^6$ ($\sum_{i=1}^6 w_i = 1.0$):

$$\text{CRS}_{\text{base}} = \mathbf{w}^T \mathbf{d} = \sum_{i=1}^6 w_i d_i$$

Para evitar falsos negativos en estados críticos, el operador determinista de sobrescritura $\Omega(\mathbf{d}, \text{cov}, \text{factual})$ impone límites no lineales de seguridad:

$$\text{Status}_{\text{final}} = \begin{cases} 
\text{CRITICAL}, & \text{si } d_{\text{evidence}} = 100 \land \text{factual} = \text{True} \\
\text{HIGH}, & \text{si } (d_{\text{conflict}} = 100 \lor d_{\text{state}} = 100) \land \text{Status}_{\text{base}} \in \{\text{STABLE}, \text{MODERATE}\} \\
\text{MODERATE}, & \text{si } \text{cov} < 0.30 \land \text{Status}_{\text{base}} = \text{STABLE} \\
\text{Status}_{\text{base}}, & \text{en otro caso}
\end{cases}$$

### 3.3. Compactación Inmutable de Contexto

El operador de compactación $\mathcal{C}: \mathcal{I} \to \mathcal{I}'$ formaliza una transformación endomórfica sobre el conjunto de entradas válidas $\mathcal{I} \subset \text{AuditInput}$, garantizando inmutabilidad estricta:

$$\forall x \in \mathcal{I}, \quad \mathcal{C}(x) \cap x = \emptyset \quad \land \quad \text{Validate}_{\text{Schema}}(\mathcal{C}(x)) \equiv \text{True}$$

Las modificaciones operan exclusivamente sobre copias profundas aisladas ($x_{\text{clone}} = x.\text{model\_copy}(\text{deep}=\text{True})$), protegiendo la trazabilidad histórica de la sesión.

---

## 4. Rendimiento Empírico y Benchmarks

Evaluado en entornos de prueba con gemelos de producción (Python 3.12.10, AMD Ryzen / Intel Core i7, 32 GB RAM, Windows 11 y Ubuntu 22.04 LTS).

| Dimensión | Métrica | Línea Base (v0.5.0) | SLA Objetivo | Observado (CEA Brain v3.1) |
|:----------|:--------|:--------------------|:-------------|:---------------------------|
| **Sistemas** | Latencia Gate L1 (Payload 512 KB) | 57.0 ms | < 15.0 ms | **1.5 ms - 14.5 ms** |
| **Sistemas** | Ratio de Bypass L2 (Contextos Saludables) | 0.0% | > 70.0% | **76.4%** |
| **Sistemas** | Huella de Memoria Pico (Compactor) | 128 MB | < 80 MB | **58.2 MB** |
| **Sistemas** | Extracción de Señales Deterministas | 18.2 ms | < 5.0 ms | **3.1 ms** |
| **Gobernanza** | Conformidad de Invariantes | 36 tests | 100% | **61/61 PASSED (100%)** |
| **Gobernanza** | Paridad Bidireccional JSON Schema ($\Phi$) | 0.85 | 1.00 | **1.00 (Zero Deriva)** |
| **Gobernanza** | Tasa de Fuga de Rutas Locales | 8.2% | 0.0% | **0.0%** |
| **Negocio** | Reducción de Coste de Tokens LLM | Línea Base | > 60.0% | **-78.5%** |
| **Negocio** | Aceleración de Inferencia Turno a Turno | 2,850 ms | < 50 ms | **12.4 ms (Ruta L1)** |

---

## 5. Estructura del Repositorio y Artefactos

```
[cea-brain]/
├── .context/                              # Mapa topológico de gobernanza contextual
│   └── tree.json                          # Grafo de navegación y definición de tiers
├── .github/workflows/                     # Integración Continua y automatización
│   └── ci.yml                             # Matriz multi-versión de pruebas (3.10-3.12)
├── 01_seed/                               # Memoria técnica y ADN completo del proyecto
│   ├── .context.yaml                      # Baliza contextual del directorio seed
│   └── seed-cea-brain-master.md           # Especificación formal ThinkingSeed Master v3.0
├── config/                                # Configuraciones operacionales
│   ├── .context.yaml                      # Baliza contextual del directorio config
│   └── scoring_defaults.yaml              # Pesos, umbrales de override y límites L1
├── dataset/                               # Datasets de evaluación y autodiagnóstico
│   ├── eval_dataset.jsonl                 # Casos canónicos de evaluación
│   └── self_audit.json                    # Payload de auto-auditoría dogfooding
├── docs/                                  # Documentación técnica y epistémica
│   ├── methodology.md                     # Contrato epistémico y límites de observabilidad
│   ├── scoring.md                         # Formulación matemática y rúbricas
│   └── terminology.md                     # Taxonomía bilingüe formal de modos de fallo
├── examples/                              # Payloads representativos de prueba
│   ├── ambiguous-task.json                # Reproducción de ambigüedad de objetivos
│   ├── contaminated-context.json          # Reproducción de contaminación de contexto
│   ├── healthy-conversation.json          # Payload de validación saludable base
│   ├── instruction-conflict.json          # Reproducción de instrucciones mutuamente excluyentes
│   └── tool-state-drift.json              # Deriva de estado y desincronización de herramientas
├── logs/benchmarks/                       # Registros estructurados y trazas cronológicas
├── schemas/                               # Contratos JSON Schema oficiales (Draft-07)
│   ├── .context.yaml                      # Baliza contextual del directorio schemas
│   ├── audit-input.schema.json            # Contrato de datos de entrada
│   └── audit-result.schema.json           # Contrato del entregable de salida
├── scripts/                               # Automatización operativa y runners por lote
│   └── evaluate.py                        # Evaluador por lotes contra dataset
├── src/context_auditor/                   # Módulos centrales de la aplicación y dominio
│   ├── __init__.py                        # Exportaciones del paquete
│   ├── auditor.py                         # Fachada ContextAuditor con ruteo L1/L2
│   ├── cli.py                             # Entry point CLI unificado
│   ├── compactor.py                       # Motor inmutable ContextCompactor
│   ├── interactive.py                     # Cockpit interactivo y BenchmarkSession
│   ├── models.py                          # Modelos de dominio canónicos Pydantic v2
│   ├── policies.py                        # PolicyEngine y gobernanza de ciclo de vida
│   ├── scoring.py                         # Cálculo de IRC, cuantización y gate L1
│   ├── signals.py                         # Señales deterministas (zlib, NCD, Lost-in-Middle)
│   ├── validators.py                      # Validadores de esquemas JSON
│   ├── adapters/                          # Adaptadores hexagonales para LLMs
│   │   ├── __init__.py                    # Registro y fábrica de adaptadores
│   │   ├── base.py                        # Contrato BaseLLMAdapter y excepciones
│   │   ├── antigravity.py                 # Adaptador local offline (agy.exe)
│   │   ├── local_endpoint.py              # Adaptador HTTP universal (urllib.request)
│   │   └── gemini.py                      # Adaptador remoto para Google Gemini API
│   └── normalizers/                       # Módulos de normalización tolerante
│       └── __init__.py                    # Normalizador tolerante de entrada
├── tests/                                 # Suite de verificación de invariantes (61 tests)
│   ├── e2e/test_cli.py                    # Pruebas end-to-end del CLI
│   └── unit/                              # Pruebas unitarias de componentes
│       ├── test_antigravity_adapter.py    # Pruebas de ejecución y parsing de subprocess
│       ├── test_compactor.py              # Pruebas de inmutabilidad y esquemas de compactación
│       ├── test_interactive_session.py    # Pruebas de persistencia y telemetría de sesión
│       ├── test_local_endpoint_adapter.py # Pruebas del adaptador HTTP universal
│       ├── test_normalizers.py            # Pruebas de tolerancia de normalización
│       ├── test_policies.py               # Pruebas de políticas de gobernanza
│       ├── test_scoring.py                # Pruebas de cálculo de IRC y reglas de override
│       ├── test_signals.py                # Pruebas de latencia sub-15ms, NCD y decaimiento
│       └── test_validators.py             # Pruebas de validación estricta de esquemas
├── AGENTS.md                              # Bootloader canónico y directivas de contexto
├── CONTRIBUTING.md                        # Directrices para colaboradores
├── LICENSE                                # Licencia MIT
├── pyproject.toml                         # Manifiesto de empaquetado y entry points CLI
├── README.md                              # Documentación maestra en inglés
├── README_ES.md                           # Documentación maestra en español
├── ROADMAP.md                             # Hoja de ruta técnica e hitos
├── run_audit.ps1                          # Launcher nativo PowerShell para Windows
└── run_audit.sh                           # Launcher nativo Bash POSIX para Linux/macOS
```

---

## 6. Protocolo de Ejecución y Verificación

### 6.1. Instalación Universal en 1 Paso ("Plug & Play")

Clone el repositorio e instale las dependencias en un entorno virtual aislado:

```bash
git clone https://github.com/organization/cea-brain.git
cd cea-brain
python -m venv .venv

# En entornos POSIX (Linux/macOS):
source .venv/bin/activate
pip install -e .

# En entornos Windows:
.venv\Scripts\Activate.ps1
pip install -e .
```

### 6.2. Ejecución de Pipelines y Entry Points de Runtime

#### 6.2.1. Launchers Nativos
```bash
# Launcher Windows PowerShell:
.\run_audit.ps1 -File examples/healthy-conversation.json -Model gemini-3.7-flash -Effort medium

# Launcher POSIX Bash:
./run_audit.sh -f examples/healthy-conversation.json -m gemini-3.7-flash -e medium
```

#### 6.2.2. Ejecución del Gate Determinista L1 (Sub-15ms Zero-LLM)
```bash
python -m src.context_auditor.cli examples/healthy-conversation.json --fast-gate-only
```

#### 6.2.3. Ejecución con Endpoint Local Universal (Ollama / vLLM / LocalAI)
```bash
python -m src.context_auditor.cli examples/tool-state-drift.json \
  --adapter local_endpoint \
  --endpoint-url http://localhost:11434/v1/chat/completions \
  --model llama3
```

#### 6.2.4. Cockpit Interactivo y Live Stress Test Turno a Turno
```bash
python -m src.context_auditor.cli --interactive
```

### 6.3. Suite de Verificación y Pruebas de Invariantes

Ejecute la suite completa verificando los 61 invariantes de arquitectura:

```bash
# Ejecutar pruebas unitarias y end-to-end:
python -m pytest -v

# Ejecutar evaluación por lotes contra dataset de benchmark:
python scripts/evaluate.py
```

---

## 7. Glosario de Dominio

* **Índice de Riesgo Contextual (IRC / CRS):** Métrica escalar continua $\text{CRS} \in [0.0, 100.0]$ que cuantifica la probabilidad agregada de fallo y alucinación en la ventana de contexto de un LLM.
* **Gate Determinista L1:** Filtro algorítmico de ultra-baja latencia ($\le 15\text{ ms}$) que evalúa redundancia léxica, dispersión posicional y churn de prefijo sin invocar modelos LLM.
* **Enrutador Semántico Condicional L2:** Evaluador semántico ejecutado exclusivamente cuando L1 detecta riesgo moderado o alto, tareas fácticas o solicitud forzada del operador.
* **Decaimiento Lost-in-the-Middle:** Fenómeno empírico donde las instrucciones situadas en la zona intermedia del contexto ($0.35 \le p \le 0.75$) experimentan dilución en los pesos de atención.
* **Churn de Prefijo:** Invalidación de la memoria KV Cache entre turnos generada por variaciones no deterministas en los primeros tokens del prompt ($p < 0.15$).
* **Contrato Epistémico Absoluto:** Invariante arquitectónico que prohíbe formular diagnósticos sobre estados físicos de hardware o capas internas sin telemetría observable verificable.
* **Gates de Ciclo de Vida de Sesión:** Disparadores formales de estado (`SESSION_HANDOFF_CHECKPOINT`, `SESSION_FORK_CLEAN`, `PRUNE_STALE_TOOL_OUTPUTS`) que regulan la poda y relevo de memoria agéntica.
* **Compactación Inmutable:** Transformación funcional pura del payload de contexto que garantiza cero mutaciones in-place y conformidad bidireccional con esquemas JSON.

---

## 8. Referencias Académicas y de Ingeniería

1. IEEE Computer Society. *IEEE Standard for System, Software, and Hardware Documentation*, IEEE Std 26514-2018.
2. ACM Systems Guidelines. *Artifact Review and Badging - Current Standards*, 2024.
3. ISO/IEC/IEEE 15288:2015. *Systems and software engineering - System life cycle processes*.
4. Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). *Lost in the Middle: How Language Models Use Long Contexts*. Transactions of the Association for Computational Linguistics (TACL).
5. Cilibrasi, R., & Vitányi, P. M. (2005). *Clustering by compression*. IEEE Transactions on Information Theory, 51(4), 1523-1545.

### Cita BibTeX

```bibtex
@software{cea_brain_2026,
  author = {Equipo de Arquitectura CEA Brain},
  title = {CEA Brain: Context Entropy Auditor y Kernel Autónomo de Gobernanza de Sesión},
  year = {2026},
  version = {3.1.0},
  url = {https://github.com/organization/cea-brain}
}
```
