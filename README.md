# PetCare 

## Descripción

Este proyecto consiste en una aplicación backend para la gestión de un sistema de cuidado de mascotas (**PetCare**), completamente dockerizada para facilitar su despliegue y ejecución en cualquier entorno.

La aplicación incluye:

* API backend en Python (Flask)
* Base de datos MariaDB
* Frontend conectado a la API
* Orquestación completa con Docker Compose

---

## Tecnologías utilizadas

* Python 3.11
* Flask
* MariaDB
* Docker
* Docker Compose

---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/SuperDuperEquipo/petcare-backend
git clone https://github.com/SuperDuperEquipo/petcare-backend
cd petcare-backend
```

---

### 2. Configurar variables de entorno

Crear un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

---

### 3. Levantar los servicios

```bash
docker-compose up --build
```

---

### 4. Acceder a la aplicación

* Backend API: http://localhost:5000
* Frontend: http://localhost:3000

---

##  Servicios definidos

### Backend (API)

* Construido con Flask
* Ejecuta migraciones automáticamente:

  ```bash
  flask db upgrade
  ```
* Puerto expuesto: 5000

---

### Base de datos (MariaDB)

* Contenedor independiente
* Persistencia mediante volumen
* Healthcheck configurado

---

### Frontend

* Aplicación cliente conectada al backend
* Puerto expuesto: 3000

---

## Red y volúmenes

* Red personalizada: `petcare_net`
* Volumen persistente: `petcare_db_data`

---

## Comandos útiles

### Detener servicios

```bash
docker-compose down
```

### Ver logs

```bash
docker-compose logs -f
```

### Reconstruir contenedores

```bash
docker-compose up --build
```

---

