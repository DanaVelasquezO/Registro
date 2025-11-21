import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Obtener ruta absoluta del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ejecutar_sql(ruta_archivo, conexion):
    cursor = conexion.cursor()
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Ejecutar sentencias separadas por ";"
    for sentencia in sql_script.split(";"):
        sentencia = sentencia.strip()
        if sentencia:
            try:
                cursor.execute(sentencia)
            except Exception as e:
                print(f"\nError ejecutando sentencia:\n{sentencia}\n{e}\n")

    conexion.commit()
    cursor.close()


def ejecutar_setup():
    DB_NAME = os.getenv("DB_NAME")

    # -------------------------------------------
    # 1) Conectar SOLO al servidor MySQL
    # -------------------------------------------
    conexion = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conexion.cursor()

    # -------------------------------------------
    # 2) Verificar si existe la BD
    # -------------------------------------------
    cursor.execute("SHOW DATABASES LIKE %s", (DB_NAME,))
    existe = cursor.fetchone()

    if existe:
        print("La base de datos ya existe. Setup omitido.")
        cursor.close()
        conexion.close()
        return

    print("La base no existe. Ejecutando setup...")

    # -------------------------------------------
    # 3) Ejecutar script de creación
    # -------------------------------------------
    path_creacion = os.path.join(BASE_DIR, "db", "sql", "creacion_db.sql")
    ejecutar_sql(path_creacion, conexion)

    # RE-conectar pero ahora dentro de la BD creada
    conexion.close()
    conexion = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=DB_NAME
    )

    # -------------------------------------------
    # 4) Ejecutar inserciones iniciales
    # -------------------------------------------
    path_inserciones = os.path.join(BASE_DIR, "db", "sql", "inserciones.sql")
    ejecutar_sql(path_inserciones, conexion)

    print("Base creada e inicializada correctamente.")

    conexion.close()
