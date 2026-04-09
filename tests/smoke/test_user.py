def test_smoke_register_user(client):
    """Humo: POST /api/v1/auth/register debe devolver 201"""
    res = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Dueño Humo",
            "email": "dueno_humo@petcare.com",
            "password": "password123",
        },
    )
    print(f"\nSmoke Register: {res.status_code}")
    assert res.status_code == 201


def test_smoke_login_user(client, usuario_registrado):
    """Humo: POST /api/v1/auth/login debe devolver 200"""
    res = client.post(
        "/api/v1/auth/login",
        json={"email": "test@petcare.com", "password": usuario_registrado["password"]},
    )
    print(f"\nSmoke Login: {res.status_code}")
    assert res.status_code == 200


def test_smoke_logout(client, usuario_registrado):
    """Humo: POST /api/v1/auth/logout debe devolver 200"""
    res = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {usuario_registrado['token']}"},
    )
    print(f"\nSmoke Logout: {res.status_code}")
    assert res.status_code == 200


def test_smoke_get_profile(client, auth_token):
    """Humo: GET /api/v1/auth/profile debe devolver 200"""
    res = client.get(
        "/api/v1/auth/profile",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke GET Profile: {res.status_code}")
    assert res.status_code == 200


def test_smoke_update_profile(client, auth_token):
    """Humo: PUT /api/v1/auth/profile debe devolver 200"""
    res = client.put(
        "/api/v1/auth/profile",
        json={"name": "Nombre Actualizado"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke PUT Profile: {res.status_code}")
    assert res.status_code == 200


def test_smoke_get_users_list(client, admin_token):
    """Humo: GET /api/v1/admin/users (solo para admin) debe devolver 200"""
    res = client.get(
        "/api/v1/admin/users", headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"\nSmoke GET Users: {res.status_code}")
    assert res.status_code == 200
