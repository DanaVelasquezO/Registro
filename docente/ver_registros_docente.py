import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ver_registros_docente(codigo_docente, ventana_padre=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title(f"Mis Registros - Docente {codigo_docente}")
    ventana.geometry("1200x600")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(True, True)
    
    # Comportamiento modal
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Centrar ventana
    centrar_ventana(ventana, 1200, 600)
    
    # Título
    titulo = tk.Label(
        ventana,
        text=f"Mis Registros Auxiliares",
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Obtener información del docente
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT Nombre_docente FROM Docente WHERE Codigo_docente = %s", (codigo_docente,))
        resultado = cursor.fetchone()
        nombre_docente = resultado[0] if resultado else "Docente"
        cursor.close()
        conexion.close()
    except Exception as e:
        nombre_docente = "Docente"
        messagebox.showerror("Error", f"Error al cargar información del docente: {str(e)}")
    
    # Información del docente
    info_frame = tk.Frame(ventana, bg="#E3F2FD")
    info_frame.pack(pady=5)
    
    tk.Label(info_frame, text=f"Docente: {nombre_docente}", 
             font=("Arial", 12, "bold"), bg="#E3F2FD").pack()
    tk.Label(info_frame, text=f"ID Docente: {codigo_docente}", 
             font=("Arial", 11), bg="#E3F2FD").pack()
    
    # Frame de controles
    frame_controles = tk.Frame(ventana, bg="#E3F2FD")
    frame_controles.pack(pady=10, padx=20, fill="x")
    
    # Búsqueda
    tk.Label(frame_controles, text="Buscar:", bg="#E3F2FD", font=("Arial", 10)).pack(side="left", padx=5)
    entry_busqueda = tk.Entry(frame_controles, font=("Arial", 10), width=30)
    entry_busqueda.pack(side="left", padx=5)
    
    # Filtros
    tk.Label(frame_controles, text="Año:", bg="#E3F2FD", font=("Arial", 10)).pack(side="left", padx=5)
    combo_año = ttk.Combobox(frame_controles, values=["Todos"] + list(range(2020, 2031)), state="readonly", width=10)
    combo_año.set("Todos")
    combo_año.pack(side="left", padx=5)
    
    tk.Label(frame_controles, text="Nivel:", bg="#E3F2FD", font=("Arial", 10)).pack(side="left", padx=5)
    combo_nivel = ttk.Combobox(frame_controles, values=["Todos", "Primaria", "Secundaria"], state="readonly", width=10)
    combo_nivel.set("Todos")
    combo_nivel.pack(side="left", padx=5)
    
    # Frame de tabla
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Scrollbars
    scroll_y = tk.Scrollbar(frame_tabla)
    scroll_y.pack(side="right", fill="y")
    
    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")
    
    # Treeview
    treeview = ttk.Treeview(
        frame_tabla,
        columns=("Registro", "Nivel", "Colegio", "Año", "Bimestre", "Grado", "Seccion", "Curso", "Promedio", "Estudiantes", "Competencias"),
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
        selectmode="browse",
        show="headings"
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
        ("Estudiantes", 90),
        ("Competencias", 100)
    ]
    
    for col, width in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=width, anchor="center")
    
    treeview.pack(fill="both", expand=True)
    
    # Función para cargar registros del docente
    def cargar_registros(filtros=None):
        try:
            # Limpiar tabla
            for item in treeview.get_children():
                treeview.delete(item)
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Consulta para obtener registros del docente
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
                    COUNT(DISTINCT er.Codigo_estudiante) as total_estudiantes,
                    COUNT(DISTINCT cr.Id_competencia) as total_competencias
                FROM REGISTRO_AUXILIAR r
                JOIN Docente_Registro dr ON r.Numero_de_registro = dr.Numero_de_registro
                LEFT JOIN Estudiante_Registro er ON r.Numero_de_registro = er.Numero_de_registro
                LEFT JOIN Competencias_Registro cr ON r.Numero_de_registro = cr.Numero_de_registro
                WHERE dr.Codigo_docente = %s
            """
            
            parametros = [codigo_docente]
            
            # Aplicar filtros
            if filtros:
                busqueda = filtros.get('busqueda', '')
                año = filtros.get('año', 'Todos')
                nivel = filtros.get('nivel', 'Todos')
                
                if busqueda:
                    query += " AND (r.Nombre_colegio LIKE %s OR r.Curso LIKE %s)"
                    parametros.extend([f"%{busqueda}%", f"%{busqueda}%"])
                
                if año != "Todos":
                    query += " AND r.Año = %s"
                    parametros.append(int(año))
                
                if nivel != "Todos":
                    query += " AND r.Nivel = %s"
                    parametros.append(nivel)
            
            query += """
                GROUP BY r.Numero_de_registro, r.Nivel, r.Nombre_colegio, r.Año, 
                         r.Bimestre, r.Grado, r.Seccion, r.Curso, r.Promedio_curso
                ORDER BY r.Año DESC, r.Bimestre, r.Numero_de_registro DESC
            """
            
            cursor.execute(query, parametros)
            registros = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Llenar tabla
            for registro in registros:
                treeview.insert("", "end", values=registro)
                
            # Mostrar conteo
            lbl_contador.config(text=f"Total de registros: {len(registros)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar registros: {str(e)}")
    
    # Función para buscar
    def buscar_registros(event=None):
        filtros = {
            'busqueda': entry_busqueda.get().strip(),
            'año': combo_año.get(),
            'nivel': combo_nivel.get()
        }
        cargar_registros(filtros)
    
    # Función para ver detalles del registro seleccionado
    def ver_detalles_registro():
        seleccion = treeview.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un registro para ver detalles")
            return
        
        item = treeview.item(seleccion[0])
        valores = item["values"]
        if valores:
            numero_registro = valores[0]
            mostrar_detalles_registro(numero_registro)
    
    # Función para obtener competencias con indicadores
    def obtener_competencias_con_indicadores(numero_registro):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener competencias del registro
            cursor.execute("""
                SELECT DISTINCT c.id_competencia, c.competencia
                FROM Competencias c
                JOIN Competencias_Registro cr ON c.id_competencia = cr.Id_competencia
                WHERE cr.Numero_de_registro = %s
                ORDER BY c.competencia
            """, (numero_registro,))
            competencias = cursor.fetchall()
            
            # Para cada competencia, obtener sus indicadores
            competencias_con_indicadores = []
            for competencia in competencias:
                id_competencia, nombre_competencia = competencia
                
                # Obtener indicadores de esta competencia para este registro
                cursor.execute("""
                    SELECT i.Id_indicador, i.Indicadores_competencias
                    FROM Indicadores i
                    JOIN Indicadores_Registro ir ON i.Id_indicador = ir.Id_indicador
                    WHERE ir.Numero_de_registro = %s AND i.Id_competencia = %s
                    ORDER BY i.Id_indicador
                """, (numero_registro, id_competencia))
                
                indicadores = cursor.fetchall()
                competencias_con_indicadores.append({
                    'id': id_competencia,
                    'nombre': nombre_competencia,
                    'indicadores': indicadores
                })
            
            cursor.close()
            conexion.close()
            return competencias_con_indicadores
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar competencias: {str(e)}")
            return []
    
    # Función para mostrar detalles del registro
    def mostrar_detalles_registro(numero_registro):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener información detallada del registro
            cursor.execute("""
                SELECT 
                    r.Nivel, r.Nombre_colegio, r.Año, r.Bimestre, 
                    r.Grado, r.Seccion, r.Curso, r.Promedio_curso
                FROM REGISTRO_AUXILIAR r
                WHERE r.Numero_de_registro = %s
            """, (numero_registro,))
            
            registro_info = cursor.fetchone()
            
            if registro_info:
                nivel, colegio, año, bimestre, grado, seccion, curso, promedio = registro_info
                
                # Obtener estudiantes del registro
                cursor.execute("""
                    SELECT e.Codigo_estudiante, e.Nombre_estudiante
                    FROM Estudiante e
                    JOIN Estudiante_Registro er ON e.Codigo_estudiante = er.Codigo_estudiante
                    WHERE er.Numero_de_registro = %s
                    ORDER BY e.Nombre_estudiante
                """, (numero_registro,))
                estudiantes = cursor.fetchall()
                
                cursor.close()
                conexion.close()
                
                # Obtener competencias con indicadores
                competencias_con_indicadores = obtener_competencias_con_indicadores(numero_registro)
                
                # Mostrar ventana de detalles
                mostrar_ventana_detalles(numero_registro, registro_info, estudiantes, competencias_con_indicadores)
            else:
                messagebox.showerror("Error", "Registro no encontrado")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar detalles: {str(e)}")
    
    def mostrar_ventana_detalles(numero_registro, registro_info, estudiantes, competencias_con_indicadores):
        ventana_detalles = tk.Toplevel(ventana)
        ventana_detalles.title(f"Detalles del Registro #{numero_registro}")
        ventana_detalles.geometry("700x600")
        ventana_detalles.config(bg="#E3F2FD")
        ventana_detalles.resizable(True, True)
        
        ventana_detalles.transient(ventana)
        ventana_detalles.grab_set()
        
        # Frame principal con scroll
        main_frame = tk.Frame(ventana_detalles, bg="#E3F2FD")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg="#E3F2FD")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#E3F2FD")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        tk.Label(scrollable_frame, text=f"Detalles del Registro #{numero_registro}", 
                font=("Arial", 14, "bold"), bg="#E3F2FD", fg="#0D47A1").pack(pady=10)
        
        # Información básica
        frame_info = tk.LabelFrame(scrollable_frame, text="Información del Registro", 
                                 font=("Arial", 11, "bold"), bg="#E3F2FD", fg="#0D47A1")
        frame_info.pack(fill="x", padx=10, pady=5)
        
        nivel, colegio, año, bimestre, grado, seccion, curso, promedio = registro_info
        
        info_text = f"""
Colegio: {colegio}
Nivel: {nivel}
Año: {año} | Bimestre: {bimestre}
Grado: {grado} | Sección: {seccion}
Curso: {curso}
Promedio del curso: {promedio if promedio else 'No asignado'}
        """.strip()
        
        tk.Label(frame_info, text=info_text, font=("Arial", 10), bg="#E3F2FD", 
                justify="left").pack(padx=10, pady=10)
        
        # Estudiantes
        frame_estudiantes = tk.LabelFrame(scrollable_frame, text=f"Estudiantes ({len(estudiantes)})", 
                                        font=("Arial", 11, "bold"), bg="#E3F2FD", fg="#0D47A1")
        frame_estudiantes.pack(fill="x", padx=10, pady=5)
        
        lista_estudiantes = tk.Listbox(frame_estudiantes, font=("Arial", 9), height=6)
        lista_estudiantes.pack(fill="x", padx=10, pady=10)
        
        for estudiante in estudiantes:
            lista_estudiantes.insert(tk.END, f"{estudiante[0]} - {estudiante[1]}")
        
        # Competencias con Indicadores
        frame_competencias = tk.LabelFrame(scrollable_frame, text=f"Competencias e Indicadores ({len(competencias_con_indicadores)})", 
                                         font=("Arial", 11, "bold"), bg="#E3F2FD", fg="#0D47A1")
        frame_competencias.pack(fill="x", padx=10, pady=5)
        
        if competencias_con_indicadores:
            for competencia in competencias_con_indicadores:
                # Frame para cada competencia
                frame_competencia = tk.Frame(frame_competencias, bg="#F5F5F5", relief="solid", bd=1)
                frame_competencia.pack(fill="x", padx=5, pady=2)
                
                # Nombre de la competencia
                lbl_competencia = tk.Label(frame_competencia, 
                                         text=f"🏆 {competencia['nombre']}",
                                         font=("Arial", 10, "bold"), 
                                         bg="#F5F5F5", fg="#0D47A1")
                lbl_competencia.pack(anchor="w", padx=5, pady=2)
                
                # Indicadores de la competencia
                if competencia['indicadores']:
                    for indicador in competencia['indicadores']:
                        id_indicador, nombre_indicador = indicador
                        lbl_indicador = tk.Label(frame_competencia, 
                                               text=f"   • {nombre_indicador}",
                                               font=("Arial", 9), 
                                               bg="#F5F5F5", fg="#333333")
                        lbl_indicador.pack(anchor="w", padx=15, pady=1)
                else:
                    lbl_sin_indicadores = tk.Label(frame_competencia, 
                                                 text="   • Sin indicadores asignados",
                                                 font=("Arial", 9), 
                                                 bg="#F5F5F5", fg="#666666")
                    lbl_sin_indicadores.pack(anchor="w", padx=15, pady=1)
        else:
            tk.Label(frame_competencias, text="No hay competencias asignadas a este registro", 
                    font=("Arial", 10), bg="#E3F2FD", fg="#666666").pack(pady=10)
        
        # Botón cerrar
        tk.Button(scrollable_frame, text="Cerrar", font=("Arial", 10), 
                 bg="#757575", fg="white", command=ventana_detalles.destroy).pack(pady=10)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        centrar_ventana(ventana_detalles, 700, 600)
    
    # Botón ver detalles
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=10)
    
    btn_detalles = tk.Button(
        frame_botones,
        text="Ver Detalles del Registro",
        font=("Arial", 10, "bold"),
        bg="#1976D2",
        fg="white",
        width=25,
        command=ver_detalles_registro
    )
    btn_detalles.pack(side="left", padx=5)
    
    # Contador de registros
    lbl_contador = tk.Label(ventana, text="Total de registros: 0", 
                           font=("Arial", 10), bg="#E3F2FD", fg="#0D47A1")
    lbl_contador.pack(pady=5)
    
    # Conectar eventos
    entry_busqueda.bind("<KeyRelease>", buscar_registros)
    combo_año.bind("<<ComboboxSelected>>", buscar_registros)
    combo_nivel.bind("<<ComboboxSelected>>", buscar_registros)
    
    # Cargar datos iniciales
    cargar_registros()
    
    return ventana