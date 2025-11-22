import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_gestion_indicadores_registro(registro_id=None, ventana_padre=None):
    """
    Gestiona la asociación de indicadores a un registro auxiliar específico
    """
    if registro_id is None:
        messagebox.showerror("Error", "No se proporcionó un registro")
        return
    
    ventana = tk.Toplevel(ventana_padre)
    ventana.title(f"Asociar Indicadores - Registro #{registro_id}")
    ventana.geometry("1000x700")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(True, True)
    
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Frame principal
    main_frame = tk.Frame(ventana, bg="#E3F2FD")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Título
    titulo = tk.Label(
        main_frame,
        text=f"Asociar Indicadores al Registro #{registro_id}",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Obtener información del registro
    def obtener_info_registro():
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT Nombre_colegio, Nivel, Año, Bimestre, Grado, Seccion, Curso
                FROM REGISTRO_AUXILIAR 
                WHERE Numero_de_registro = %s
            """, (registro_id,))
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            
            if resultado:
                colegio, nivel, año, bimestre, grado, seccion, curso = resultado
                return f"{colegio} - {curso} ({grado}° {seccion}) - {año} - {bimestre}"
            return f"Registro #{registro_id}"
        except Exception as e:
            return f"Registro #{registro_id}"
    
    info_registro = tk.Label(
        main_frame,
        text=obtener_info_registro(),
        font=("Arial", 11),
        bg="#E3F2FD",
        fg="#666666"
    )
    info_registro.pack(pady=5)
    
    # Frame con dos columnas
    frame_contenedor = tk.Frame(main_frame, bg="#E3F2FD")
    frame_contenedor.pack(fill="both", expand=True, pady=10)
    
    # Columna izquierda - Competencias e Indicadores disponibles
    frame_disponibles = tk.LabelFrame(frame_contenedor, text="Competencias e Indicadores Disponibles", 
                                    font=("Arial", 11, "bold"), bg="#E3F2FD", fg="#0D47A1")
    frame_disponibles.pack(side="left", fill="both", expand=True, padx=(0, 5))
    
    # Columna derecha - Indicadores Asociados
    frame_asociados = tk.LabelFrame(frame_contenedor, text="Indicadores Asociados al Registro", 
                                  font=("Arial", 11, "bold"), bg="#E3F2FD", fg="#0D47A1")
    frame_asociados.pack(side="right", fill="both", expand=True, padx=(5, 0))
    
    # ===== COMPETENCIAS DISPONIBLES =====
    def cargar_competencias_disponibles():
        try:
            # Limpiar treeview
            for item in tree_competencias.get_children():
                tree_competencias.delete(item)
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener competencias que están asociadas al registro
            cursor.execute("""
                SELECT c.Id_competencia, c.Competencia
                FROM Competencias c
                JOIN Competencias_Registro cr ON c.Id_competencia = cr.Id_competencia
                WHERE cr.Numero_de_registro = %s
                ORDER BY c.Competencia
            """, (registro_id,))
            
            competencias = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            for id_comp, competencia in competencias:
                tree_competencias.insert("", "end", values=(id_comp, competencia), tags=(id_comp,))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar competencias: {str(e)}")
    
    # Treeview para competencias
    frame_tree_comp = tk.Frame(frame_disponibles)
    frame_tree_comp.pack(fill="both", expand=True, padx=10, pady=10)
    
    scroll_y_comp = tk.Scrollbar(frame_tree_comp)
    scroll_y_comp.pack(side="right", fill="y")
    
    tree_competencias = ttk.Treeview(
        frame_tree_comp,
        columns=("ID", "Competencia"),
        yscrollcommand=scroll_y_comp.set,
        show="headings",
        height=8
    )
    
    scroll_y_comp.config(command=tree_competencias.yview)
    
    tree_competencias.heading("ID", text="ID")
    tree_competencias.heading("Competencia", text="Competencia")
    tree_competencias.column("ID", width=80)
    tree_competencias.column("Competencia", width=300)
    
    tree_competencias.pack(fill="both", expand=True)
    
    # Indicadores de la competencia seleccionada
    lbl_indicadores = tk.Label(frame_disponibles, text="Indicadores de la competencia:", 
                             font=("Arial", 10, "bold"), bg="#E3F2FD")
    lbl_indicadores.pack(pady=(10, 5))
    
    frame_indicadores_comp = tk.Frame(frame_disponibles)
    frame_indicadores_comp.pack(fill="both", expand=True, padx=10, pady=5)
    
    scroll_y_ind = tk.Scrollbar(frame_indicadores_comp)
    scroll_y_ind.pack(side="right", fill="y")
    
    tree_indicadores_comp = ttk.Treeview(
        frame_indicadores_comp,
        columns=("ID", "Indicador", "Asociado"),
        yscrollcommand=scroll_y_ind.set,
        show="headings",
        height=6
    )
    
    scroll_y_ind.config(command=tree_indicadores_comp.yview)
    
    tree_indicadores_comp.heading("ID", text="ID")
    tree_indicadores_comp.heading("Indicador", text="Indicador")
    tree_indicadores_comp.heading("Asociado", text="Asociado")
    tree_indicadores_comp.column("ID", width=60)
    tree_indicadores_comp.column("Indicador", width=250)
    tree_indicadores_comp.column("Asociado", width=80)
    
    tree_indicadores_comp.pack(fill="both", expand=True)
    
    # ===== INDICADORES ASOCIADOS =====
    def cargar_indicadores_asociados():
        try:
            # Limpiar treeview
            for item in tree_indicadores_asoc.get_children():
                tree_indicadores_asoc.delete(item)
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener indicadores asociados al registro
            cursor.execute("""
                SELECT i.Id_indicador, i.Indicadores_competencias, c.Competencia
                FROM Indicadores i
                JOIN Indicadores_Registro ir ON i.Id_indicador = ir.Id_indicador
                JOIN Competencias c ON i.Id_competencia = c.Id_competencia
                WHERE ir.Numero_de_registro = %s
                ORDER BY c.Competencia, i.Id_indicador
            """, (registro_id,))
            
            indicadores = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            for id_ind, indicador, competencia in indicadores:
                tree_indicadores_asoc.insert("", "end", 
                                           values=(id_ind, indicador, competencia),
                                           tags=(id_ind,))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar indicadores asociados: {str(e)}")
    
    # Treeview para indicadores asociados
    frame_tree_asoc = tk.Frame(frame_asociados)
    frame_tree_asoc.pack(fill="both", expand=True, padx=10, pady=10)
    
    scroll_y_asoc = tk.Scrollbar(frame_tree_asoc)
    scroll_y_asoc.pack(side="right", fill="y")
    
    tree_indicadores_asoc = ttk.Treeview(
        frame_tree_asoc,
        columns=("ID", "Indicador", "Competencia"),
        yscrollcommand=scroll_y_asoc.set,
        show="headings",
        height=15
    )
    
    scroll_y_asoc.config(command=tree_indicadores_asoc.yview)
    
    tree_indicadores_asoc.heading("ID", text="ID")
    tree_indicadores_asoc.heading("Indicador", text="Indicador")
    tree_indicadores_asoc.heading("Competencia", text="Competencia")
    tree_indicadores_asoc.column("ID", width=60)
    tree_indicadores_asoc.column("Indicador", width=250)
    tree_indicadores_asoc.column("Competencia", width=200)
    
    tree_indicadores_asoc.pack(fill="both", expand=True)
    
    # ===== FUNCIONALIDADES =====
    def on_seleccion_competencia(event):
        seleccion = tree_competencias.selection()
        if not seleccion:
            return
        
        # Limpiar indicadores anteriores
        for item in tree_indicadores_comp.get_children():
            tree_indicadores_comp.delete(item)
        
        item = seleccion[0]
        id_competencia = tree_competencias.item(item, "values")[0]
        
        cargar_indicadores_competencia(id_competencia)
    
    def cargar_indicadores_competencia(id_competencia):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener todos los indicadores de esta competencia
            cursor.execute("""
                SELECT i.Id_indicador, i.Indicadores_competencias
                FROM Indicadores i
                WHERE i.Id_competencia = %s
                ORDER BY i.Id_indicador
            """, (id_competencia,))
            
            indicadores = cursor.fetchall()
            
            # Verificar cuáles están asociados al registro
            for id_ind, indicador in indicadores:
                cursor.execute("""
                    SELECT 1 FROM Indicadores_Registro 
                    WHERE Id_indicador = %s AND Numero_de_registro = %s
                """, (id_ind, registro_id))
                
                asociado = "✓" if cursor.fetchone() else "✗"
                tree_indicadores_comp.insert("", "end", 
                                           values=(id_ind, indicador, asociado),
                                           tags=(id_ind,))
            
            cursor.close()
            conexion.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar indicadores: {str(e)}")
    
    def asociar_indicador():
        seleccion = tree_indicadores_comp.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un indicador")
            return
        
        item = seleccion[0]
        id_indicador = tree_indicadores_comp.item(item, "values")[0]
        indicador = tree_indicadores_comp.item(item, "values")[1]
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Verificar si ya está asociado
            cursor.execute("""
                SELECT 1 FROM Indicadores_Registro 
                WHERE Id_indicador = %s AND Numero_de_registro = %s
            """, (id_indicador, registro_id))
            
            if cursor.fetchone():
                messagebox.showinfo("Información", "Este indicador ya está asociado al registro")
                return
            
            # Asociar indicador al registro
            cursor.execute("""
                INSERT INTO Indicadores_Registro (Id_indicador, Numero_de_registro)
                VALUES (%s, %s)
            """, (id_indicador, registro_id))
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            messagebox.showinfo("Éxito", f"Indicador '{indicador}' asociado al registro")
            
            # Actualizar interfaces
            cargar_indicadores_competencia(tree_competencias.item(tree_competencias.selection()[0], "values")[0])
            cargar_indicadores_asociados()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al asociar indicador: {str(e)}")
    
    def desasociar_indicador():
        seleccion = tree_indicadores_asoc.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un indicador")
            return
        
        item = seleccion[0]
        id_indicador = tree_indicadores_asoc.item(item, "values")[0]
        indicador = tree_indicadores_asoc.item(item, "values")[1]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de desasociar el indicador '{indicador}'?"):
            try:
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                
                # Eliminar asociación
                cursor.execute("""
                    DELETE FROM Indicadores_Registro 
                    WHERE Id_indicador = %s AND Numero_de_registro = %s
                """, (id_indicador, registro_id))
                
                conexion.commit()
                cursor.close()
                conexion.close()
                
                messagebox.showinfo("Éxito", f"Indicador '{indicador}' desasociado del registro")
                
                # Actualizar interfaces
                if tree_competencias.selection():
                    id_competencia = tree_competencias.item(tree_competencias.selection()[0], "values")[0]
                    cargar_indicadores_competencia(id_competencia)
                cargar_indicadores_asociados()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al desasociar indicador: {str(e)}")
    
    # ===== BOTONES =====
    frame_botones = tk.Frame(frame_disponibles, bg="#E3F2FD")
    frame_botones.pack(pady=10)
    
    btn_asociar = tk.Button(
        frame_botones,
        text="➕ Asociar Indicador Seleccionado",
        font=("Arial", 10, "bold"),
        bg="#388E3C",
        fg="white",
        width=25,
        command=asociar_indicador
    )
    btn_asociar.pack(pady=5)
    
    frame_botones_asoc = tk.Frame(frame_asociados, bg="#E3F2FD")
    frame_botones_asoc.pack(pady=10)
    
    btn_desasociar = tk.Button(
        frame_botones_asoc,
        text="➖ Desasociar Indicador Seleccionado",
        font=("Arial", 10, "bold"),
        bg="#D32F2F",
        fg="white",
        width=25,
        command=desasociar_indicador
    )
    btn_desasociar.pack(pady=5)
    
    # Botón cerrar
    frame_cerrar = tk.Frame(main_frame, bg="#E3F2FD")
    frame_cerrar.pack(pady=10)
    
    btn_cerrar = tk.Button(
        frame_cerrar,
        text="Cerrar",
        font=("Arial", 10),
        bg="#757575",
        fg="white",
        width=15,
        command=ventana.destroy
    )
    btn_cerrar.pack()
    
    # Conectar eventos
    tree_competencias.bind("<<TreeviewSelect>>", on_seleccion_competencia)
    
    # Cargar datos iniciales
    cargar_competencias_disponibles()
    cargar_indicadores_asociados()
    
    ventana.after(100, lambda: centrar_ventana(ventana, 1000, 700))
    
    return ventana