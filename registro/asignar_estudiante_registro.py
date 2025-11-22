import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_asignar_estudiante_registro(codigo_estudiante, nombre_estudiante, ventana_padre=None, callback_actualizar=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title(f"Asignar {nombre_estudiante} a Registro")
    ventana.geometry("600x400")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)
    
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Título
    titulo = tk.Label(
        ventana,
        text=f"Asignar Estudiante a Registro",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=10)
    
    # Información del estudiante
    info_frame = tk.Frame(ventana, bg="#E3F2FD")
    info_frame.pack(pady=5)
    
    tk.Label(info_frame, text=f"Estudiante: {nombre_estudiante}", 
             font=("Arial", 11, "bold"), bg="#E3F2FD").pack()
    tk.Label(info_frame, text=f"Código: {codigo_estudiante}", 
             font=("Arial", 10), bg="#E3F2FD").pack()
    
    # Frame del formulario
    frame_form = tk.Frame(ventana, bg="#E3F2FD")
    frame_form.pack(pady=15, padx=20, fill="both", expand=True)
    
    # Obtener registros disponibles
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Obtener registros que no tengan a este estudiante asignado
        cursor.execute("""
            SELECT r.Numero_de_registro, r.Nombre_colegio, r.Curso, r.Grado, r.Seccion
            FROM REGISTRO_AUXILIAR r
            WHERE r.Numero_de_registro NOT IN (
                SELECT er.Numero_de_registro 
                FROM Estudiante_Registro er 
                WHERE er.Codigo_estudiante = %s
            )
            ORDER BY r.Año DESC, r.Numero_de_registro DESC
        """, (codigo_estudiante,))
        
        registros_disponibles = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar registros: {str(e)}")
        ventana.destroy()
        return
    
    if not registros_disponibles:
        messagebox.showinfo("Sin registros", "El estudiante ya está asignado a todos los registros disponibles.")
        ventana.destroy()
        return
    
    # Label y combobox para seleccionar registro
    tk.Label(frame_form, text="Seleccionar Registro:", 
             font=("Arial", 11, "bold"), bg="#E3F2FD").pack(anchor="w", pady=5)
    
    # Crear combobox con registros disponibles
    registros_dict = {}
    for registro in registros_disponibles:
        num_registro, colegio, curso, grado, seccion = registro
        display_text = f"Registro #{num_registro} - {colegio} - {curso} ({grado}° {seccion})"
        registros_dict[display_text] = num_registro
    
    combo_registros = ttk.Combobox(
        frame_form, 
        values=list(registros_dict.keys()),
        state="readonly",
        font=("Arial", 10),
        width=60
    )
    combo_registros.pack(fill="x", pady=5)
    
    # Información del registro seleccionado
    info_registro_frame = tk.Frame(frame_form, bg="#E3F2FD")
    info_registro_frame.pack(fill="x", pady=10)
    
    lbl_info_registro = tk.Label(
        info_registro_frame, 
        text="Seleccione un registro para ver más detalles",
        font=("Arial", 9),
        bg="#E3F2FD",
        fg="#666666",
        wraplength=500,
        justify="left"
    )
    lbl_info_registro.pack(anchor="w")
    
    def actualizar_info_registro(event=None):
        seleccion = combo_registros.get()
        if seleccion and seleccion in registros_dict:
            numero_registro = registros_dict[seleccion]
            try:
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                
                cursor.execute("""
                    SELECT r.Nivel, r.Nombre_colegio, r.Año, r.Bimestre, 
                           r.Grado, r.Seccion, r.Curso, r.Promedio_curso,
                           COUNT(DISTINCT er.Codigo_estudiante) as total_estudiantes,
                           COUNT(DISTINCT dr.Codigo_docente) as total_docentes,
                           COUNT(DISTINCT cr.Id_competencia) as total_competencias
                    FROM REGISTRO_AUXILIAR r
                    LEFT JOIN Estudiante_Registro er ON r.Numero_de_registro = er.Numero_de_registro
                    LEFT JOIN Docente_Registro dr ON r.Numero_de_registro = dr.Numero_de_registro
                    LEFT JOIN Competencias_Registro cr ON r.Numero_de_registro = cr.Numero_de_registro
                    WHERE r.Numero_de_registro = %s
                    GROUP BY r.Numero_de_registro
                """, (numero_registro,))
                
                registro_info = cursor.fetchone()
                cursor.close()
                conexion.close()
                
                if registro_info:
                    nivel, colegio, año, bimestre, grado, seccion, curso, promedio, estudiantes, docentes, competencias = registro_info
                    info_text = f"""
Colegio: {colegio}
Nivel: {nivel} | Año: {año} | Bimestre: {bimestre}
Grado: {grado}° | Sección: {seccion} | Curso: {curso}
Promedio: {promedio if promedio else 'N/A'}
Estadísticas: {estudiantes} estudiantes, {docentes} docentes, {competencias} competencias
                    """.strip()
                    lbl_info_registro.config(text=info_text, fg="#0D47A1")
                
            except Exception as e:
                lbl_info_registro.config(text=f"Error al cargar información: {str(e)}", fg="red")
    
    combo_registros.bind("<<ComboboxSelected>>", actualizar_info_registro)
    
    def asignar_estudiante():
        seleccion = combo_registros.get()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un registro")
            return
        
        numero_registro = registros_dict[seleccion]
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Verificar si ya existe la asignación (por si acaso)
            cursor.execute("""
                SELECT 1 FROM Estudiante_Registro 
                WHERE Codigo_estudiante = %s AND Numero_de_registro = %s
            """, (codigo_estudiante, numero_registro))
            
            if cursor.fetchone():
                messagebox.showwarning("Asignación existente", 
                                    "El estudiante ya está asignado a este registro")
            else:
                # Insertar la asignación
                cursor.execute("""
                    INSERT INTO Estudiante_Registro (Codigo_estudiante, Numero_de_registro)
                    VALUES (%s, %s)
                """, (codigo_estudiante, numero_registro))
                
                conexion.commit()
                messagebox.showinfo("Éxito", 
                                  f"Estudiante asignado correctamente al registro #{numero_registro}")
                
                if callback_actualizar:
                    callback_actualizar()
                
                ventana.destroy()
            
            cursor.close()
            conexion.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al asignar estudiante: {str(e)}")
    
    # Frame de botones
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=15)
    
    btn_asignar = tk.Button(
        frame_botones,
        text="✅ Asignar a Registro",
        font=("Arial", 11, "bold"),
        bg="#388E3C",
        fg="white",
        width=18,
        command=asignar_estudiante
    )
    btn_asignar.pack(side="left", padx=5)
    
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
    centrar_ventana(ventana, 600, 400)
    
    return ventana