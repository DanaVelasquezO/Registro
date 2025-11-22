import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os
from db.conexion import obtener_conexion

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_cargar_excel(ventana_padre=None, callback_actualizar=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Cargar Estudiantes desde Excel")
    ventana.geometry("650x650")  # Más alto para que quepa el botón
    ventana.resizable(False, False)
    ventana.config(bg="#E3F2FD")
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Variables
    archivo_seleccionado = tk.StringVar()
    datos_excel = []
    
    # Título
    titulo = tk.Label(
        ventana,
        text="Cargar Estudiantes desde Excel",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Frame de instrucciones
    frame_instrucciones = tk.Frame(ventana, bg="#FFF3CD", relief="solid", bd=1)
    frame_instrucciones.pack(pady=10, padx=20, fill="x")
    
    instrucciones = [
        "📋 Instrucciones para el archivo Excel:",
        "• El archivo debe tener una columna 'Nombres' con los nombres completos",
        "• Formatos soportados: .xlsx, .xls",
        "• Los códigos se generarán automáticamente",
        "• Los nombres duplicados serán ignorados"
    ]
    
    for i, instruccion in enumerate(instrucciones):
        lbl = tk.Label(
            frame_instrucciones,
            text=instruccion,
            font=("Arial", 9),
            bg="#FFF3CD",
            justify="left",
            anchor="w"
        )
        lbl.grid(row=i, column=0, sticky="w", padx=5, pady=2)
    
    # Frame de selección de archivo
    frame_archivo = tk.Frame(ventana, bg="#E3F2FD")
    frame_archivo.pack(pady=10, padx=20, fill="x")
    
    lbl_archivo = tk.Label(
        frame_archivo,
        text="Archivo Excel:",
        font=("Arial", 10, "bold"),
        bg="#E3F2FD"
    )
    lbl_archivo.grid(row=0, column=0, sticky="w", pady=5)
    
    entry_archivo = tk.Entry(
        frame_archivo,
        textvariable=archivo_seleccionado,
        font=("Arial", 10),
        width=50,
        state="readonly"
    )
    entry_archivo.grid(row=1, column=0, sticky="we", pady=5)
    
    btn_examinar = tk.Button(
        frame_archivo,
        text="Examinar",
        font=("Arial", 10),
        bg="#1976D2",
        fg="white",
        command=lambda: seleccionar_archivo()
    )
    btn_examinar.grid(row=1, column=1, padx=5, pady=5)
    
    # Frame de vista previa
    frame_vista_previa = tk.Frame(ventana, bg="#E3F2FD")
    frame_vista_previa.pack(pady=10, padx=20, fill="both", expand=True)
    
    lbl_vista_previa = tk.Label(
        frame_vista_previa,
        text="Vista previa de datos:",
        font=("Arial", 10, "bold"),
        bg="#E3F2FD"
    )
    lbl_vista_previa.pack(anchor="w", pady=(0, 5))
    
    # Contenedor para el treeview y scrollbars
    frame_tree = tk.Frame(frame_vista_previa)
    frame_tree.pack(fill="both", expand=True)
    
    # Scrollbars
    scroll_y = tk.Scrollbar(frame_tree)
    scroll_y.pack(side="right", fill="y")
    
    scroll_x = tk.Scrollbar(frame_tree, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")
    
    # Treeview
    treeview_previa = ttk.Treeview(
        frame_tree,
        columns=("Número", "Nombre"),
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
        height=8,
        show="headings"
    )
    
    scroll_y.config(command=treeview_previa.yview)
    scroll_x.config(command=treeview_previa.xview)
    
    treeview_previa.heading("Número", text="#")
    treeview_previa.heading("Nombre", text="Nombre del Estudiante")
    treeview_previa.column("Número", width=60, anchor="center")
    treeview_previa.column("Nombre", width=400)
    
    treeview_previa.pack(fill="both", expand=True)
    
    # Frame de resultados
    frame_resultados = tk.Frame(ventana, bg="#E3F2FD")
    frame_resultados.pack(pady=10, padx=20, fill="x")
    
    lbl_resultados = tk.Label(
        frame_resultados,
        text="Estudiantes a importar: 0",
        font=("Arial", 10, "bold"),
        bg="#E3F2FD",
        fg="#D32F2F"
    )
    lbl_resultados.pack(anchor="w")
    
    # === BOTÓN DE IMPORTAR - SIEMPRE VISIBLE ===
    frame_boton_importar = tk.Frame(ventana, bg="#E3F2FD")
    frame_boton_importar.pack(pady=15, padx=20, fill="x")
    
    # Botón IMPORTAR - SIEMPRE VISIBLE, pero inicialmente deshabilitado
    btn_importar = tk.Button(
        frame_boton_importar,
        text="Importar estudiantes a la bases de datos",
        font=("Arial", 9, "bold"),
        bg="#9E9E9E",  # Gris cuando está deshabilitado
        fg="white",
        width=40,
        height=2,
        state="disabled",
        command=lambda: importar_estudiantes()
    )
    btn_importar.pack(pady=10)
    
    # Frame de botones inferiores
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=10, padx=20, fill="x")
    
    btn_cancelar = tk.Button(
        frame_botones,
        text="Cerrar Ventana",
        font=("Arial", 10),
        bg="#757575",
        fg="white",
        width=15,
        command=ventana.destroy
    )
    btn_cancelar.pack()
    
    def seleccionar_archivo():
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[
                ("Archivos Excel", "*.xlsx *.xls"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            archivo_seleccionado.set(archivo)
            cargar_vista_previa(archivo)
    
    def cargar_vista_previa(archivo):
        nonlocal datos_excel
        
        try:
            # Leer archivo Excel
            df = pd.read_excel(archivo)
            
            # Verificar si existe columna 'Nombres'
            if 'Nombres' not in df.columns:
                messagebox.showerror("Error", 
                    "El archivo Excel debe tener una columna llamada 'Nombres'\n\n"
                    "Columnas encontradas:\n" + 
                    "\n".join(df.columns.tolist()))
                # Deshabilitar botón
                btn_importar.config(state="disabled", bg="#9E9E9E", 
                                  text="Importar estudiantes a la bases de datos")
                return
            
            # Limpiar treeview
            for item in treeview_previa.get_children():
                treeview_previa.delete(item)
            
            # Cargar datos
            datos_excel = df['Nombres'].dropna().str.strip().tolist()
            datos_excel = [nombre for nombre in datos_excel if nombre]
            
            if not datos_excel:
                messagebox.showwarning("Sin datos", "No se encontraron nombres en la columna 'Nombres'")
                btn_importar.config(state="disabled", bg="#9E9E9E",
                                  text="Importar estudiantes a la bases de datos")
                lbl_resultados.config(text="Estudiantes a importar: 0")
                return
            
            # Mostrar en treeview
            for i, nombre in enumerate(datos_excel[:50], 1):
                treeview_previa.insert("", "end", values=(i, nombre))
            
            if len(datos_excel) > 50:
                treeview_previa.insert("", "end", values=("...", f"Y {len(datos_excel) - 50} más ..."))
            
            lbl_resultados.config(text=f"Estudiantes a importar: {len(datos_excel)}")
            
            # HABILITAR el botón de importar
            btn_importar.config(state="normal", bg="#4CAF50",
                              text=f"Importar {len(datos_excel)} estudiantes")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo Excel:\n{str(e)}")
            btn_importar.config(state="disabled", bg="#9E9E9E",
                              text=" Importar estudiantes a la bases de datos")
    
    def importar_estudiantes():
        if not datos_excel:
            messagebox.showwarning("Sin datos", 
                "No hay estudiantes para importar.\n\n"
                "Por favor seleccione un archivo Excel válido con la columna 'Nombres'.")
            return
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Obtener nombres existentes
            cursor.execute("SELECT Nombre_estudiante FROM Estudiante")
            nombres_existentes = set([row[0] for row in cursor.fetchall()])
            
            # Filtrar nombres nuevos
            nombres_nuevos = [nombre for nombre in datos_excel if nombre not in nombres_existentes]
            nombres_duplicados = [nombre for nombre in datos_excel if nombre in nombres_existentes]
            
            if not nombres_nuevos:
                messagebox.showinfo("Sin nuevos datos", 
                    "Todos los estudiantes del archivo ya existen en la base de datos.\n\n"
                    "No se importó ningún nuevo estudiante.")
                return
            
            # Insertar nuevos estudiantes
            estudiantes_insertados = 0
            nombres_demasiado_largos = []
            
            for nombre in nombres_nuevos:
                if len(nombre) <= 40:
                    cursor.execute("INSERT INTO Estudiante (Nombre_estudiante) VALUES (%s)", (nombre,))
                    estudiantes_insertados += 1
                else:
                    nombres_demasiado_largos.append(nombre)
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            # Mostrar resultados detallados
            mensaje = f"✅ ESTUDIANTES IMPORTADOS EXITOSAMENTE: {estudiantes_insertados}"
            
            if nombres_duplicados:
                mensaje += f"\n\nDUPLICADOS OMITIDOS: {len(nombres_duplicados)}"
                if len(nombres_duplicados) <= 10:
                    mensaje += "\n" + "\n".join(f"• {nombre}" for nombre in nombres_duplicados)
                else:
                    mensaje += f"\n(mostrando los primeros 10)\n" + "\n".join(f"• {nombre}" for nombre in nombres_duplicados[:10])
            
            if nombres_demasiado_largos:
                mensaje += f"\n\nNOMBRES DEMASIADO LARGOS (>40 caracteres): {len(nombres_demasiado_largos)}"
                if len(nombres_demasiado_largos) <= 5:
                    mensaje += "\n" + "\n".join(f"• {nombre}" for nombre in nombres_demasiado_largos)
            
            messagebox.showinfo("Importación Completada", mensaje)
            
            if callback_actualizar:
                callback_actualizar()
                
            ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar estudiantes:\n{str(e)}")
    
    # Centrar ventana después de crear todos los widgets
    ventana.after(100, lambda: centrar_ventana(ventana, 650, 650))
    
    return ventana