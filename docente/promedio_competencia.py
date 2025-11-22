from db.conexion import obtener_conexion

def calcular_promedio_competencia(numero_registro, codigo_estudiante, id_competencia=None):
    """
    Calcula el promedio de una competencia específica o de todas las competencias
    para un estudiante en un registro
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        if id_competencia:
            # Calcular promedio de una competencia específica
            cursor.execute("""
                SELECT 
                    C.Id_competencia,
                    C.Competencia,
                    AVG(NR.Nota) AS Promedio_competencia
                FROM Notas_Registro NR
                JOIN Indicadores I ON NR.Id_indicador = I.Id_indicador
                JOIN Competencias C ON NR.Id_competencia = C.Id_competencia
                WHERE NR.Numero_de_registro = %s
                  AND NR.Codigo_estudiante = %s
                  AND C.Id_competencia = %s
                GROUP BY C.Id_competencia, C.Competencia
            """, (numero_registro, codigo_estudiante, id_competencia))
        else:
            # Calcular promedio de todas las competencias
            cursor.execute("""
                SELECT 
                    C.Id_competencia,
                    C.Competencia,
                    AVG(NR.Nota) AS Promedio_competencia
                FROM Notas_Registro NR
                JOIN Indicadores I ON NR.Id_indicador = I.Id_indicador
                JOIN Competencias C ON NR.Id_competencia = C.Id_competencia
                WHERE NR.Numero_de_registro = %s
                  AND NR.Codigo_estudiante = %s
                GROUP BY C.Id_competencia, C.Competencia
                ORDER BY C.Id_competencia
            """, (numero_registro, codigo_estudiante))
        
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        return resultados
        
    except Exception as e:
        print(f"Error al calcular promedio de competencia: {e}")
        return None

def obtener_competencias_con_promedios(numero_registro, codigo_estudiante):
    """
    Obtiene todas las competencias con sus promedios para un estudiante
    """
    return calcular_promedio_competencia(numero_registro, codigo_estudiante)