def test_get_tips_sin_token(client):
    """Sin token debe devolver 401"""
    res = client.get('/api/v1/tips')
    print(f"\nRespuesta sin token: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401

def test_crear_tip_sin_titulo(client, admin_token):
    """Sin title debe devolver 422"""
    res = client.post('/api/v1/tips', json={
        "content": "Contenido",
        "species": "Perro",
        "category": "Salud"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    print(f"\nError sin titulo: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422

def test_crear_tip_sin_content(client, admin_token):
    """Sin content debe devolver 422"""
    res = client.post('/api/v1/tips', json={
        "title": "Tip de prueba",
        "species": "Perro",
        "category": "Salud"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    print(f"\nError sin content: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422

def test_crear_tip_body_no_json(client, admin_token):
    """Body que no es JSON debe devolver 400"""
    res = client.post('/api/v1/tips',
        data="no es un JSON",
        content_type="text/plain",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"\nError body no JSON: {res.status_code} - {res.get_json()}")
    assert res.status_code == 400

def test_crear_tip_rol_usuario_normal(client, auth_token):
    """Un usuario normal no puede crear tips, debe devolver 403"""
    res = client.post('/api/v1/tips', json={
        "title": "Tip de prueba",
        "content": "Contenido",
        "species": "Perro",
        "category": "Salud"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    print(f"\nError rol usuario normal: {res.status_code} - {res.get_json()}")
    assert res.status_code == 403

def test_token_expirado_tips(client, app):
    """Token vencido debe devolver 401"""
    from flask_jwt_extended import create_access_token
    from datetime import timedelta

    with app.app_context():
        with app.test_request_context():
            token_expirado = create_access_token(
                identity="1",
                expires_delta=timedelta(seconds=-1)
            )

    res = client.get('/api/v1/tips', headers={
        "Authorization": f"Bearer {token_expirado}"
    })
    print(f"\nError token expirado: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401

def test_crear_tip_campos_vacios(client, admin_token):
    """Campos vacíos (strings vacíos o espacios) deben devolver 422"""
    res = client.post('/api/v1/tips', json={
        "title": "   ",
        "content": "",
        "species": "Perro",
        "category": "Salud"
    }, headers={"Authorization": f"Bearer {admin_token}"})

    print(f"\nError campos vacíos: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422