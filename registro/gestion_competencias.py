import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_gestion_competencias(ventana_padre=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Gestion de Competencias e Indicadores")
    ventana.geometry("900x700")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(True, True)
    
    # Hacer la ventana modal
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Frame principal
    main_frame = tk.Frame(ventana, bg="#E3F2FD")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Titulo
    titulo = tk.Label(
        main_frame,
        text="Gestion de Competencias e Indicadores",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Frame principal con pestañas
    notebook = ttk.Notebook(main_frame)
    notebook.pack(pady=10, fill="both", expand=True)
    
    # Pestaña de Competencias
    frame_competencias = tk.Frame(notebook, bg="#E3F2FD")
    notebook.add(frame_competencias, text="Competencias")
    
    # Pestaña de Indicadores
    frame_indicadores = tk.Frame(notebook, bg="#E3F2FD")
    notebook.add(frame_indicadores, text="Indicadores")
    
    # ===== CONTENIDO PESTAÑA COMPETENCIAS =====
    def cargar_competencias():
        try:
            # Limpiar treeview
            for item in tree_competencias.get_children():
                tree_competencias.delete(item)
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT c.Id_competencia, c.Competencia, 
                       COUNT(i.Id_indicador) as total_indicadores
                FROM Competencias c
                LEFT JOIN Indicadores i ON c.Id_competencia = i.Id_competencia
                GROUP BY c.Id_competencia, c.Competencia
                ORDER BY c.Id_competencia
            """)
            competencias = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            for id_comp, competencia, total_indicadores in competencias:
                tree_competencias.insert("", "end", values=(id_comp, competencia, total_indicadores))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar competencias: {str(e)}")
    
    # Treeview para competencias
    frame_tree_comp = tk.Frame(frame_competencias)
    frame_tree_comp.pack(pady=10, fill="both", expand=True)
    
    scroll_y = tk.Scrollbar(frame_tree_comp)
    scroll_y.pack(side="right", fill="y")
    
    tree_competencias = ttk.Treeview(
        frame_tree_comp,
        columns=("ID", "Competencia", "Indicadores"),
        yscrollcommand=scroll_y.set,
        show="headings",
        height=10
    )
    
    scroll_y.config(command=tree_competencias.yview)
    
    tree_competencias.heading("ID", text="ID")
    tree_competencias.heading("Competencia", text="Competencia")
    tree_competencias.heading("Indicadores", text="Total Indicadores")
    tree_competencias.column("ID", width=80)
    tree_competencias.column("Competencia", width=450)
    tree_competencias.column("Indicadores", width=120)
    
    tree_competencias.pack(fill="both", expand=True)
    
    # Frame para agregar competencia
    frame_add_comp = tk.Frame(frame_competencias, bg="#E3F2FD")
    frame_add_comp.pack(pady=10, fill="x")
    
    tk.Label(frame_add_comp, text="Nueva Competencia:", bg="#E3F2FD", font=("Arial", 10)).pack(side="left", padx=5)
    entry_nueva_comp = tk.Entry(frame_add_comp, font=("Arial", 10), width=50)
    entry_nueva_comp.pack(side="left", padx=5)
    
    def agregar_competencia():
        competencia = entry_nueva_comp.get().strip()
        if not competencia:
            messagebox.showwarning("Campo vacio", "Por favor ingrese la competencia")
            return
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO Competencias (Competencia) VALUES (%s)", (competencia,))
            conexion.commit()
            cursor.close()
            conexion.close()
            
            messagebox.showinfo("Exito", "Competencia agregada correctamente")
            entry_nueva_comp.delete(0, tk.END)
            cargar_competencias()
            cargar_competencias_combo()  # Actualizar combo también
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar competencia: {str(e)}")
    
    btn_add_comp = tk.Button(
        frame_add_comp,
        text="Agregar",
        font=("Arial", 9),
        bg="#388E3C",
        fg="white",
        command=agregar_competencia
    )
    btn_add_comp.pack(side="left", padx=5)
    
    # ===== CONTENIDO PESTAÑA INDICADORES =====
    def cargar_competencias_combo():
        """Cargar competencias para el combobox"""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT Id_competencia, Competencia FROM Competencias ORDER BY Competencia")
            competencias = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Actualizar combobox
            combo_competencias['values'] = [f"{id_comp} - {comp}" for id_comp, comp in competencias]
            if competencias:
                combo_competencias.set(combo_competencias['values'][0])
            else:
                combo_competencias.set("")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar competencias: {str(e)}")
    
    def cargar_indicadores():
        try:
            # Limpiar treeview
            for item in tree_indicadores.get_children():
                tree_indicadores.delete(item)
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT i.Id_indicador, i.Indicadores_competencias, 
                       c.Id_competencia, c.Competencia 
                FROM Indicadores i
                JOIN Competencias c ON i.Id_competencia = c.Id_competencia
                ORDER BY c.Competencia, i.Id_indicador
            """)
            indicadores = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            for id_ind, indicador, id_comp, competencia in indicadores:
                tree_indicadores.insert("", "end", values=(id_ind, indicador, f"{id_comp} - {competencia}"))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar indicadores: {str(e)}")
    
    # Treeview para indicadores
    frame_tree_ind = tk.Frame(frame_indicadores)
    frame_tree_ind.pack(pady=10, fill="both", expand=True)
    
    scroll_y_ind = tk.Scrollbar(frame_tree_ind)
    scroll_y_ind.pack(side="right", fill="y")
    
    tree_indicadores = ttk.Treeview(
        frame_tree_ind,
        columns=("ID", "Indicador", "Competencia"),
        yscrollcommand=scroll_y_ind.set,
        show="headings",
        height=10
    )
    
    scroll_y_ind.config(command=tree_indicadores.yview)
    
    tree_indicadores.heading("ID", text="ID")
    tree_indicadores.heading("Indicador", text="Indicador")
    tree_indicadores.heading("Competencia", text="Competencia")
    tree_indicadores.column("ID", width=80)
    tree_indicadores.column("Indicador", width=400)
    tree_indicadores.column("Competencia", width=250)
    
    tree_indicadores.pack(fill="both", expand=True)
    
    # Frame para agregar indicador
    frame_add_ind = tk.Frame(frame_indicadores, bg="#E3F2FD")
    frame_add_ind.pack(pady=10, fill="x")
    
    # Competencia para el indicador
    tk.Label(frame_add_ind, text="Competencia:", bg="#E3F2FD", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
    combo_competencias = ttk.Combobox(frame_add_ind, font=("Arial", 10), width=40, state="readonly")
    combo_competencias.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    # Indicador
    tk.Label(frame_add_ind, text="Indicador:", bg="#E3F2FD", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
    entry_nuevo_ind = tk.Entry(frame_add_ind, font=("Arial", 10), width=50)
    entry_nuevo_ind.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    def agregar_indicador():
        indicador = entry_nuevo_ind.get().strip()
        competencia_seleccionada = combo_competencias.get()
        
        if not indicador:
            messagebox.showwarning("Campo vacio", "Por favor ingrese el indicador")
            return
        
        if not competencia_seleccionada:
            messagebox.showwarning("Seleccion requerida", "Por favor seleccione una competencia")
            return
        
        # Extraer ID de la competencia del texto seleccionado
        try:
            id_competencia = int(competencia_seleccionada.split(" - ")[0])
        except:
            messagebox.showerror("Error", "Formato de competencia invalido")
            return
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Verificar si ya existe el mismo indicador para la misma competencia
            cursor.execute("""
                SELECT Id_indicador FROM Indicadores 
                WHERE Indicadores_competencias = %s AND Id_competencia = %s
            """, (indicador, id_competencia))
            
            if cursor.fetchone():
                messagebox.showwarning("Duplicado", "Este indicador ya existe para la competencia seleccionada")
                return
            
            # Insertar nuevo indicador
            cursor.execute("""
                INSERT INTO Indicadores (Indicadores_competencias, Id_competencia) 
                VALUES (%s, %s)
            """, (indicador, id_competencia))
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            messagebox.showinfo("Exito", "Indicador agregado correctamente")
            entry_nuevo_ind.delete(0, tk.END)
            cargar_indicadores()
            cargar_competencias()  # Actualizar también la pestaña de competencias
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar indicador: {str(e)}")
    
    btn_add_ind = tk.Button(
        frame_add_ind,
        text="Agregar Indicador",
        font=("Arial", 9),
        bg="#388E3C",
        fg="white",
        command=agregar_indicador
    )
    btn_add_ind.grid(row=1, column=2, padx=5, pady=5)
    
    # Boton Cerrar en un frame separado
    frame_botones = tk.Frame(main_frame, bg="#E3F2FD")
    frame_botones.pack(pady=10)
    
    btn_cerrar = tk.Button(
        frame_botones,
        text="Cerrar",
        font=("Arial", 10),
        bg="#757575",
        fg="white",
        width=15,
        command=ventana.destroy
    )
    btn_cerrar.pack()
    
    # Cargar datos iniciales
    cargar_competencias()
    cargar_competencias_combo()
    cargar_indicadores()

    ventana.after(100, lambda: centrar_ventana(ventana, 900, 700))
    
    return ventana