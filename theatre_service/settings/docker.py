from .base import *
import os


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ["POSTGRES_HOST"],
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
    }
}


DJANGO_SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]


MEDIA_URL = "/media/"
MEDIA_ROOT = "vol/web/media"

STATIC_URL = "/static/"
