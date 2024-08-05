# Gunicorn Development config file

wsgi_app = "polizador.wsgi:application"
loglevel = "debug"
workers= 3
bind = "unix:/home/willy/dev/polizador-production2-dev/polizador/polizador-dev.sock"
reload = True
accesslog = errorlog = "/var/log/gunicorn/dev.log"
capture_output = True
pidfile = "/var/run/gunicorn/dev.pid"
daemon = True
