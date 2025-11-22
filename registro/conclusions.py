import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_gestion_conclusiones(numero_registro, ventana_padre=None, callback_actualizar=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title(f"Conclusiones Descriptivas - Registro #{numero_registro}")
    ventana.geometry("700x500")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(True, True)
    
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Título
    titulo = tk.Label(
        ventana,
        text=f"Conclusiones Descriptivas - Registro #{numero_registro}",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Frame de información del registro
    frame_info = tk.Frame(ventana, bg="#E3F2FD")
    frame_info.pack(pady=10, padx=20, fill="x")
    
    # Cargar información del registro
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT Nivel, Nombre_colegio, Año, Bimestre, Grado, Seccion, Curso, Conclusiones_descriptivas
            FROM REGISTRO_AUXILIAR 
            WHERE Numero_de_registro = %s
        """, (numero_registro,))
        registro = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if registro:
            nivel, colegio, año, bimestre, grado, seccion, curso, conclusiones_actuales = registro
            
            info_text = f"{colegio} - {grado}°{seccion} - {curso} - {año} - Bimestre {bimestre}"
            lbl_info = tk.Label(
                frame_info,
                text=info_text,
                font=("Arial", 11, "bold"),
                bg="#E3F2FD",
                fg="#0D47A1"
            )
            lbl_info.pack()
            
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar información del registro: {str(e)}")
    
    # Frame de conclusiones
    frame_conclusiones = tk.Frame(ventana, bg="#E3F2FD")
    frame_conclusiones.pack(pady=10, padx=20, fill="both", expand=True)
    
    tk.Label(
        frame_conclusiones,
        text="Conclusiones Descriptivas:",
        font=("Arial", 11, "bold"),
        bg="#E3F2FD"
    ).pack(anchor="w", pady=(0, 5))
    
    # Área de texto para conclusiones
    text_conclusiones = tk.Text(
        frame_conclusiones,
        font=("Arial", 10),
        width=80,
        height=15,
        wrap="word"
    )
    text_conclusiones.pack(fill="both", expand=True)
    
    # Cargar conclusiones existentes si las hay
    if registro and conclusiones_actuales:
        text_conclusiones.insert("1.0", conclusiones_actuales)
    
    # Scrollbar para el área de texto
    scroll_text = tk.Scrollbar(text_conclusiones)
    scroll_text.pack(side="right", fill="y")
    text_conclusiones.config(yscrollcommand=scroll_text.set)
    scroll_text.config(command=text_conclusiones.yview)
    
    def guardar_conclusiones():
        conclusiones = text_conclusiones.get("1.0", "end-1c").strip()
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            cursor.execute("""
                UPDATE REGISTRO_AUXILIAR 
                SET Conclusiones_descriptivas = %s 
                WHERE Numero_de_registro = %s
            """, (conclusiones, numero_registro))
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            messagebox.showinfo("Éxito", "Conclusiones guardadas correctamente")
            
            if callback_actualizar:
                callback_actualizar()
                
            ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar conclusiones: {str(e)}")
    
    # Frame de botones
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=15)
    
    btn_guardar = tk.Button(
        frame_botones,
        text="💾 Guardar Conclusiones",
        font=("Arial", 11, "bold"),
        bg="#388E3C",
        fg="white",
        width=20,
        command=guardar_conclusiones
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
    centrar_ventana(ventana, 700, 500)
    
    return ventana