import tkinter as tk
from tkinter import messagebox
from docente.ver_registros_docente import ver_registros_docente
from docente import ventana_ingresar_notas
from docente.componentes.promedio_notas import ventana_promedio_notas  
from db.conexion import obtener_conexion

def obtener_nombre_docente(codigo_docente):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT Nombre_docente FROM Docente WHERE Codigo_docente = %s", (codigo_docente,))
        resultado = cursor.fetchone()
        nombre_docente = resultado[0] if resultado else f"Docente (ID: {codigo_docente})"
        cursor.close()
        conexion.close()
        return nombre_docente
    except Exception as e:
        print(f"Error al obtener nombre del docente: {e}")
        return f"Docente (ID: {codigo_docente})"

def iniciar_docente(codigo_docente):
    nombre_docente = obtener_nombre_docente(codigo_docente)
    # Crear ventana principal para docente
    ventana = tk.Tk()
    ventana.title("Panel del Docente")
    ventana.geometry("500x450")  # Aumentado para el nuevo botón
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)
    ventana.eval('tk::PlaceWindow . center')  # Centrar ventana

    titulo = tk.Label(
        ventana,
        text=f"Bienvenido Docente: {nombre_docente}",
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=20)

    frame = tk.Frame(ventana, bg="#E3F2FD")
    frame.pack(pady=10)

    btn_registros = tk.Button(
        frame,
        text="Ver mis Registros Auxiliares",
        width=25,
        font=("Arial", 12),
        bg="#1565C0",
        fg="white",
        command=lambda: ver_registros_docente(codigo_docente, ventana)
    )
    btn_registros.grid(row=0, column=0, padx=10, pady=10)

    btn_notas = tk.Button(
        frame,
        text="Ingresar Notas",
        width=25,
        font=("Arial", 12),
        bg="#1976D2",
        fg="white",
        command=lambda: ventana_ingresar_notas(codigo_docente, ventana)
    )
    btn_notas.grid(row=1, column=0, padx=10, pady=10)

    # NUEVO BOTÓN PARA PROMEDIOS
    btn_promedios = tk.Button(
        frame,
        text="Calcular Promedios",
        width=25,
        font=("Arial", 12),
        bg="#388E3C",
        fg="white",
        command=lambda: ventana_promedio_notas(codigo_docente, ventana)
    )
    btn_promedios.grid(row=2, column=0, padx=10, pady=10)

    def cerrar_sesion():
        if messagebox.askokcancel("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            ventana.destroy()
            # Volver al login
            from app.login import iniciar_login
            iniciar_login()

    btn_salir = tk.Button(
        ventana,
        text="Cerrar Sesión",
        font=("Arial", 12, "bold"),
        bg="#EF5350",
        fg="white",
        width=15,
        command=cerrar_sesion
    )
    btn_salir.pack(pady=20)

    # Manejar cierre de ventana
    def on_closing():
        cerrar_sesion()

    ventana.protocol("WM_DELETE_WINDOW", on_closing)
    
    ventana.mainloop()