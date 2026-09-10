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
#   ./build.sh <nombre-contenedor-geoserver>
#   ./build.sh geoserver-gdu

set -euo pipefail

CONTAINER="${1:?Uso: $0 <nombre-contenedor-geoserver>}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="$SCRIPT_DIR/.build"

command -v javac >/dev/null || { echo "Falta javac (paquete openjdk-17-jdk-headless o similar)"; exit 1; }

rm -rf "$WORK"
mkdir -p "$WORK/libs" "$WORK/out"

echo ">>> Copiando WEB-INF/lib de $CONTAINER (classpath de compilación)..."
docker cp "$CONTAINER:/usr/local/tomcat/webapps/geoserver/WEB-INF/lib" "$WORK/libs_full"

CP="$(find "$WORK/libs_full" -name '*.jar' | tr '\n' ':')"

echo ">>> Compilando..."
javac --release 17 -cp "$CP" -d "$WORK/out" "$SCRIPT_DIR/src/ar/gov/ipduv/gdu/geoserver/UpdatedByTransactionListener.java"

cp "$SCRIPT_DIR/applicationContext.xml" "$WORK/out/"
( cd "$WORK/out" && jar cf "$SCRIPT_DIR/gdu-updated-by-listener.jar" applicationContext.xml ar/gov/ipduv/gdu/geoserver/*.class )

echo ">>> OK: $SCRIPT_DIR/gdu-updated-by-listener.jar"
rm -rf "$WORK"
