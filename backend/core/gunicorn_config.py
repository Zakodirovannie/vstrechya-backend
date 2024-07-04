"""Gunicorn *production* config file"""

import multiprocessing

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "core.wsgi:application"
# The number of worker processes for handling requests
workers = multiprocessing.cpu_count() * 2 + 1
# The socket to bind
bind = "0.0.0.0:8010"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
# Daemonize the Gunicorn process (detach & enter background)
daemon = False
