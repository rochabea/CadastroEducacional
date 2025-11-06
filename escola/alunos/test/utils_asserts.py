# tests/utils_asserts.py
import time

def assert_has_csrf(html: str):
    """
    Verifica de forma simples se o HTML contém o input do CSRF do Django.
    """
    token_marker = 'name="csrfmiddlewaretoken"'
    assert token_marker in html or "csrf_token" in html.lower(), "Página não contém CSRF token."

class Stopwatch:
    """
    with Stopwatch() as sw: ...; sw.elapsed -> segundos decorrido
    """
    def __enter__(self):
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self._t0
