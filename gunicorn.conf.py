# Gunicorn configuration file
import os
from dotenv import load_dotenv

load_dotenv()

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('WORKERS', '1'))  # Number of worker processes
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
loglevel = os.getenv('LOG_LEVEL', 'info')
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'project-space-api'

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (for production with certificates)
# keyfile = None
# certfile = None

# Environment
raw_env = [
    f"FLASK_ENV={os.getenv('FLASK_ENV', 'production')}",
]

# Preload application for better performance
preload_app = True

# Enable auto-restart when code changes (development only)
reload = os.getenv('FLASK_ENV', 'production') == 'development'
