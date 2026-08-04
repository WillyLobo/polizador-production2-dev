"""Ejecuta management commands whitelisteados (core.management_commands_registry) como
subprocesos, capturando su salida en vivo hacia ManagementCommandRun.log.

Se usa un subprocess en vez de call_command() in-process para que la captura de salida
sea confiable (cubre tanto self.stdout.write() como logging.*, sin pisar sys.stdout del
proceso web) y para poder matar un comando colgado sin afectar al worker de Django.
"""

import os
import signal
import subprocess
import sys
import threading

from django.conf import settings
from django.db import close_old_connections
from django.utils import timezone

from core.models import ManagementCommandRun

MANAGE_PY = settings.BASE_DIR / "manage.py"

_LOG_FLUSH_LINES = 5


def start_run(command_key, argv_extra, user):
    run = ManagementCommandRun.objects.create(
        command=command_key,
        argv=[command_key, *argv_extra],
        started_by=user,
    )
    threading.Thread(target=_execute, args=(run.pk,), daemon=True).start()
    return run


def kill_run(run):
    if run.status != ManagementCommandRun.Status.RUNNING or not run.pid:
        return
    try:
        os.kill(run.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    # UPDATE condicional: si _execute() ya cerró la corrida (llegó a pasar entre el
    # chequeo de arriba y acá), no la pisamos con KILLED.
    ManagementCommandRun.objects.filter(
        pk=run.pk, status=ManagementCommandRun.Status.RUNNING
    ).update(status=ManagementCommandRun.Status.KILLED)


def _execute(run_id):
    # Thread nuevo: sin conexiones de DB heredadas ni una cerrada correctamente al final.
    close_old_connections()
    try:
        run = ManagementCommandRun.objects.get(pk=run_id)
        try:
            proc = subprocess.Popen(
                [sys.executable, str(MANAGE_PY), *run.argv],
                cwd=str(settings.BASE_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except OSError as exc:
            run.status = ManagementCommandRun.Status.FAILED
            run.log = f"No se pudo iniciar el proceso: {exc}\n"
            run.finished_at = timezone.now()
            run.save(update_fields=["status", "log", "finished_at"])
            return

        run.pid = proc.pid
        run.save(update_fields=["pid"])

        buffer = []
        for line in proc.stdout:
            buffer.append(line)
            if len(buffer) >= _LOG_FLUSH_LINES:
                _flush(run, buffer)
        if buffer:
            _flush(run, buffer)

        return_code = proc.wait()
        finished_at = timezone.now()

        # UPDATE condicional (compare-and-swap a nivel SQL): si kill_run() ya marcó
        # KILLED —puede pasar en cualquier momento entre proc.wait() y este punto,
        # corriendo en otro thread— no lo pisamos con SUCCESS/FAILED. Un
        # read-then-write en Python (refresh_from_db + save) tiene una ventana de
        # carrera real acá; el UPDATE ...WHERE status='running' no.
        end_status = (
            ManagementCommandRun.Status.SUCCESS if return_code == 0 else ManagementCommandRun.Status.FAILED
        )
        updated = ManagementCommandRun.objects.filter(
            pk=run.pk, status=ManagementCommandRun.Status.RUNNING
        ).update(status=end_status, return_code=return_code, finished_at=finished_at)
        if not updated:
            ManagementCommandRun.objects.filter(pk=run.pk).update(
                return_code=return_code, finished_at=finished_at
            )
    finally:
        close_old_connections()


def _flush(run, buffer):
    run.log += "".join(buffer)
    run.save(update_fields=["log"])
    buffer.clear()
