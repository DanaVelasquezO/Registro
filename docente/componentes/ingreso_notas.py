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
    print(f"Mostrando estudiante: {estudiante['nombre']} - Registro: {numero_registro}")
    # Función para mostrar información del estudiante
    def mostrar_estudiante(estudiante, numero_registro):
        
        nonlocal estudiante_actual
        estudiante_actual = estudiante
        
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
            
            # Frame para competencias
            frame_competencias = tk.Frame(frame_ingreso, bg="#E3F2FD")
            frame_competencias.pack(fill="x", padx=10, pady=10)
            
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
                    frame_indicador.pack(fill="x", padx=10, pady=2)
                    
                    # Nombre del indicador
                    lbl_indicador = tk.Label(frame_indicador, text=nombre_indicador, 
                                           font=("Arial", 9), bg="#E3F2FD", width=40, anchor="w")
                    lbl_indicador.pack(side="left")
                    
                    # Combobox para nota
                    combo_nota = ttk.Combobox(frame_indicador, 
                                            values=[str(i) for i in range(0, 21)],
                                            state="readonly", 
                                            width=5,
                                            font=("Arial", 9))
                    combo_nota.pack(side="left", padx=10)
                    
                    # Cargar nota existente si existe
                    cargar_nota_existente(numero_registro, estudiante_actual['codigo'], id_indicador, combo_nota)
                    
                    # Guardar referencia
                    indicadores_dict[f"{id_competencia}_{id_indicador}"] = {
                        'combobox': combo_nota,
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
                # Botón guardar todas las notas
                btn_guardar_todas = tk.Button(
                    frame_ingreso,
                    text="💾 Guardar Todas las Notas",
                    font=("Arial", 11, "bold"),
                    bg="#388E3C",
                    fg="white",
                    width=20,
                    command=lambda: guardar_todas_las_notas(numero_registro)
                )
                btn_guardar_todas.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar competencias: {str(e)}")
    
    # Función para cargar nota existente
    def cargar_nota_existente(numero_registro, codigo_estudiante, id_indicador, combobox):
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
                # Convertir decimal a entero para el combobox
                nota_entera = int(round(float(resultado[0])))
                combobox.set(str(nota_entera))
            
        except Exception as e:
            print(f"Error al cargar nota existente: {e}")
    
    # Función para guardar todas las notas
    def guardar_todas_las_notas(numero_registro):
        if not estudiante_actual:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un estudiante")
            return
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            notas_guardadas = 0
            
            for key, info in indicadores_dict.items():
                nota_str = info['combobox'].get()
                
                if nota_str and nota_str.strip():
                    try:
                        nota = int(nota_str)
                        if 0 <= nota <= 20:
                            # Convertir a decimal para la base de datos
                            nota_decimal = float(nota)
                            
                            # Guardar en Notas_Registro
                            cursor.execute("""
                                INSERT INTO Notas_Registro (Numero_de_registro, Codigo_estudiante, 
                                                          Id_competencia, Id_indicador, Nota)
                                VALUES (%s, %s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE Nota = %s
                            """, (numero_registro, estudiante_actual['codigo'], 
                                  info['id_competencia'], info['id_indicador'], 
                                  nota_decimal, nota_decimal))
                            
                            notas_guardadas += 1
                    except ValueError:
                        pass
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            messagebox.showinfo("Éxito", f"Se guardaron {notas_guardadas} notas para {estudiante_actual['nombre']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar notas: {str(e)}")
    
    return {
        'frame': frame_ingreso,
        'mostrar_estudiante': mostrar_estudiante,
        'guardar_notas': guardar_todas_las_notas
    }