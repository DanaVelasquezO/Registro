import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_editar_registro(numero_registro, ventana_padre=None, callback_actualizar=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title(f"Editar Registro #{numero_registro}")
    ventana.geometry("700x600")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)
    
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Título
    titulo = tk.Label(
        ventana,
        text=f"Editar Registro #{numero_registro}",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Frame principal con scroll
    main_frame = tk.Frame(ventana, bg="#E3F2FD")
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
    
    # Cargar datos actuales del registro
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Datos del registro
        cursor.execute("""
            SELECT Nivel, Nombre_colegio, Año, Bimestre, Grado, Seccion, Curso, Promedio_curso
            FROM REGISTRO_AUXILIAR 
            WHERE Numero_de_registro = %s
        """, (numero_registro,))
        registro = cursor.fetchone()
        
        if not registro:
            messagebox.showerror("Error", "Registro no encontrado")
            ventana.destroy()
            return
        
        # Docentes asociados
        cursor.execute("""
            SELECT d.Codigo_docente, d.Nombre_docente 
            FROM Docente d
            JOIN Docente_Registro dr ON d.Codigo_docente = dr.Codigo_docente
            WHERE dr.Numero_de_registro = %s
        """, (numero_registro,))
        docentes_asociados = cursor.fetchall()
        
        # Competencias asociadas - USANDO LOS NOMBRES CORRECTOS DE COLUMNAS
        cursor.execute("""
            SELECT c.id_competencia, c.competencia 
            FROM Competencias c
            JOIN Competencias_Registro cr ON c.id_competencia = cr.Id_competencia
            WHERE cr.Numero_de_registro = %s
        """, (numero_registro,))
        competencias_asociadas = cursor.fetchall()
        
        # Todos los docentes disponibles
        cursor.execute("SELECT Codigo_docente, Nombre_docente FROM Docente ORDER BY Nombre_docente")
        todos_docentes = cursor.fetchall()
        
        # Todas las competencias disponibles - USANDO LOS NOMBRES CORRECTOS
        cursor.execute("SELECT id_competencia, competencia FROM Competencias ORDER BY competencia")
        todas_competencias = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar registro: {str(e)}")
        ventana.destroy()
        return
    
    nivel_actual, colegio_actual, año_actual, bimestre_actual, grado_actual, seccion_actual, curso_actual, promedio_actual = registro
    
    # Frame del formulario
    frame_form = tk.Frame(scrollable_frame, bg="#E3F2FD")
    frame_form.pack(pady=10, fill="x")
    
    # SECCIÓN 1: DATOS BÁSICOS DEL REGISTRO
    frame_datos = tk.LabelFrame(frame_form, text="Datos del Registro", font=("Arial", 11, "bold"), 
                               bg="#E3F2FD", fg="#0D47A1")
    frame_datos.pack(fill="x", pady=10)
    
    entries = {}
    row = 0
    
    # Campos editables
    campos = [
        ("Nivel:", ["Primaria", "Secundaria"], "nivel", nivel_actual),
        ("Año:", list(range(2020, 2031)), "año", año_actual),
        ("Bimestre:", ["I", "II", "III", "IV"], "bimestre", bimestre_actual),
        ("Grado:", ["1", "2", "3", "4", "5", "6"], "grado", grado_actual),
        ("Sección:", ["A", "B", "C", "D"], "seccion", seccion_actual)
    ]
    
    for label_text, opciones, key, valor_actual in campos:
        tk.Label(frame_datos, text=label_text, bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5, padx=10)
        if opciones:
            combo = ttk.Combobox(frame_datos, values=opciones, state="readonly", width=20)
            combo.set(valor_actual)
            combo.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[key] = combo
        else:
            entry = tk.Entry(frame_datos, font=("Arial", 10), width=25)
            entry.insert(0, str(valor_actual))
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[key] = entry
        row += 1
    
    # Colegio
    tk.Label(frame_datos, text="Nombre del Colegio:", bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5, padx=10)
    entries["colegio"] = tk.Entry(frame_datos, font=("Arial", 10), width=25)
    entries["colegio"].insert(0, colegio_actual)
    entries["colegio"].grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1
    
    # Curso
    tk.Label(frame_datos, text="Curso:", bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5, padx=10)
    entries["curso"] = tk.Entry(frame_datos, font=("Arial", 10), width=25)
    entries["curso"].insert(0, curso_actual)
    entries["curso"].grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1
    
    # Promedio del curso
    tk.Label(frame_datos, text="Promedio del Curso:", bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5, padx=10)
    entries["promedio"] = tk.Entry(frame_datos, font=("Arial", 10), width=25)
    entries["promedio"].insert(0, str(promedio_actual) if promedio_actual else "")
    entries["promedio"].grid(row=row, column=1, padx=10, pady=5, sticky="w")
    
    # SECCIÓN 2: GESTIÓN DE DOCENTES
    frame_docentes = tk.LabelFrame(frame_form, text="Docentes Asociados", font=("Arial", 11, "bold"), 
                                  bg="#E3F2FD", fg="#0D47A1")
    frame_docentes.pack(fill="x", pady=10)
    
    # Lista de docentes actuales
    lbl_docentes_actuales = tk.Label(frame_docentes, text="Docentes actuales:", bg="#E3F2FD", font=("Arial", 10, "bold"))
    lbl_docentes_actuales.grid(row=0, column=0, sticky="w", pady=5, padx=10)
    
    listbox_docentes = tk.Listbox(frame_docentes, width=40, height=4)
    listbox_docentes.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    
    for docente in docentes_asociados:
        listbox_docentes.insert(tk.END, f"{docente[0]} - {docente[1]}")
    
    # Combobox para agregar docente
    lbl_agregar_docente = tk.Label(frame_docentes, text="Agregar docente:", bg="#E3F2FD", font=("Arial", 10))
    lbl_agregar_docente.grid(row=2, column=0, sticky="w", pady=5, padx=10)
    
    combo_docentes = ttk.Combobox(frame_docentes, values=[f"{d[0]} - {d[1]}" for d in todos_docentes], state="readonly")
    combo_docentes.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    
    def agregar_docente():
        docente_seleccionado = combo_docentes.get()
        if docente_seleccionado and docente_seleccionado not in listbox_docentes.get(0, tk.END):
            listbox_docentes.insert(tk.END, docente_seleccionado)
            combo_docentes.set('')
    
    btn_agregar_docente = tk.Button(frame_docentes, text="➕ Agregar", bg="#4CAF50", fg="white",
                                   font=("Arial", 9), command=agregar_docente)
    btn_agregar_docente.grid(row=2, column=2, padx=5, pady=5)
    
    def eliminar_docente():
        seleccion = listbox_docentes.curselection()
        if seleccion:
            listbox_docentes.delete(seleccion[0])
    
    btn_eliminar_docente = tk.Button(frame_docentes, text="➖ Eliminar", bg="#F44336", fg="white",
                                    font=("Arial", 9), command=eliminar_docente)
    btn_eliminar_docente.grid(row=1, column=2, padx=5, pady=5)
    
    # SECCIÓN 3: GESTIÓN DE COMPETENCIAS
    frame_competencias = tk.LabelFrame(frame_form, text="Competencias Asociadas", font=("Arial", 11, "bold"), 
                                      bg="#E3F2FD", fg="#0D47A1")
    frame_competencias.pack(fill="x", pady=10)
    
    # Lista de competencias actuales
    lbl_competencias_actuales = tk.Label(frame_competencias, text="Competencias actuales:", bg="#E3F2FD", font=("Arial", 10, "bold"))
    lbl_competencias_actuales.grid(row=0, column=0, sticky="w", pady=5, padx=10)
    
    listbox_competencias = tk.Listbox(frame_competencias, width=40, height=4)
    listbox_competencias.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    
    for competencia in competencias_asociadas:
        listbox_competencias.insert(tk.END, f"{competencia[0]} - {competencia[1]}")
    
    # Combobox para agregar competencia
    lbl_agregar_competencia = tk.Label(frame_competencias, text="Agregar competencia:", bg="#E3F2FD", font=("Arial", 10))
    lbl_agregar_competencia.grid(row=2, column=0, sticky="w", pady=5, padx=10)
    
    combo_competencias = ttk.Combobox(frame_competencias, values=[f"{c[0]} - {c[1]}" for c in todas_competencias], state="readonly")
    combo_competencias.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    
    def agregar_competencia():
        competencia_seleccionada = combo_competencias.get()
        if competencia_seleccionada and competencia_seleccionada not in listbox_competencias.get(0, tk.END):
            listbox_competencias.insert(tk.END, competencia_seleccionada)
            combo_competencias.set('')
    
    btn_agregar_competencia = tk.Button(frame_competencias, text="➕ Agregar", bg="#4CAF50", fg="white",
                                      font=("Arial", 9), command=agregar_competencia)
    btn_agregar_competencia.grid(row=2, column=2, padx=5, pady=5)
    
    def eliminar_competencia():
        seleccion = listbox_competencias.curselection()
        if seleccion:
            listbox_competencias.delete(seleccion[0])
    
    btn_eliminar_competencia = tk.Button(frame_competencias, text="➖ Eliminar", bg="#F44336", fg="white",
                                       font=("Arial", 9), command=eliminar_competencia)
    btn_eliminar_competencia.grid(row=1, column=2, padx=5, pady=5)
    
    def actualizar_registro():
        # Validar campos obligatorios
        campos_obligatorios = ["nivel", "año", "bimestre", "grado", "seccion", "colegio", "curso"]
        for campo in campos_obligatorios:
            if not entries[campo].get().strip():
                messagebox.showwarning("Campo vacío", f"Por favor complete el campo: {campo}")
                return
        
        # Validar promedio
        promedio = entries["promedio"].get().strip()
        if promedio:
            try:
                promedio_float = float(promedio)
                if promedio_float < 0 or promedio_float > 20:
                    messagebox.showwarning("Promedio inválido", "El promedio debe estar entre 0 y 20")
                    return
            except ValueError:
                messagebox.showwarning("Promedio inválido", "El promedio debe ser un número válido")
                return
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Actualizar registro auxiliar
            cursor.execute("""
                UPDATE REGISTRO_AUXILIAR 
                SET Nivel = %s, Nombre_colegio = %s, Año = %s, Bimestre = %s, 
                    Grado = %s, Seccion = %s, Curso = %s, Promedio_curso = %s
                WHERE Numero_de_registro = %s
            """, (
                entries["nivel"].get(),
                entries["colegio"].get(),
                entries["año"].get(),
                entries["bimestre"].get(),
                entries["grado"].get(),
                entries["seccion"].get(),
                entries["curso"].get(),
                float(promedio) if promedio else None,
                numero_registro
            ))
            
            # Actualizar docentes
            cursor.execute("DELETE FROM Docente_Registro WHERE Numero_de_registro = %s", (numero_registro,))
            docentes_actuales = listbox_docentes.get(0, tk.END)
            for docente_str in docentes_actuales:
                codigo_docente = docente_str.split(" - ")[0]
                cursor.execute("INSERT INTO Docente_Registro (Codigo_docente, Numero_de_registro) VALUES (%s, %s)",
                             (codigo_docente, numero_registro))
            
            # Actualizar competencias
            cursor.execute("DELETE FROM Competencias_Registro WHERE Numero_de_registro = %s", (numero_registro,))
            competencias_actuales = listbox_competencias.get(0, tk.END)
            for competencia_str in competencias_actuales:
                id_competencia = competencia_str.split(" - ")[0]
                cursor.execute("INSERT INTO Competencias_Registro (Id_competencia, Numero_de_registro) VALUES (%s, %s)",
                             (id_competencia, numero_registro))
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            messagebox.showinfo("Éxito", "Registro actualizado correctamente")
            
            if callback_actualizar:
                callback_actualizar()
                
            ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar registro: {str(e)}")
    
    # Frame de botones
    frame_botones = tk.Frame(scrollable_frame, bg="#E3F2FD")
    frame_botones.pack(pady=15)
    
    btn_guardar = tk.Button(
        frame_botones,
        text="💾 Guardar Cambios",
        font=("Arial", 11, "bold"),
        bg="#F57C00",
        fg="white",
        width=18,
        command=actualizar_registro
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
    
    # Empaquetar canvas y scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Centrar ventana
    centrar_ventana(ventana, 700, 600)
    
    return ventana