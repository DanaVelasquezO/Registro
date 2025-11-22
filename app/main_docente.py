import tkinter as tk
from tkinter import messagebox
from app.login import iniciar_login


def iniciar_docente(codigo_docente):
    ventana = tk.Toplevel()
    ventana.title("Panel del Docente")
    ventana.geometry("500x400")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)

    # ---------------- TÍTULO ----------------
    titulo = tk.Label(
        ventana,
        text=f"Bienvenido Docente (ID: {codigo_docente})",
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=20)

    # ---------------- BOTONES PRINCIPALES ----------------
    frame = tk.Frame(ventana, bg="#E3F2FD")
    frame.pack(pady=10)

    btn_registros = tk.Button(
        frame,
        text="Ver Registros Auxiliares",
        width=25,
        font=("Arial", 12),
        bg="#1565C0",
        fg="white",
        padx=10,
        pady=10,
        command=lambda: messagebox.showinfo(
            "Registros Auxiliares",
            "Este módulo será añadido después."
        )
    )
    btn_registros.grid(row=0, column=0, padx=10, pady=10)

    btn_notas = tk.Button(
        frame,
        text="Ingresar Notas",
        width=25,
        font=("Arial", 12),
        bg="#1976D2",
        fg="white",
        padx=10,
        pady=10,
        command=lambda: messagebox.showinfo(
            "Notas",
            "Este módulo será añadido después."
        )
    )
    btn_notas.grid(row=1, column=0, padx=10, pady=10)

    # ---------------- CERRAR SESIÓN ----------------

    def cerrar_sesion():
        ventana.destroy()
        iniciar_login()

    btn_salir = tk.Button(
        ventana,
        text="Cerrar Sesión",
        font=("Arial", 12, "bold"),
        bg="#EF5350",
        fg="white",
        width=15,
        pady=10,
        command=cerrar_sesion
    )
    btn_salir.pack(pady=25)

    ventana.mainloop()
