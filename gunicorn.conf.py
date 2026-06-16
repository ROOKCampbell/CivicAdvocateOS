"""
Gunicorn Production Configuration
Filename: gunicorn.conf.py
"""
import multiprocessing
import os

# --- Binding & Networking ---
bind = os.getenv("WSGI_BIND", "127.0.0.1:8000")
backlog = 2048

# --- Worker Performance Tuning ---
workers = int(os.getenv("WSGI_WORKERS", (multiprocessing.cpu_count() * 2) + 1))
worker_class = 'gthread'
threads = 4
worker_connections = 1000

# --- Resource & Timeout Management ---
timeout = 30
keepalive = 2
max_requests = 5000
max_requests_jitter = 50

# --- Process Security ---
user = None
group = None
umask = 0o022

# --- Logging Infrastructure ---
accesslog = "-"  
errorlog = "-"
loglevel = "info"
access_log_format = '%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# --- Lifecycle Hooks ---
preload_app = True
daemon = False

def on_starting(server):
    server.log.info("Initialization Vector Complete: Starting Gunicorn WSGI Master Process.")

def worker_int(worker):
    worker.log.info(f"Worker Interrupted (PID: {worker.pid}). Executing graceful teardown.")
