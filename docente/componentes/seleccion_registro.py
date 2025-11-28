import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def crear_frame_seleccion_registro(parent, codigo_docente, callback_cargar_estudiantes):

    frame_seleccion = tk.LabelFrame(parent, text="Seleccionar Registro", 
                                  font=("Arial", 12, "bold"), bg="#E3F2FD", fg="#0D47A1")
    frame_seleccion.pack(fill="x", padx=20, pady=10)
    
    tk.Label(frame_seleccion, text="Registro:", bg="#E3F2FD", font=("Arial", 10)).pack(side="left", padx=5)
    
    # Combobox para seleccionar registro
    combo_registros = ttk.Combobox(frame_seleccion, state="readonly", width=50)
    combo_registros.pack(side="left", padx=5)
    
    # Botón cargar estudiantes
    btn_cargar = tk.Button(
        frame_seleccion,
        text="Cargar Estudiantes",
        font=("Arial", 10, "bold"),
        bg="#388E3C",
        fg="white",
        width=15
    )
    btn_cargar.pack(side="left", padx=10)
    
    # Información del registro seleccionado
    lbl_info_registro = tk.Label(frame_seleccion, text="Seleccione un registro", 
                                font=("Arial", 9), bg="#E3F2FD", fg="#666666")
    lbl_info_registro.pack(side="left", padx=10)
    
    # Variables
    registros_dict = {}
    
    # Función para cargar registros del docente
    def cargar_registros():
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            cursor.execute("""
                SELECT DISTINCT r.Numero_de_registro, r.Nombre_colegio, r.Año, r.Bimestre, 
                               r.Grado, r.Seccion, r.Curso
                FROM REGISTRO_AUXILIAR r
                JOIN Docente_Registro dr ON r.Numero_de_registro = dr.Numero_de_registro
                WHERE dr.Codigo_docente = %s
                ORDER BY r.Año DESC, r.Bimestre, r.Numero_de_registro DESC
            """, (codigo_docente,))
            
            registros = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Limpiar combobox
            combo_registros.set('')
            combo_registros['values'] = []
            registros_dict.clear()
            
            if registros:
                valores_combo = []
                for registro in registros:
                    num_registro, colegio, año, bimestre, grado, seccion, curso = registro
                    display_text = f"Registro #{num_registro} - {colegio} - {curso} ({grado}° {seccion}) - {año}"
                    valores_combo.append(display_text)
                    registros_dict[display_text] = {
                        'numero': num_registro,
                        'colegio': colegio,
                        'año': año,
                        'bimestre': bimestre,
                        'grado': grado,
                        'seccion': seccion,
                        'curso': curso
                    }
                
                combo_registros['values'] = valores_combo
            else:
                messagebox.showinfo("Información", "No tiene registros asignados")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar registros: {str(e)}")
    
    # Función para actualizar información del registro
    def actualizar_info_registro(event=None):
        seleccion = combo_registros.get()
        if seleccion and seleccion in registros_dict:
            registro = registros_dict[seleccion]
            info_text = f"{registro['colegio']} - {registro['curso']} ({registro['grado']}° {registro['seccion']}) - {registro['año']}"
            lbl_info_registro.config(text=info_text, fg="#0D47A1")
        else:
            lbl_info_registro.config(text="Seleccione un registro", fg="#666666")
    
    # Función para cargar estudiantes
    def cargar_estudiantes():
        seleccion = combo_registros.get()
        if not seleccion or seleccion not in registros_dict:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un registro")
            return
        
        numero_registro = registros_dict[seleccion]['numero']
        callback_cargar_estudiantes(numero_registro)
    
    # Conectar eventos
    combo_registros.bind("<<ComboboxSelected>>", actualizar_info_registro)
    btn_cargar.config(command=cargar_estudiantes)
    
    # Cargar registros al iniciar
    cargar_registros()
    
    # Retornar elementos importantes para el control externo
    return {
        'frame': frame_seleccion,
        'combo_registros': combo_registros,
        'btn_cargar': btn_cargar,
        'lbl_info_registro': lbl_info_registro,
        'get_registro_seleccionado': lambda: registros_dict.get(combo_registros.get())
    }