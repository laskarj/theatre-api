import socket
from dotenv import load_dotenv

from .docker import *


load_dotenv()


DEBUG = True

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())

INTERNAL_IPS = ([ip[: ip.rfind(".")] + ".1" for ip in ips]
                + ["127.0.0.1", "10.0.2.2"])

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
