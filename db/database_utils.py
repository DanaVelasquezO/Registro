from db.conexion import obtener_conexion

def ejecutar_consulta(consulta, parametros=None, fetch=False, fetch_all=False):
    """
    Función utilitaria para ejecutar consultas de manera segura
    """
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if not conexion:
            raise Exception("No se pudo establecer conexión con la base de datos")
            
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros or ())
        
        if fetch:
            resultado = cursor.fetchone()
        elif fetch_all:
            resultado = cursor.fetchall()
        else:
            resultado = None
        
        return resultado
        
    except Exception as e:
        print(f"Error en consulta: {e}")
        raise e
    finally:
        # Cerrar cursor y conexión en orden
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def ejecutar_multiples_consultas(consultas):
    """
    Ejecuta múltiples consultas de forma segura
    """
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if not conexion:
            raise Exception("No se pudo establecer conexión con la base de datos")
            
        cursor = conexion.cursor()
        resultados = []
        
        for consulta, parametros in consultas:
            cursor.execute(consulta, parametros or ())
            # Si es una consulta SELECT, obtener resultados
            if consulta.strip().upper().startswith('SELECT'):
                resultados.append(cursor.fetchall())
            else:
                resultados.append(None)
        
        return resultados
        
    except Exception as e:
        print(f"Error en consultas múltiples: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()