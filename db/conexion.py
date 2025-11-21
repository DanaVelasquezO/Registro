from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

load_dotenv()

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            autocommit=True
        )

        if conexion.is_connected():
            return conexion
        else:
            print("No se pudo conectar a MySQL.")
            return None

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None


def test_conexion():
    conexion = obtener_conexion()
    if conexion is None:
        print("Conexión fallida.")
        return

    try:
        if not conexion.is_connected():
            conexion.reconnect()

        print(f"Conexión correcta a la BD: {os.getenv('DB_NAME')}")

    except Error as e:
        print(f"Error durante la prueba de conexión: {e}")
    
    finally:
        conexion.close()
