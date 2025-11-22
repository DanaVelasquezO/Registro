import tkinter as tk
from tkinter import ttk, messagebox
from registro.componentes.filtros_busqueda import crear_frame_filtros
from registro.componentes.tabla_registros import crear_tabla_registros
from registro.componentes.botones_accion import crear_botones_accion

def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_ver_registros(ventana_padre=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Gestión de Registros")
    ventana.geometry("1200x700")
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
        text="Gestión de Registros Académicos",
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=10)
    
    # Frame de tabla
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Crear tabla (SOLO UN PARÁMETRO AHORA)
    datos_tabla = crear_tabla_registros(frame_tabla)
    treeview = datos_tabla['treeview']
    actualizar_tabla_func = datos_tabla['actualizar_tabla']
    
    # Frame de filtros (pasar la función de actualización)
    frame_filtros = crear_frame_filtros(ventana, actualizar_tabla_func)
    frame_filtros.pack(pady=10, padx=20, fill="x")
    
    # Frame de botones de acción
    frame_botones_accion = crear_botones_accion(ventana, actualizar_tabla_func, treeview)
    frame_botones_accion.pack(pady=10, padx=20, fill="x")
    
    # Empaquetar el frame de la tabla
    datos_tabla['frame'].pack(fill="both", expand=True)
    
    # Cargar datos iniciales
    actualizar_tabla_func()
    
    return ventana