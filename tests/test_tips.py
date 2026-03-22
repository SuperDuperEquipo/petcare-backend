# Pruebas unitarias
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


# Pruebas de integración
def test_get_tips_con_token(client, auth_token):
    """Con token válido debe devolver lista vacía"""
    res = client.get('/api/v1/tips', headers={
        "Authorization": f"Bearer {auth_token}"
    })
    print(f"\nLista de tips: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()['total'] == 0

def test_crear_tip_exitoso(client, admin_token):
    """Admin puede crear tip con datos válidos"""
    res = client.post('/api/v1/tips', json={
        "title": "Tip de salud",
        "content": "Dale agua fresca a tu mascota",
        "species": "Perro",
        "category": "Salud"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    print(f"\nTip creado: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201
    assert res.get_json()['tip']['titulo'] == 'Tip de salud'

def test_crear_tip_y_verificar_en_lista(client, admin_token, auth_token):
    """Crear un tip y verificar que aparece en el GET"""
    client.post('/api/v1/tips', json={
        "title": "Tip visible",
        "content": "Contenido visible",
        "species": "Gato",
        "category": "Nutrición"
    }, headers={"Authorization": f"Bearer {admin_token}"})

    res = client.get('/api/v1/tips', headers={
        "Authorization": f"Bearer {auth_token}"
    })
    print(f"\nTip en lista: {res.status_code} - total={res.get_json()['total']}")
    assert res.status_code == 200
    assert res.get_json()['total'] == 1
