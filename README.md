[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/8dHAom8r)

## Repartición de tareas a priori

### Antonia:

* Set up frontend: Vite (Vainilla) + Tailwind
* Configurar como PWA
* Crear vistas frontend (Login, principal para ver llamadas, historial de llamadas, llamada misma)
* Set up backend: FastAPI + SQLAlchemy + Docker
* Crear modelo de migraciones base backend
* Funcionamiento Offline (ver contactos y ver historial de llamadas)

### Tomás:

* Conexión WebRTC
* Historial de llamadas

### Pablo:

* Notificaciones push
* Endpoints base
* Rellenar con seed
* Deployeo
* Arreglos para que quede perfecta

---

## Integridad Académica

Este código fue desarrollado con asistencia de Inteligencia Artificial:

* Modelo: GPT-4o
* Plataforma: Página Web de Chat GPT
* Cómo se usó: archivos *.html

---

## Frontend

Para inicializar, es necesario que encontrándose en la raíz de la carpeta `Frontend`, ejecute los siguientes comandos:

```bash
npm install
npm run dev
```

### Arquitectura

```
Frontend/
├── public/
│   ├── icono.png
│   ├── manifest.json
│   └── service-worker.js
├── src/
│   ├── js/
│   ├── css/
│   ├── html/
├── .gitignore
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
```

---

## Backend

### Arquitectura

```
Backend/
├── Api/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── main.py
│   ├── packages.py
│   ├── database.py
│   ├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
```

### Variables de entorno

Es necesario tener las variables de ambiente. Para ello se debe copiar el archivo `env.example` como `.env` y reemplazar los valores por los propios.

### Docker

Para correr Docker, debes ejecutar el siguiente comando desde el directorio donde está ubicado `docker-compose.yml`:

```bash
docker compose up -d
```

### Generar seeds

```bash
docker exec -it /route/ npm run seed:run
```

### Diagrama E-R

![Diagrama ER](Backend/Api/E-R.png)

### Comandos útiles de Sequelize y PostgreSQL

- Iniciar PostgreSQL:`sudo service postgresql start` o `psql postgres`
- Conectarse a una base de datos:`\c "nombre_bdd"`
- Ver tablas:`\d`
- Ver usuarios:`\du`
- Ver bases de datos:`\l`
- Crear un usuario:`sudo -u postgres createuser --superuser [usuario]`
- Crear una base de datos:`sudo -u postgres createdb [nombre_bdd]` o `CREATE DATABASE nombre`
- Eliminar una base de datos:`DROP DATABASE nombre;`
- Asignar contraseña a un usuario:`ALTER USER [usuario] WITH PASSWORD 'clave';`
- Conectarse con usuario:`psql -U tu_usuario -d nombre_db`
- Reiniciar esquema:`DROP SCHEMA public CASCADE; CREATE SCHEMA public;`
- Reiniciar secuencia de IDs:
  `ALTER SEQUENCE name_seq RESTART WITH 1;`
