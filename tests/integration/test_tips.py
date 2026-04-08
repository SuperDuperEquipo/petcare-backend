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
