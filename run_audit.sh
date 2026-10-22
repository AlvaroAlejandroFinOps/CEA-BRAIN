#!/usr/bin/env bash
# Context Entropy Auditor (CEA) - POSIX Shell Runner
set -euo pipefail

FILE=""
MODEL="gemini-3.7-flash"
EFFORT="medium"
INTERACTIVE=false

usage() {
    echo "Usage: $0 [-f file] [-m model] [-e effort] [-i]"
    echo "  -f <path>    Path to JSON audit input file"
    echo "  -m <model>   Model identifier (default: gemini-3.7-flash)"
    echo "  -e <effort>  Reasoning effort: low|medium|high|max (default: medium)"
    echo "  -i           Launch interactive benchmark and live stress testing menu"
    exit 1
}

while getopts "f:m:e:ih" opt; do
    case "${opt}" in
        f) FILE="${OPTARG}" ;;
        m) MODEL="${OPTARG}" ;;
        e) EFFORT="${OPTARG}" ;;
        i) INTERACTIVE=true ;;
        h|*) usage ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${SCRIPT_DIR}/src"

echo "================================================================="
echo "  CONTEXT ENTROPY AUDITOR (CEA) - POSIX Shell Launcher"
echo "================================================================="

if command -v agy &> /dev/null; then
    echo "  [OK] Antigravity CLI detectado: $(command -v agy)"
else
    echo "  [AVISO] agy no encontrado en PATH. Se usará adaptador alternativo si aplica."
fi

if [ "${INTERACTIVE}" = true ] || [ -z "${FILE}" ]; then
    echo "  Iniciando CLI Interactivo y Live Stress Test Suite..."
    python3 -m src.context_auditor.cli --interactive --model "${MODEL}" --effort "${EFFORT}"
else
    echo "  Auditando archivo: ${FILE} (Modelo: ${MODEL}, Effort: ${EFFORT})..."
    python3 -m src.context_auditor.cli "${FILE}" --adapter antigravity --model "${MODEL}" --effort "${EFFORT}"
fi
