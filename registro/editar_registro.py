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
    ventana.geometry("600x500")
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
    
    # Cargar datos actuales del registro
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT Nivel, Nombre_colegio, Año, Bimestre, Grado, Seccion, Curso, Promedio_curso
            FROM REGISTRO_AUXILIAR 
            WHERE Numero_de_registro = %s
        """, (numero_registro,))
        registro = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if not registro:
            messagebox.showerror("Error", "Registro no encontrado")
            ventana.destroy()
            return
            
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar registro: {str(e)}")
        ventana.destroy()
        return
    
    nivel_actual, colegio_actual, año_actual, bimestre_actual, grado_actual, seccion_actual, curso_actual, promedio_actual = registro
    
    # Frame del formulario
    frame_form = tk.Frame(ventana, bg="#E3F2FD")
    frame_form.pack(pady=10, padx=20, fill="x")
    
    # Campos editables
    campos = [
        ("Nivel:", ["Primaria", "Secundaria"], "nivel", nivel_actual),
        ("Año:", list(range(2020, 2031)), "año", año_actual),
        ("Bimestre:", ["I", "II", "III", "IV"], "bimestre", bimestre_actual),
        ("Grado:", ["1", "2", "3", "4", "5", "6"], "grado", grado_actual),
        ("Sección:", ["A", "B", "C", "D"], "seccion", seccion_actual)
    ]
    
    entries = {}
    row = 0
    
    for label_text, opciones, key, valor_actual in campos:
        tk.Label(frame_form, text=label_text, bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5)
        if opciones:
            combo = ttk.Combobox(frame_form, values=opciones, state="readonly", width=20)
            combo.set(valor_actual)
            combo.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[key] = combo
        else:
            entry = tk.Entry(frame_form, font=("Arial", 10), width=25)
            entry.insert(0, str(valor_actual))
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[key] = entry
        row += 1
    
    # Colegio
    tk.Label(frame_form, text="Nombre del Colegio:", bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5)
    entries["colegio"] = tk.Entry(frame_form, font=("Arial", 10), width=25)
    entries["colegio"].insert(0, colegio_actual)
    entries["colegio"].grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1
    
    # Curso
    tk.Label(frame_form, text="Curso:", bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5)
    entries["curso"] = tk.Entry(frame_form, font=("Arial", 10), width=25)
    entries["curso"].insert(0, curso_actual)
    entries["curso"].grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1
    
    # Promedio del curso
    tk.Label(frame_form, text="Promedio del Curso:", bg="#E3F2FD", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5)
    entries["promedio"] = tk.Entry(frame_form, font=("Arial", 10), width=25)
    entries["promedio"].insert(0, str(promedio_actual) if promedio_actual else "")
    entries["promedio"].grid(row=row, column=1, padx=10, pady=5, sticky="w")
    
    def actualizar_registro():
        # Validar campos obligatorios
        campos_obligatorios = ["nivel", "año", "bimestre", "grado", "seccion", "colegio", "curso"]
        for campo in campos_obligatorios:
            if not entries[campo].get().strip():
                messagebox.showwarning("Campo vacío", f"Por favor complete el campo: {campo}")
                return
        
        # Validar promedio (opcional pero debe ser numérico si se ingresa)
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
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
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
    
    # Centrar ventana
    centrar_ventana(ventana, 600, 500)
    
    return ventana