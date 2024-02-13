import socket

from .docker import *



DEBUG = True

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())

INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["debug_toolbar", "drf_spectacular", ]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware", ]

REST_FRAMEWORK.update(
    {
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }
)

SPECTACULAR_SETTINGS = {
    "TITLE": "Theatre Service API",
    "DESCRIPTION": "Order tickets for performance",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelRendering": "model",
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
    },
}
