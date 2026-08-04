from datetime import timedelta
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, TransactionTestCase

from core import management_runner
from core.forms import CheckResolucionesForm
from core.models import ManagementCommandRun

UserModel = get_user_model()


class ManagementCommandsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")

    def test_anonymous_redirected_to_login(self):
        resp = self.client.get("/administracion/comandos/")
        assert resp.status_code == 302

    def test_regular_user_forbidden(self):
        self.client.login(username="plain_user", password="pass1234!")
        resp = self.client.get("/administracion/comandos/")
        assert resp.status_code == 403

    def test_superuser_sees_registered_command_form(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/administracion/comandos/?command=resolucion_audit")
        assert resp.status_code == 200
        assert isinstance(resp.context["form"], CheckResolucionesForm)

    def test_unknown_command_key_is_rejected(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.post("/administracion/comandos/", {"command": "shell"})
        assert resp.status_code == 302
        assert ManagementCommandRun.objects.count() == 0

    @patch("core.views.management_runner.start_run")
    def test_valid_command_starts_run_and_redirects_to_detail(self, mock_start_run):
        # status=SUCCESS: es solo el objeto que el runner mockeado "devuelve" para
        # obtener el pk del redirect, no debe contar como una corrida en curso.
        mock_start_run.return_value = ManagementCommandRun.objects.create(
            command="resolucion_audit", started_by=self.superuser, status=ManagementCommandRun.Status.SUCCESS
        )
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.post("/administracion/comandos/", {"command": "resolucion_audit"})
        assert resp.status_code == 302
        mock_start_run.assert_called_once()
        assert mock_start_run.call_args.args[0] == "resolucion_audit"

    @patch("core.views.management_runner.start_run")
    def test_refuses_concurrent_runs(self, mock_start_run):
        ManagementCommandRun.objects.create(
            command="resolucion_audit", started_by=self.superuser, status=ManagementCommandRun.Status.RUNNING
        )
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.post("/administracion/comandos/", {"command": "resolucion_audit"})
        assert resp.status_code == 302
        mock_start_run.assert_not_called()


class ManagementCommandRunLogViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")
        self.client.login(username="admin_user", password="pass1234!")
        self.run = ManagementCommandRun.objects.create(
            command="resolucion_audit", started_by=self.superuser, log="hola\nmundo\n"
        )

    def test_returns_only_the_new_tail(self):
        resp = self.client.get(f"/administracion/comandos/{self.run.pk}/log/?offset=5")
        assert resp.status_code == 200
        data = resp.json()
        assert data["chunk"] == "mundo\n"
        assert data["offset"] == len(self.run.log)
        assert data["status"] == "running"

    @patch("core.views.management_runner.kill_run")
    def test_kill_view_delegates_to_runner(self, mock_kill_run):
        resp = self.client.post(f"/administracion/comandos/{self.run.pk}/kill/")
        assert resp.status_code == 302
        mock_kill_run.assert_called_once_with(self.run)


class CheckResolucionesFormTest(TestCase):
    def test_takes_no_arguments(self):
        form = CheckResolucionesForm(data={})
        assert form.is_valid()
        assert form.to_argv() == []


class ManagementCommandRunDurationTest(TestCase):
    def setUp(self):
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")

    def test_duration_none_while_running_without_finished_at_is_elapsed_since_start(self):
        run = ManagementCommandRun.objects.create(command="resolucion_audit", started_by=self.superuser)
        assert run.status == ManagementCommandRun.Status.RUNNING
        assert run.duration is not None
        assert run.duration_display != "—"

    def test_duration_uses_finished_at_once_terminal(self):
        run = ManagementCommandRun.objects.create(command="resolucion_audit", started_by=self.superuser)
        run.status = ManagementCommandRun.Status.SUCCESS
        run.finished_at = run.started_at + timedelta(minutes=1, seconds=5)
        run.save()
        assert run.duration_display == "1m 5s"


class ManagementRunnerTest(TransactionTestCase):
    """Ejercita _execute()/kill_run() con un subprocess.Popen mockeado.

    TransactionTestCase (no TestCase): _execute() llama a close_old_connections(), que
    con CONN_MAX_AGE=0 cierra la conexión activa en cada llamada. Bajo TestCase normal
    (que envuelve el test en una transacción atómica compartida) eso deja la conexión
    en estado "closed_in_transaction" y revienta cualquier query posterior con
    InterfaceError — es el mismo llamado que hace el thread real en producción, así que
    hay que testearlo en un escenario sin esa transacción envolvente."""

    def setUp(self):
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")

    def _fake_popen(self, lines, returncode):
        proc = MagicMock()
        proc.pid = 12345
        proc.stdout = iter(lines)
        proc.wait.return_value = returncode
        return proc

    @patch("core.management_runner.subprocess.Popen")
    def test_successful_run_captures_log_and_marks_success(self, mock_popen):
        mock_popen.return_value = self._fake_popen(["linea 1\n", "linea 2\n"], 0)
        run = ManagementCommandRun.objects.create(command="resolucion_audit", started_by=self.superuser)

        management_runner._execute(run.pk)

        run.refresh_from_db()
        assert run.status == ManagementCommandRun.Status.SUCCESS
        assert run.return_code == 0
        assert run.log == "linea 1\nlinea 2\n"
        assert run.pid == 12345

    @patch("core.management_runner.subprocess.Popen")
    def test_nonzero_return_code_marks_failed(self, mock_popen):
        mock_popen.return_value = self._fake_popen(["boom\n"], 1)
        run = ManagementCommandRun.objects.create(command="resolucion_audit", started_by=self.superuser)

        management_runner._execute(run.pk)

        run.refresh_from_db()
        assert run.status == ManagementCommandRun.Status.FAILED
        assert run.return_code == 1

    def test_kill_run_marks_killed_only_if_still_running(self):
        finished_run = ManagementCommandRun.objects.create(
            command="resolucion_audit",
            started_by=self.superuser,
            status=ManagementCommandRun.Status.SUCCESS,
            pid=999,
        )
        with patch("core.management_runner.os.kill") as mock_kill:
            management_runner.kill_run(finished_run)
        mock_kill.assert_not_called()
        finished_run.refresh_from_db()
        assert finished_run.status == ManagementCommandRun.Status.SUCCESS

        running_run = ManagementCommandRun.objects.create(
            command="resolucion_audit", started_by=self.superuser, pid=999
        )
        with patch("core.management_runner.os.kill") as mock_kill:
            management_runner.kill_run(running_run)
        mock_kill.assert_called_once_with(999, management_runner.signal.SIGTERM)
        running_run.refresh_from_db()
        assert running_run.status == ManagementCommandRun.Status.KILLED
