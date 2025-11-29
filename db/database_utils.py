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
        
        resultado = None
        if fetch:
            resultado = cursor.fetchone()
        elif fetch_all:
            resultado = cursor.fetchall()
        
        # CONSUMIR TODOS LOS RESULTADOS PENDIENTES
        if cursor.with_rows:
            cursor.fetchall()
        
        # Si no es una consulta de selección, hacer commit
        if not fetch and not fetch_all:
            conexion.commit()
        
        return resultado
        
    except Exception as e:
        print(f"Error en consulta: {e}")
        if conexion:
            conexion.rollback()
        raise e
    finally:
        # Cerrar cursor y conexión en orden
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def ejecutar_consulta_segura(consulta, parametros=None):
    """
    Versión más segura que siempre consume todos los resultados
    """
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if not conexion:
            raise Exception("No se pudo establecer conexión con la base de datos")
            
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros or ())
        
        # Siempre consumir todos los resultados
        if cursor.with_rows:
            resultado = cursor.fetchall()
        else:
            resultado = None
        
        conexion.commit()
        return resultado
        
    except Exception as e:
        print(f"Error en consulta segura: {e}")
        if conexion:
            conexion.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def obtener_nota_existente(numero_registro, codigo_estudiante, id_indicador):
    """
    Obtiene una nota existente de manera segura
    """
    try:
        resultado = ejecutar_consulta_segura(
            """
            SELECT Nota 
            FROM Notas_Registro 
            WHERE Numero_de_registro = %s 
            AND Codigo_estudiante = %s 
            AND Id_indicador = %s
            """,
            (numero_registro, codigo_estudiante, id_indicador)
        )
        
        if resultado and len(resultado) > 0 and resultado[0][0] is not None:
            return float(resultado[0][0])
        return None
        
    except Exception as e:
        print(f"Error al obtener nota existente: {e}")
        return None

def verificar_nota_existente(numero_registro, codigo_estudiante, id_indicador):
    """
    Verifica si existe una nota para un indicador específico
    """
    try:
        resultado = ejecutar_consulta_segura(
            """
            SELECT 1 FROM Notas_Registro 
            WHERE Numero_de_registro = %s 
            AND Codigo_estudiante = %s 
            AND Id_indicador = %s
            """,
            (numero_registro, codigo_estudiante, id_indicador)
        )
        
        return resultado is not None and len(resultado) > 0
    except Exception as e:
        print(f"Error al verificar nota existente: {e}")
        return False

def guardar_nota(numero_registro, codigo_estudiante, id_competencia, id_indicador, nota):
    """
    Guarda o actualiza una nota de manera segura
    """
    try:
        ejecutar_consulta_segura(
            """
            INSERT INTO Notas_Registro (Numero_de_registro, Codigo_estudiante, 
                                      Id_competencia, Id_indicador, Nota)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE Nota = %s
            """,
            (numero_registro, codigo_estudiante, id_competencia, id_indicador, nota, nota)
        )
        return True
    except Exception as e:
        print(f"Error al guardar nota: {e}")
        return False