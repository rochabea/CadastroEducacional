from .settings_sync import *  # ou .settings se você usa settings.py padrão

# Banco de teste pode ser sqlite em memória ou temporário
# settings_test.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {
            "NAME": ":memory:",
        },
        "OPTIONS": {
            "timeout": 20,
            "check_same_thread": False,  # <<<<<<<<<<<<<<
        },
    }
}


# Evita hashing pesado em testes
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Emails de teste
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Permite chamadas assíncronas no teste
DJANGO_ALLOW_ASYNC_UNSAFE = True
