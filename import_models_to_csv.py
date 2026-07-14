#!/usr/bin/env python3
"""
Script para importar archivos XLSX generados por export_models_to_csv.py
al modelo de datos Django, siguiendo el orden correcto de dependencias
basado en Foreign Keys entre apps y modelos.

Uso:
    python import_models_to_csv.py                   # Importa todo
    python import_models_to_csv.py --dry-run          # Solo muestra qué se importaría
    python import_models_to_csv.py --apps carga        # Solo importa la app "carga"
    python import_models_to_csv.py --output-dir /ruta  # Directorio alternativo

El orden de carga respeta las dependencias de Foreign Keys:
   FASE 1-6 : carga.app (base) — tablas sin dependencias externas primero,
              luego las que dependen de ellas en cascada.
   FASE 7   : personalizador.app — catálogo propio independiente.
   FASE 8-13: secretariador.app — depende de carga + personalizador.

Ejecutar desde el root del proyecto:
    ./import_models_to_csv.py
"""
import os
import sys
import subprocess


# -------------------------------------------------------------------
#  Dependency-ordered import list
#  Each entry: (xlsx_filename, app_label, model_name)
# -------------------------------------------------------------------

IMPORT_ORDER = [
    # === FASE 1 — carga.app: tablas base sin FKs ===
    ('carga_receptor.xlsx',                'carga',       'Receptor'),
    ('carga_area.xlsx',                    'carga',       'Area'),
    ('carga_aseguradora.xlsx',             'carga',       'Aseguradora'),
    ('carga_empresa.xlsx',                 'carga',       'Empresa'),
    ('carga_programa.xlsx',                'carga',       'Programa'),
    ('carga_provincia.xlsx',               'carga',       'Provincia'),
    ('carga_region.xlsx',                  'carga',       'Region'),
    ('carga_departamento.xlsx',            'carga',       'Departamento'),

    # === FASE 2 — carga.app: geografía jerárquica ===
    ('carga_municipio.xlsx',               'carga',       'Municipio'),
    ('carga_localidad.xlsx',               'carga',       'Localidad'),

    # === FASE 3 — carga.app: catálogos y estructuras intermedias ===
    ('carga_conjuntolicitado.xlsx',        'carga',       'ConjuntoLicitado'),
    ('carga_agente.xlsx',                  'carga',       'Agente'),
    ('carga_certificadorubro.xlsx',        'carga',       'CertificadoRubro'),
    ('carga_certificadofinanciamiento.xlsx','carga',      'CertificadoFinanciamiento'),

    # === FASE 4 — carga.app: modelos principales ===
    ('carga_obra.xlsx',                    'carga',       'Obra'),
    ('carga_poliza.xlsx',                  'carga',       'Poliza'),
    # ('carga_legacypoliza.xlsx',            'carga',       'LegacyPoliza'),
    ('carga_poliza_movimiento.xlsx',       'carga',       'Poliza_Movimiento'),
    ('carga_certificado.xlsx',             'carga',       'Certificado'),

    # === FASE 5 — carga.app: contratos y anexos ===
    ('carga_contrato.xlsx',                'carga',       'Contrato'),
    ('carga_contratorubro.xlsx',           'carga',       'ContratoRubro'),
    ('carga_contratomonto.xlsx',           'carga',       'ContratoMonto'),
    ('carga_contratosdigitales.xlsx',      'carga',       'ContratosDigitales'),
    ('carga_plandetrabajos.xlsx',          'carga',       'PlanDeTrabajos'),

    # === FASE 6 — carga.app: tablas de referencia independientes ===
    ('carga_prototipo.xlsx',               'carga',       'Prototipo'),
    ('carga_uvi.xlsx',                     'carga',       'Uvi'),
    ('carga_indec.xlsx',                   'carga',       'INDEC'),

    # === FASE 7 — personalizador.app ===
    ('personalizador_cargotipo.xlsx',      'personalizador', 'CargoTipo'),
    ('personalizador_gerencia.xlsx',       'personalizador', 'Gerencia'),
    ('personalizador_direccion.xlsx',      'personalizador', 'Direccion'),
    ('personalizador_departamento.xlsx',   'personalizador', 'Departamento'),
    ('personalizador_cargos.xlsx',         'personalizador', 'Cargos'),

    # === FASE 8-13 — secretariador.app ===
    ('secretariador_instrumentoslegalesmemorandum.xlsx',        'secretariador', 'InstrumentosLegalesMemorandum'),
    ('secretariador_instrumentoslegalesresoluciones.xlsx',      'secretariador', 'InstrumentosLegalesResoluciones'),
    ('secretariador_instrumentoslegalesresolucionesdirectorio.xlsx','secretariador', 'InstrumentosLegalesResolucionesDirectorio'),
    ('secretariador_instrumentoslegalesdecretos.xlsx',          'secretariador', 'InstrumentosLegalesDecretos'),

    ('secretariador_organigrama.xlsx',       'secretariador', 'Organigrama'),

    ('secretariador_montoviaticodiario.xlsx','secretariador', 'MontoViaticoDiario'),
    ('secretariador_comisionado.xlsx',       'secretariador', 'Comisionado'),
    ('secretariador_vehiculo.xlsx',          'secretariador', 'Vehiculo'),
    ('secretariador_solicitud.xlsx',         'secretariador', 'Solicitud'),

    ('secretariador_incorporacion.xlsx',     'secretariador', 'Incorporacion'),
    ('secretariador_comisionadosolicitud.xlsx','secretariador', 'ComisionadoSolicitud'),
]


def run_import(xlsx_path, app_label, model_name, manage_py_dir, dry_run=False):
    """Import a XLSX file using the Django import_export management command.

    Returns (success: bool, stdout: str, stderr: str)
    """
    resource = f"{app_label}.{model_name}"
    cmd = [
        sys.executable,
        os.path.join(manage_py_dir, 'manage.py'),
        'import',
        resource,
        xlsx_path,
        '--format', 'XLSX',
        '--noinput',
    ]
    if dry_run:
        cmd.append('--dry-run')
    cmd.append('--raise-errors')

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'polizador.settings'},
    )
    return (result.returncode == 0), result.stdout, result.stderr


def main():
    # Determine project root (mirror export script logic)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(script_dir) == 'polizador':
        project_root = os.path.dirname(script_dir)
        polizador_path = script_dir
    else:
        project_root = script_dir
        polizador_path = os.path.join(script_dir, 'polizador')

    # Parse arguments
    args = sys.argv[1:]
    target_apps = None  # None means all
    output_dir = os.path.join(project_root, 'csv_exports')
    dry_run = False

    i = 0
    while i < len(args):
        if args[i] == '--apps' and i + 1 < len(args):
            target_apps = set(a.strip() for a in args[i+1].split(','))
            i += 2
        elif args[i] == '--output-dir' and i + 1 < len(args):
            output_dir = args[i+1]
            i += 2
        elif args[i] == '--dry-run':
            dry_run = True
            i += 1
        else:
            print(f"[WARN] Unknown argument: {args[i]}")
            i += 1

    if not os.path.isdir(output_dir):
        print(f"[ERROR] Directory does not exist: {output_dir}")
        sys.exit(1)

    # Filter import order based on --apps filter
    entries = IMPORT_ORDER
    if target_apps is not None:
        entries = [
            (fn, app, model) for fn, app, model in entries if app in target_apps
        ]

    # Print summary
    print("=" * 72)
    mode_word = "DRY RUN" if dry_run else "IMPORT"
    print(f"  Modo       : {mode_word}")
    print(f"  Directorio : {output_dir}")
    print(f"  Archivos   : {len(entries)} XLSX")
    apps_involved = sorted(set(app for _, app, _ in entries))
    print(f"  Apps       : {', '.join(apps_involved)}")
    print("=" * 72)

    # Run imports
    total_success = 0
    total_failed = 0
    total_records = 0
    all_errors = []

    for xlsx_filename, app_label, model_name in entries:
        filepath = os.path.join(output_dir, xlsx_filename)

        phase_label = f"[{app_label}]"
        print(f"\n── {phase_label:20s} -> {model_name:35s} | {xlsx_filename}")

        # Check file exists
        if not os.path.isfile(filepath):
            print("  [SKIP] Archivo no encontrado")
            total_failed += 1
            continue

        try:
            success, stdout, stderr = run_import(
                filepath, app_label, model_name, polizador_path, dry_run=dry_run
            )
            output = stdout + stderr
            print(output.strip())
            if success:
                total_success += 1
            else:
                all_errors.append((xlsx_filename, model_name, [output]))
                total_failed += 1
        except Exception as e:
            print(f"  [ERROR] Excepción inesperada: {e}")
            import traceback
            traceback.print_exc()
            total_failed += 1

    # Summary
    print("\n" + "=" * 72)
    mode_word = "Importado" if not dry_run else "Dry run completado"
    print(f"  {mode_word}")
    print(f"  Exitosos : {total_success}/{len(entries)} archivos")
    print(f"  Fallidos : {total_failed}/{len(entries)} archivos")

    if all_errors:
        print("\n  -- Resumen de errores por archivo --")
        for fn, model, errs in all_errors:
            print(f"\n  File: {fn} ({model}):")
            for e in errs[:5]:
                print(f"     {e}")

    sys.exit(1 if total_failed > 0 else 0)


if __name__ == '__main__':
    main()
