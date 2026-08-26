#!/usr/bin/env bash
# Deploy manual: git pull + collectstatic + migrate + reinicio de gunicorn +
# asociación del release/commits en Sentry, todo en un solo comando.
#
# Uso: polizador/scripts/deploy.sh

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_DIR="$REPO_ROOT/polizador"

cd "$REPO_ROOT"
git pull

cd "$PROJECT_DIR"
source ../env/bin/activate

python manage.py collectstatic --noinput
python manage.py migrate

sudo systemctl restart gunicorn.service

# --- Release de Sentry ---
# sentry_sdk.init() en settings.py ya etiqueta los eventos con el release
# (= SHA del checkout al arrancar gunicorn), pero Sentry no sabe qué commits
# pertenecen a ese release hasta que se lo decimos acá. Esto es lo que
# habilita "Suspect Commits" y las sugerencias de commit al resolver un issue.
#
# Requiere sentry-cli instalado en el server:
#   curl -sL https://sentry.io/get-cli/ | bash
export $(grep -E '^SENTRY_(AUTH_TOKEN|ORG|PROJECT)=' .env | xargs)

VERSION="$(git -C "$REPO_ROOT" rev-parse HEAD)"

sentry-cli releases new "$VERSION"
sentry-cli releases set-commits "$VERSION" --local
sentry-cli releases finalize "$VERSION"
sentry-cli releases deploys "$VERSION" new -e production

echo "Deploy completo. Release $VERSION asociado en Sentry."
