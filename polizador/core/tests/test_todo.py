from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase

from core.management.commands.seed_todos import TODOS
from core.models import Todo

UserModel = get_user_model()


class TodoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")
        self.todo = Todo.objects.create(title="Revisar backups", created_by=self.superuser)

    def test_anonymous_redirected_to_login(self):
        resp = self.client.get("/administracion/tareas/")
        assert resp.status_code == 302

    def test_regular_user_forbidden(self):
        self.client.login(username="plain_user", password="pass1234!")
        resp = self.client.get("/administracion/tareas/")
        assert resp.status_code == 403

    def test_superuser_can_list(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/administracion/tareas/")
        assert resp.status_code == 200
        assert self.todo in resp.context["todos"]

    def test_superuser_can_create(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.post("/administracion/tareas/nueva/", {"title": "Nueva tarea", "description": ""})
        assert resp.status_code == 302
        created = Todo.objects.get(title="Nueva tarea")
        assert created.created_by == self.superuser
        assert created.status == Todo.Status.PENDIENTE

    def test_superuser_can_update_status(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.post(f"/administracion/tareas/{self.todo.pk}/estado/", {"status": Todo.Status.RESUELTO})
        assert resp.status_code == 302
        self.todo.refresh_from_db()
        assert self.todo.status == Todo.Status.RESUELTO

    def test_invalid_status_rejected(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.post(f"/administracion/tareas/{self.todo.pk}/estado/", {"status": "no-existe"})
        assert resp.status_code == 302
        self.todo.refresh_from_db()
        assert self.todo.status == Todo.Status.PENDIENTE

    def test_superuser_can_delete(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.post(f"/administracion/tareas/{self.todo.pk}/eliminar/")
        assert resp.status_code == 302
        assert not Todo.objects.filter(pk=self.todo.pk).exists()


class SeedTodosCommandTest(TestCase):
    def test_creates_one_todo_per_entry(self):
        call_command("seed_todos")
        assert Todo.objects.count() == len(TODOS)

    def test_dry_run_creates_nothing(self):
        call_command("seed_todos", "--dry-run")
        assert Todo.objects.count() == 0

    def test_is_idempotent_and_does_not_overwrite_status(self):
        call_command("seed_todos")
        first_title = TODOS[0][1]
        todo = Todo.objects.get(title=first_title)
        todo.status = Todo.Status.RESUELTO
        todo.save(update_fields=["status"])

        call_command("seed_todos")

        assert Todo.objects.count() == len(TODOS)
        todo.refresh_from_db()
        assert todo.status == Todo.Status.RESUELTO
