import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def ventana_eliminar_estudiante(estudiante_data, ventana_padre=None, callback_actualizar=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Eliminar Estudiante")
    ventana.geometry("500x300")
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
    
    codigo_estudiante, nombre_estudiante = estudiante_data
    
    # Título
    titulo = tk.Label(
        ventana,
        text="Eliminar Estudiante",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#D32F2F"
    )
    titulo.pack(pady=15)
    
    # Frame de información
    frame_info = tk.Frame(ventana, bg="#E3F2FD")
    frame_info.pack(pady=10, padx=20, fill="x")
    
    # Información del estudiante
    tk.Label(frame_info, text="Estudiante a eliminar:", bg="#E3F2FD", 
             font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5)
    
    tk.Label(frame_info, text=f"Código: {codigo_estudiante}", bg="#E3F2FD", 
             font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=2)
    
    tk.Label(frame_info, text=f"Nombre: {nombre_estudiante}", bg="#E3F2FD", 
             font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=2)
    
    # Verificar registros asociados
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Contar registros auxiliares asociados
        cursor.execute("""
            SELECT COUNT(*) FROM Estudiante_Registro 
            WHERE Codigo_estudiante = %s
        """, (codigo_estudiante,))
        total_registros = cursor.fetchone()[0]
        
        # Obtener lista de registros específicos
        cursor.execute("""
            SELECT ra.Numero_de_registro, ra.Curso, ra.Grado, ra.Seccion
            FROM Estudiante_Registro er
            JOIN REGISTRO_AUXILIAR ra ON er.Numero_de_registro = ra.Numero_de_registro
            WHERE er.Codigo_estudiante = %s
        """, (codigo_estudiante,))
        registros = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        # Mostrar información de registros asociados
        tk.Label(frame_info, text="Registros asociados:", bg="#E3F2FD", 
                font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=(10,5))
        
        if total_registros > 0:
            lbl_advertencia = tk.Label(
                frame_info, 
                text=f"El estudiante está asociado a {total_registros} registro(s) auxiliar(es)",
                font=("Arial", 10, "bold"), 
                bg="#FFF3CD", 
                fg="#856404",
                relief="solid",
                bd=1
            )
            lbl_advertencia.grid(row=4, column=0, sticky="we", pady=5, ipadx=5, ipady=2)
            
            # Mostrar lista de registros
            frame_registros = tk.Frame(frame_info, bg="#F8F9FA", relief="solid", bd=1)
            frame_registros.grid(row=5, column=0, sticky="we", pady=5)
            
            for i, registro in enumerate(registros):
                num_reg, curso, grado, seccion = registro
                lbl_reg = tk.Label(
                    frame_registros,
                    text=f"• Registro #{num_reg}: {curso} - {grado}°{seccion}",
                    font=("Arial", 9),
                    bg="#F8F9FA",
                    fg="#495057"
                )
                lbl_reg.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            
            lbl_info = tk.Label(
                frame_info,
                text="Para eliminar al estudiante, primero debe removerlo de todos los registros asociados.",
                font=("Arial", 9),
                bg="#E3F2FD",
                fg="#D32F2F",
                wraplength=450
            )
            lbl_info.grid(row=6, column=0, sticky="w", pady=5)
            
            puede_eliminar = False
        else:
            lbl_sin_registros = tk.Label(
                frame_info,
                text="✅ El estudiante no tiene registros asociados. Puede ser eliminado.",
                font=("Arial", 10),
                bg="#E3F2FD",
                fg="#388E3C"
            )
            lbl_sin_registros.grid(row=4, column=0, sticky="w", pady=5)
            puede_eliminar = True
            
    except Exception as e:
        messagebox.showerror("Error", f"Error al verificar registros: {str(e)}")
        puede_eliminar = False
    
    def confirmar_eliminacion():
        if not puede_eliminar:
            messagebox.showwarning("No se puede eliminar", 
                                 "No es posible eliminar al estudiante porque tiene registros asociados.")
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar al estudiante?\n\n"
            f"Código: {codigo_estudiante}\n"
            f"Nombre: {nombre_estudiante}\n\n"
            "Esta acción no se puede deshacer.",
            icon="warning"
        )
        
        if confirmacion:
            try:
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                
                # Eliminar estudiante
                cursor.execute("DELETE FROM Estudiante WHERE Codigo_estudiante = %s", (codigo_estudiante,))
                conexion.commit()
                cursor.close()
                conexion.close()
                
                messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
                
                if callback_actualizar:
                    callback_actualizar()
                    
                ventana.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar estudiante: {str(e)}")
    
    # Frame de botones
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=15)
    
    if puede_eliminar:
        btn_eliminar = tk.Button(
            frame_botones,
            text="Eliminar Estudiante",
            font=("Arial", 10, "bold"),
            bg="#D32F2F",
            fg="white",
            width=18,
            command=confirmar_eliminacion
        )
        btn_eliminar.pack(side="left", padx=5)
    
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
    
    # Centrar la ventana después de crear todos los widgets
    centrar_ventana(ventana)
    
    return ventana