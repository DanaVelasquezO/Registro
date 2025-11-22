import tkinter as tk
from tkinter import messagebox
from db.conexion import obtener_conexion


def iniciar_login():
    ventana = tk.Tk()
    ventana.title("Ingreso al Sistema")
    ventana.geometry("350x260")
    ventana.resizable(False, False)
    ventana.config(bg="#E3F2FD")

    # ---------- TÍTULO ----------
    titulo = tk.Label(
        ventana, 
        text="Inicio de Sesión", 
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=20)

    # ---------- CAMPOS ----------
    frame = tk.Frame(ventana, bg="#E3F2FD")
    frame.pack()

    tk.Label(frame, text="Usuario:", bg="#E3F2FD", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="w")
    entrada_usuario = tk.Entry(frame, font=("Arial", 12))
    entrada_usuario.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Contraseña:", bg="#E3F2FD", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
    entrada_password = tk.Entry(frame, font=("Arial", 12), show="*")
    entrada_password.grid(row=1, column=1, pady=5)

    # ---------- FUNCIÓN VALIDAR ----------
    def validar():
        usuario = entrada_usuario.get().strip()
        clave = entrada_password.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Campos vacíos", "Debe ingresar usuario y contraseña.")
            return

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT rol, codigo_docente
            FROM Usuarios
            WHERE usuario = %s AND clave = %s
        """, (usuario, clave))

        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado is None:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            return

        rol, codigo_docente = resultado

        ventana.destroy()  # cerrar login

        # ======================
        # AQUI VIENE EL FIX ✔✔✔
        # ======================
        if rol == "admin":
            from app.main_admin import comenzar_admin
            comenzar_admin()

        elif rol == "docente":
            from app.main_docente import iniciar_docente
            iniciar_docente(codigo_docente)


    # ---------- BOTÓN ----------
    boton = tk.Button(
        ventana,
        text="Ingresar",
        font=("Arial", 12, "bold"),
        bg="#1976D2",
        fg="white",
        width=15,
        command=validar
    )
    boton.pack(pady=20)

    ventana.mainloop()
