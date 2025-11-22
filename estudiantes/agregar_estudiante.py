import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def centrar_ventana(ventana):  # MOVER ESTA FUNCIÓN ARRIBA
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_agregar_estudiante(ventana_padre=None, callback_actualizar=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Agregar Estudiante")
    ventana.geometry("400x200")
    ventana.resizable(False, False)
    ventana.config(bg="#E3F2FD")
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    centrar_ventana(ventana)  # AHORA SÍ PUEDES LLAMARLA
    
    # Título
    titulo = tk.Label(
        ventana,
        text="Agregar Nuevo Estudiante",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Frame del formulario
    frame_form = tk.Frame(ventana, bg="#E3F2FD")
    frame_form.pack(pady=10, padx=20, fill="x")
    
    # Campo nombre
    tk.Label(frame_form, text="Nombre del Estudiante:*", bg="#E3F2FD", 
             font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
    entry_nombre = tk.Entry(frame_form, font=("Arial", 11), width=30)
    entry_nombre.grid(row=0, column=1, padx=10, pady=8, sticky="w")
    entry_nombre.focus()
    
    # Información del código
    tk.Label(frame_form, text="Código:", bg="#E3F2FD", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
    lbl_codigo = tk.Label(frame_form, text="Auto-generado", font=("Arial", 10, "italic"), 
                         bg="#E3F2FD", fg="#666666")
    lbl_codigo.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    def guardar_estudiante():
        nombre = entry_nombre.get().strip()
        
        if not nombre:
            messagebox.showwarning("Campo vacío", "Por favor ingrese el nombre del estudiante")
            entry_nombre.focus()
            return
            
        if len(nombre) > 40:
            messagebox.showwarning("Nombre muy largo", "El nombre no puede exceder los 40 caracteres")
            return
            
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Verificar si ya existe un estudiante con el mismo nombre
            cursor.execute("SELECT Codigo_estudiante FROM Estudiante WHERE Nombre_estudiante = %s", (nombre,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Ya existe un estudiante con ese nombre")
                return
                
            # Insertar nuevo estudiante
            cursor.execute("INSERT INTO Estudiante (Nombre_estudiante) VALUES (%s)", (nombre,))
            conexion.commit()
            codigo_generado = cursor.lastrowid
            
            cursor.close()
            conexion.close()
            
            messagebox.showinfo("Éxito", f"Estudiante agregado correctamente\nCódigo: {codigo_generado}")
            
            if callback_actualizar:
                callback_actualizar()
                
            ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar estudiante: {str(e)}")
    
    # Frame de botones
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=15)
    
    btn_guardar = tk.Button(
        frame_botones,
        text="Guardar Estudiante",
        font=("Arial", 10, "bold"),
        bg="#388E3C",
        fg="white",
        width=15,
        command=guardar_estudiante
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
    ventana.bind('<Return>', lambda e: guardar_estudiante())
    
    return ventana