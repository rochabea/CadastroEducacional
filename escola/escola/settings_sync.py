from .settings import *

# DESABILITA AMBIENTE ASYNC (ESSENCIAL)
ASGI_APPLICATION = None

# Banco de testes isolado e simples
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {"NAME": ":memory:"},
    }
}

# Evita que o Django tente abrir conexões async
USE_TZ = False
