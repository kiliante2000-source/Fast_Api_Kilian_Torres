# FastAPI + MySQL + Spotify API

Esta aplicación es un ejemplo de integración de **FastAPI** con **MySQL** y la **API de Spotify**, que permite gestionar usuarios y sus canciones guardadas en Spotify, asociándolas a una base de datos local.

---

## Características

### CRUD de usuarios
- Endpoints para crear y listar usuarios en la tabla `users` de MySQL.
- La tabla `users` contiene los campos: `id`, `name` y `age`.

### Autenticación con Spotify
- Endpoints para autenticar usuarios mediante OAuth con la API de Spotify.
- Obtención de información del usuario autenticado (`display_name`, `email`, etc.).

### Guardar usuario de Spotify en la base de datos
- Endpoint que guarda en la tabla `users` la información del usuario autenticado en Spotify.
- Se usa un valor por defecto para `age` (ya que Spotify no proporciona la edad).

### Guardar canciones asociadas a un usuario
- Endpoint que obtiene las canciones guardadas por el usuario en Spotify.
- Guarda las canciones en la tabla `songs` (`spotify_id`, `name`, `artist`).
- Crea relaciones entre usuarios y canciones en la tabla `user_songs` para indicar qué canciones pertenecen a qué usuario.

---

## Configuración

### Variables de entorno

Antes de iniciar la aplicación, configura las siguientes variables de entorno:

```bash
SPOTIFY_CLIENT_ID=<tu_client_id>
SPOTIFY_CLIENT_SECRET=<tu_client_secret>
SPOTIFY_REDIRECT_URI=http://localhost:8000/spotify/callback
