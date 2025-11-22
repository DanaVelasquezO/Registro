import tkinter as tk
from tkinter import messagebox
from app.crud_usuarios import ventana_crud_usuarios
from app.login import iniciar_login


def comenzar_admin():
    ventana = tk.Toplevel()
    ventana.title("Panel del Administrador")
    ventana.geometry("500x470")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)

    # ---------------- TÍTULO ----------------
    titulo = tk.Label(
        ventana,
        text="Panel de Administración",
        font=("Arial", 18, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=25)

    # ---------------- BOTONES PRINCIPALES ----------------

    btn_docentes = tk.Button(
        ventana,
        text="Gestionar Docentes",
        font=("Arial", 13, "bold"),
        bg="#1976D2",
        fg="white",
        padx=20,
        pady=12,
        width=22,
        command=lambda: messagebox.showinfo(
            "Gestión de Docentes",
            "Este módulo será añadido después."
        )
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
        command=ventana_crud_usuarios
    )
    btn_usuarios.pack(pady=10)

    btn_registros = tk.Button(
        ventana,
        text="Ver Registros Académicos",
        font=("Arial", 13, "bold"),
        bg="#0D47A1",
        fg="white",
        padx=20,
        pady=12,
        width=22,
        command=lambda: messagebox.showinfo(
            "Registros Auxiliares",
            "Este módulo será añadido después."
        )
    )
    btn_registros.pack(pady=10)

    # ---------------- CERRAR SESIÓN ----------------

    def cerrar_sesion():
        ventana.destroy()   # Cierra solo panel admin
        iniciar_login()     # Vuelve al login

    btn_logout = tk.Button(
        ventana,
        text="Cerrar Sesión",
        font=("Arial", 12, "bold"),
        bg="#EF5350",
        fg="white",
        width=18,
        padx=20,
        pady=10,
        command=cerrar_sesion
    )
    btn_logout.pack(pady=30)

    ventana.mainloop()
