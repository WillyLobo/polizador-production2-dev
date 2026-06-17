from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalizador', '0005_rename_customuser_tables'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "ALTER TABLE IF EXISTS secretariador_customuser_groups RENAME TO personalizador_customuser_groups;",
                "ALTER TABLE IF EXISTS secretariador_customuser_user_permissions RENAME TO personalizador_customuser_user_permissions;",
            ],
            reverse_sql=[
                "ALTER TABLE IF EXISTS personalizador_customuser_groups RENAME TO secretariador_customuser_groups;",
                "ALTER TABLE IF EXISTS personalizador_customuser_user_permissions RENAME TO secretariador_customuser_user_permissions;",
            ],
        ),
    ]
