#!/usr/bin/env python3
"""
Script para exportar todos los modelos de las apps Django a archivos XLSX.

Uso:
    python export_models_to_csv.py
    
Opciones:
    --apps carga,secretariador,personalizador   Apps a exportar (por defecto todas)
    --output-dir csv_exports                    Directorio de salida
    
Requiere:
    - Virtual environment activado o PYTHONPATH configurado
    - django-import-export instalado
    - settings.py con try/except alrededor de la carga de credenciales GCS

Ejecutar desde el root del proyecto:
    ./export_models_to_csv.py
"""
import os
import sys
import subprocess


def main():
    # Determine project root (parent of 'polizador' directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.basename(script_dir) == 'polizador':
        project_root = os.path.dirname(script_dir)
        polizador_path = script_dir
    else:
        project_root = script_dir
        polizador_path = os.path.join(script_dir, 'polizador')
    
    sys.path.insert(0, polizador_path)
    sys.path.insert(0, project_root)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polizador.settings')
    
    import django
    django.setup()
    
    from django.apps import apps
    
    # Parse arguments
    args = sys.argv[1:]
    apps_list = ['carga', 'secretariador', 'personalizador']
    output_dir = os.path.join(project_root, 'csv_exports')
    
    i = 0
    while i < len(args):
        if args[i] == '--apps' and i + 1 < len(args):
            apps_list = [a.strip() for a in args[i+1].split(',')]
            i += 2
        elif args[i] == '--output-dir' and i + 1 < len(args):
            output_dir = args[i+1]
            i += 2
        else:
            i += 1
    
    os.makedirs(output_dir, exist_ok=True)
    
    total_files = []
    
    for app_label in apps_list:
        try:
            app_config = apps.get_app_config(app_label)
        except LookupError:
            print(f"[ERROR] App '{app_label}' no encontrada")
            continue
        
        models = sorted(
            [m for m in app_config.get_models() if hasattr(m, '_meta')],
            key=lambda m: m.__name__
        )
        
        if not models:
            print(f"[WARN] No hay modelos en '{app_label}'")
            continue
        
        print(f"\nApp: {app_label} ({len(models)} modelos)")
        
        for model in models:
            try:
                filename = app_label + '_' + model.__name__.lower() + '.xlsx'
                filepath = os.path.join(output_dir, filename)
                
                cmd = [
                    sys.executable, 'polizador/manage.py', 'export', 'XLSX',
                    f'{app_label}.{model.__name__}', '--encoding', 'utf-8'
                ]
                
                with open(filepath, 'wb') as outfile:
                    result = subprocess.run(cmd, cwd=project_root, stdout=outfile)
                
                if result.returncode == 0:
                    count = model.objects.count()
                    print(f"  OK    {model.__name__:40s} -> {filepath} ({count:,} registros)")
                    total_files.append(filepath)
                else:
                    print(f"  FAIL  {model.__name__:40s} -> Error en exportacion")
            
            except Exception as e:
                print(f"  FAIL  {model.__name__:40s} -> {e}")
    
    print(f"\nExportacion completada. {len(total_files)} archivos en '{output_dir}/'")


if __name__ == '__main__':
    main()
