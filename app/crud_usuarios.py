import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion


# ============================
# VENTANA PRINCIPAL DEL CRUD
# ============================
def ventana_crud_usuarios():

    ventana = tk.Toplevel()
    ventana.title("Gestión de Usuarios del Sistema")
    ventana.geometry("800x500")
    ventana.resizable(False, False)
    ventana.config(bg="#E3F2FD")

    titulo = tk.Label(
        ventana,
        text="Gestión de Usuarios",
        font=("Arial", 18, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=10)

    # ============================
    # TABLA LISTADO DE USUARIOS
    # ============================
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(pady=10)

    columnas = ("id", "usuario", "rol", "docente")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

    tabla.heading("id", text="ID")
    tabla.heading("usuario", text="Usuario")
    tabla.heading("rol", text="Rol")
    tabla.heading("docente", text="Docente Asociado")

    tabla.column("id", width=60)
    tabla.column("usuario", width=180)
    tabla.column("rol", width=120)
    tabla.column("docente", width=200)

    tabla.pack()

    # ============================
    # FUNCIONES CRUD
    # ============================

    def cargar_usuarios():
        tabla.delete(*tabla.get_children())
        con = obtener_conexion()
        cursor = con.cursor()

        cursor.execute("""
            SELECT U.id_usuario, U.usuario, U.rol,
                   COALESCE(D.Nombre_docente, '---')
            FROM Usuarios U
            LEFT JOIN Docente D ON D.Codigo_docente = U.codigo_docente
            ORDER BY id_usuario
        """)

        for fila in cursor.fetchall():
            tabla.insert("", tk.END, values=fila)

        con.close()

    def abrir_crear_usuario():
        ventana_crear = tk.Toplevel()
        ventana_crear.title("Crear Usuario")
        ventana_crear.geometry("350x350")
        ventana_crear.config(bg="#FFF")

        tk.Label(ventana_crear, text="Nuevo Usuario", font=("Arial", 14, "bold")).pack(pady=10)

        # CAMPOS
        tk.Label(ventana_crear, text="Usuario:").pack()
        entry_user = tk.Entry(ventana_crear)
        entry_user.pack(pady=5)

        tk.Label(ventana_crear, text="Contraseña:").pack()
        entry_clave = tk.Entry(ventana_crear, show="*")
        entry_clave.pack(pady=5)

        tk.Label(ventana_crear, text="Rol:").pack()
        combo_rol = ttk.Combobox(ventana_crear, values=["admin", "docente"])
        combo_rol.pack(pady=5)

        tk.Label(ventana_crear, text="Docente asociado (opcional):").pack()
        combo_docente = ttk.Combobox(ventana_crear)
        combo_docente.pack(pady=5)

        # Cargar docentes
        con = obtener_conexion()
        cursor = con.cursor()
        cursor.execute("SELECT Codigo_docente, Nombre_docente FROM Docente")
        docentes = cursor.fetchall()
        con.close()

        dic_docentes = {d[1]: d[0] for d in docentes}
        combo_docente["values"] = list(dic_docentes.keys())

        def crear_usuario():
            user = entry_user.get().strip()
            clave = entry_clave.get().strip()
            rol = combo_rol.get().strip()
            doc = combo_docente.get().strip()

            if user == "" or clave == "" or rol == "":
                messagebox.showwarning("Campos vacíos", "Complete todos los campos obligatorios.")
                return

            id_doc = dic_docentes.get(doc, None)

            con = obtener_conexion()
            cursor = con.cursor()

            try:
                cursor.execute("""
                    INSERT INTO Usuarios (usuario, clave, rol, codigo_docente)
                    VALUES (%s, %s, %s, %s)
                """, (user, clave, rol, id_doc))

                con.commit()
                messagebox.showinfo("Éxito", "Usuario creado correctamente.")
                cargar_usuarios()
                ventana_crear.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear usuario:\n{e}")

            con.close()

        tk.Button(ventana_crear, text="Crear Usuario", bg="#4CAF50", fg="white", command=crear_usuario).pack(pady=15)

    def eliminar_usuario():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Seleccione uno", "Seleccione un usuario para eliminar.")
            return

        valores = tabla.item(seleccionado, "values")
        user_id = valores[0]

        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este usuario?"):
            con = obtener_conexion()
            cursor = con.cursor()

            cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (user_id,))
            con.commit()
            con.close()

            cargar_usuarios()

    def abrir_editar_usuario():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Seleccione uno", "Seleccione un usuario para editar.")
            return

        valores = tabla.item(seleccionado, "values")
        user_id = valores[0]
        user_act = valores[1]
        rol_act = valores[2]
        docente_act = valores[3]

        ventana_edit = tk.Toplevel()
        ventana_edit.title("Editar Usuario")
        ventana_edit.geometry("350x350")
        ventana_edit.config(bg="#FFF")

        tk.Label(ventana_edit, text="Editar Usuario", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(ventana_edit, text="Usuario:").pack()
        entry_user = tk.Entry(ventana_edit)
        entry_user.insert(0, user_act)
        entry_user.pack(pady=5)

        tk.Label(ventana_edit, text="Nueva Contraseña (opcional):").pack()
        entry_clave = tk.Entry(ventana_edit, show="*")
        entry_clave.pack(pady=5)

        tk.Label(ventana_edit, text="Rol:").pack()
        combo_rol = ttk.Combobox(ventana_edit, values=["admin", "docente"])
        combo_rol.set(rol_act)
        combo_rol.pack(pady=5)

        tk.Label(ventana_edit, text="Docente asociado:").pack()
        combo_doc = ttk.Combobox(ventana_edit)
        combo_doc.pack()

        con = obtener_conexion()
        cursor = con.cursor()
        cursor.execute("SELECT Codigo_docente, Nombre_docente FROM Docente")
        docentes = cursor.fetchall()
        con.close()

        dic_doc = {d[1]: d[0] for d in docentes}
        combo_doc["values"] = list(dic_doc.keys())

        def actualizar():
            nuevo_user = entry_user.get().strip()
            nueva_clave = entry_clave.get().strip()
            nuevo_rol = combo_rol.get().strip()
            doc_sel = combo_doc.get().strip()
            id_doc = dic_doc.get(doc_sel, None)

            if nuevo_user == "" or nuevo_rol == "":
                messagebox.showwarning("Campos vacíos", "Complete los campos obligatorios.")
                return

            con = obtener_conexion()
            cursor = con.cursor()

            if nueva_clave == "":
                cursor.execute("""
                    UPDATE Usuarios
                    SET usuario=%s, rol=%s, codigo_docente=%s
                    WHERE id_usuario=%s
                """, (nuevo_user, nuevo_rol, id_doc, user_id))
            else:
                cursor.execute("""
                    UPDATE Usuarios
                    SET usuario=%s, clave=%s, rol=%s, codigo_docente=%s
                    WHERE id_usuario=%s
                """, (nuevo_user, nueva_clave, nuevo_rol, id_doc, user_id))

            con.commit()
            con.close()
            cargar_usuarios()
            ventana_edit.destroy()

        tk.Button(ventana_edit, text="Guardar Cambios", bg="#1976D2", fg="white", command=actualizar).pack(pady=20)

    # ============================
    # BOTONES CRUD
    # ============================
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=15)

    tk.Button(frame_botones, text="Crear Usuario", width=15, bg="#4CAF50", fg="white",
              command= abrir_crear_usuario).grid(row=0, column=0, padx=10)

    tk.Button(frame_botones, text="Editar Usuario", width=15, bg="#0277BD", fg="white",
              command= abrir_editar_usuario).grid(row=0, column=1, padx=10)

    tk.Button(frame_botones, text="Eliminar Usuario", width=15, bg="#D32F2F", fg="white",
              command= eliminar_usuario).grid(row=0, column=2, padx=10)

    # CARGAR DATOS INICIALES
    cargar_usuarios()

    ventana.mainloop()
