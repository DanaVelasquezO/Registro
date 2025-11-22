import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def ventana_editar_estudiante(estudiante_data, ventana_padre=None, callback_actualizar=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Editar Estudiante")
    ventana.geometry("450x250")
    ventana.resizable(False, False)
    ventana.config(bg="#E3F2FD")
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Centrar ventana - FUNCIÓN DENTRO DE LA FUNCIÓN PRINCIPAL
    def centrar_ventana(ventana):
        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    centrar_ventana(ventana)  # AHORA SÍ ESTÁ DENTRO DE LA FUNCIÓN PRINCIPAL
    
    codigo_estudiante, nombre_actual = estudiante_data
    
    # Título
    titulo = tk.Label(
        ventana,
        text="Editar Estudiante",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Frame del formulario
    frame_form = tk.Frame(ventana, bg="#E3F2FD")
    frame_form.pack(pady=10, padx=20, fill="x")
    
    # Código (solo lectura)
    tk.Label(frame_form, text="Código Estudiante:", bg="#E3F2FD", 
             font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8)
    lbl_codigo = tk.Label(frame_form, text=str(codigo_estudiante), font=("Arial", 10, "bold"), 
                         bg="#E3F2FD", fg="#0D47A1")
    lbl_codigo.grid(row=0, column=1, padx=10, pady=8, sticky="w")
    
    # Campo nombre
    tk.Label(frame_form, text="Nombre del Estudiante:*", bg="#E3F2FD", 
             font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
    entry_nombre = tk.Entry(frame_form, font=("Arial", 11), width=35)
    entry_nombre.grid(row=1, column=1, padx=10, pady=8, sticky="w")
    entry_nombre.insert(0, nombre_actual)
    entry_nombre.select_range(0, tk.END)
    entry_nombre.focus()
    
    # Información de registros asociados
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM Estudiante_Registro 
            WHERE Codigo_estudiante = %s
        """, (codigo_estudiante,))
        total_registros = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        
        tk.Label(frame_form, text="Registros asociados:", bg="#E3F2FD", 
                font=("Arial", 9)).grid(row=2, column=0, sticky="w", pady=5)
        lbl_registros = tk.Label(frame_form, text=str(total_registros), font=("Arial", 9), 
                               bg="#E3F2FD", fg="#D32F2F" if total_registros > 0 else "#666666")
        lbl_registros.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
    except Exception as e:
        print(f"Error al cargar información de registros: {e}")
    
    def actualizar_estudiante():
        nuevo_nombre = entry_nombre.get().strip()
        
        if not nuevo_nombre:
            messagebox.showwarning("Campo vacío", "Por favor ingrese el nombre del estudiante")
            entry_nombre.focus()
            return
            
        if len(nuevo_nombre) > 40:
            messagebox.showwarning("Nombre muy largo", "El nombre no puede exceder los 40 caracteres")
            return
            
        if nuevo_nombre == nombre_actual:
            messagebox.showinfo("Sin cambios", "No se realizaron cambios en el nombre")
            ventana.destroy()
            return
            
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Verificar si ya existe otro estudiante con el mismo nombre
            cursor.execute("""
                SELECT Codigo_estudiante FROM Estudiante 
                WHERE Nombre_estudiante = %s AND Codigo_estudiante != %s
            """, (nuevo_nombre, codigo_estudiante))
            
            if cursor.fetchone():
                messagebox.showerror("Error", "Ya existe otro estudiante con ese nombre")
                return
                
            # Actualizar estudiante
            cursor.execute("""
                UPDATE Estudiante 
                SET Nombre_estudiante = %s 
                WHERE Codigo_estudiante = %s
            """, (nuevo_nombre, codigo_estudiante))
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
            
            if callback_actualizar:
                callback_actualizar()
                
            ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar estudiante: {str(e)}")
    
    # Frame de botones
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=15)
    
    btn_guardar = tk.Button(
        frame_botones,
        text="Guardar Cambios",
        font=("Arial", 10, "bold"),
        bg="#F57C00",
        fg="white",
        width=15,
        command=actualizar_estudiante
    )
    btn_guardar.pack(side="left", padx=5)
    
    btn_cancelar = tk.Button(
        frame_botones,
        text="Cancelar",
        font=("Arial", 10),
        bg="#757575",
        fg="white",
        width=15,
        command=ventana.destroy
    )
    btn_cancelar.pack(side="left", padx=5)
    
    # Enter para guardar
    ventana.bind('<Return>', lambda e: actualizar_estudiante())
    
    return ventana