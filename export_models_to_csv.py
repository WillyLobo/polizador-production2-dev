#!/usr/bin/env python3
"""
Script para exportar todos los modelos de las apps Django a archivos CSV.

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
import csv


def make_resource(model_class):
    """Factory function to create a ModelResource for the given model."""
    from import_export import resources
    
    class DynamicResource(resources.ModelResource):
        class Meta:
            model = model_class
            export_order = [f.name for f in model_class._meta.fields]
    
    return DynamicResource


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
                resource = make_resource(model)
                queryset = model.objects.all()
                dataset = resource().export(queryset)
                
                filename = model.__name__.lower() + '.csv'
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    if dataset.headers:
                        writer.writerow(dataset.headers)
                    for row in dataset:
                        writer.writerow(list(row))
                
                count = queryset.count()
                print(f"  OK    {model.__name__:40s} -> {filepath} ({count:,} registros)")
                total_files.append(filepath)
            
            except Exception as e:
                print(f"  FAIL  {model.__name__:40s} -> {e}")
    
    print(f"\nExportacion completada. {len(total_files)} archivos en '{output_dir}/'")


if __name__ == '__main__':
    main()
