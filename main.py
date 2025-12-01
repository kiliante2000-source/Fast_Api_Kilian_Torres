# from dotenv import load_dotnev
# load_dotnev()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import mysql.connector
from configuration.connection import DatabaseConnection
import os

APY_KEY_OPENWEATHER = os.getenv("SPOTIFY_API_KEY")

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# ---Apartado de usuario
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

@app.post("/users")
async def post_user(request: Request):
    my_db = DatabaseConnection(
        host="localhost",
        user="root",
        password="password",
        database="mi_base_datos"
    )
    db_connection = await my_db.connect()
    request = await request.json()
    username = request.form().get("name")
    age = request.form().get("age")
    mycursor = db_connection.cursor()
    mycursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (username, age))
    db_connection.commit()
    return JSONResponse(content={"message": "User added successfully"}, status_code=201)


@app.get("users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.put("users/{user_id}")
async def update_user(user_id: int):
    my_db = DatabaseConnection(
        host="localhost",
        user="root",
        password="password",
        database="my_db"
    )
    db_connection = await my_db.connect()
    mycursor = db_connection.cursor()
    mycursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (username, age))
    db_connection.commit()
    
    return {"message": "User updated successfully"}

@app.delete("users/{user_id}")
async def delete_user(user_id: int):
    my_db = DatabaseConnection(
        host="localhost",
        user="root",
        password="password",
        database="mi_base_datos"
    )
    db_connection = await my_db.connect()
    mycursor = db_connection.cursor()
    mycursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db_connection.commit()
    return {"message": "User deleted successfully"}
    

# @appget("/weather/{city}")
# async def get_weather(city: str):
#     db_connection = DatabaseConnection(
#         host="localhost",
#         user="root",
#         password="password",
#         database="mi_base_datos"
#     )
    






