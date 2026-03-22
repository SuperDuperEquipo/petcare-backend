"""
Tests unitarios para el modelo User.

Verifican la lógica del modelo de forma aislada, sin necesidad
de llamadas HTTP. La base de datos es SQLite en memoria.
"""

import pytest
from app.auth.models.user import User
from app.core.extensions import db


class TestUserPasswordHashing:
    """Pruebas sobre el hashing de contraseñas."""

    def test_set_password_no_guarda_texto_plano(self):
        """La contraseña almacenada nunca debe ser el texto original."""
        user = User(name="Ana", email="ana@test.com")
        user.set_password("secreto123")

        assert user.password_hash != "secreto123"

    def test_set_password_genera_hash(self):
        """set_password debe poblar el atributo password_hash."""
        user = User(name="Ana", email="ana@test.com")
        user.set_password("secreto123")

        assert user.password_hash is not None
        assert len(user.password_hash) > 0

    def test_check_password_correcto(self):
        """check_password retorna True cuando la contraseña es correcta."""
        user = User(name="Ana", email="ana@test.com")
        user.set_password("miPassword")

        assert user.check_password("miPassword") is True

    def test_check_password_incorrecto(self):
        """check_password retorna False cuando la contraseña es incorrecta."""
        user = User(name="Ana", email="ana@test.com")
        user.set_password("miPassword")

        assert user.check_password("otraPassword") is False

    def test_check_password_vacio(self):
        """check_password retorna False para una contraseña vacía."""
        user = User(name="Ana", email="ana@test.com")
        user.set_password("miPassword")

        assert user.check_password("") is False

    def test_hashes_distintos_para_mismo_password(self):
        """Dos usuarios con la misma contraseña deben tener hashes diferentes (salt)."""
        user1 = User(name="Ana", email="ana@test.com")
        user2 = User(name="Bob", email="bob@test.com")
        user1.set_password("igualPassword")
        user2.set_password("igualPassword")

        assert user1.password_hash != user2.password_hash


class TestUserToDict:
    """Pruebas sobre la serialización del usuario."""

    def test_to_dict_no_incluye_password_hash(self):
        """to_dict no debe exponer el hash de la contraseña."""
        user = User(name="Carlos", email="carlos@test.com")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        data = user.to_dict()
        assert "password_hash" not in data
        assert "password" not in data

    def test_to_dict_contiene_campos_esperados(self):
        """to_dict debe contener id, name, email, role, is_active y created_at."""
        user = User(name="Carlos", email="carlos@test.com")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        data = user.to_dict()
        assert "id" in data
        assert "name" in data
        assert "email" in data
        assert "role" in data
        assert "is_active" in data
        assert "created_at" in data

    def test_to_dict_valores_correctos(self):
        """to_dict debe reflejar los valores reales del usuario."""
        user = User(name="Carlos", email="carlos@test.com")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        data = user.to_dict()
        assert data["name"] == "Carlos"
        assert data["email"] == "carlos@test.com"
        assert data["role"] == "user"
        assert data["is_active"] is True


class TestUserDefaults:
    """Pruebas sobre los valores por defecto del modelo."""

    def test_rol_por_defecto_es_user(self):
        """El rol por defecto de un nuevo usuario debe ser 'user'."""
        user = User(name="Pepe", email="pepe@test.com")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        assert user.role == "user"

    def test_is_active_por_defecto_es_true(self):
        """Un usuario recién creado debe estar activo por defecto."""
        user = User(name="Pepe", email="pepe@test.com")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        assert user.is_active is True

    def test_created_at_se_asigna_automaticamente(self):
        """created_at debe asignarse al guardar el usuario."""
        user = User(name="Pepe", email="pepe@test.com")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        assert user.created_at is not None

    def test_email_es_unico(self):
        """No se pueden crear dos usuarios con el mismo email."""
        from sqlalchemy.exc import IntegrityError

        u1 = User(name="Uno", email="dup@test.com")
        u1.set_password("pass123")
        u2 = User(name="Dos", email="dup@test.com")
        u2.set_password("pass456")

        db.session.add(u1)
        db.session.commit()
        db.session.add(u2)

        with pytest.raises(IntegrityError):
            db.session.commit()
