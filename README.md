# 🐾 PetCare

## Descripción

Este proyecto consiste en una aplicación backend para la gestión de un sistema de cuidado de mascotas (**PetCare**), completamente dockerizada para facilitar su despliegue y ejecución en cualquier entorno.

La aplicación incluye:

- API backend en Python (Flask)
- Base de datos MariaDB
- Frontend conectado a la API
- Orquestación completa con Docker Compose

---

## Tecnologías utilizadas

- Python 3.11
- Flask
- MariaDB
- Docker
- Docker Compose

---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

    git clone https://github.com/SuperDuperEquipo/petcare-backend
    cd petcare-backend

---

### 2. Configurar variables de entorno

Crear un archivo `.env` basado en `.env.example`:

    cp .env.example .env

---

### 3. Levantar los servicios

    docker-compose up --build

---

### 4. Acceder a la aplicación

- Backend API: http://localhost:5000
- Frontend: http://localhost:3000

---

## Servicios definidos

### Backend (API)

- Construido con Flask
- Ejecuta migraciones automáticamente:

        flask db upgrade

- Puerto expuesto: 5000

---

### Base de datos (MariaDB)

- Contenedor independiente
- Persistencia mediante volumen
- Healthcheck configurado

---

### Frontend

- Aplicación cliente conectada al backend
- Puerto expuesto: 3000

---

## Red y volúmenes

- Red personalizada: `petcare_net`
- Volumen persistente: `petcare_db_data`

---

## Ejecución de pruebas

### Requisitos

- Python 3.10 o superior
- pip
- virtualenv (opcional)

---

### Preparar entorno de pruebas

Crear entorno virtual:

    python -m venv venv

Activar entorno:

Linux / Mac:

    source venv/bin/activate

Windows:

    venv\Scripts\activate

Instalar dependencias:

    pip install -r requirements.txt

Instalar dependencias de testing:

    pip install -r requirements-test.txt

---

### Ejecutar pruebas

Ejecutar todas las pruebas:

    pytest

Pruebas unitarias:

    pytest tests/unit/

Pruebas de integración:

    pytest tests/integration/

Pruebas smoke:

    pytest tests/smoke/

---

### Ejecuciones específicas

Archivo específico:

    pytest tests/unit/test_pets.py

Prueba específica:

    pytest tests/unit/test_pets.py::test_nombre_de_la_prueba

---

### Opciones útiles

Modo detallado:

    pytest -v

Mostrar logs:

    pytest -s

Detener en primer error:

    pytest -x

Limpiar caché:

    pytest --cache-clear

---

### Consideraciones

- Configurar variables de entorno (.env si aplica)
- Algunas pruebas requieren base de datos activa
- Revisar `conftest.py` para configuración global

---

## Comandos útiles

Detener servicios:

    docker-compose down

Ver logs:

    docker-compose logs -f

Reconstruir contenedores:

    docker-compose up --build

---
