"""
Prueba de integración end-to-end del sistema PetCare.

Verifica el flujo completo del negocio en una sola prueba secuencial:
  1. Registrar usuario (propietario)
  2. Completar perfil del propietario
  3. Crear mascota
  4. Agregar vacuna a la mascota
  5. Crear cita para la mascota

Cada paso verifica el estado correcto antes de continuar con el siguiente.
"""


def test_flujo_completo_registro_propietario_mascota_vacuna_cita(client):
    """
    E2E: registrar usuario → completar perfil → crear mascota
         → agregar vacuna → crear cita
    """

    # ------------------------------------------------------------------ #
    # 1. Registrar usuario (este usuario es el propietario de mascotas)   #
    # ------------------------------------------------------------------ #
    res_registro = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Ana García",
            "email": "ana.garcia@petcare.com",
            "password": "segura123",
        },
    )
    assert res_registro.status_code == 201, (
        f"[E2E-1] Registro falló: {res_registro.get_json()}"
    )
    data_registro = res_registro.get_json()
    token = data_registro["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    usuario = data_registro["user"]

    assert usuario["email"] == "ana.garcia@petcare.com"
    assert usuario["role"] == "user"
    assert "password_hash" not in usuario
    print(f"\n[E2E-1] Usuario registrado: id={usuario['id']}, email={usuario['email']}")

    # ------------------------------------------------------------------ #
    # 2. Completar perfil del propietario                                 #
    # ------------------------------------------------------------------ #
    res_perfil = client.put(
        "/api/v1/auth/profile",
        json={"name": "Ana García (Propietaria)"},
        headers=headers,
    )
    assert res_perfil.status_code == 200, (
        f"[E2E-2] Actualizar perfil falló: {res_perfil.get_json()}"
    )
    print("[E2E-2] Perfil del propietario actualizado")

    # Verificar que el perfil refleja el cambio
    res_get_perfil = client.get("/api/v1/auth/profile", headers=headers)
    assert res_get_perfil.status_code == 200
    assert res_get_perfil.get_json()["user"]["email"] == "ana.garcia@petcare.com"
    print("[E2E-2] Perfil verificado correctamente")

    # ------------------------------------------------------------------ #
    # 3. Crear mascota                                                    #
    # ------------------------------------------------------------------ #
    res_mascota = client.post(
        "/api/v1/pets",
        json={
            "name": "Milo",
            "species": "Perro",
            "breed": "Labrador",
            "birth_date": "2022-03-15",
            "weight": 25.5,
        },
        headers=headers,
    )
    assert res_mascota.status_code == 201, (
        f"[E2E-3] Crear mascota falló: {res_mascota.get_json()}"
    )
    mascota = res_mascota.get_json()["mascota"]
    mascota_id = mascota["id"]
    assert mascota["nombre"] == "Milo"
    print(f"[E2E-3] Mascota creada: id={mascota_id}, nombre={mascota['nombre']}")

    # Verificar que la mascota aparece en el listado
    res_lista_mascotas = client.get("/api/v1/pets", headers=headers)
    assert res_lista_mascotas.status_code == 200
    assert res_lista_mascotas.get_json()["total"] == 1
    print("[E2E-3] Mascota verificada en listado")

    # ------------------------------------------------------------------ #
    # 4. Agregar vacuna a la mascota                                      #
    # ------------------------------------------------------------------ #
    res_vacuna = client.post(
        f"/api/v1/pets/{mascota_id}/vaccines",
        json={
            "name": "Rabia",
            "date_applied": "2026-01-10",
            "next_dose": "2027-01-10",
            "vet": "Dr. Martínez",
        },
        headers=headers,
    )
    assert res_vacuna.status_code == 201, (
        f"[E2E-4] Agregar vacuna falló: {res_vacuna.get_json()}"
    )
    vacuna = res_vacuna.get_json()["vacuna"]
    vacuna_id = vacuna["id"]
    assert vacuna["name"] == "Rabia"
    assert vacuna["vet"] == "Dr. Martínez"
    print(f"[E2E-4] Vacuna registrada: id={vacuna_id}, nombre={vacuna['name']}")

    # Verificar que la vacuna aparece en el historial
    res_vacunas = client.get(f"/api/v1/pets/{mascota_id}/vaccines", headers=headers)
    assert res_vacunas.status_code == 200
    vacunas_lista = res_vacunas.get_json()["vacunas"]
    assert len(vacunas_lista) == 1
    assert vacunas_lista[0]["name"] == "Rabia"
    print("[E2E-4] Vacuna verificada en historial")

    # ------------------------------------------------------------------ #
    # 5. Crear cita para la mascota                                       #
    # ------------------------------------------------------------------ #
    res_cita = client.post(
        "/api/v1/appointments",
        json={
            "title": "Control anual",
            "date": "2027-04-15",
            "time": "10:30:00",
            "type": "Consulta",
            "description": "Revisión general y refuerzo de vacunas",
            "pet_id": mascota_id,
        },
        headers=headers,
    )
    assert res_cita.status_code == 201, (
        f"[E2E-5] Crear cita falló: {res_cita.get_json()}"
    )
    cita = res_cita.get_json()["cita"]
    cita_id = cita["id"]
    assert cita["titulo"] == "Control anual"
    print(f"[E2E-5] Cita creada: id={cita_id}, titulo={cita['titulo']}")

    # Verificar que la cita aparece en el listado
    res_citas = client.get("/api/v1/appointments", headers=headers)
    assert res_citas.status_code == 200
    assert res_citas.get_json()["total"] == 1
    print("[E2E-5] Cita verificada en listado")

    print("\n[E2E] Flujo completo verificado exitosamente:")
    print(f"      Usuario   : id={usuario['id']}")
    print(f"      Mascota   : id={mascota_id}")
    print(f"      Vacuna    : id={vacuna_id}")
    print(f"      Cita      : id={cita_id}")
