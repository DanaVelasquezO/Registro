import tkinter as tk
from tkinter import ttk
from estudiantes.gestion_estudiantes import ventana_agregar_estudiante, ventana_eliminar_estudiante
from registro.crear_registro import ventana_crear_registro
from registro.editar_registro import ventana_editar_registro

def crear_botones_accion(parent, actualizar_tabla, treeview):
    """
    Crea los botones de acción para la gestión de registros
    """
    frame_botones = tk.Frame(parent, bg="#E3F2FD")
    frame_botones.pack(pady=10, padx=20, fill="x")
    
    # Frame para los botones (izquierda)
    frame_izquierda = tk.Frame(frame_botones, bg="#E3F2FD")
    frame_izquierda.pack(side="left")
    
    # Frame para los botones (derecha)
    frame_derecha = tk.Frame(frame_botones, bg="#E3F2FD")
    frame_derecha.pack(side="right")
    
    # Función para obtener el registro seleccionado
    def obtener_registro_seleccionado():
        seleccion = treeview.selection()
        if not seleccion:
            return None
        item = treeview.item(seleccion[0])
        valores = item["values"]
        if valores:
            return valores[0]
        return None
    
    # Botón Crear Registro
    btn_crear = tk.Button(
        frame_izquierda,
        text="Crear Registro",
        font=("Arial", 9, "bold"),
        bg="#388E3C",
        fg="white",
        width=15,
        command=lambda: ventana_crear_registro(parent, actualizar_tabla)
    )
    btn_crear.pack(side="left", padx=2)
    
    # Botón Gestionar Estudiantes
    btn_estudiantes = tk.Button(
        frame_izquierda,
        text="Gestionar Estudiantes",
        font=("Arial", 9, "bold"),
        bg="#7B1FA2",
        fg="white",
        width=18,
        command=lambda: ventana_agregar_estudiante(parent, actualizar_tabla)
    )
    btn_estudiantes.pack(side="left", padx=2)
    
    # Botón Editar
    # Botón Editar
    btn_editar = tk.Button(
        frame_derecha,
        text="Editar",
        font=("Arial", 9, "bold"),
        bg="#F57C00",
        fg="white",
        width=10,
        command=lambda: ventana_editar_registro(obtener_registro_seleccionado(), parent, actualizar_tabla)
    )
    
    # Botón Eliminar
    btn_eliminar = tk.Button(
        frame_derecha,
        text="Eliminar",
        font=("Arial", 9, "bold"),
        bg="#D32F2F",
        fg="white",
        width=10,
        command=lambda: ventana_eliminar_estudiante(parent, obtener_registro_seleccionado(), actualizar_tabla)
    )
    btn_eliminar.pack(side="left", padx=2)
    
    return frame_botones