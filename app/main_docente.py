import tkinter as tk
from tkinter import messagebox

def iniciar_docente(codigo_docente):
    # Crear ventana principal para docente
    ventana = tk.Tk()
    ventana.title("Panel del Docente")
    ventana.geometry("500x400")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)
    ventana.eval('tk::PlaceWindow . center')  # Centrar ventana

    titulo = tk.Label(
        ventana,
        text=f"Bienvenido Docente (ID: {codigo_docente})",
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
        command=lambda: messagebox.showinfo("Próximamente", "Módulo registros…")
    )
    btn_registros.grid(row=0, column=0, padx=10, pady=10)

    btn_notas = tk.Button(
        frame,
        text="Ingresar Notas",
        width=25,
        font=("Arial", 12),
        bg="#1976D2",
        fg="white",
        command=lambda: messagebox.showinfo("Próximamente", "Módulo notas…")
    )
    btn_notas.grid(row=1, column=0, padx=10, pady=10)

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