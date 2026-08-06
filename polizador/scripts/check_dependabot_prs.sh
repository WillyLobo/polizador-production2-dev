#!/usr/bin/env bash
# Para cada PR abierta de Dependabot (ecosystem pip), instala localmente las
# versiones que propone (via el diff de requirements.txt), corre el test
# suite contra esa versión, y restaura requirements.txt al finalizar cada una.
#
# Uso:
#   ./scripts/check_dependabot_prs.sh          # revisa todas las PRs abiertas dependabot/pip/*
#   ./scripts/check_dependabot_prs.sh 8 9      # sólo esos números de PR
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."   # polizador/, donde vive manage.py

PY="../env/bin/python"
PIP="../env/bin/pip"
REPO="WillyLobo/polizador-production2-dev"
LOG_DIR="/tmp/claude-1000/-home-willy-dev-polizador-production2-dev/3f507574-e855-4f96-9f3d-f697b340e6d6/scratchpad/dependabot-pr-checks"
mkdir -p "$LOG_DIR"

if ! command -v gh >/dev/null 2>&1; then
    echo "gh CLI no está disponible en PATH." >&2
    exit 1
fi

if [ "$#" -gt 0 ]; then
    PR_NUMS="$*"
else
    PR_NUMS=$(gh pr list --repo "$REPO" --state open --json number,headRefName \
        --jq '.[] | select(.headRefName | startswith("dependabot/pip/")) | .number')
fi

restore_requirements() {
    "$PIP" install -q -r requirements.txt
}
trap restore_requirements EXIT

declare -A RESULTS

for num in $PR_NUMS; do
    title=$(gh pr view "$num" --repo "$REPO" --json title --jq .title 2>/dev/null)
    echo
    echo "=== PR #$num: $title ==="

    SPECS=$(gh pr diff "$num" --repo "$REPO" 2>/dev/null | grep -E '^\+[A-Za-z0-9_.-]+==' | sed 's/^+//')

    if [ -z "$SPECS" ]; then
        echo "  (sin cambios de paquetes detectados, se omite)"
        RESULTS[$num]="SKIPPED"
        continue
    fi

    echo "  Instalando: $(echo "$SPECS" | tr '\n' ' ')"
    LOG_FILE="$LOG_DIR/pr-${num}.log"

    if ! $PIP install -q $SPECS > "$LOG_FILE" 2>&1; then
        echo "  INSTALL FAILED (ver $LOG_FILE)"
        RESULTS[$num]="INSTALL_FAILED"
        restore_requirements
        continue
    fi

    if $PY manage.py test --keepdb >> "$LOG_FILE" 2>&1; then
        echo "  PASS"
        RESULTS[$num]="PASS"
    else
        echo "  FAIL (ver $LOG_FILE)"
        RESULTS[$num]="FAIL"
    fi

    restore_requirements
done

echo
echo "=== Resumen ==="
for num in "${!RESULTS[@]}"; do
    echo "PR #$num: ${RESULTS[$num]}"
done
