import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

class CRUDDocentes:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestión de Docentes")
        self.ventana.geometry("800x600")
        self.ventana.config(bg="#E3F2FD")
        self.ventana.resizable(True, True)
        
        # Centrar ventana
        self.centrar_ventana()
        
        self.crear_interfaz()
        self.cargar_docentes()

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 800
        alto = 600
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    def crear_interfaz(self):
        # Título
        titulo = tk.Label(
            self.ventana,
            text="Gestión de Docentes",
            font=("Arial", 18, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1"
        )
        titulo.pack(pady=10)

        # Frame de búsqueda
        frame_busqueda = tk.Frame(self.ventana, bg="#E3F2FD")
        frame_busqueda.pack(pady=10, fill="x", padx=20)

        tk.Label(frame_busqueda, text="Buscar:", bg="#E3F2FD", font=("Arial", 10)).pack(side="left", padx=5)
        self.entry_busqueda = tk.Entry(frame_busqueda, font=("Arial", 10), width=30)
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind("<KeyRelease>", self.buscar_docente)

        btn_buscar = tk.Button(
            frame_busqueda,
            text="Buscar",
            font=("Arial", 10),
            bg="#1976D2",
            fg="white",
            command=self.buscar_docente
        )
        btn_buscar.pack(side="left", padx=5)

        # Frame de formulario
        frame_form = tk.Frame(self.ventana, bg="#E3F2FD")
        frame_form.pack(pady=10, fill="x", padx=20)

        # Código del docente (ahora es autoincrementable, solo para mostrar)
        tk.Label(frame_form, text="Código Docente:", bg="#E3F2FD", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.label_codigo = tk.Label(frame_form, text="Auto-generado", font=("Arial", 10, "bold"), bg="#E3F2FD", fg="#0D47A1")
        self.label_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Nombre del docente
        tk.Label(frame_form, text="Nombre del Docente:*", bg="#E3F2FD", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 10), width=40)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w", columnspan=3)

        # Frame de botones del formulario
        frame_botones_form = tk.Frame(self.ventana, bg="#E3F2FD")
        frame_botones_form.pack(pady=10)

        btn_guardar = tk.Button(
            frame_botones_form,
            text="Guardar Docente",
            font=("Arial", 10, "bold"),
            bg="#388E3C",
            fg="white",
            width=15,
            command=self.guardar_docente
        )
        btn_guardar.pack(side="left", padx=5)

        btn_editar = tk.Button(
            frame_botones_form,
            text="Editar Docente",
            font=("Arial", 10, "bold"),
            bg="#F57C00",
            fg="white",
            width=15,
            command=self.editar_docente
        )
        btn_editar.pack(side="left", padx=5)

        btn_eliminar = tk.Button(
            frame_botones_form,
            text="Eliminar Docente",
            font=("Arial", 10, "bold"),
            bg="#D32F2F",
            fg="white",
            width=15,
            command=self.eliminar_docente
        )
        btn_eliminar.pack(side="left", padx=5)

        btn_limpiar = tk.Button(
            frame_botones_form,
            text="Limpiar Campos",
            font=("Arial", 10),
            bg="#757575",
            fg="white",
            width=15,
            command=self.limpiar_campos
        )
        btn_limpiar.pack(side="left", padx=5)

        # Treeview para mostrar docentes
        frame_tabla = tk.Frame(self.ventana)
        frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        # Scrollbars
        scroll_y = tk.Scrollbar(frame_tabla)
        scroll_y.pack(side="right", fill="y")

        scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        # Tabla - AÑADIR show="headings" PARA QUE MUESTRE LAS COLUMNAS
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("Código", "Nombre", "Registros Asociados"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode="browse",
            height=15,
            show="headings"  # ¡ESTO ES IMPORTANTE!
        )

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        # Configurar columnas
        self.tabla.heading("Código", text="Código Docente")
        self.tabla.heading("Nombre", text="Nombre del Docente")
        self.tabla.heading("Registros Asociados", text="Registros Asociados")

        self.tabla.column("Código", width=120, anchor="center")
        self.tabla.column("Nombre", width=400)
        self.tabla.column("Registros Asociados", width=150, anchor="center")

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_docente)

    def cargar_docentes(self):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener docentes con conteo de registros asociados
            cursor.execute("""
                SELECT d.Codigo_docente, d.Nombre_docente, 
                       COUNT(dr.Numero_de_registro) as total_registros
                FROM Docente d
                LEFT JOIN Docente_Registro dr ON d.Codigo_docente = dr.Codigo_docente
                GROUP BY d.Codigo_docente, d.Nombre_docente
                ORDER BY d.Nombre_docente
            """)
            docentes = cursor.fetchall()
            cursor.close()
            conexion.close()

            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Llenar tabla
            for docente in docentes:
                codigo, nombre, registros = docente
                self.tabla.insert("", "end", values=(codigo, nombre, registros))

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar docentes: {str(e)}")

    def guardar_docente(self):
        nombre = self.entry_nombre.get().strip()

        # Validaciones
        if not nombre:
            messagebox.showwarning("Campo incompleto", "Por favor ingrese el nombre del docente")
            return

        if len(nombre) > 40:
            messagebox.showwarning("Nombre muy largo", "El nombre del docente no puede exceder los 40 caracteres")
            return

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Verificar si el nombre ya existe (opcional, según tu requerimiento)
            cursor.execute("SELECT Codigo_docente FROM Docente WHERE Nombre_docente = %s", (nombre,))
            existe = cursor.fetchone()

            if existe:
                messagebox.showerror("Error", "Ya existe un docente con ese nombre")
                return

            # Insertar nuevo docente (el código es autoincrementable)
            cursor.execute("INSERT INTO Docente (Nombre_docente) VALUES (%s)", (nombre,))

            conexion.commit()
            
            # Obtener el código generado
            codigo_generado = cursor.lastrowid
            
            cursor.close()
            conexion.close()

            messagebox.showinfo("Éxito", f"Docente guardado correctamente\nCódigo asignado: {codigo_generado}")
            self.limpiar_campos()
            self.cargar_docentes()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar docente: {str(e)}")

    def seleccionar_docente(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item["values"]
            
            if valores:
                # Mostrar código
                self.label_codigo.config(text=str(valores[0]))
                # Llenar campo de nombre
                self.entry_nombre.delete(0, tk.END)
                self.entry_nombre.insert(0, valores[1])

    def editar_docente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un docente para editar")
            return

        item = self.tabla.item(seleccion[0])
        codigo_docente = item["values"][0]
        
        nombre = self.entry_nombre.get().strip()

        # Validaciones
        if not nombre:
            messagebox.showwarning("Campo incompleto", "Por favor ingrese el nombre del docente")
            return

        if len(nombre) > 40:
            messagebox.showwarning("Nombre muy largo", "El nombre del docente no puede exceder los 40 caracteres")
            return

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Verificar si el nombre ya existe en otro docente
            cursor.execute("""
                SELECT Codigo_docente FROM Docente 
                WHERE Nombre_docente = %s AND Codigo_docente != %s
            """, (nombre, codigo_docente))
            existe = cursor.fetchone()

            if existe:
                messagebox.showerror("Error", "Ya existe otro docente con ese nombre")
                return

            # Actualizar docente
            cursor.execute("""
                UPDATE Docente 
                SET Nombre_docente = %s
                WHERE Codigo_docente = %s
            """, (nombre, codigo_docente))

            conexion.commit()
            cursor.close()
            conexion.close()

            messagebox.showinfo("Éxito", "Docente actualizado correctamente")
            self.limpiar_campos()
            self.cargar_docentes()

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar docente: {str(e)}")

    def eliminar_docente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un docente para eliminar")
            return

        item = self.tabla.item(seleccion[0])
        codigo_docente = item["values"][0]
        nombre_docente = item["values"][1]
        registros_asociados = item["values"][2]

        # Verificar si tiene registros asociados
        if registros_asociados > 0:
            messagebox.showwarning(
                "No se puede eliminar",
                f"No se puede eliminar al docente '{nombre_docente}' porque tiene {registros_asociados} registro(s) auxiliar(es) asociado(s).\n\nElimine primero los registros asociados."
            )
            return

        # Verificar si tiene usuarios asociados
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id_usuario FROM Usuarios WHERE codigo_docente = %s", (codigo_docente,))
            tiene_usuarios = cursor.fetchone()
            cursor.close()
            conexion.close()

            if tiene_usuarios:
                messagebox.showwarning(
                    "No se puede eliminar",
                    f"No se puede eliminar al docente '{nombre_docente}' porque tiene usuario(s) asociado(s).\n\nElimine primero el usuario asociado."
                )
                return

        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar usuarios: {str(e)}")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar al docente?\n\n"
            f"Código: {codigo_docente}\n"
            f"Nombre: {nombre_docente}\n\n"
            f"Esta acción no se puede deshacer."
        )

        if not confirmacion:
            return

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM Docente WHERE Codigo_docente = %s", (codigo_docente,))
            conexion.commit()
            cursor.close()
            conexion.close()

            messagebox.showinfo("Éxito", "Docente eliminado correctamente")
            self.limpiar_campos()
            self.cargar_docentes()

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar docente: {str(e)}")

    def buscar_docente(self, event=None):
        busqueda = self.entry_busqueda.get().strip()
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            if busqueda:
                cursor.execute("""
                    SELECT d.Codigo_docente, d.Nombre_docente, 
                           COUNT(dr.Numero_de_registro) as total_registros
                    FROM Docente d
                    LEFT JOIN Docente_Registro dr ON d.Codigo_docente = dr.Codigo_docente
                    WHERE d.Nombre_docente LIKE %s OR d.Codigo_docente LIKE %s
                    GROUP BY d.Codigo_docente, d.Nombre_docente
                    ORDER BY d.Nombre_docente
                """, (f"%{busqueda}%", f"%{busqueda}%"))
            else:
                cursor.execute("""
                    SELECT d.Codigo_docente, d.Nombre_docente, 
                           COUNT(dr.Numero_de_registro) as total_registros
                    FROM Docente d
                    LEFT JOIN Docente_Registro dr ON d.Codigo_docente = dr.Codigo_docente
                    GROUP BY d.Codigo_docente, d.Nombre_docente
                    ORDER BY d.Nombre_docente
                """)
                
            docentes = cursor.fetchall()
            cursor.close()
            conexion.close()

            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Llenar tabla con resultados
            for docente in docentes:
                self.tabla.insert("", "end", values=docente)

        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar docentes: {str(e)}")

    def limpiar_campos(self):
        self.label_codigo.config(text="Auto-generado")
        self.entry_nombre.delete(0, tk.END)
        self.entry_busqueda.delete(0, tk.END)
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection())

def ventana_crud_docentes(ventana_padre=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.transient(ventana_padre)
    ventana.grab_set()
    app = CRUDDocentes(ventana)
    return app