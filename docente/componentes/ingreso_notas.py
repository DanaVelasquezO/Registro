import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def crear_frame_ingreso_notas(parent):
    """
    Crea el frame de ingreso de notas
    """
    frame_ingreso = tk.LabelFrame(parent, text="Ingreso de Notas", 
                                font=("Arial", 11, "bold"), bg="#E3F2FD", fg="#0D47A1")
    
    # Variables
    indicadores_dict = {}
    estudiante_actual = None
    numero_registro_actual = None
    
    # Función para mostrar información del estudiante
    def mostrar_estudiante(estudiante, numero_registro):
        nonlocal estudiante_actual, numero_registro_actual
        estudiante_actual = estudiante
        numero_registro_actual = numero_registro
        
        print(f"Mostrando estudiante: {estudiante['nombre']} - Registro: {numero_registro}")
        
        # Limpiar frame
        for widget in frame_ingreso.winfo_children():
            widget.destroy()
        
        # Información del estudiante
        info_estudiante = tk.Frame(frame_ingreso, bg="#E3F2FD")
        info_estudiante.pack(fill="x", padx=10, pady=5)
        
        tk.Label(info_estudiante, text=f"Estudiante: {estudiante['nombre']}", 
                font=("Arial", 11, "bold"), bg="#E3F2FD").pack(side="left")
        tk.Label(info_estudiante, text=f"Código: {estudiante['codigo']}", 
                font=("Arial", 10), bg="#E3F2FD").pack(side="left", padx=20)
        
        # Cargar competencias e indicadores
        cargar_competencias_indicadores(numero_registro)
    
    # Función para cargar competencias e indicadores
    def cargar_competencias_indicadores(numero_registro):
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
            print(f"Cargando competencias para registro: {numero_registro}")
            competencias = cursor.fetchall()
            
            # Frame para competencias con scroll
            frame_competencias_container = tk.Frame(frame_ingreso, bg="#E3F2FD")
            frame_competencias_container.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Scrollbar para competencias
            scrollbar_competencias = tk.Scrollbar(frame_competencias_container)
            scrollbar_competencias.pack(side="right", fill="y")
            
            # Canvas para scroll
            canvas_competencias = tk.Canvas(frame_competencias_container, bg="#E3F2FD", 
                                          yscrollcommand=scrollbar_competencias.set)
            canvas_competencias.pack(side="left", fill="both", expand=True)
            scrollbar_competencias.config(command=canvas_competencias.yview)
            
            # Frame interno para competencias (dentro del canvas)
            frame_competencias = tk.Frame(canvas_competencias, bg="#E3F2FD")
            canvas_competencias.create_window((0, 0), window=frame_competencias, anchor="nw")
            
            def configurar_scroll_region(event):
                canvas_competencias.configure(scrollregion=canvas_competencias.bbox("all"))
            
            frame_competencias.bind("<Configure>", configurar_scroll_region)
            
            row = 0
            indicadores_dict.clear()
            
            for competencia in competencias:
                id_competencia, nombre_competencia = competencia
                
                # Frame para cada competencia
                frame_competencia = tk.LabelFrame(frame_competencias, text=nombre_competencia, 
                                                font=("Arial", 10, "bold"), bg="#E3F2FD", fg="#0D47A1")
                frame_competencia.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
                frame_competencias.columnconfigure(0, weight=1)
                
                # Obtener indicadores de esta competencia para este registro
                cursor.execute("""
                    SELECT i.Id_indicador, i.Indicadores_competencias
                    FROM Indicadores i
                    JOIN Indicadores_Registro ir ON i.Id_indicador = ir.Id_indicador
                    WHERE ir.Numero_de_registro = %s AND i.Id_competencia = %s
                    ORDER BY i.Id_indicador
                """, (numero_registro, id_competencia))
                
                indicadores = cursor.fetchall()
                
                # Crear campos para cada indicador
                for idx, indicador in enumerate(indicadores):
                    id_indicador, nombre_indicador = indicador
                    
                    # Frame para cada indicador
                    frame_indicador = tk.Frame(frame_competencia, bg="#E3F2FD")
                    frame_indicador.pack(fill="x", padx=10, pady=3)
                    
                    # Nombre del indicador (más ancho)
                    lbl_indicador = tk.Label(frame_indicador, text=nombre_indicador, 
                                           font=("Arial", 9), bg="#E3F2FD", width=60, anchor="w")
                    lbl_indicador.pack(side="left", padx=(0, 10))
                    
                    # Entry para nota (en lugar de combobox)
                    entry_nota = tk.Entry(frame_indicador, 
                                        font=("Arial", 9),
                                        width=8,
                                        justify="center")
                    entry_nota.pack(side="left", padx=5)
                    
                    # Tooltip para mostrar formato permitido
                    def crear_tooltip(widget, text):
                        def mostrar_tooltip(event):
                            tooltip = tk.Toplevel(widget)
                            tooltip.wm_overrideredirect(True)
                            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
                            label = tk.Label(tooltip, text=text, background="lightyellow", 
                                           relief="solid", borderwidth=1, font=("Arial", 8))
                            label.pack()
                            tooltip.after(3000, tooltip.destroy)
                        widget.bind("<Enter>", mostrar_tooltip)
                    
                    crear_tooltip(entry_nota, "Ingrese nota de 0 a 20 (ej: 17.90)")
                    
                    # Cargar nota existente si existe
                    cargar_nota_existente(numero_registro, estudiante_actual['codigo'], id_indicador, entry_nota)
                    
                    # Guardar referencia
                    indicadores_dict[f"{id_competencia}_{id_indicador}"] = {
                        'entry': entry_nota,
                        'id_indicador': id_indicador,
                        'id_competencia': id_competencia,
                        'nombre_indicador': nombre_indicador
                    }
                
                row += 1
            
            cursor.close()
            conexion.close()
            
            # Si no hay indicadores, mostrar mensaje
            if not indicadores_dict:
                tk.Label(frame_ingreso, text="No hay indicadores asignados a este registro", 
                        font=("Arial", 10), bg="#E3F2FD", fg="#666666").pack(pady=20)
            else:
                # Frame para botones
                frame_botones = tk.Frame(frame_ingreso, bg="#E3F2FD")
                frame_botones.pack(pady=10, fill="x")
                
                # Botón guardar todas las notas
                btn_guardar_todas = tk.Button(
                    frame_botones,
                    text="💾 Guardar Todas las Notas",
                    font=("Arial", 11, "bold"),
                    bg="#388E3C",
                    fg="white",
                    width=20,
                    command=guardar_todas_las_notas
                )
                btn_guardar_todas.pack(side="left", padx=5)
                
                # Botón limpiar todas las notas
                btn_limpiar = tk.Button(
                    frame_botones,
                    text="🔄 Limpiar Todas las Notas",
                    font=("Arial", 11),
                    bg="#F57C00",
                    fg="white",
                    width=18,
                    command=limpiar_todas_las_notas
                )
                btn_limpiar.pack(side="left", padx=5)
                
                # Información sobre formato
                lbl_info = tk.Label(frame_botones, 
                                  text="Formato: 0-20 (ej: 17.90)", 
                                  font=("Arial", 9), bg="#E3F2FD", fg="#666666")
                lbl_info.pack(side="left", padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar competencias: {str(e)}")
    
    # Función para cargar nota existente
    def cargar_nota_existente(numero_registro, codigo_estudiante, id_indicador, entry_nota):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Buscar nota en Notas_Registro
            cursor.execute("""
                SELECT Nota 
                FROM Notas_Registro 
                WHERE Numero_de_registro = %s 
                AND Codigo_estudiante = %s 
                AND Id_indicador = %s
            """, (numero_registro, codigo_estudiante, id_indicador))
            
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            
            if resultado and resultado[0] is not None:
                # Mostrar la nota exacta (puede ser decimal)
                nota = float(resultado[0])
                entry_nota.insert(0, f"{nota:.2f}")
            
        except Exception as e:
            print(f"Error al cargar nota existente: {e}")
    
    # Función para validar nota
    def validar_nota(nota_str):
        """Valida que la nota esté entre 0 y 20"""
        try:
            nota = float(nota_str)
            return 0 <= nota <= 20
        except ValueError:
            return False
    
    # Función para limpiar todas las notas
    def limpiar_todas_las_notas():
        for key, info in indicadores_dict.items():
            info['entry'].delete(0, tk.END)
    
    # Función para guardar todas las notas
    def guardar_todas_las_notas():
        if not estudiante_actual or not numero_registro_actual:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un estudiante")
            return
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            notas_guardadas = 0
            notas_invalidas = []
            
            for key, info in indicadores_dict.items():
                nota_str = info['entry'].get().strip()
                
                if nota_str:
                    if validar_nota(nota_str):
                        try:
                            nota = float(nota_str)
                            
                            # Guardar en Notas_Registro
                            cursor.execute("""
                                INSERT INTO Notas_Registro (Numero_de_registro, Codigo_estudiante, 
                                                          Id_competencia, Id_indicador, Nota)
                                VALUES (%s, %s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE Nota = %s
                            """, (numero_registro_actual, estudiante_actual['codigo'], 
                                  info['id_competencia'], info['id_indicador'], 
                                  nota, nota))
                            
                            notas_guardadas += 1
                        except ValueError:
                            notas_invalidas.append(info['nombre_indicador'])
                    else:
                        notas_invalidas.append(info['nombre_indicador'])
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            # Mostrar resultado
            mensaje = f"Se guardaron {notas_guardadas} notas para {estudiante_actual['nombre']}"
            if notas_invalidas:
                mensaje += f"\n\nNotas inválidas ({len(notas_invalidas)}):\n"
                mensaje += "\n".join([f"- {ind}" for ind in notas_invalidas[:3]])  # Mostrar solo las primeras 3
                if len(notas_invalidas) > 3:
                    mensaje += f"\n- ... y {len(notas_invalidas) - 3} más"
                mensaje += "\n\nLas notas deben estar entre 0 y 20"
            
            messagebox.showinfo("Resultado", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar notas: {str(e)}")
    
    # Retornar el frame y las funciones
    return {
        'frame': frame_ingreso,
        'mostrar_estudiante': mostrar_estudiante,
        'guardar_notas': guardar_todas_las_notas,
        'limpiar_notas': limpiar_todas_las_notas
    }