import tkinter as tk
from docente.componentes import (
    crear_frame_seleccion_registro,
    crear_frame_lista_estudiantes,
    crear_frame_ingreso_notas
)
# Añade esta importación
from docente.componentes.ing_nota_estudiante import ventana_ingreso_nota_estudiante

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_ingresar_notas(codigo_docente, ventana_padre=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Ingresar Notas")
    ventana.geometry("1000x700")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(True, True)
    
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    centrar_ventana(ventana, 1000, 700)
    
    # Título
    titulo = tk.Label(
        ventana,
        text="Sistema de Ingreso de Notas",
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Frame principal
    frame_principal = tk.Frame(ventana, bg="#E3F2FD")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Variables
    numero_registro_actual = None
    frame_lista_estudiantes_obj = None
    
    # Crear frame de selección de registro
    frame_seleccion = crear_frame_seleccion_registro(
        frame_principal, 
        codigo_docente,
        lambda numero_registro: cargar_estudiantes(numero_registro)
    )
    
    # Frame para contener lista de estudiantes
    frame_contenedor = tk.Frame(frame_principal, bg="#E3F2FD")
    frame_contenedor.pack(fill="both", expand=True, pady=10)
    
    # Función para cargar estudiantes
    def cargar_estudiantes(numero_registro):
        nonlocal numero_registro_actual, frame_lista_estudiantes_obj
        
        numero_registro_actual = numero_registro
        
        # Limpiar frame anterior
        if frame_lista_estudiantes_obj:
            frame_lista_estudiantes_obj['frame'].pack_forget()
        
        # Crear frame de lista de estudiantes
        frame_lista_estudiantes_obj = crear_frame_lista_estudiantes(
            frame_contenedor,
            lambda treeview: seleccionar_estudiante(treeview, numero_registro)
        )
        frame_lista_estudiantes_obj['frame'].pack(fill="both", expand=True)
        frame_lista_estudiantes_obj['cargar_estudiantes'](numero_registro)
    
    # Función para seleccionar estudiante
    def seleccionar_estudiante(treeview, numero_registro):
        seleccion = treeview.selection()
        if not seleccion:
            return
        
        item = treeview.item(seleccion[0])
        valores = item["values"]
        
        if valores and len(valores) >= 2:
            estudiante = {
                'codigo': valores[0],
                'nombre': valores[1]
            }
            
            # Abrir ventana separada para ingresar notas
            ventana_ingreso_nota_estudiante(estudiante, numero_registro, ventana)
    
    return ventana