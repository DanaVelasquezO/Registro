import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def crear_tabla_registros(parent):
    frame = tk.Frame(parent)
    
    # Scrollbars
    scroll_y = tk.Scrollbar(frame)
    scroll_y.pack(side="right", fill="y")
    
    scroll_x = tk.Scrollbar(frame, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")
    
    # Treeview
    treeview = ttk.Treeview(
        frame,
        columns=("Registro", "Nivel", "Colegio", "Año", "Bimestre", "Grado", "Seccion", "Curso", "Promedio", "Docente", "Estudiantes", "Competencias"),
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
        selectmode="browse",
        show="headings",
        height=15
    )
    
    scroll_y.config(command=treeview.yview)
    scroll_x.config(command=treeview.xview)
    
    # Configurar columnas
    columnas = [
        ("Registro", 80),
        ("Nivel", 80),
        ("Colegio", 150),
        ("Año", 60),
        ("Bimestre", 80),
        ("Grado", 60),
        ("Seccion", 60),
        ("Curso", 120),
        ("Promedio", 80),
        ("Docente", 120),
        ("Estudiantes", 90),
        ("Competencias", 100)
    ]
    
    for col, width in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=width, anchor="center")
    
    treeview.pack(fill="both", expand=True)
    
    def actualizar_tabla(filtros=None):
        try:
            # Limpiar tabla
            for item in treeview.get_children():
                treeview.delete(item)
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Construir consulta con filtros
            query = """
                SELECT 
                    r.Numero_de_registro,
                    r.Nivel,
                    r.Nombre_colegio,
                    r.Año,
                    r.Bimestre,
                    r.Grado,
                    r.Seccion,
                    r.Curso,
                    r.Promedio_curso,
                    d.Nombre_docente,
                    COUNT(er.Codigo_estudiante) as total_estudiantes,
                    COUNT(DISTINCT cr.Id_competencia) as total_competencias
                FROM REGISTRO_AUXILIAR r
                LEFT JOIN Docente_Registro dr ON r.Numero_de_registro = dr.Numero_de_registro
                LEFT JOIN Docente d ON dr.Codigo_docente = d.Codigo_docente
                LEFT JOIN Estudiante_Registro er ON r.Numero_de_registro = er.Numero_de_registro
                LEFT JOIN Competencias_Registro cr ON r.Numero_de_registro = cr.Numero_de_registro
            """
            
            condiciones = []
            parametros = []
            
            # Aplicar filtros si se proporcionan
            if filtros:
                busqueda = filtros.get('busqueda', '')
                if busqueda:
                    condiciones.append("(r.Nombre_colegio LIKE %s OR r.Curso LIKE %s OR d.Nombre_docente LIKE %s)")
                    parametros.extend([f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"])
                
                nivel = filtros.get('nivel', 'Todos')
                if nivel != "Todos":
                    condiciones.append("r.Nivel = %s")
                    parametros.append(nivel)
                
                grado = filtros.get('grado', 'Todos')
                if grado != "Todos":
                    condiciones.append("r.Grado = %s")
                    parametros.append(grado)
            
            if condiciones:
                query += " WHERE " + " AND ".join(condiciones)
            
            query += """
                GROUP BY r.Numero_de_registro, r.Nivel, r.Nombre_colegio, r.Año, 
                         r.Bimestre, r.Grado, r.Seccion, r.Curso, r.Promedio_curso, d.Nombre_docente
                ORDER BY r.Año DESC, r.Numero_de_registro DESC
            """
            
            cursor.execute(query, parametros)
            registros = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Llenar tabla
            for registro in registros:
                treeview.insert("", "end", values=registro)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar registros: {str(e)}")
    
    datos_tabla = {
        'treeview': treeview,
        'actualizar_tabla': actualizar_tabla,
        'frame': frame
    }
    
    return datos_tabla