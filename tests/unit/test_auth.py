"""
Tests unitarios para el módulo Auth.

Verifican la lógica de validación y comportamiento específico de los
endpoints de autenticación: register, login, logout y profile.
Usan base de datos SQLite en memoria mediante el fixture `client`.
"""

import pytest

REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
LOGOUT_URL = "/api/v1/auth/logout"
PROFILE_URL = "/api/v1/auth/profile"


# ===========================================================================
# REGISTER — Validaciones de entrada
# ===========================================================================


class TestRegisterValidacion:
    """Pruebas unitarias de validación del endpoint de registro."""

    def test_registro_sin_body_retorna_400(self, client):
        """Sin body la petición debe devolver 400."""
        res = client.post(REGISTER_URL)
        assert res.status_code == 400

    def test_registro_body_no_json_retorna_400(self, client):
        """Body que no es JSON debe devolver 400."""
        res = client.post(REGISTER_URL, data="texto plano", content_type="text/plain")
        assert res.status_code == 400

    def test_registro_sin_name_retorna_422(self, client):
        """Sin campo name debe devolver 422."""
        res = client.post(
            REGISTER_URL, json={"email": "nuevo@test.com", "password": "pass123"}
        )
        assert res.status_code == 422
        assert "error" in res.get_json()

    def test_registro_sin_email_retorna_422(self, client):
        """Sin campo email debe devolver 422."""
        res = client.post(
            REGISTER_URL, json={"name": "Test", "password": "pass123"}
        )
        assert res.status_code == 422

    def test_registro_sin_password_retorna_422(self, client):
        """Sin campo password debe devolver 422."""
        res = client.post(
            REGISTER_URL, json={"name": "Test", "email": "nuevo@test.com"}
        )
        assert res.status_code == 422

    def test_registro_name_solo_espacios_retorna_422(self, client):
        """Nombre compuesto solo de espacios debe devolver 422."""
        res = client.post(
            REGISTER_URL,
            json={"name": "   ", "email": "nuevo@test.com", "password": "pass123"},
        )
        assert res.status_code == 422

    def test_registro_password_5_chars_retorna_422(self, client):
        """Contraseña de exactamente 5 caracteres debe devolver 422."""
        res = client.post(
            REGISTER_URL,
            json={"name": "Test", "email": "nuevo@test.com", "password": "12345"},
        )
        assert res.status_code == 422

    def test_registro_password_6_chars_es_valida(self, client):
        """Contraseña de exactamente 6 caracteres debe ser aceptada."""
        res = client.post(
            REGISTER_URL,
            json={"name": "Test", "email": "p6@test.com", "password": "123456"},
        )
        assert res.status_code == 201

    def test_registro_email_duplicado_retorna_409(self, client):
        """Registrar el mismo email dos veces debe devolver 409."""
        payload = {"name": "Primero", "email": "dup@test.com", "password": "pass123"}
        client.post(REGISTER_URL, json=payload)
        res = client.post(REGISTER_URL, json=payload)
        assert res.status_code == 409
        assert "error" in res.get_json()

    def test_registro_email_normalizado_a_minusculas(self, client):
        """El email debe guardarse siempre en minúsculas."""
        res = client.post(
            REGISTER_URL,
            json={"name": "Test", "email": "UPPER@TEST.COM", "password": "pass123"},
        )
        assert res.status_code == 201
        assert res.get_json()["user"]["email"] == "upper@test.com"

    def test_registro_rol_por_defecto_es_user(self, client):
        """El rol por defecto de un nuevo usuario debe ser 'user'."""
        res = client.post(
            REGISTER_URL,
            json={"name": "Test", "email": "rol@test.com", "password": "pass123"},
        )
        assert res.get_json()["user"]["role"] == "user"

    def test_registro_retorna_access_token(self, client):
        """El registro exitoso debe devolver un access_token."""
        res = client.post(
            REGISTER_URL,
            json={"name": "Test", "email": "tok@test.com", "password": "pass123"},
        )
        data = res.get_json()
        assert "access_token" in data
        assert data["access_token"] is not None

    def test_registro_no_expone_password_hash(self, client):
        """La respuesta no debe incluir el campo password_hash."""
        res = client.post(
            REGISTER_URL,
            json={"name": "Test", "email": "nohash@test.com", "password": "pass123"},
        )
        user_data = res.get_json().get("user", {})
        assert "password_hash" not in user_data
        assert "password" not in user_data


# ===========================================================================
# LOGIN — Validaciones de entrada
# ===========================================================================


class TestLoginValidacion:
    """Pruebas unitarias de validación del endpoint de login."""

    def test_login_sin_body_retorna_400(self, client):
        """Sin body debe devolver 400."""
        res = client.post(LOGIN_URL)
        assert res.status_code == 400

    def test_login_body_no_json_retorna_400(self, client):
        """Body que no es JSON debe devolver 400."""
        res = client.post(LOGIN_URL, data="no json", content_type="text/plain")
        assert res.status_code == 400

    def test_login_sin_email_retorna_422(self, client):
        """Sin campo email debe devolver 422."""
        res = client.post(LOGIN_URL, json={"password": "pass123"})
        assert res.status_code == 422

    def test_login_sin_password_retorna_422(self, client):
        """Sin campo password debe devolver 422."""
        res = client.post(LOGIN_URL, json={"email": "alguien@test.com"})
        assert res.status_code == 422

    def test_login_password_incorrecta_retorna_401(self, client, usuario_registrado):
        """Contraseña incorrecta debe devolver 401."""
        res = client.post(
            LOGIN_URL,
            json={
                "email": usuario_registrado["user"]["email"],
                "password": "clave_incorrecta",
            },
        )
        assert res.status_code == 401
        assert "error" in res.get_json()

    def test_login_email_inexistente_retorna_401(self, client):
        """Un email que no existe debe devolver 401."""
        res = client.post(
            LOGIN_URL,
            json={"email": "fantasma@test.com", "password": "cualquier"},
        )
        assert res.status_code == 401

    def test_login_usuario_inactivo_retorna_403(self, client, app):
        """Un usuario con is_active=False no puede iniciar sesión."""
        from app.auth.models.user import User
        from app.core.extensions import db

        with app.app_context():
            user = User(name="Inactivo", email="inactivo@test.com", is_active=False)
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()

        res = client.post(
            LOGIN_URL, json={"email": "inactivo@test.com", "password": "pass123"}
        )
        assert res.status_code == 403
        assert "error" in res.get_json()

    def test_login_acepta_email_en_mayusculas(self, client, usuario_registrado):
        """El login debe funcionar aunque el email se envíe en mayúsculas."""
        res = client.post(
            LOGIN_URL,
            json={
                "email": usuario_registrado["user"]["email"].upper(),
                "password": usuario_registrado["password"],
            },
        )
        assert res.status_code == 200

    def test_login_exitoso_retorna_token(self, client, usuario_registrado):
        """Login exitoso debe retornar un access_token."""
        res = client.post(
            LOGIN_URL,
            json={
                "email": usuario_registrado["user"]["email"],
                "password": usuario_registrado["password"],
            },
        )
        data = res.get_json()
        assert "access_token" in data
        assert data["access_token"] is not None


# ===========================================================================
# LOGOUT — Validaciones de token
# ===========================================================================


class TestLogoutValidacion:
    """Pruebas unitarias de validación del endpoint de logout."""

    def test_logout_sin_token_retorna_401(self, client):
        """Sin header Authorization debe devolver 401."""
        res = client.post(LOGOUT_URL)
        assert res.status_code == 401

    def test_logout_token_invalido_retorna_422(self, client):
        """Token con formato incorrecto debe devolver 422."""
        res = client.post(
            LOGOUT_URL,
            headers={"Authorization": "Bearer token_completamente_invalido"},
        )
        assert res.status_code == 422

    def test_logout_sin_prefijo_bearer_retorna_401(self, client):
        """Header sin prefijo Bearer debe devolver 401."""
        res = client.post(
            LOGOUT_URL,
            headers={"Authorization": "SinPrefijo alguntokenfake"},
        )
        assert res.status_code == 401

    def test_logout_token_revocado_no_reutilizable(self, client, usuario_registrado):
        """Después del logout, el mismo token no puede usarse de nuevo."""
        token = usuario_registrado["token"]
        client.post(LOGOUT_URL, headers={"Authorization": f"Bearer {token}"})
        res = client.post(LOGOUT_URL, headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 401

    def test_logout_exitoso_retorna_mensaje(self, client, usuario_registrado):
        """Logout exitoso debe retornar un mensaje de confirmación."""
        res = client.post(
            LOGOUT_URL,
            headers={"Authorization": f"Bearer {usuario_registrado['token']}"},
        )
        assert res.status_code == 200
        assert "message" in res.get_json()


# ===========================================================================
# PROFILE — Validaciones de GET y PUT
# ===========================================================================


class TestProfileValidacion:
    """Pruebas unitarias de validación de los endpoints de perfil."""

    def test_get_profile_sin_token_retorna_401(self, client):
        """GET /profile sin token debe devolver 401."""
        res = client.get(PROFILE_URL)
        assert res.status_code == 401

    def test_get_profile_token_invalido_retorna_422(self, client):
        """GET /profile con token inválido debe devolver 422."""
        res = client.get(
            PROFILE_URL, headers={"Authorization": "Bearer token_invalido"}
        )
        assert res.status_code == 422

    def test_get_profile_retorna_datos_del_usuario(self, client, auth_token):
        """GET /profile con token válido debe devolver id, name y email."""
        res = client.get(
            PROFILE_URL, headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert res.status_code == 200
        data = res.get_json()
        assert "user" in data
        assert "id" in data["user"]
        assert "name" in data["user"]
        assert "email" in data["user"]

    def test_update_profile_sin_token_retorna_401(self, client):
        """PUT /profile sin token debe devolver 401."""
        res = client.put(PROFILE_URL, json={"name": "Nuevo"})
        assert res.status_code == 401

    def test_update_profile_token_invalido_retorna_422(self, client):
        """PUT /profile con token inválido debe devolver 422."""
        res = client.put(
            PROFILE_URL,
            json={"name": "Nuevo"},
            headers={"Authorization": "Bearer token_invalido"},
        )
        assert res.status_code == 422

    def test_update_profile_actualiza_nombre(self, client, auth_token):
        """PUT /profile debe actualizar el nombre del usuario."""
        res = client.put(
            PROFILE_URL,
            json={"name": "Nombre Actualizado"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 200

    def test_update_profile_sin_body_es_valido(self, client, auth_token):
        """PUT /profile sin body JSON no debe fallar (actualización vacía)."""
        res = client.put(
            PROFILE_URL,
            json={},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 200
