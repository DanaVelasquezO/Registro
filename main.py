from db.setup import ejecutar_setup
from db.conexion import obtener_conexion
from app.login import iniciar_login

def main():
    # 1. inicializar base de datos
    ejecutar_setup()

    # 2. conectar normalmente
    conexion = obtener_conexion()
    if not conexion:
        print("No se pudo conectar a la BD")
        return
    conexion.close()

    # 3. iniciar login
    iniciar_login()

if __name__ == "__main__":
    main()
