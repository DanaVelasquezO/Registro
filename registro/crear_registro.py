import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from db.conexion import obtener_conexion

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_crear_registro(ventana_padre=None, callback_actualizar=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Crear Nuevo Registro Auxiliar")
    ventana.geometry("700x800")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)
    
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Variables
    estudiantes_seleccionados = []
    competencias_seleccionadas = []
    docentes_seleccionados = []
    
    # Titulo
    titulo = tk.Label(
        ventana,
        text="Crear Nuevo Registro Auxiliar",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Frame del formulario principal
    frame_form = tk.Frame(ventana, bg="#E3F2FD")
    frame_form.pack(pady=10, padx=20, fill="x")
    
    # Campos basicos del registro
    campos = [
        ("Nivel:", ["Primaria", "Secundaria"], "nivel"),
        ("Año:", list(range(2020, 2031)), "año"),
        ("Bimestre:", ["I", "II", "III", "IV"], "bimestre"),
        ("Grado:", ["1", "2", "3", "4", "5", "6"], "grado"),
        ("Seccion:", ["A", "B", "C", "D"], "seccion")
    ]
    
    entries = {}
    row = 0
    
    for label_text, opciones, key in campos:
        tk.Label(frame_form, text=label_text, bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5)
        if opciones:
            combo = ttk.Combobox(frame_form, values=opciones, state="readonly", width=20)
            combo.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[key] = combo
        else:
            entry = tk.Entry(frame_form, font=("Arial", 10), width=25)
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[key] = entry
        row += 1
    
    # Colegio y Curso (texto libre)
    tk.Label(frame_form, text="Nombre del Colegio:", bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5)
    entries["colegio"] = tk.Entry(frame_form, font=("Arial", 10), width=25)
    entries["colegio"].grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1
    
    tk.Label(frame_form, text="Curso:", bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5)
    entries["curso"] = tk.Entry(frame_form, font=("Arial", 10), width=25)
    entries["curso"].grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1
    
    # Frame para seleccion multiple
    frame_seleccion = tk.Frame(ventana, bg="#E3F2FD")
    frame_seleccion.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Pestañas para seleccion multiple
    notebook = ttk.Notebook(frame_seleccion)
    notebook.pack(fill="both", expand=True)
    
    # Pestaña de Estudiantes
    frame_estudiantes = tk.Frame(notebook, bg="#E3F2FD")
    notebook.add(frame_estudiantes, text="Estudiantes")
    
    # Pestaña de Competencias
    frame_competencias = tk.Frame(notebook, bg="#E3F2FD")
    notebook.add(frame_competencias, text="Competencias")
    
    # Pestaña de Docentes
    frame_docentes = tk.Frame(notebook, bg="#E3F2FD")
    notebook.add(frame_docentes, text="Docentes")
    
    # ===== FUNCIONALIDAD: CARGA DESDE EXCEL =====
    def cargar_estudiantes_desde_excel():
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel con estudiantes",
            filetypes=[
                ("Archivos Excel", "*.xlsx *.xls"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if not archivo:
            return
        
        try:
            # Leer archivo Excel
            df = pd.read_excel(archivo)
            
            # Verificar si existe columna 'Nombres'
            if 'Nombres' not in df.columns:
                messagebox.showerror("Error", 
                    "El archivo Excel debe tener una columna llamada 'Nombres'\n\n"
                    "Columnas encontradas:\n" + 
                    "\n".join(df.columns.tolist()))
                return
            
            # Obtener nombres del Excel
            nombres_excel = df['Nombres'].dropna().str.strip().tolist()
            nombres_excel = [nombre for nombre in nombres_excel if nombre]
            
            if not nombres_excel:
                messagebox.showwarning("Sin datos", "No se encontraron nombres en el archivo Excel")
                return
            
            # Buscar codigos de estudiantes en la base de datos
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener todos los estudiantes existentes
            cursor.execute("SELECT Codigo_estudiante, Nombre_estudiante FROM Estudiante")
            estudiantes_db = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Crear diccionario nombre -> codigo
            estudiante_dict = {nombre: codigo for codigo, nombre in estudiantes_db}
            
            # Limpiar seleccion actual
            estudiantes_seleccionados.clear()
            
            # Buscar coincidencias
            estudiantes_encontrados = []
            estudiantes_no_encontrados = []
            
            for nombre in nombres_excel:
                if nombre in estudiante_dict:
                    codigo = estudiante_dict[nombre]
                    estudiantes_encontrados.append((codigo, nombre))
                    estudiantes_seleccionados.append(codigo)
                else:
                    estudiantes_no_encontrados.append(nombre)
            
            # Actualizar interfaz
            actualizar_lista_estudiantes()
            
            # Mostrar resultados
            mensaje = f"Estudiantes cargados: {len(estudiantes_encontrados)}"
            if estudiantes_no_encontrados:
                mensaje += f"\n\nNo encontrados: {len(estudiantes_no_encontrados)}"
                if len(estudiantes_no_encontrados) <= 10:
                    mensaje += "\n" + "\n".join(estudiantes_no_encontrados)
                else:
                    mensaje += f"\n(mostrando los primeros 10)\n" + "\n".join(estudiantes_no_encontrados[:10])
            
            messagebox.showinfo("Carga desde Excel", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo Excel:\n{str(e)}")
    
    def actualizar_lista_estudiantes():
        # Limpiar frame
        for widget in frame_estudiantes.winfo_children():
            widget.destroy()
        
        # Frame para controles de estudiantes
        frame_controles_est = tk.Frame(frame_estudiantes, bg="#E3F2FD")
        frame_controles_est.pack(pady=10, fill="x")
        
        # Boton para cargar desde Excel
        btn_excel = tk.Button(
            frame_controles_est,
            text="Cargar Estudiantes desde Excel",
            font=("Arial", 10, "bold"),
            bg="#7B1FA2",
            fg="white",
            command=cargar_estudiantes_desde_excel
        )
        btn_excel.pack(pady=5)
        
        # Label con contador
        lbl_contador = tk.Label(
            frame_controles_est,
            text=f"Estudiantes seleccionados: {len(estudiantes_seleccionados)}",
            font=("Arial", 10, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1"
        )
        lbl_contador.pack(pady=5)
        
        # Frame para lista de estudiantes con scroll
        frame_lista_est = tk.Frame(frame_estudiantes)
        frame_lista_est.pack(fill="both", expand=True)
        
        scroll_y = tk.Scrollbar(frame_lista_est)
        scroll_y.pack(side="right", fill="y")
        
        lista_estudiantes = tk.Listbox(
            frame_lista_est,
            yscrollcommand=scroll_y.set,
            font=("Arial", 9),
            height=8
        )
        scroll_y.config(command=lista_estudiantes.yview)
        
        # Cargar nombres de estudiantes seleccionados
        try:
            if estudiantes_seleccionados:
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                
                placeholders = ','.join(['%s'] * len(estudiantes_seleccionados))
                cursor.execute(f"""
                    SELECT Codigo_estudiante, Nombre_estudiante 
                    FROM Estudiante 
                    WHERE Codigo_estudiante IN ({placeholders})
                    ORDER BY Nombre_estudiante
                """, estudiantes_seleccionados)
                
                estudiantes = cursor.fetchall()
                cursor.close()
                conexion.close()
                
                for codigo, nombre in estudiantes:
                    lista_estudiantes.insert(tk.END, f"{codigo} - {nombre}")
            else:
                lista_estudiantes.insert(tk.END, "No hay estudiantes seleccionados")
                lista_estudiantes.config(state="disabled")
                
        except Exception as e:
            lista_estudiantes.insert(tk.END, f"Error al cargar estudiantes: {str(e)}")
        
        lista_estudiantes.pack(fill="both", expand=True)
    
    def cargar_indicadores_por_competencia(competencias_seleccionadas):
        """Cargar indicadores para las competencias seleccionadas"""
        try:
            # Limpiar frame de indicadores si existe
            for widget in frame_competencias.winfo_children():
                if isinstance(widget, tk.Frame) and hasattr(widget, 'es_frame_indicadores'):
                    widget.destroy()
            
            if not competencias_seleccionadas:
                return
            
            # Crear frame para indicadores
            frame_indicadores = tk.Frame(frame_competencias, bg="#E3F2FD")
            frame_indicadores.pack(fill="x", pady=5)
            frame_indicadores.es_frame_indicadores = True
            
            tk.Label(frame_indicadores, text="Indicadores de las competencias seleccionadas:", 
                    font=("Arial", 10, "bold"), bg="#E3F2FD").pack(anchor="w")
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener todos los indicadores de las competencias seleccionadas
            placeholders = ','.join(['%s'] * len(competencias_seleccionadas))
            cursor.execute(f"""
                SELECT i.Id_indicador, i.Indicadores_competencias, c.Competencia
                FROM Indicadores i
                JOIN Competencias c ON i.Id_competencia = c.Id_competencia
                WHERE i.Id_competencia IN ({placeholders})
                ORDER BY c.Competencia, i.Id_indicador
            """, competencias_seleccionadas)
            
            indicadores = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Frame para lista con scroll
            frame_lista_ind = tk.Frame(frame_indicadores)
            frame_lista_ind.pack(fill="x", pady=5)
            
            scroll_y = tk.Scrollbar(frame_lista_ind)
            scroll_y.pack(side="right", fill="y")
            
            lista_indicadores = tk.Listbox(
                frame_lista_ind,
                yscrollcommand=scroll_y.set,
                font=("Arial", 9),
                height=6
            )
            scroll_y.config(command=lista_indicadores.yview)
            
            # Agrupar por competencia
            indicadores_por_competencia = {}
            for id_ind, indicador, competencia in indicadores:
                if competencia not in indicadores_por_competencia:
                    indicadores_por_competencia[competencia] = []
                indicadores_por_competencia[competencia].append((id_ind, indicador))
            
            # Mostrar en la lista
            for competencia, indicadores_list in indicadores_por_competencia.items():
                lista_indicadores.insert(tk.END, f"--- {competencia} ---")
                for id_ind, indicador in indicadores_list:
                    lista_indicadores.insert(tk.END, f"  • {indicador}")
            
            lista_indicadores.pack(fill="x")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar indicadores: {str(e)}")
    
    def cargar_competencias():
        try:
            # Limpiar frame
            for widget in frame_competencias.winfo_children():
                widget.destroy()
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT Id_competencia, Competencia FROM Competencias ORDER BY Id_competencia")
            competencias = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Frame para lista con scroll
            frame_lista_comp = tk.Frame(frame_competencias)
            frame_lista_comp.pack(fill="both", expand=True)
            
            scroll_y = tk.Scrollbar(frame_lista_comp)
            scroll_y.pack(side="right", fill="y")
            
            lista_competencias = tk.Listbox(
                frame_lista_comp,
                yscrollcommand=scroll_y.set,
                font=("Arial", 9),
                selectmode="multiple",
                height=8
            )
            scroll_y.config(command=lista_competencias.yview)
            
            # Diccionario para mapear indice a ID de competencia
            competencia_dict = {}
            
            for idx, (id_comp, competencia) in enumerate(competencias):
                lista_competencias.insert(tk.END, f"{id_comp} - {competencia}")
                competencia_dict[idx] = id_comp
            
            lista_competencias.pack(fill="both", expand=True)
            
            def seleccionar_competencias():
                # Limpiar seleccion anterior
                competencias_seleccionadas.clear()
                
                # Obtener seleccion actual
                seleccion = lista_competencias.curselection()
                for idx in seleccion:
                    id_comp = competencia_dict[idx]
                    competencias_seleccionadas.append(id_comp)
                
                # Cargar indicadores de las competencias seleccionadas
                cargar_indicadores_por_competencia(competencias_seleccionadas)
                
                messagebox.showinfo("Seleccion", f"Competencias seleccionadas: {len(competencias_seleccionadas)}")
            
            # Boton para confirmar seleccion
            btn_seleccionar = tk.Button(
                frame_competencias,
                text="Confirmar Seleccion de Competencias",
                font=("Arial", 10, "bold"),
                bg="#388E3C",
                fg="white",
                command=seleccionar_competencias
            )
            btn_seleccionar.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar competencias: {str(e)}")
    
    def cargar_docentes():
        try:
            # Limpiar frame
            for widget in frame_docentes.winfo_children():
                widget.destroy()
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT Codigo_docente, Nombre_docente FROM Docente ORDER BY Nombre_docente")
            docentes = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Frame para lista con scroll
            frame_lista_doc = tk.Frame(frame_docentes)
            frame_lista_doc.pack(fill="both", expand=True)
            
            scroll_y = tk.Scrollbar(frame_lista_doc)
            scroll_y.pack(side="right", fill="y")
            
            lista_docentes = tk.Listbox(
                frame_lista_doc,
                yscrollcommand=scroll_y.set,
                font=("Arial", 9),
                selectmode="single",  # Solo un docente por registro
                height=8
            )
            scroll_y.config(command=lista_docentes.yview)
            
            # Diccionario para mapear indice a ID de docente
            docente_dict = {}
            
            for idx, (codigo, nombre) in enumerate(docentes):
                lista_docentes.insert(tk.END, f"{codigo} - {nombre}")
                docente_dict[idx] = codigo
            
            lista_docentes.pack(fill="both", expand=True)
            
            def seleccionar_docente():
                # Limpiar seleccion anterior
                docentes_seleccionados.clear()
                
                # Obtener seleccion actual (solo el primero)
                seleccion = lista_docentes.curselection()
                if seleccion:
                    id_doc = docente_dict[seleccion[0]]
                    docentes_seleccionados.append(id_doc)
                    messagebox.showinfo("Seleccion", f"Docente seleccionado correctamente")
                else:
                    messagebox.showwarning("Seleccion", "Por favor seleccione un docente")
            
            # Boton para confirmar seleccion
            btn_seleccionar = tk.Button(
                frame_docentes,
                text="Confirmar Seleccion de Docente",
                font=("Arial", 10, "bold"),
                bg="#1976D2",
                fg="white",
                command=seleccionar_docente
            )
            btn_seleccionar.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar docentes: {str(e)}")
    
    def guardar_registro():
        # Validar campos obligatorios
        campos_obligatorios = ["nivel", "año", "bimestre", "grado", "seccion", "colegio", "curso"]
        for campo in campos_obligatorios:
            if not entries[campo].get().strip():
                messagebox.showwarning("Campo vacio", f"Por favor complete el campo: {campo}")
                return
        
        if not estudiantes_seleccionados:
            messagebox.showwarning("Seleccion requerida", "Debe seleccionar al menos un estudiante")
            return
        
        if not competencias_seleccionadas:
            messagebox.showwarning("Seleccion requerida", "Debe seleccionar al menos una competencia")
            return
        
        if not docentes_seleccionados:
            messagebox.showwarning("Seleccion requerida", "Debe seleccionar al menos un docente")
            return
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Insertar registro auxiliar
            cursor.execute("""
                INSERT INTO REGISTRO_AUXILIAR 
                (Nivel, Nombre_colegio, Año, Bimestre, Grado, Seccion, Curso) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                entries["nivel"].get(),
                entries["colegio"].get(),
                entries["año"].get(),
                entries["bimestre"].get(),
                entries["grado"].get(),
                entries["seccion"].get(),
                entries["curso"].get()
            ))
            
            numero_registro = cursor.lastrowid
            
            # Asociar estudiantes
            for codigo_est in estudiantes_seleccionados:
                cursor.execute("""
                    INSERT INTO Estudiante_Registro (Codigo_estudiante, Numero_de_registro)
                    VALUES (%s, %s)
                """, (codigo_est, numero_registro))
            
            # Asociar competencias
            for id_comp in competencias_seleccionadas:
                cursor.execute("""
                    INSERT INTO Competencias_Registro (Id_competencia, Numero_de_registro)
                    VALUES (%s, %s)
                """, (id_comp, numero_registro))
            
            # Asociar docentes
            for codigo_doc in docentes_seleccionados:
                cursor.execute("""
                    INSERT INTO Docente_Registro (Codigo_docente, Numero_de_registro)
                    VALUES (%s, %s)
                """, (codigo_doc, numero_registro))
            
            # Obtener todos los indicadores de las competencias seleccionadas
            placeholders = ','.join(['%s'] * len(competencias_seleccionadas))
            cursor.execute(f"""
                SELECT Id_indicador FROM Indicadores 
                WHERE Id_competencia IN ({placeholders})
            """, competencias_seleccionadas)
            
            indicadores = cursor.fetchall()
            
            # Asociar indicadores al registro
            for (id_indicador,) in indicadores:
                cursor.execute("""
                    INSERT INTO Indicadores_Registro (Id_indicador, Numero_de_registro)
                    VALUES (%s, %s)
                """, (id_indicador, numero_registro))
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            messagebox.showinfo("Exito", 
                f"Registro creado correctamente\n"
                f"Numero de registro: {numero_registro}\n"
                f"Estudiantes: {len(estudiantes_seleccionados)}\n"
                f"Competencias: {len(competencias_seleccionadas)}\n"
                f"Docentes: {len(docentes_seleccionados)}")
            
            if callback_actualizar:
                callback_actualizar()
                
            ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear registro: {str(e)}")
    
    # Cargar datos iniciales
    actualizar_lista_estudiantes()
    cargar_competencias()
    cargar_docentes()
    
    # Frame de botones
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=15)
    
    btn_guardar = tk.Button(
        frame_botones,
        text="Guardar Registro",
        font=("Arial", 11, "bold"),
        bg="#388E3C",
        fg="white",
        width=20,
        command=guardar_registro
    )
    btn_guardar.pack(side="left", padx=5)
    
    btn_cancelar = tk.Button(
        frame_botones,
        text="Cancelar",
        font=("Arial", 11),
        bg="#757575",
        fg="white",
        width=15,
        command=ventana.destroy
    )
    btn_cancelar.pack(side="left", padx=5)
    
    # Centrar ventana
    centrar_ventana(ventana, 700, 800)
    
    return ventana