import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion
from estudiantes.agregar_estudiante import ventana_agregar_estudiante
from estudiantes.editar_estudiante import ventana_editar_estudiante
from estudiantes.eliminar_estudiante import ventana_eliminar_estudiante
from estudiantes.cargar_excel import ventana_cargar_excel
from registro.asignar_estudiante_registro import ventana_asignar_estudiante_registro  # NUEVA IMPORTACIÓN

def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_gestion_estudiantes(ventana_padre=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Gestión de Estudiantes")
    ventana.geometry("1000x600")  # Aumenté el ancho para más botones
    ventana.config(bg="#E3F2FD")
    ventana.resizable(True, True)
    
    # Comportamiento modal
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Centrar ventana
    centrar_ventana(ventana)
    
    # Título
    titulo = tk.Label(
        ventana,
        text="Gestión de Estudiantes",
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=10)
    
    # Frame de controles
    frame_controles = tk.Frame(ventana, bg="#E3F2FD")
    frame_controles.pack(pady=10, padx=20, fill="x")
    
    # Búsqueda
    tk.Label(frame_controles, text="Buscar:", bg="#E3F2FD", font=("Arial", 10)).pack(side="left", padx=5)
    entry_busqueda = tk.Entry(frame_controles, font=("Arial", 10), width=30)
    entry_busqueda.pack(side="left", padx=5)
    
    # Botones de acción
    frame_botones = tk.Frame(frame_controles, bg="#E3F2FD")
    frame_botones.pack(side="right")
    
    # PRIMERO DEFINIR LAS FUNCIONES QUE USARÁN LOS BOTONES
    def actualizar_tabla():
        try:
            # Limpiar tabla
            for item in treeview.get_children():
                treeview.delete(item)
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener estudiantes con conteo de registros
            cursor.execute("""
                SELECT e.Codigo_estudiante, e.Nombre_estudiante, 
                       COUNT(er.Numero_de_registro) as total_registros
                FROM Estudiante e
                LEFT JOIN Estudiante_Registro er ON e.Codigo_estudiante = er.Codigo_estudiante
                GROUP BY e.Codigo_estudiante, e.Nombre_estudiante
                ORDER BY e.Nombre_estudiante
            """)
            
            estudiantes = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Llenar tabla
            for estudiante in estudiantes:
                treeview.insert("", "end", values=estudiante)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estudiantes: {str(e)}")
    
    def buscar_estudiantes(event=None):
        busqueda = entry_busqueda.get().strip()
        
        try:
            # Limpiar tabla
            for item in treeview.get_children():
                treeview.delete(item)
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            if busqueda:
                cursor.execute("""
                    SELECT e.Codigo_estudiante, e.Nombre_estudiante, 
                           COUNT(er.Numero_de_registro) as total_registros
                    FROM Estudiante e
                    LEFT JOIN Estudiante_Registro er ON e.Codigo_estudiante = er.Codigo_estudiante
                    WHERE e.Nombre_estudiante LIKE %s OR e.Codigo_estudiante LIKE %s
                    GROUP BY e.Codigo_estudiante, e.Nombre_estudiante
                    ORDER BY e.Nombre_estudiante
                """, (f"%{busqueda}%", f"%{busqueda}%"))
            else:
                cursor.execute("""
                    SELECT e.Codigo_estudiante, e.Nombre_estudiante, 
                           COUNT(er.Numero_de_registro) as total_registros
                    FROM Estudiante e
                    LEFT JOIN Estudiante_Registro er ON e.Codigo_estudiante = er.Codigo_estudiante
                    GROUP BY e.Codigo_estudiante, e.Nombre_estudiante
                    ORDER BY e.Nombre_estudiante
                """)
            
            estudiantes = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            for estudiante in estudiantes:
                treeview.insert("", "end", values=estudiante)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar estudiantes: {str(e)}")
    
    def editar_seleccionado():
        seleccion = treeview.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un estudiante para editar")
            return
        
        item = treeview.item(seleccion[0])
        valores = item["values"]
        if valores:
            datos_estudiante = (valores[0], valores[1])
            ventana_editar_estudiante(datos_estudiante, ventana, actualizar_tabla)
    
    def eliminar_seleccionado():
        seleccion = treeview.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un estudiante para eliminar")
            return
        
        item = treeview.item(seleccion[0])
        valores = item["values"]
        if valores:
            datos_estudiante = (valores[0], valores[1])
            ventana_eliminar_estudiante(datos_estudiante, ventana, actualizar_tabla)
    
    def asignar_a_registro():
        seleccion = treeview.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un estudiante para asignar a registro")
            return
        
        item = treeview.item(seleccion[0])
        valores = item["values"]
        if valores:
            codigo_estudiante = valores[0]
            nombre_estudiante = valores[1]
            ventana_asignar_estudiante_registro(codigo_estudiante, nombre_estudiante, ventana, actualizar_tabla)
    
    # AHORA SÍ CREAR LOS BOTONES (después de definir las funciones)
    btn_agregar = tk.Button(
        frame_botones,
        text="Agregar",
        font=("Arial", 9, "bold"),
        bg="#388E3C",
        fg="white",
        width=10,
        command=lambda: ventana_agregar_estudiante(ventana, actualizar_tabla)
    )
    btn_agregar.pack(side="left", padx=2)
    
    btn_excel = tk.Button(
        frame_botones,
        text="Excel",
        font=("Arial", 9, "bold"),
        bg="#7B1FA2",
        fg="white",
        width=10,
        command=lambda: ventana_cargar_excel(ventana, actualizar_tabla)
    )
    btn_excel.pack(side="left", padx=2)
    
    btn_editar = tk.Button(
        frame_botones,
        text="Editar",
        font=("Arial", 9, "bold"),
        bg="#F57C00",
        fg="white",
        width=10,
        command=editar_seleccionado
    )
    btn_editar.pack(side="left", padx=2)
    
    btn_asignar = tk.Button(
        frame_botones,
        text="Asignar a Registro",
        font=("Arial", 9, "bold"),
        bg="#1976D2",
        fg="white",
        width=15,
        command=asignar_a_registro
    )
    btn_asignar.pack(side="left", padx=2)
    
    btn_eliminar = tk.Button(
        frame_botones,
        text="Eliminar",
        font=("Arial", 9, "bold"),
        bg="#D32F2F",
        fg="white",
        width=10,
        command=eliminar_seleccionado
    )
    btn_eliminar.pack(side="left", padx=2)
    
    # Tabla de estudiantes
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Scrollbars
    scroll_y = tk.Scrollbar(frame_tabla)
    scroll_y.pack(side="right", fill="y")
    
    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")
    
    # Treeview
    treeview = ttk.Treeview(
        frame_tabla,
        columns=("Código", "Nombre", "Registros"),
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
        selectmode="browse",
        show="headings"
    )
    
    scroll_y.config(command=treeview.yview)
    scroll_x.config(command=treeview.xview)
    
    # Configurar columnas
    treeview.heading("Código", text="Código Estudiante")
    treeview.heading("Nombre", text="Nombre del Estudiante")
    treeview.heading("Registros", text="Registros Asociados")
    
    treeview.column("Código", width=120, anchor="center")
    treeview.column("Nombre", width=400)
    treeview.column("Registros", width=120, anchor="center")
    
    treeview.pack(fill="both", expand=True)
    
    # Conectar el evento de búsqueda
    entry_busqueda.bind("<KeyRelease>", buscar_estudiantes)
    
    # Cargar datos iniciales
    actualizar_tabla()
    
    return ventana