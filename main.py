from dotenv import load_dotenv
import os
load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
import mysql.connector
from configuration.connection import DatabaseConnection
import os

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mininayara23",
        database="my_db"
    )
    return conn


app = FastAPI()
#Creamos la autentificación con spotify
sp_auth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri= redirect_uri,
    scope="user-read-private user-read-email user-library-read",
    show_dialog=True
)

sp = spotipy.Spotify(auth_manager=sp_auth)


@app.get("/")
async def read_root():
    token = sp_auth.get_cached_token()
    if not token:
        auth_url = sp_auth.get_authorize_url()
        return RedirectResponse(auth_url)

    return {"message": "Welcome to the Spotify API integration with FastAPI!"}

#ahora una vez auntenticados obtenemos los datos del usuario
@app.get("/spotify/callback")
async def spotify_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code in callback"}

    token_info = sp_auth.get_access_token(code)

    sp = spotipy.Spotify(auth=token_info["access_token"])
    user = sp.current_user()

    return {"user": user}

#ahora tenemos que hacer que los datos del usuario se guarden en la base de datos que tenemos con parametros nam ey age
@app.post("/spotify/save_user")
async def save_user_songs():
    token = sp_auth.get_cached_token()
    if not token:
        return {"error": "User not authenticated"}

    sp = spotipy.Spotify(auth=token["access_token"])
    user = sp.current_user()
    username = user.get('display_name', 'NoName')

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Guardar usuario si no existe
    cursor.execute("SELECT id FROM users WHERE name=%s", (username,))
    user_row = cursor.fetchone()
    if user_row:
        user_id = user_row[0]
    else:
        cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (username, 25))
        conn.commit()
        user_id = cursor.lastrowid

    # 2. Obtener canciones guardadas por el usuario en Spotify
    results = sp.current_user_saved_tracks(limit=50)
    for item in results['items']:
        track = item['track']
        spotify_id = track['id']
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        # Guardar canción si no existe
        cursor.execute("SELECT id FROM songs WHERE spotify_id=%s", (spotify_id,))
        song_row = cursor.fetchone()
        if song_row:
            song_id = song_row[0]
        else:
            cursor.execute(
                "INSERT INTO songs (spotify_id, name, artist) VALUES (%s, %s, %s)",
                (spotify_id, track_name, artist_name)
            )
            conn.commit()
            song_id = cursor.lastrowid

        # 3. Asociar canción con usuario si no existe
        cursor.execute(
            "SELECT * FROM user_songs WHERE user_id=%s AND song_id=%s",
            (user_id, song_id)
        )
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO user_songs (user_id, song_id) VALUES (%s, %s)",
                (user_id, song_id)
            )
            conn.commit()

    conn.close()
    return {"message": f"Saved songs for user {username}"}

# @app.get("/spotify/user/getsongs")
# async def spotify_callback_get_song(request: Request):
#     code = request.query_params.get("code")
#     if not code:
#         return {"error": "No code received"}

#     sp_oauth = SpotifyOAuth(
#         client_id=os.getenv("SPOTIFY_CLIENT_ID"),
#         client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
#         redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
#         scope="user-read-private user-read-email user-library-read"
#     )

#     token_info = sp_oauth.get_access_token(code)
#     access_token = token_info['access_token']

#     sp = spotipy.Spotify(auth=access_token)
#     results = sp.current_user_saved_tracks(limit=5)
    
#     songs = [{"name": t["track"]["name"], "artist": t["track"]["artists"][0]["name"]} for t in results['items']]
#     return {"songs": songs}

#

# ---Apartado de usuario
#Apartado de obtencion de todos los usuarios de la base de datos
@app.get("/users")
async def get_users():
    my_db = DatabaseConnection(
        host="localhost",
        user="root",
        password="Mininayara23",
        database="my_db"
    )
    db_connection = await my_db.connect()
    mycursor = db_connection.cursor()
    mycursor.execute("SELECT * FROM users")
    users = mycursor.fetchall()
    db_connection.close()
    return {"users": users}

#Apartado de obtencion de usuario por id de la base de datos
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    my_db = DatabaseConnection(
        host="localhost",
        user="root",
        password="Mininayara23",
        database="my_db"
    )
    db_connection = await my_db.connect()
    mycursor = db_connection.cursor()
    mycursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = mycursor.fetchone()
    db_connection.close()
    return {"user": user}

#Apartado de creacion de usuario en la base de datos
@app.post("/users")
async def post_user(request: Request):
    my_db = DatabaseConnection(
        host="localhost",
        user="root",
        password="Mininayara23",
        database="my_db"
    )
    db_connection = await my_db.connect()
    request = await request.json()
    username = request.get("name")
    age = request.get("age")
    mycursor = db_connection.cursor()
    mycursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (username, age))
    db_connection.commit()
    db_connection.close()
    return JSONResponse(content={"message": "User added successfully"}, status_code=201)



#apartado de actualizacion de usuario de la base de datos
@app.put("/users/{user_id}")
async def update_user(user_id: int, data:dict):
    my_db = DatabaseConnection(
        host="localhost",
        user="root",
        password="Mininayara23",
        database="my_db"
    )
    request = data
    username = request.get("name")
    age = request.get("age")
    db_connection = await my_db.connect()
    mycursor = db_connection.cursor()
    mycursor.execute("UPDATE users SET name = %s, age = %s WHERE id = %s", (username, age, user_id))
    db_connection.commit()
    db_connection.close()
    return {"message": "User updated successfully"}

#Apartado de borrado de usuario de la base de datos
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    my_db = DatabaseConnection(
        host="localhost",
        user="root",
        password="Mininayara23",
        database="my_db"
    )
    db_connection = await my_db.connect()
    mycursor = db_connection.cursor()
    mycursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db_connection.commit()
    db_connection.close()
    return {"message": "User deleted successfully"}

#Método 
@app.get("/spotify/auth")
async def spotify_auth():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope = "user-read-private user-read-email user-library-read"
    )
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)
    






