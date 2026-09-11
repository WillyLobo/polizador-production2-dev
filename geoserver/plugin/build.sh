#!/usr/bin/env bash
#
# Recompila gdu-updated-by-listener.jar contra el classpath real de un
# GeoServer corriendo (no usa Maven ni resuelve dependencias por su cuenta --
# se compiló la primera vez así, sin Maven instalado en el entorno de
# desarrollo, y se mantiene igual para no depender de más herramientas de las
# necesarias). Solo hace falta volver a correr esto si cambia la versión de
# GeoServer (las firmas de DispatcherCallback/TransactionType podrían variar
# entre versiones -- ver los comentarios en el .java).
#
# Uso:
#   ./build.sh [WEB-INF/lib de GeoServer]
#   ./build.sh                                          # default: instalación nativa vía deploy_geoserver.sh
#   ./build.sh /opt/geoserver/webapps/geoserver/WEB-INF/lib

set -euo pipefail

WEBINF_LIB="${1:-/opt/geoserver/webapps/geoserver/WEB-INF/lib}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="$SCRIPT_DIR/.build"

command -v javac >/dev/null || { echo "Falta javac (paquete openjdk-17-jdk-headless o similar)"; exit 1; }
[[ -d "$WEBINF_LIB" ]] || { echo "No existe $WEBINF_LIB -- ¿corrió ./deploy_geoserver.sh geoserver? pasar la ruta como argumento si GeoServer está en otro lado"; exit 1; }

rm -rf "$WORK"
mkdir -p "$WORK/libs" "$WORK/out"

echo ">>> Copiando $WEBINF_LIB (classpath de compilación, dueño del usuario de servicio geoserver -- requiere sudo)..."
sudo cp -r "$WEBINF_LIB" "$WORK/libs_full"
sudo chown -R "$(id -u):$(id -g)" "$WORK/libs_full"

CP="$(find "$WORK/libs_full" -name '*.jar' | tr '\n' ':')"

echo ">>> Compilando..."
javac --release 17 -cp "$CP" -d "$WORK/out" "$SCRIPT_DIR/src/ar/gov/ipduv/gdu/geoserver/UpdatedByTransactionListener.java"

cp "$SCRIPT_DIR/applicationContext.xml" "$WORK/out/"
( cd "$WORK/out" && jar cf "$SCRIPT_DIR/gdu-updated-by-listener.jar" applicationContext.xml ar/gov/ipduv/gdu/geoserver/*.class )

echo ">>> OK: $SCRIPT_DIR/gdu-updated-by-listener.jar"
rm -rf "$WORK"
