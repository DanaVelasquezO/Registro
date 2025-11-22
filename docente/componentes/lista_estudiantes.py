import tkinter as tk
from tkinter import ttk
from db.conexion import obtener_conexion

def crear_frame_lista_estudiantes(parent, callback_seleccion_estudiante):
    """
    Crea el frame de lista de estudiantes
    """
    frame_lista = tk.LabelFrame(parent, text="Lista de Estudiantes", 
                              font=("Arial", 11, "bold"), bg="#E3F2FD", fg="#0D47A1")
    
    # Scrollbars
    frame_scroll = tk.Frame(frame_lista, bg="#E3F2FD")
    frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)
    
    scroll_y = tk.Scrollbar(frame_scroll)
    scroll_y.pack(side="right", fill="y")
    
    scroll_x = tk.Scrollbar(frame_scroll, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")
    
    # Treeview para estudiantes
    treeview_estudiantes = ttk.Treeview(
        frame_scroll,
        columns=("Código", "Nombre"),
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
        selectmode="browse",
        show="headings",
        height=12
    )
    
    scroll_y.config(command=treeview_estudiantes.yview)
    scroll_x.config(command=treeview_estudiantes.xview)
    
    # Configurar columnas
    treeview_estudiantes.heading("Código", text="Código Estudiante")
    treeview_estudiantes.heading("Nombre", text="Nombre del Estudiante")
    
    treeview_estudiantes.column("Código", width=120, anchor="center")
    treeview_estudiantes.column("Nombre", width=400, anchor="w")
    
    treeview_estudiantes.pack(fill="both", expand=True)
    
    # Función para cargar estudiantes
    def cargar_estudiantes(numero_registro):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            cursor.execute("""
                SELECT e.Codigo_estudiante, e.Nombre_estudiante
                FROM Estudiante e
                JOIN Estudiante_Registro er ON e.Codigo_estudiante = er.Codigo_estudiante
                WHERE er.Numero_de_registro = %s
                ORDER BY e.Nombre_estudiante
            """, (numero_registro,))
            
            estudiantes = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Limpiar tabla
            for item in treeview_estudiantes.get_children():
                treeview_estudiantes.delete(item)
            
            # Insertar estudiantes
            for estudiante in estudiantes:
                codigo, nombre = estudiante
                treeview_estudiantes.insert("", "end", values=(codigo, nombre))
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al cargar estudiantes: {str(e)}")
    
    # Conectar evento de selección - CORREGIDO
    def on_seleccion(event):
        seleccion = treeview_estudiantes.selection()
        if seleccion:
            callback_seleccion_estudiante(treeview_estudiantes)
    
    treeview_estudiantes.bind("<<TreeviewSelect>>", on_seleccion)
    
    return {
        'frame': frame_lista,
        'treeview': treeview_estudiantes,
        'cargar_estudiantes': cargar_estudiantes
    }