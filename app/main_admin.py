import tkinter as tk
from tkinter import messagebox

def iniciar_admin():
    ventana = tk.Tk()
    ventana.title("Panel del Administrador")
    ventana.geometry("500x350")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)

    titulo = tk.Label(
        ventana,
        text="Panel de Administración",
        font=("Arial", 18, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=20)

    # BOTONES DE NAVEGACIÓN (expansibles luego)
    frame = tk.Frame(ventana, bg="#E3F2FD")
    frame.pack(pady=10)

    btn_estudiantes = tk.Button(
        frame,
        text="Gestionar Estudiantes",
        width=25,
        font=("Arial", 12),
        bg="#1565C0",
        fg="white",
        command=lambda: messagebox.showinfo("Próximamente", "Módulo estudiantes...")
    )
    btn_estudiantes.grid(row=0, column=0, padx=10, pady=5)

    btn_competencias = tk.Button(
        frame,
        text="Gestionar Competencias",
        width=25,
        font=("Arial", 12),
        bg="#1976D2",
        fg="white",
        command=lambda: messagebox.showinfo("Próximamente", "Módulo competencias...")
    )
    btn_competencias.grid(row=1, column=0, padx=10, pady=5)

    btn_registros = tk.Button(
        frame,
        text="Gestionar Registros Auxiliares",
        width=25,
        font=("Arial", 12),
        bg="#0D47A1",
        fg="white",
        command=lambda: messagebox.showinfo("Próximamente", "Módulo registros...")
    )
    btn_registros.grid(row=2, column=0, padx=10, pady=5)

    btn_salir = tk.Button(
        ventana,
        text="Cerrar Sesión",
        font=("Arial", 12, "bold"),
        bg="#EF5350",
        fg="white",
        width=15,
        command=ventana.destroy
    )
    btn_salir.pack(pady=20)

    ventana.mainloop()
