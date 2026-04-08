def test_get_users_sin_token(client):
    """Sin token debe devolver 401"""
    res = client.get('/api/v1/admin/users')
    print(f"\nSin token users: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401


def test_get_users_usuario_normal(client, auth_token):
    """Usuario normal no puede acceder, debe devolver 403"""
    res = client.get(
        '/api/v1/admin/users',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nUsuario normal users: {res.status_code} - {res.get_json()}")
    assert res.status_code == 403


def test_delete_user_sin_token(client):
    """DELETE sin token debe devolver 401"""
    res = client.delete('/api/v1/admin/users/1')
    print(f"\nDelete sin token: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401


def test_delete_user_usuario_normal(client, auth_token):
    """Usuario normal no puede eliminar, debe devolver 403"""
    res = client.delete(
        '/api/v1/admin/users/1',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nDelete usuario normal: {res.status_code} - {res.get_json()}")
    assert res.status_code == 403


def test_delete_user_no_existente(client, admin_token):
    """Eliminar usuario inexistente debe devolver 404"""
    res = client.delete(
        '/api/v1/admin/users/9999',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"\nDelete no existente: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404

def test_get_users_token_invalido(client):
    """Token inválido debe devolver 422"""
    res = client.get(
        '/api/v1/admin/users',
        headers={"Authorization": "Bearer token_invalido"}
    )
    print(f"\nToken inválido: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422
    assert "Not enough segments" in res.get_json()["msg"]