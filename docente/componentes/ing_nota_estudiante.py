import tkinter as tk
from tkinter import ttk, messagebox
from db.database_utils import (
    ejecutar_consulta_segura, 
    obtener_nota_existente, 
    verificar_nota_existente, 
    guardar_nota
)

def centrar_ventana(ventana, ancho, alto):
    """Centra la ventana en la pantalla"""
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_ingreso_nota_estudiante(estudiante, numero_registro, ventana_padre=None):
    """
    Abre una ventana separada para ingresar notas de un estudiante específico
    """
    ventana = tk.Toplevel(ventana_padre)
    ventana.title(f"Ingreso de Notas - {estudiante['nombre']}")
    ventana.geometry("900x650")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(True, True)
    
    if ventana_padre:
        ventana.transient(ventana_padre)
        ventana.grab_set()
    
    centrar_ventana(ventana, 900, 650)
    
    # Variables
    indicadores_dict = {}
    
    # Título
    titulo_frame = tk.Frame(ventana, bg="#0D47A1")
    titulo_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Label(
        titulo_frame,
        text="Ingreso de Notas",
        font=("Arial", 14, "bold"),
        bg="#0D47A1",
        fg="white"
    ).pack(pady=5)
    
    # Información del estudiante
    info_frame = tk.Frame(ventana, bg="#BBDEFB", relief="ridge", bd=2)
    info_frame.pack(fill="x", padx=20, pady=10)
    
    tk.Label(
        info_frame,
        text=f"Estudiante: {estudiante['nombre']}",
        font=("Arial", 12, "bold"),
        bg="#BBDEFB"
    ).pack(side="left", padx=10, pady=8)
    
    tk.Label(
        info_frame,
        text=f"Código: {estudiante['codigo']}",
        font=("Arial", 11),
        bg="#BBDEFB"
    ).pack(side="left", padx=20, pady=8)
    
    tk.Label(
        info_frame,
        text=f"Registro: {numero_registro}",
        font=("Arial", 11),
        bg="#BBDEFB"
    ).pack(side="right", padx=10, pady=8)
    
    # Frame principal con scroll
    main_frame = tk.Frame(ventana, bg="#E3F2FD")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Canvas y scrollbar
    canvas = tk.Canvas(main_frame, bg="#E3F2FD")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#E3F2FD")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Cargar competencias e indicadores
    cargar_competencias_indicadores(scrollable_frame, estudiante, numero_registro, indicadores_dict)
    
    # Frame de botones
    botones_frame = tk.Frame(ventana, bg="#E3F2FD")
    botones_frame.pack(fill="x", padx=20, pady=15)
    
    # Botón guardar todas las notas
    btn_guardar = tk.Button(
        botones_frame,
        text="Guardar Todas las Notas",
        font=("Arial", 12, "bold"),
        bg="#388E3C",
        fg="white",
        width=20,
        command=lambda: guardar_todas_las_notas(estudiante, numero_registro, indicadores_dict, ventana)
    )
    btn_guardar.pack(side="left", padx=5)
    
    # Botón actualizar notas existentes
    btn_actualizar = tk.Button(
        botones_frame,
        text="Actualizar Notas",
        font=("Arial", 12),
        bg="#1976D2",
        fg="white",
        width=15,
        command=lambda: actualizar_notas_existentes(estudiante, numero_registro, indicadores_dict)
    )
    btn_actualizar.pack(side="left", padx=5)
    
    # Botón limpiar todas las notas
    btn_limpiar = tk.Button(
        botones_frame,
        text="Limpiar Campos",
        font=("Arial", 12),
        bg="#F57C00",
        fg="white",
        width=15,
        command=lambda: limpiar_todas_las_notas(indicadores_dict)
    )
    btn_limpiar.pack(side="left", padx=5)
    
    # Botón cerrar
    btn_cerrar = tk.Button(
        botones_frame,
        text="Cerrar",
        font=("Arial", 12),
        bg="#757575",
        fg="white",
        width=12,
        command=ventana.destroy
    )
    btn_cerrar.pack(side="right", padx=5)
    
    return ventana

def cargar_competencias_indicadores(parent, estudiante, numero_registro, indicadores_dict):
    """
    Carga las competencias e indicadores para el estudiante y registro específicos
    """
    try:
        # Obtener competencias usando la función utilitaria
        competencias = ejecutar_consulta_segura(
            """
            SELECT DISTINCT c.id_competencia, c.competencia
            FROM Competencias c
            JOIN Competencias_Registro cr ON c.id_competencia = cr.Id_competencia
            WHERE cr.Numero_de_registro = %s
            ORDER BY c.competencia
            """,
            (numero_registro,)
        )
        
        if not competencias:
            tk.Label(
                parent,
                text="No hay competencias asignadas a este registro",
                font=("Arial", 11),
                bg="#E3F2FD",
                fg="#666666"
            ).pack(pady=20)
            return
        
        for competencia in competencias:
            id_competencia, nombre_competencia = competencia
            
            # Frame para cada competencia
            frame_competencia = tk.LabelFrame(
                parent, 
                text=nombre_competencia,
                font=("Arial", 11, "bold"),
                bg="#E3F2FD",
                fg="#0D47A1"
            )
            frame_competencia.pack(fill="x", padx=5, pady=8)
            
            # Obtener indicadores usando la función utilitaria
            indicadores = ejecutar_consulta_segura(
                """
                SELECT i.Id_indicador, i.Indicadores_competencias
                FROM Indicadores i
                JOIN Indicadores_Registro ir ON i.Id_indicador = ir.Id_indicador
                WHERE ir.Numero_de_registro = %s AND i.Id_competencia = %s
                ORDER BY i.Id_indicador
                """,
                (numero_registro, id_competencia)
            )
            
            if not indicadores:
                tk.Label(
                    frame_competencia,
                    text="No hay indicadores para esta competencia",
                    font=("Arial", 9),
                    bg="#E3F2FD",
                    fg="#666666"
                ).pack(pady=5)
                continue
            
            # Crear campos para cada indicador
            for idx, indicador in enumerate(indicadores):
                id_indicador, nombre_indicador = indicador
                
                # Frame para cada indicador
                frame_indicador = tk.Frame(frame_competencia, bg="#E3F2FD")
                frame_indicador.pack(fill="x", padx=15, pady=4)
                
                # Nombre del indicador
                lbl_indicador = tk.Label(
                    frame_indicador, 
                    text=nombre_indicador,
                    font=("Arial", 9),
                    bg="#E3F2FD",
                    width=70,
                    anchor="w",
                    wraplength=600
                )
                lbl_indicador.pack(side="left", padx=(0, 15))
                
                # Entry para nota con validación en tiempo real
                var_nota = tk.StringVar()
                entry_nota = tk.Entry(
                    frame_indicador,
                    font=("Arial", 10),
                    width=8,
                    justify="center",
                    textvariable=var_nota
                )
                entry_nota.pack(side="left", padx=5)
                
                # Etiqueta para mostrar estado de validación
                lbl_estado = tk.Label(
                    frame_indicador,
                    text="",
                    font=("Arial", 8),
                    bg="#E3F2FD",
                    width=12
                )
                lbl_estado.pack(side="left", padx=5)
                
                # Validación en tiempo real
                def crear_callback(entry, lbl, var, id_comp=id_competencia, id_ind=id_indicador):
                    def callback(*args):
                        validar_nota_en_tiempo_real(entry, lbl, var.get())
                    return callback
                
                var_nota.trace("w", crear_callback(entry_nota, lbl_estado, var_nota))
                
                # Cargar nota existente si existe
                cargar_nota_existente(numero_registro, estudiante['codigo'], id_indicador, entry_nota, lbl_estado)
                
                # Guardar referencia
                indicadores_dict[f"{id_competencia}_{id_indicador}"] = {
                    'entry': entry_nota,
                    'lbl_estado': lbl_estado,
                    'var_nota': var_nota,
                    'id_indicador': id_indicador,
                    'id_competencia': id_competencia,
                    'nombre_indicador': nombre_indicador
                }
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar competencias: {str(e)}")

def cargar_nota_existente(numero_registro, codigo_estudiante, id_indicador, entry_nota, lbl_estado):
    """
    Carga la nota existente para un indicador específico
    """
    try:
        nota_existente = obtener_nota_existente(numero_registro, codigo_estudiante, id_indicador)
        
        if nota_existente is not None:
            entry_nota.delete(0, tk.END)
            entry_nota.insert(0, f"{nota_existente:.2f}")
            lbl_estado.config(text="Guardado", fg="#388E3C")
            print(f"✓ Nota cargada: {nota_existente} para indicador {id_indicador}")
        else:
            print(f"○ No se encontró nota para indicador {id_indicador}")
        
    except Exception as e:
        print(f"✗ Error al cargar nota existente para indicador {id_indicador}: {e}")

def validar_nota_en_tiempo_real(entry, lbl_estado, nota_str):
    """
    Valida la nota en tiempo real mientras el usuario escribe
    """
    if not nota_str.strip():
        lbl_estado.config(text="", fg="black")
        entry.config(bg="white")
        return
    
    try:
        # Permitir entrada vacía o solo un punto
        if nota_str == "" or nota_str == ".":
            lbl_estado.config(text="", fg="black")
            entry.config(bg="white")
            return
            
        nota = float(nota_str)
        if 0 <= nota <= 20:
            lbl_estado.config(text="Valida", fg="#388E3C")
            entry.config(bg="#C8E6C9")  # Verde claro
        else:
            lbl_estado.config(text="Invalida 0-20", fg="#D32F2F")
            entry.config(bg="#FFCDD2")  # Rojo claro
            # Mostrar alerta inmediatamente cuando se ingresa un número fuera de rango
            messagebox.showwarning("Nota Invalida", 
                                f"La nota debe estar entre 0 y 20.\n"
                                f"Valor ingresado: {nota}", 
                                parent=entry.winfo_toplevel())
            # Seleccionar el texto invalido para facilitar corrección
            entry.select_range(0, tk.END)
            entry.focus()
            
    except ValueError:
        # Solo mostrar error si no está vacío y no es solo un signo negativo o punto
        if nota_str and nota_str != '-' and nota_str != '.':
            lbl_estado.config(text="No es numero", fg="#D32F2F")
            entry.config(bg="#FFCDD2")
            messagebox.showerror("Error de formato", 
                               "Por favor ingrese un numero valido.\n"
                               "Ejemplos: 15.5, 18, 20.0",
                               parent=entry.winfo_toplevel())
            entry.select_range(0, tk.END)
            entry.focus()

def validar_nota(nota_str):
    """Valida que la nota esté entre 0 y 20"""
    try:
        nota = float(nota_str)
        return 0 <= nota <= 20
    except ValueError:
        return False

def limpiar_todas_las_notas(indicadores_dict):
    """Limpia todas las notas en los campos"""
    for key, info in indicadores_dict.items():
        info['entry'].delete(0, tk.END)
        info['lbl_estado'].config(text="", fg="black")
        info['entry'].config(bg="white")

def guardar_todas_las_notas(estudiante, numero_registro, indicadores_dict, ventana):
    """Guarda todas las notas del estudiante"""
    if not indicadores_dict:
        messagebox.showwarning("Sin datos", "No hay indicadores para guardar")
        return
    
    try:
        notas_guardadas = 0
        notas_invalidas = []
        
        for key, info in indicadores_dict.items():
            nota_str = info['entry'].get().strip()
            
            if nota_str:
                if validar_nota(nota_str):
                    try:
                        nota = float(nota_str)
                        
                        # Usar la función segura para guardar
                        if guardar_nota(numero_registro, estudiante['codigo'], 
                                      info['id_competencia'], info['id_indicador'], nota):
                            notas_guardadas += 1
                            info['lbl_estado'].config(text="Guardado", fg="#388E3C")
                            print(f"✓ Nota guardada: {nota} para indicador {info['id_indicador']}")
                        else:
                            notas_invalidas.append(info['nombre_indicador'])
                            info['lbl_estado'].config(text="Error BD", fg="#D32F2F")
                        
                    except Exception as e:
                        notas_invalidas.append(info['nombre_indicador'])
                        info['lbl_estado'].config(text="Error", fg="#D32F2F")
                        print(f"✗ Error al guardar nota para {info['nombre_indicador']}: {e}")
                else:
                    notas_invalidas.append(info['nombre_indicador'])
                    info['lbl_estado'].config(text="Invalida", fg="#D32F2F")
        
        # Mostrar resultado
        mensaje = f"Se guardaron {notas_guardadas} notas para {estudiante['nombre']}"
        if notas_invalidas:
            mensaje += f"\n\nNotas invalidas ({len(notas_invalidas)}):\n"
            mensaje += "\n".join([f"- {ind}" for ind in notas_invalidas[:3]])
            if len(notas_invalidas) > 3:
                mensaje += f"\n- ... y {len(notas_invalidas) - 3} mas"
            mensaje += "\n\nLas notas deben estar entre 0 y 20"
        else:
            mensaje += "\n\n¡Todas las notas se guardaron correctamente!"
        
        messagebox.showinfo("Resultado", mensaje)
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar notas: {str(e)}")

def actualizar_notas_existentes(estudiante, numero_registro, indicadores_dict):
    """
    Actualiza las notas que ya existen en la base de datos
    """
    try:
        notas_actualizadas = 0
        notas_invalidas = []
        
        for key, info in indicadores_dict.items():
            nota_str = info['entry'].get().strip()
            
            if nota_str:
                # Verificar si existe una nota previa
                existe_nota = verificar_nota_existente(
                    numero_registro, estudiante['codigo'], info['id_indicador']
                )
                
                if existe_nota:  # Solo actualizar si ya existe una nota
                    if validar_nota(nota_str):
                        try:
                            nota = float(nota_str)
                            
                            # Usar la función segura para actualizar
                            if guardar_nota(numero_registro, estudiante['codigo'], 
                                          info['id_competencia'], info['id_indicador'], nota):
                                notas_actualizadas += 1
                                info['lbl_estado'].config(text="Actualizada", fg="#1976D2")
                                print(f"✓ Nota actualizada: {nota} para indicador {info['id_indicador']}")
                            else:
                                notas_invalidas.append(info['nombre_indicador'])
                                info['lbl_estado'].config(text="Error BD", fg="#D32F2F")
                            
                        except Exception as e:
                            notas_invalidas.append(info['nombre_indicador'])
                            info['lbl_estado'].config(text="Error", fg="#D32F2F")
                            print(f"✗ Error al actualizar nota para {info['nombre_indicador']}: {e}")
                    else:
                        notas_invalidas.append(info['nombre_indicador'])
                        info['lbl_estado'].config(text="Invalida", fg="#D32F2F")
        
        # Mostrar resultado
        if notas_actualizadas > 0:
            mensaje = f"Se actualizaron {notas_actualizadas} notas existentes para {estudiante['nombre']}"
            if notas_invalidas:
                mensaje += f"\n\nNo se pudieron actualizar {len(notas_invalidas)} notas por valores invalidos"
            messagebox.showinfo("Actualizacion Exitosa", mensaje)
        else:
            messagebox.showinfo("Informacion", 
                              "No se encontraron notas existentes para actualizar.\n"
                              "Use 'Guardar Todas las Notas' para crear nuevas notas.")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar notas: {str(e)}")