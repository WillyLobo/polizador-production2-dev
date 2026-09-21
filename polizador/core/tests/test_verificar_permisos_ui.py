"""
Tests de core/management/commands/verificar_permisos_ui.py -- la red de seguridad
de la migracion de gates por nombre de grupo a gates por permiso.

Lo que importa probar aca no es que el comando diga "OK" (eso lo verifica correrlo
contra una replica), sino que sepa decir "DIFIERE" cuando de verdad difiere: un
comando que siempre pasa es peor que no tener comando.
"""
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import TestCase

from core.management.commands import verificar_permisos_ui as cmd

UserModel = get_user_model()


class VerificarPermisosUiTest(TestCase):
    def setUp(self):
        self.grupo = Group.objects.create(name="grupo_de_prueba")
        self.perm_equivalente = Permission.objects.get(
            content_type__app_label="carga", codename="view_obra"
        )
        self.perm_ajeno = Permission.objects.get(
            content_type__app_label="carga", codename="view_localidad"
        )
        self.grupo.permissions.add(self.perm_equivalente)

        self.en_grupo = UserModel.objects.create_user(username="en_grupo", password="x")
        self.en_grupo.groups.add(self.grupo)
        self.fuera = UserModel.objects.create_user(username="fuera", password="x")

    def _correr(self, equivalencias):
        salida = StringIO()
        original = cmd.EQUIVALENCIAS
        cmd.EQUIVALENCIAS = equivalencias
        try:
            call_command("verificar_permisos_ui", "--detalle", stdout=salida)
        finally:
            cmd.EQUIVALENCIAS = original
        return salida.getvalue()

    def _entrada(self, permisos):
        return {
            "ubicacion": "test",
            "gate": "gate de prueba",
            "grupos": ["grupo_de_prueba"],
            "modo": "alguno",
            "superuser_en_grupos": False,
            "permisos": permisos,
        }

    def test_permiso_equivalente_reporta_ok(self):
        salida = self._correr([self._entrada(["carga.view_obra"])])
        assert "[OK    ]" in salida
        assert "DIFIERE" not in salida

    def test_permiso_mas_amplio_falla(self):
        # view_localidad no lo tiene nadie del grupo, pero se lo damos al de afuera:
        # el gate por permiso dejaria entrar a alguien que el grupo no dejaba.
        self.fuera.user_permissions.add(self.perm_ajeno)
        with self.assertRaises(SystemExit):
            self._correr([self._entrada(["carga.view_localidad"])])

    def test_permiso_inexistente_falla(self):
        with self.assertRaises(SystemExit):
            self._correr([self._entrada(["carga.permiso_que_no_existe"])])

    def test_y_permisos_se_exige_del_lado_de_los_grupos(self):
        # Replica el caso de la API: el gate viejo era "grupo AND permiso de modelo".
        # Sin el AND, el lado "grupo" incluiria a en_grupo y el lado "permiso" no.
        entrada = self._entrada(["carga.view_localidad"])
        entrada["y_permisos"] = ["carga.view_localidad"]
        salida = self._correr([entrada])
        assert "[OK    ]" in salida, salida
