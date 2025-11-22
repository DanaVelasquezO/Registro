import tkinter as tk
from tkinter import ttk, messagebox
from db.conexion import obtener_conexion
from registro.crear_registro import ventana_crear_registro
from registro.ver_registros import ventana_ver_registros
# from registro.editar_registro import ventana_editar_registro  # COMENTAR TEMPORALMENTE
from registro.gestion_competencias import ventana_gestion_competencias

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def ventana_gestion_registros(ventana_padre=None):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Gestión de Registros Auxiliares")
    ventana.geometry("500x500")
    ventana.config(bg="#E3F2FD")
    ventana.resizable(False, False)
    
    ventana.transient(ventana_padre)
    ventana.grab_set()
    
    # Título
    titulo = tk.Label(
        ventana,
        text="Gestión de Registros Auxiliares",
        font=("Arial", 16, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    titulo.pack(pady=30)
    
    # Frame de botones
    frame_botones = tk.Frame(ventana, bg="#E3F2FD")
    frame_botones.pack(pady=20, padx=50, fill="both", expand=True)
    
    # Botón Crear Registro
    btn_crear = tk.Button(
        frame_botones,
        text="Crear Nuevo Registro",
        font=("Arial", 12, "bold"),
        bg="#388E3C",
        fg="white",
        width=25,
        height=2,
        command=lambda: ventana_crear_registro(ventana, actualizar_estadisticas)
    )
    btn_crear.pack(pady=15)
    
    # Botón Ver Registros
    btn_ver = tk.Button(
        frame_botones,
        text="Ver Todos los Registros",
        font=("Arial", 12, "bold"),
        bg="#1976D2",
        fg="white",
        width=25,
        height=2,
        command=lambda: ventana_ver_registros(ventana)
    )
    btn_ver.pack(pady=15)
    
    # Botón Gestionar Competencias
    btn_competencias = tk.Button(
        frame_botones,
        text="Gestionar Competencias",
        font=("Arial", 12, "bold"),
        bg="#7B1FA2",
        fg="white",
        width=25,
        height=2,
        command=lambda: ventana_gestion_competencias(ventana)
    )
    btn_competencias.pack(pady=15)
    
    # Frame de estadísticas
    frame_stats = tk.Frame(ventana, bg="#E3F2FD")
    frame_stats.pack(pady=20, padx=50, fill="x")
    
    lbl_estadisticas = tk.Label(
        frame_stats,
        text="Cargando estadísticas...",
        font=("Arial", 10),
        bg="#E3F2FD",
        fg="#666666"
    )
    lbl_estadisticas.pack()
    
    def actualizar_estadisticas():
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Contar registros totales
            cursor.execute("SELECT COUNT(*) FROM REGISTRO_AUXILIAR")
            total_registros = cursor.fetchone()[0]
            
            # Contar registros por nivel
            cursor.execute("""
                SELECT Nivel, COUNT(*) 
                FROM REGISTRO_AUXILIAR 
                GROUP BY Nivel
            """)
            niveles = cursor.fetchall()
            
            # Contar competencias definidas
            cursor.execute("SELECT COUNT(*) FROM Competencias")
            total_competencias = cursor.fetchone()[0]
            
            cursor.close()
            conexion.close()
            
            # Construir texto de estadísticas
            texto_stats = f"Estadísticas: {total_registros} registros totales"
            if niveles:
                texto_stats += " | "
                texto_stats += " | ".join([f"{nivel}: {cant}" for nivel, cant in niveles])
            texto_stats += f" | {total_competencias} competencias"
            
            lbl_estadisticas.config(text=texto_stats)
            
        except Exception as e:
            lbl_estadisticas.config(text="Error al cargar estadísticas")
    
    # Botón Cerrar
    btn_cerrar = tk.Button(
        ventana,
        text="Cerrar",
        font=("Arial", 10),
        bg="#757575",
        fg="white",
        width=15,
        command=ventana.destroy
    )
    btn_cerrar.pack(pady=10)
    
    # Cargar estadísticas iniciales
    actualizar_estadisticas()
    
    # Centrar ventana
    centrar_ventana(ventana, 500, 500)
    
    return ventana