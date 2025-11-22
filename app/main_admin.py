import tkinter as tk
from tkinter import messagebox
from app.crud_usuarios import ventana_crud_usuarios
from app.crud_docentes import ventana_crud_docentes
from estudiantes.gestion_estudiantes import ventana_gestion_estudiantes 
from registro.gestion_registros import ventana_gestion_registros  # NUEVA IMPORTACIÓN

def iniciar_admin():
    ventana = tk.Tk()
    ventana.title("Panel del Administrador")
    ventana.geometry("500x600")  # Aumenté el alto para el nuevo botón
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)
    ventana.eval('tk::PlaceWindow . center')

    titulo = tk.Label(
        ventana,
        text="Panel de Administración",
        font=("Arial", 18, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=25)

    # ------- BOTONES -------
    btn_docentes = tk.Button(
        ventana,
        text="Gestionar Docentes",
        font=("Arial", 13, "bold"),
        bg="#1976D2",
        fg="white",
        padx=20,
        pady=12,
        width=22,
        command=lambda: ventana_crud_docentes(ventana)
    )
    btn_docentes.pack(pady=10)

    btn_usuarios = tk.Button(
        ventana,
        text="Gestionar Usuarios",
        font=("Arial", 13, "bold"),
        bg="#1565C0",
        fg="white",
        padx=20,
        pady=12,
        width=22,
        command=lambda: ventana_crud_usuarios(ventana)
    )
    btn_usuarios.pack(pady=10)

    btn_estudiantes = tk.Button(
        ventana,
        text="Gestionar Estudiantes",
        font=("Arial", 13, "bold"),
        bg="#2E7D32",
        fg="white",
        padx=20,
        pady=12,
        width=22,
        command=lambda: ventana_gestion_estudiantes(ventana)
    )
    btn_estudiantes.pack(pady=10)

    # NUEVO BOTÓN PARA GESTIÓN DE REGISTROS
    btn_registros = tk.Button(
        ventana,
        text="Gestionar Registros",
        font=("Arial", 13, "bold"),
        bg="#7B1FA2",  # Color morado para distinguir
        fg="white",
        padx=20,
        pady=12,
        width=22,
        command=lambda: ventana_gestion_registros(ventana)
    )
    btn_registros.pack(pady=10)

    # ------- CERRAR SESIÓN -------
    def cerrar_sesion():
        if messagebox.askokcancel("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            ventana.destroy()
            from app.login import iniciar_login
            iniciar_login()

    btn_logout = tk.Button(
        ventana,
        text="Cerrar Sesión",
        font=("Arial", 12, "bold"),
        bg="#EF5350",
        fg="white",
        padx=20,
        pady=10,
        width=18,
        command=cerrar_sesion
    )
    btn_logout.pack(pady=30)

    def on_closing():
        cerrar_sesion()

    ventana.protocol("WM_DELETE_WINDOW", on_closing)
    ventana.mainloop()