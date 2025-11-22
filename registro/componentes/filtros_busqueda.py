import tkinter as tk
from tkinter import ttk

def crear_frame_filtros(parent, actualizar_tabla=None):
    """
    Crea el frame de filtros de búsqueda
    """
    frame_filtros = tk.Frame(parent, bg="#E3F2FD")
    
    # Título de filtros
    lbl_filtros = tk.Label(
        frame_filtros,
        text="Filtros de Búsqueda:",
        font=("Arial", 10, "bold"),
        bg="#E3F2FD",
        fg="#0D47A1"
    )
    lbl_filtros.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    # Búsqueda general
    lbl_busqueda = tk.Label(frame_filtros, text="Buscar:", bg="#E3F2FD")
    lbl_busqueda.grid(row=1, column=0, padx=5, pady=2, sticky="w")
    entry_busqueda = tk.Entry(frame_filtros, width=20)
    entry_busqueda.grid(row=1, column=1, padx=5, pady=2)
    
    # Filtro por nivel
    lbl_nivel = tk.Label(frame_filtros, text="Nivel:", bg="#E3F2FD")
    lbl_nivel.grid(row=1, column=2, padx=5, pady=2, sticky="w")
    combo_nivel = ttk.Combobox(frame_filtros, width=15, state="readonly")
    combo_nivel['values'] = ['Todos', 'Primaria', 'Secundaria']
    combo_nivel.set('Todos')
    combo_nivel.grid(row=1, column=3, padx=5, pady=2)
    
    # Filtro por grado
    lbl_grado = tk.Label(frame_filtros, text="Grado:", bg="#E3F2FD")
    lbl_grado.grid(row=1, column=4, padx=5, pady=2, sticky="w")
    combo_grado = ttk.Combobox(frame_filtros, width=15, state="readonly")
    combo_grado['values'] = ['Todos', '1ro', '2do', '3ro', '4to', '5to', '6to']
    combo_grado.set('Todos')
    combo_grado.grid(row=1, column=5, padx=5, pady=2)
    
    # Botón de buscar
    btn_buscar = tk.Button(
        frame_filtros,
        text="🔍 Buscar",
        font=("Arial", 9, "bold"),
        bg="#1976D2",
        fg="white",
        width=10,
        command=lambda: aplicar_filtros(actualizar_tabla)
    )
    btn_buscar.grid(row=1, column=6, padx=10, pady=2)
    
    # Botón de limpiar
    btn_limpiar = tk.Button(
        frame_filtros,
        text="🔄 Limpiar",
        font=("Arial", 9),
        bg="#757575",
        fg="white",
        width=10,
        command=lambda: limpiar_filtros(actualizar_tabla)
    )
    btn_limpiar.grid(row=1, column=7, padx=5, pady=2)
    
    def aplicar_filtros(actualizar_func):
        """Aplica los filtros de búsqueda"""
        filtros = {
            'busqueda': entry_busqueda.get().strip(),
            'nivel': combo_nivel.get(),
            'grado': combo_grado.get()
        }
        
        if actualizar_func:
            actualizar_func(filtros)
    
    def limpiar_filtros(actualizar_func):
        """Limpia todos los filtros"""
        entry_busqueda.delete(0, tk.END)
        combo_nivel.set('Todos')
        combo_grado.set('Todos')
        
        if actualizar_func:
            actualizar_func({})
    
    def obtener_filtros():
        """Obtiene los valores actuales de los filtros"""
        return {
            'busqueda': entry_busqueda.get().strip(),
            'nivel': combo_nivel.get(),
            'grado': combo_grado.get()
        }
    
    # Guardar referencia a la función y widgets para acceso externo
    frame_filtros.obtener_filtros = obtener_filtros
    frame_filtros.entry_busqueda = entry_busqueda
    frame_filtros.combo_nivel = combo_nivel
    frame_filtros.combo_grado = combo_grado
    
    # Conectar eventos automáticos si se proporciona actualizar_tabla
    if actualizar_tabla:
        entry_busqueda.bind("<KeyRelease>", lambda e: aplicar_filtros(actualizar_tabla))
        combo_nivel.bind("<<ComboboxSelected>>", lambda e: aplicar_filtros(actualizar_tabla))
        combo_grado.bind("<<ComboboxSelected>>", lambda e: aplicar_filtros(actualizar_tabla))
    
    return frame_filtros

def obtener_filtros(frame_filtros):
    """
    Función auxiliar para obtener filtros desde fuera
    """
    if hasattr(frame_filtros, 'obtener_filtros'):
        return frame_filtros.obtener_filtros()
    return {}