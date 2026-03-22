"""
Tests de integración para el módulo auth.

Prueban los endpoints reales de la API:
  POST /api/v1/auth/register
  POST /api/v1/auth/login
  POST /api/v1/auth/logout

Cada test hace una petición HTTP y verifica el código de estado
y el cuerpo de la respuesta.
"""

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
LOGOUT_URL = "/api/v1/auth/logout"

USUARIO_VALIDO = {
    "name": "María López",
    "email": "maria@petcare.com",
    "password": "password123",
}


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ===========================================================================
# REGISTER
# ===========================================================================


class TestRegister:
    """Pruebas para POST /api/v1/auth/register"""

    # --- Casos exitosos ---

    def test_registro_exitoso_retorna_201(self, client):
        resp = client.post(REGISTER_URL, json=USUARIO_VALIDO)
        assert resp.status_code == 201

    def test_registro_exitoso_retorna_token(self, client):
        resp = client.post(REGISTER_URL, json=USUARIO_VALIDO)
        data = resp.get_json()
        assert "access_token" in data
        assert data["access_token"] is not None

    def test_registro_exitoso_retorna_datos_usuario(self, client):
        resp = client.post(REGISTER_URL, json=USUARIO_VALIDO)
        data = resp.get_json()
        assert "user" in data
        assert data["user"]["email"] == USUARIO_VALIDO["email"]
        assert data["user"]["name"] == USUARIO_VALIDO["name"]

    def test_registro_exitoso_rol_por_defecto_user(self, client):
        resp = client.post(REGISTER_URL, json=USUARIO_VALIDO)
        data = resp.get_json()
        assert data["user"]["role"] == "user"

    def test_registro_no_expone_password_hash(self, client):
        resp = client.post(REGISTER_URL, json=USUARIO_VALIDO)
        data = resp.get_json()
        assert "password_hash" not in data["user"]
        assert "password" not in data["user"]

    def test_registro_email_se_guarda_en_minusculas(self, client):
        payload = {**USUARIO_VALIDO, "email": "MARIA@PETCARE.COM"}
        resp = client.post(REGISTER_URL, json=payload)
        data = resp.get_json()
        assert data["user"]["email"] == "maria@petcare.com"

    # --- Casos de error: body inválido ---

    def test_registro_sin_body_retorna_400(self, client):
        resp = client.post(REGISTER_URL, data="no-es-json", content_type="text/plain")
        assert resp.status_code == 400

    def test_registro_body_vacio_retorna_400(self, client):
        resp = client.post(REGISTER_URL)
        assert resp.status_code == 400

    # --- Casos de error: campos obligatorios ---

    def test_registro_sin_name_retorna_422(self, client):
        payload = {"email": "nuevo@test.com", "password": "pass123"}
        resp = client.post(REGISTER_URL, json=payload)
        assert resp.status_code == 422

    def test_registro_sin_email_retorna_422(self, client):
        payload = {"name": "Nuevo", "password": "pass123"}
        resp = client.post(REGISTER_URL, json=payload)
        assert resp.status_code == 422

    def test_registro_sin_password_retorna_422(self, client):
        payload = {"name": "Nuevo", "email": "nuevo@test.com"}
        resp = client.post(REGISTER_URL, json=payload)
        assert resp.status_code == 422

    def test_registro_name_vacio_retorna_422(self, client):
        payload = {"name": "  ", "email": "nuevo@test.com", "password": "pass123"}
        resp = client.post(REGISTER_URL, json=payload)
        assert resp.status_code == 422

    # --- Casos de error: validaciones de negocio ---

    def test_registro_password_muy_corta_retorna_422(self, client):
        """Contraseña con menos de 6 caracteres debe ser rechazada."""
        payload = {**USUARIO_VALIDO, "password": "abc"}
        resp = client.post(REGISTER_URL, json=payload)
        assert resp.status_code == 422

    def test_registro_password_exactamente_5_chars_retorna_422(self, client):
        payload = {**USUARIO_VALIDO, "password": "12345"}
        resp = client.post(REGISTER_URL, json=payload)
        assert resp.status_code == 422

    def test_registro_password_exactamente_6_chars_es_valida(self, client):
        payload = {**USUARIO_VALIDO, "password": "123456"}
        resp = client.post(REGISTER_URL, json=payload)
        assert resp.status_code == 201

    def test_registro_email_duplicado_retorna_409(self, client):
        """Registrar dos veces el mismo email debe fallar con 409."""
        client.post(REGISTER_URL, json=USUARIO_VALIDO)
        resp = client.post(REGISTER_URL, json=USUARIO_VALIDO)
        assert resp.status_code == 409

    def test_registro_email_duplicado_mensaje_error(self, client):
        client.post(REGISTER_URL, json=USUARIO_VALIDO)
        resp = client.post(REGISTER_URL, json=USUARIO_VALIDO)
        data = resp.get_json()
        assert "error" in data


# ===========================================================================
# LOGIN
# ===========================================================================


class TestLogin:
    """Pruebas para POST /api/v1/auth/login"""

    # --- Casos exitosos ---

    def test_login_exitoso_retorna_200(self, client, usuario_registrado):
        resp = client.post(
            LOGIN_URL,
            json={
                "email": usuario_registrado["user"]["email"],
                "password": usuario_registrado["password"],
            },
        )
        assert resp.status_code == 200

    def test_login_exitoso_retorna_token(self, client, usuario_registrado):
        resp = client.post(
            LOGIN_URL,
            json={
                "email": usuario_registrado["user"]["email"],
                "password": usuario_registrado["password"],
            },
        )
        data = resp.get_json()
        assert "access_token" in data
        assert data["access_token"] is not None

    def test_login_exitoso_retorna_datos_usuario(self, client, usuario_registrado):
        resp = client.post(
            LOGIN_URL,
            json={
                "email": usuario_registrado["user"]["email"],
                "password": usuario_registrado["password"],
            },
        )
        data = resp.get_json()
        assert data["user"]["email"] == usuario_registrado["user"]["email"]

    def test_login_acepta_email_en_mayusculas(self, client, usuario_registrado):
        """El login debe funcionar aunque el email se envíe en mayúsculas."""
        resp = client.post(
            LOGIN_URL,
            json={
                "email": usuario_registrado["user"]["email"].upper(),
                "password": usuario_registrado["password"],
            },
        )
        assert resp.status_code == 200

    # --- Casos de error: body inválido ---

    def test_login_sin_body_retorna_400(self, client):
        resp = client.post(LOGIN_URL, data="no-json", content_type="text/plain")
        assert resp.status_code == 400

    def test_login_body_vacio_retorna_400(self, client):
        resp = client.post(LOGIN_URL)
        assert resp.status_code == 400

    # --- Casos de error: campos obligatorios ---

    def test_login_sin_email_retorna_422(self, client):
        resp = client.post(LOGIN_URL, json={"password": "password123"})
        assert resp.status_code == 422

    def test_login_sin_password_retorna_422(self, client):
        resp = client.post(LOGIN_URL, json={"email": "alguien@test.com"})
        assert resp.status_code == 422

    # --- Casos de error: credenciales inválidas ---

    def test_login_password_incorrecta_retorna_401(self, client, usuario_registrado):
        """Contraseña incorrecta debe devolver 401."""
        resp = client.post(
            LOGIN_URL,
            json={
                "email": usuario_registrado["user"]["email"],
                "password": "contraseña_incorrecta",
            },
        )
        assert resp.status_code == 401

    def test_login_password_incorrecta_mensaje_error(self, client, usuario_registrado):
        resp = client.post(
            LOGIN_URL,
            json={
                "email": usuario_registrado["user"]["email"],
                "password": "mal_password",
            },
        )
        data = resp.get_json()
        assert "error" in data

    def test_login_email_inexistente_retorna_401(self, client):
        """Un email que no existe debe devolver 401 (no revelar si existe o no)."""
        resp = client.post(
            LOGIN_URL,
            json={"email": "noexiste@petcare.com", "password": "cualquier"},
        )
        assert resp.status_code == 401

    def test_login_usuario_inactivo_retorna_403(self, client, app):
        """Un usuario desactivado no debe poder iniciar sesión."""
        from app.auth.models.user import User
        from app.core.extensions import db

        with app.app_context():
            user = User(name="Inactivo", email="inactivo@petcare.com", is_active=False)
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

        resp = client.post(
            LOGIN_URL,
            json={"email": "inactivo@petcare.com", "password": "password123"},
        )
        assert resp.status_code == 403

    def test_login_usuario_inactivo_mensaje_error(self, client, app):
        from app.auth.models.user import User
        from app.core.extensions import db

        with app.app_context():
            user = User(name="Inactivo2", email="inactivo2@petcare.com", is_active=False)
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

        resp = client.post(
            LOGIN_URL,
            json={"email": "inactivo2@petcare.com", "password": "password123"},
        )
        data = resp.get_json()
        assert "error" in data


# ===========================================================================
# LOGOUT
# ===========================================================================


class TestLogout:
    """Pruebas para POST /api/v1/auth/logout"""

    # --- Casos exitosos ---

    def test_logout_exitoso_retorna_200(self, client, usuario_registrado):
        resp = client.post(
            LOGOUT_URL,
            headers=auth_headers(usuario_registrado["token"]),
        )
        assert resp.status_code == 200

    def test_logout_exitoso_mensaje_confirmacion(self, client, usuario_registrado):
        resp = client.post(
            LOGOUT_URL,
            headers=auth_headers(usuario_registrado["token"]),
        )
        data = resp.get_json()
        assert "message" in data

    def test_logout_token_queda_revocado(self, client, usuario_registrado):
        """Después del logout el mismo token no debe poder usarse de nuevo."""
        token = usuario_registrado["token"]
        client.post(LOGOUT_URL, headers=auth_headers(token))

        # Intentar logout con el mismo token revocado
        resp = client.post(LOGOUT_URL, headers=auth_headers(token))
        assert resp.status_code == 401

    # --- Casos de error ---

    def test_logout_sin_token_retorna_401(self, client):
        """Sin token de autorización debe devolver 401."""
        resp = client.post(LOGOUT_URL)
        assert resp.status_code == 401

    def test_logout_token_invalido_retorna_422(self, client):
        """Un token con formato incorrecto debe ser rechazado."""
        resp = client.post(
            LOGOUT_URL,
            headers={"Authorization": "Bearer token_completamente_invalido"},
        )
        assert resp.status_code == 422

    def test_logout_token_malformado_sin_bearer(self, client):
        """Header sin el prefijo Bearer debe ser rechazado."""
        resp = client.post(
            LOGOUT_URL,
            headers={"Authorization": "SinPrefijo alguntokenfake"},
        )
        assert resp.status_code == 401
