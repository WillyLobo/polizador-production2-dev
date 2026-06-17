from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalizador', '0004_fix_customuser_content_types'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=[
                        "ALTER TABLE IF EXISTS secretariador_customuser RENAME TO personalizador_customuser;",
                        "ALTER TABLE IF EXISTS secretariador_historicalcustomuser RENAME TO personalizador_historicalcustomuser;",
                    ],
                    reverse_sql=[
                        "ALTER TABLE IF EXISTS personalizador_customuser RENAME TO secretariador_customuser;",
                        "ALTER TABLE IF EXISTS personalizador_historicalcustomuser RENAME TO secretariador_historicalcustomuser;",
                    ],
                ),
            ],
            state_operations=[
                migrations.AlterModelTable(
                    name='customuser',
                    table=None,
                ),
                migrations.AlterModelTable(
                    name='historicalcustomuser',
                    table=None,
                ),
            ],
        ),
    ]
