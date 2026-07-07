# Polla Mundial 2026

Aplicación web desarrollada en Streamlit para gestionar una polla privada del Mundial 2026. Permite registrar usuarios, consultar partidos, hacer pronósticos con combinadas y llevar una tabla de posiciones automática.

## Características

- Base de datos dual: SQLite (desarrollo local) y PostgreSQL (producción).
- Autenticación con contraseña hasheada (bcrypt).
- Bloqueo automático de pronósticos 1 hora antes de cada partido (hora de Bogotá).
- Funciones administrativas integradas.

## Instalación y Ejecución Local

1. Asegúrate de tener Python 3.12+ instalado.
2. Clona el repositorio y ubícate en la carpeta del proyecto.
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

> **Nota:** La primera vez que se ejecuta, la base de datos `polla_mundial.db` se creará automáticamente junto con las tablas necesarias.

### Usuario Administrador por Defecto
- **Usuario:** `admin`
- **Contraseña:** `unad2026`

## Despliegue en Streamlit Community Cloud

La aplicación está diseñada para ser desplegada gratuitamente sin modificar código.

1. Sube tu código a un repositorio público de GitHub.
2. Ve a [Streamlit Community Cloud](https://share.streamlit.io/) e inicia sesión.
3. Crea una nueva aplicación apuntando al repositorio de GitHub, configurando `app.py` como el archivo principal.
4. **Base de datos de producción:** En Streamlit Community Cloud, ve a los ajustes avanzados (Secrets) y agrega tu conexión a PostgreSQL así:

```toml
DATABASE_URL="postgres://usuario:contraseña@host:puerto/nombre_db"
```

Si detecta `DATABASE_URL`, utilizará PostgreSQL automáticamente; si no, usará SQLite.

## API de Fútbol
El proyecto incluye un script de sincronización (`services/sync_service.py`) preparado para extraer datos de las APIs `football-data.org` o `TheSportsDB`.

Actualmente, el sistema está configurado para mostrar cómo los partidos son agregados automáticamente en caso de no contar con una Key.

## Estructura
```
app.py                # Entrada principal de Streamlit
config.py             # Manejo de la URL de base de datos
database/             # Conexión e inicialización y schema.sql
repositories/         # Funciones puras de SQL sin ORMs
services/             # Lógica de sincronización y cálculo de puntajes
pages/                # Páginas de Streamlit
utils/                # Utilidades de hora y hash
```