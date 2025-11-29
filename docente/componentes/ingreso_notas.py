import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion
from docente.componentes.ing_nota_estudiante import ventana_ingreso_nota_estudiante

def crear_frame_ingreso_notas(parent):
    """
    Crea el frame de ingreso de notas (versión simplificada que abre ventanas separadas)
    """
    frame_ingreso = tk.LabelFrame(parent, text="Ingreso de Notas", 
                                font=("Arial", 11, "bold"), bg="#E3F2FD", fg="#0D47A1")
    frame_ingreso.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Mensaje inicial
    mensaje_inicial = tk.Label(
        frame_ingreso,
        text="Seleccione un estudiante de la lista para ingresar sus notas",
        font=("Arial", 11),
        bg="#E3F2FD",
        fg="#666666"
    )
    mensaje_inicial.pack(pady=50)
    
    def mostrar_estudiante(estudiante, numero_registro):
        """
        Abre una ventana separada para ingresar notas del estudiante seleccionado
        """
        try:
            # Abrir ventana de ingreso de notas para el estudiante específico
            ventana_ingreso_nota_estudiante(estudiante, numero_registro, parent)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el ingreso de notas: {str(e)}")
    
    def guardar_notas():
        """Función placeholder - no se usa en esta versión"""
        messagebox.showinfo("Información", "Use la ventana de ingreso de notas del estudiante")
    
    def limpiar_notas():
        """Función placeholder - no se usa en esta versión"""
        messagebox.showinfo("Información", "Use la ventana de ingreso de notas del estudiante")
    
    # Retornar el frame y las funciones
    return {
        'frame': frame_ingreso,
        'mostrar_estudiante': mostrar_estudiante,
        'guardar_notas': guardar_notas,
        'limpiar_notas': limpiar_notas
    }