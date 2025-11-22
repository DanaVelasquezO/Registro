from db.conexion import obtener_conexion

def calcular_promedio_final_estudiante(numero_registro, codigo_estudiante):
    """
    Calcula el promedio final de un estudiante en un registro
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Usar el procedimiento almacenado si existe, o calcular directamente
        cursor.execute("""
            SELECT AVG(Nota) AS Promedio_final
            FROM Notas_Registro
            WHERE Numero_de_registro = %s
              AND Codigo_estudiante = %s
        """, (numero_registro, codigo_estudiante))
        
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if resultado and resultado[0] is not None:
            return float(resultado[0])
        return 0.0
        
    except Exception as e:
        print(f"Error al calcular promedio final: {e}")
        return 0.0

def convertir_a_literal(promedio):
    """
    Convierte un promedio numérico a literal según la escala peruana
    """
    try:
        if promedio >= 18.00:
            return "AD"
        elif promedio >= 16.00:
            return "A"
        elif promedio >= 14.00:
            return "B"
        elif promedio >= 12.00:
            return "C"
        elif promedio >= 11.00:
            return "D"
        else:
            return "E"
    except:
        return "E"

def generar_conclusion_descriptiva(promedio):
    """
    Genera una conclusión descriptiva basada en el promedio
    """
    try:
        if promedio >= 18.00:
            return "Excelente desempeño académico - Logro destacado"
        elif promedio >= 16.00:
            return "Buen desempeño académico - Logro esperado"
        elif promedio >= 14.00:
            return "Desempeño satisfactorio - En proceso"
        elif promedio >= 12.00:
            return "Desempeño regular - Requiere mejora"
        elif promedio >= 11.00:
            return "Desempeño mínimo - Necesita apoyo"
        else:
            return "Desempeño insuficiente - Requiere refuerzo urgente"
    except:
        return "Sin datos suficientes para evaluación"

def calcular_promedios_todos_estudiantes(numero_registro):
    """
    Calcula promedios para todos los estudiantes de un registro
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Obtener todos los estudiantes del registro
        cursor.execute("""
            SELECT e.Codigo_estudiante, e.Nombre_estudiante
            FROM Estudiante e
            JOIN Estudiante_Registro er ON e.Codigo_estudiante = er.Codigo_estudiante
            WHERE er.Numero_de_registro = %s
            ORDER BY e.Nombre_estudiante
        """, (numero_registro,))
        
        estudiantes = cursor.fetchall()
        
        resultados = []
        for codigo_estudiante, nombre_estudiante in estudiantes:
            # Calcular promedio final
            promedio_final = calcular_promedio_final_estudiante(numero_registro, codigo_estudiante)
            nota_literal = convertir_a_literal(promedio_final)
            conclusion = generar_conclusion_descriptiva(promedio_final)
            
            # Obtener promedios por competencia
            competencias = obtener_competencias_con_promedios(numero_registro, codigo_estudiante)
            
            resultados.append({
                'codigo_estudiante': codigo_estudiante,
                'nombre_estudiante': nombre_estudiante,
                'promedio_final': promedio_final,
                'nota_literal': nota_literal,
                'conclusion': conclusion,
                'competencias': competencias
            })
        
        cursor.close()
        conexion.close()
        
        return resultados
        
    except Exception as e:
        print(f"Error al calcular promedios para todos los estudiantes: {e}")
        return []