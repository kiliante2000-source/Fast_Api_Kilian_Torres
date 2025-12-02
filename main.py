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

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

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

#---Apartado de canciones de spotify API y autenticacion

token_info = None  # fuera de la función
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

@app.get("/spotify/callback")
async def spotify_callback_get_song(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code received"}

    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-read-private user-read-email user-library-read"
    )

    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']

    sp = spotipy.Spotify(auth=access_token)
    results = sp.current_user_saved_tracks(limit=5)
    
    songs = [{"name": t["track"]["name"], "artist": t["track"]["artists"][0]["name"]} for t in results['items']]
    return {"songs": songs}
    


    

#Apartado de obtencion de artistas de spotify API

# Apartado de obtencion de albums de spotify API

    






