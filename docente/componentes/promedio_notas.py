import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def convertir_a_literal(promedio):
    """Convierte promedio numérico a literal"""
    try:
        if promedio >= 18.00: return "AD"
        elif promedio >= 16.00: return "A"
        elif promedio >= 14.00: return "B"
        elif promedio >= 12.00: return "C"
        elif promedio >= 11.00: return "D"
        else: return "E"
    except: return "E"

def generar_conclusion(promedio):
    """Genera conclusión descriptiva"""
    try:
        if promedio >= 18.00: return "Excelente desempeño académico"
        elif promedio >= 16.00: return "Buen desempeño académico"
        elif promedio >= 14.00: return "Desempeño satisfactorio"
        elif promedio >= 12.00: return "Desempeño regular, necesita mejorar"
        elif promedio >= 11.00: return "Desempeño mínimo, requiere apoyo"
        else: return "Necesita refuerzo urgente"
    except: return "Sin datos suficientes"

def calcular_promedios_todos_estudiantes(numero_registro):
    """Calcula promedios para todos los estudiantes usando SOLO Notas_Registro"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Obtener estudiantes del registro
        cursor.execute("""
            SELECT e.Codigo_estudiante, e.Nombre_estudiante
            FROM Estudiante e
            JOIN Estudiante_Registro er ON e.Codigo_estudiante = er.Codigo_estudiante
            WHERE er.Numero_de_registro = %s
            ORDER BY e.Nombre_estudiante
        """, (numero_registro,))
        estudiantes = cursor.fetchall()
        
        resultados = []
        for codigo_estudiante, nombre_estudiante in estudiantes:
            # Calcular promedio final desde Notas_Registro
            cursor.execute("""
                SELECT AVG(Nota) 
                FROM Notas_Registro 
                WHERE Numero_de_registro = %s AND Codigo_estudiante = %s
            """, (numero_registro, codigo_estudiante))
            
            resultado = cursor.fetchone()
            promedio_final = float(resultado[0]) if resultado and resultado[0] else 0.0
            
            resultados.append({
                'codigo_estudiante': codigo_estudiante,
                'nombre_estudiante': nombre_estudiante,
                'promedio_final': promedio_final,
                'nota_literal': convertir_a_literal(promedio_final),
                'conclusion': generar_conclusion(promedio_final)
            })
        
        cursor.close()
        conexion.close()
        return resultados
        
    except Exception as e:
        print(f"Error al calcular promedios: {e}")
        return []
    
def ventana_promedio_notas(codigo_docente, ventana_padre=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Cálculo de Promedios")
    ventana.geometry("1000x600")
    ventana.config(bg="#E3F2FD")
    
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    main_frame = tk.Frame(ventana, bg="#E3F2FD")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    titulo = tk.Label(
        main_frame,
        text="Cálculo de Promedios y Notas Literales",
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=15)
    
    # Frame de selección
    frame_seleccion = tk.LabelFrame(main_frame, text="Seleccionar Registro", 
                                  font=("Arial", 12, "bold"), bg="#E3F2FD", fg="#0D47A1")
    frame_seleccion.pack(fill="x", padx=10, pady=10)
    
    tk.Label(frame_seleccion, text="Registro:", bg="#E3F2FD", font=("Arial", 10)).pack(side="left", padx=5)
    
    combo_registros = ttk.Combobox(frame_seleccion, state="readonly", width=50)
    combo_registros.pack(side="left", padx=5)
    
    btn_calcular = tk.Button(
        frame_seleccion,
        text="Calcular Promedios",
        font=("Arial", 10, "bold"),
        bg="#388E3C",
        fg="white",
        command=lambda: calcular_promedios_registro()
    )
    btn_calcular.pack(side="left", padx=10)
    
    # Variables
    registros_dict = {}
    treeview = None
    
    def cargar_registros():
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            cursor.execute("""
                SELECT DISTINCT r.Numero_de_registro, r.Nombre_colegio, r.Año, r.Bimestre, 
                               r.Grado, r.Seccion, r.Curso
                FROM REGISTRO_AUXILIAR r
                JOIN Docente_Registro dr ON r.Numero_de_registro = dr.Numero_de_registro
                WHERE dr.Codigo_docente = %s
                ORDER BY r.Año DESC, r.Bimestre, r.Numero_de_registro DESC
            """, (codigo_docente,))
            
            registros = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            combo_registros.set('')
            combo_registros['values'] = []
            registros_dict.clear()
            
            if registros:
                valores_combo = []
                for registro in registros:
                    num_registro, colegio, año, bimestre, grado, seccion, curso = registro
                    display_text = f"Registro #{num_registro} - {colegio} - {curso} ({grado}° {seccion})"
                    valores_combo.append(display_text)
                    registros_dict[display_text] = {'numero': num_registro}
                
                combo_registros['values'] = valores_combo
            else:
                messagebox.showinfo("Información", "No tiene registros asignados")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar registros: {str(e)}")
    
    def calcular_promedios_registro():
        seleccion = combo_registros.get()
        if not seleccion or seleccion not in registros_dict:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un registro")
            return
        
        numero_registro = registros_dict[seleccion]['numero']
        
        try:
            # Limpiar tabla anterior si existe
            nonlocal treeview
            if treeview:
                treeview.destroy()
            
            # Calcular promedios
            resultados = calcular_promedios_todos_estudiantes(numero_registro)
            
            if not resultados:
                messagebox.showinfo("Información", "No hay notas registradas para calcular promedios")
                return
            
            # Contar estudiantes con y sin notas
            estudiantes_con_notas = sum(1 for r in resultados if r['promedio_final'] > 0)
            estudiantes_sin_notas = len(resultados) - estudiantes_con_notas
            
            # Crear tabla
            frame_tabla = tk.Frame(main_frame)
            frame_tabla.pack(fill="both", expand=True, pady=10)
            
            # Scrollbars
            scroll_y = tk.Scrollbar(frame_tabla)
            scroll_y.pack(side="right", fill="y")
            
            treeview = ttk.Treeview(
                frame_tabla,
                columns=("Estudiante", "Promedio Final", "Nota Literal", "Conclusión"),
                yscrollcommand=scroll_y.set,
                show="headings",
                height=12
            )
            
            scroll_y.config(command=treeview.yview)
            
            treeview.heading("Estudiante", text="Estudiante")
            treeview.heading("Promedio Final", text="Promedio Final")
            treeview.heading("Nota Literal", text="Nota Literal")
            treeview.heading("Conclusión", text="Conclusión Descriptiva")
            
            treeview.column("Estudiante", width=200)
            treeview.column("Promedio Final", width=100)
            treeview.column("Nota Literal", width=100)
            treeview.column("Conclusión", width=400)
            
            treeview.pack(fill="both", expand=True)
            
            # Insertar datos
            for resultado in resultados:
                treeview.insert("", "end", values=(
                    resultado['nombre_estudiante'],
                    f"{resultado['promedio_final']:.2f}",
                    resultado['nota_literal'],
                    resultado['conclusion']
                ))
            
            # Mensaje más informativo
            mensaje = f"Se calcularon promedios para {len(resultados)} estudiantes"
            if estudiantes_sin_notas > 0:
                mensaje += f"\n• {estudiantes_con_notas} con notas registradas"
                mensaje += f"\n• {estudiantes_sin_notas} sin notas registradas"
            
            messagebox.showinfo("Éxito", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular promedios: {str(e)}")
    
    # Cargar registros al iniciar
    cargar_registros()
    
    centrar_ventana(ventana, 1000, 600)
    
    return ventana