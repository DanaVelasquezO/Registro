import tkinter as tk
import traceback
from tkinter import messagebox
from db.conexion import obtener_conexion

# Variable global para controlar la ventana principal
ventana_principal = None

def iniciar_login():
    global ventana_principal
    
    print("\n=== INICIANDO LOGIN ===")

    # Si ya existe una ventana principal, limpiarla
    if ventana_principal is not None:
        try:
            ventana_principal.destroy()
        except:
            pass

    # Crear nueva ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Ingreso al Sistema")
    ventana_principal.geometry("350x260")
    ventana_principal.resizable(False, False)
    ventana_principal.config(bg="#E3F2FD")
    
    # Centrar ventana
    ventana_principal.eval('tk::PlaceWindow . center')

    # ---------- TÍTULO ----------
    titulo = tk.Label(
        ventana_principal,
        text="Inicio de Sesión",
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=20)

    # ---------- CAMPOS ----------
    frame = tk.Frame(ventana_principal, bg="#E3F2FD")
    frame.pack()

    tk.Label(frame, text="Usuario:", bg="#E3F2FD", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="w")
    entrada_usuario = tk.Entry(frame, font=("Arial", 12))
    entrada_usuario.grid(row=0, column=1, pady=5)
    entrada_usuario.focus_set()

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

        # Cerrar ventana de login
        ventana_principal.destroy()

        # Abrir la ventana correspondiente
        if rol == "admin":
            from app.main_admin import iniciar_admin
            iniciar_admin()
        elif rol == "docente":
            from app.main_docente import iniciar_docente
            iniciar_docente(codigo_docente)

    # ---------- BOTÓN ----------
    boton = tk.Button(
        ventana_principal,
        text="Ingresar",
        font=("Arial", 12, "bold"),
        bg="#1976D2",
        fg="white",
        width=15,
        command=validar
    )
    boton.pack(pady=20)

    # Permitir login con Enter
    ventana_principal.bind('<Return>', lambda event: validar())

    # Manejar cierre de la aplicación
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir del sistema?"):
            ventana_principal.quit()
            ventana_principal.destroy()

    ventana_principal.protocol("WM_DELETE_WINDOW", on_closing)

    ventana_principal.mainloop()