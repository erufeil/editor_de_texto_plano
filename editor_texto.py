import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from tkinter import font as tkfont
import os
import json

class EditorTexto:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Editor de Texto Simple")
        self.root.geometry("800x600")
        self.root.minsize(400, 300)

        # Ruta del archivo de configuración
        self.config_file = os.path.join(os.path.dirname(__file__), "editor_texto.cfg")

        # Variables
        self.archivo_actual = None
        self.texto_modificado = False
        self.ajuste_linea = False  # controla el ajuste de línea (wrap)
        # Variable para el estado del checkbutton en el menú Ver
        self.ajuste_linea_var = tk.BooleanVar(value=False)
        self.toolbar_visible_var = tk.BooleanVar(value=True)

        # Configuración de fuente y colores
        self.fuente_actual = "Consolas"
        self.tamanio_fuente = 11
        self.fuentes_mono_disponibles = []
        self.color_fuente = "black"
        self.color_fondo = "white"

        # Cargar configuración
        self.cargar_configuracion()

        # Configurar interfaz
        self.crear_menu()
        self.crear_toolbar()
        self.crear_area_texto()
        self.crear_barra_estado()

        # Aplicar configuración de interfaz después de crear los widgets
        self.aplicar_configuracion_interfaz()

        # Configurar eventos
        self.configurar_eventos()

        # Configurar atajos de teclado
        self.configurar_atajos()
        
    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo", command=self.nuevo_archivo, accelerator="Ctrl+N")
        menu_archivo.add_command(label="Abrir", command=self.abrir_archivo, accelerator="Ctrl+O")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Guardar", command=self.guardar_archivo, accelerator="Ctrl+S")
        menu_archivo.add_command(label="Guardar como", command=self.guardar_como, accelerator="Ctrl+Shift+S")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.salir, accelerator="Ctrl+Q")
        
        # Menú Editar
        menu_editar = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=menu_editar)
        menu_editar.add_command(label="Deshacer", command=self.deshacer, accelerator="Ctrl+Z")
        menu_editar.add_command(label="Rehacer", command=self.rehacer, accelerator="Ctrl+Y")
        menu_editar.add_separator()
        menu_editar.add_command(label="Cortar", command=self.cortar, accelerator="Ctrl+X")
        menu_editar.add_command(label="Copiar", command=self.copiar, accelerator="Ctrl+C")
        menu_editar.add_command(label="Pegar", command=self.pegar, accelerator="Ctrl+V")
        menu_editar.add_separator()
        menu_editar.add_command(label="Buscar", command=self.buscar, accelerator="Ctrl+F")
        menu_editar.add_command(label="Reemplazar", command=self.reemplazar, accelerator="Ctrl+H")
        
        # Menú Ver
        menu_ver = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=menu_ver)
        # Ajuste de línea: al activarlo, Text.wrap = 'word' y ocultar scrollbar horizontal
        menu_ver.add_checkbutton(label="Ajuste de línea", command=self.toggle_ajuste_linea, variable=self.ajuste_linea_var)
        menu_ver.add_checkbutton(label="Barra de herramientas", command=self.toggle_toolbar, variable=self.toolbar_visible_var)

        # Menú Formato
        menu_formato = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Formato", menu=menu_formato)
        menu_formato.add_command(label="Fuente...", command=self.cambiar_fuente)
        menu_formato.add_command(label="Tamaño de fuente...", command=self.cambiar_tamanio_fuente)
        menu_formato.add_separator()
        menu_formato.add_command(label="Color de fuente...", command=self.cambiar_color_fuente)
        menu_formato.add_command(label="Color de fondo...", command=self.cambiar_color_fondo)
        
    def crear_toolbar(self):
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        ttk.Button(self.toolbar, text="Nuevo", command=self.nuevo_archivo).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Abrir", command=self.abrir_archivo).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Guardar", command=self.guardar_archivo).pack(side=tk.LEFT, padx=2)

        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        ttk.Button(self.toolbar, text="Cortar", command=self.cortar).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Copiar", command=self.copiar).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Pegar", command=self.pegar).pack(side=tk.LEFT, padx=2)
        
    def crear_area_texto(self):
        # Frame para el área de texto con scrollbars
        frame_texto = ttk.Frame(self.root)
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Área de texto
        self.area_texto = tk.Text(
            frame_texto,
            wrap=tk.NONE,
            undo=True,
            maxundo=50,
            font=(self.fuente_actual, self.tamanio_fuente),
            bg=self.color_fondo,
            fg=self.color_fuente,
            insertbackground=self.color_fuente,
            selectbackground="#316AC5"
        )
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(frame_texto, orient=tk.VERTICAL, command=self.area_texto.yview)
        self.scrollbar_h = ttk.Scrollbar(frame_texto, orient=tk.HORIZONTAL, command=self.area_texto.xview)

        self.area_texto.config(yscrollcommand=scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)

        # Posicionar elementos
        self.area_texto.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        self.scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        frame_texto.grid_rowconfigure(0, weight=1)
        frame_texto.grid_columnconfigure(0, weight=1)
        
    def crear_barra_estado(self):
        self.barra_estado = ttk.Frame(self.root)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.label_posicion = ttk.Label(self.barra_estado, text="Línea: 1, Columna: 1")
        self.label_posicion.pack(side=tk.LEFT, padx=5)
        
        self.label_caracteres = ttk.Label(self.barra_estado, text="Caracteres: 0")
        self.label_caracteres.pack(side=tk.RIGHT, padx=5)
        
    def configurar_eventos(self):
        self.area_texto.bind('<KeyRelease>', self.actualizar_barra_estado)
        self.area_texto.bind('<KeyPress>', self.auto_scroll)
        self.area_texto.bind('<Button-1>', self.actualizar_barra_estado)
        self.area_texto.bind('<<Modified>>', self.texto_modificado_evento)
        self.root.protocol("WM_DELETE_WINDOW", self.salir)
        
    def configurar_atajos(self):
        self.root.bind('<Control-n>', lambda e: self.nuevo_archivo())
        self.root.bind('<Control-o>', lambda e: self.abrir_archivo())
        self.root.bind('<Control-s>', lambda e: self.guardar_archivo())
        self.root.bind('<Control-Shift-S>', lambda e: self.guardar_como())
        self.root.bind('<Control-q>', lambda e: self.salir())
        self.root.bind('<Control-z>', lambda e: self.deshacer())
        self.root.bind('<Control-y>', lambda e: self.rehacer())
        self.root.bind('<Control-x>', lambda e: self.cortar())
        self.root.bind('<Control-c>', lambda e: self.copiar())
        self.root.bind('<Control-v>', lambda e: self.pegar())
        self.root.bind('<Control-f>', lambda e: self.buscar())
        self.root.bind('<Control-h>', lambda e: self.reemplazar())
        self.root.bind('<Control-l>', lambda e: self.toggle_ajuste_linea())
        
    def auto_scroll(self, event):
        """Hace scroll automático para mantener el cursor visible con margen."""
        # Obtener la línea actual del cursor
        cursor_line = int(self.area_texto.index(tk.INSERT).split('.')[0])

        # Obtener la línea visible en la parte superior e inferior
        top_line = int(self.area_texto.index("@0,0").split('.')[0])
        bottom_line = int(self.area_texto.index(f"@0,{self.area_texto.winfo_height()}").split('.')[0])

        # Calcular un margen (número de líneas de contexto)
        visible_lines = bottom_line - top_line
        margen = max(3, visible_lines // 4)  # Al menos 3 líneas o 25% del área visible

        # Si el cursor está muy cerca del borde inferior, hacer scroll
        if cursor_line >= bottom_line - margen:
            # Posicionar el cursor en el centro-inferior de la pantalla
            target_line = cursor_line - (visible_lines // 2)
            self.area_texto.see(f"{max(1, target_line)}.0")

        # Asegurar que el cursor esté visible
        self.area_texto.see(tk.INSERT)

    def actualizar_barra_estado(self, event=None):
        # Obtener posición del cursor
        cursor_pos = self.area_texto.index(tk.INSERT)
        linea, columna = cursor_pos.split('.')
        self.label_posicion.config(text=f"Línea: {linea}, Columna: {int(columna)+1}")

        # Contar caracteres
        contenido = self.area_texto.get("1.0", tk.END)
        num_caracteres = len(contenido) - 1  # -1 para excluir el último \n
        self.label_caracteres.config(text=f"Caracteres: {num_caracteres}")
        
    def texto_modificado_evento(self, event=None):
        if self.area_texto.edit_modified():
            self.texto_modificado = True
            self.actualizar_titulo()
            self.area_texto.edit_modified(False)
            
    def actualizar_titulo(self):
        titulo = "Editor de Texto Simple"
        if self.archivo_actual:
            nombre_archivo = os.path.basename(self.archivo_actual)
            titulo = f"{nombre_archivo} - {titulo}"
        if self.texto_modificado:
            titulo = f"*{titulo}"
        self.root.title(titulo)
        
    def nuevo_archivo(self):
        if self.verificar_cambios():
            self.area_texto.delete("1.0", tk.END)
            self.archivo_actual = None
            self.texto_modificado = False
            self.actualizar_titulo()
            
    def abrir_archivo(self):
        if self.verificar_cambios():
            archivo = filedialog.askopenfilename(
                title="Abrir archivo",
                filetypes=[
                    ("Archivos de texto", "*.txt"),
                    ("Todos los archivos", "*.*")
                ]
            )
            if archivo:
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                    self.area_texto.delete("1.0", tk.END)
                    self.area_texto.insert("1.0", contenido)
                    self.archivo_actual = archivo
                    self.texto_modificado = False
                    self.actualizar_titulo()
                    self.guardar_configuracion()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")
                    
    def guardar_archivo(self):
        if self.archivo_actual:
            try:
                contenido = self.area_texto.get("1.0", tk.END + "-1c")
                with open(self.archivo_actual, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                self.texto_modificado = False
                self.actualizar_titulo()
                return True
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
                return False
        else:
            return self.guardar_como()
            
    def guardar_como(self):
        archivo = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        if archivo:
            try:
                contenido = self.area_texto.get("1.0", tk.END + "-1c")
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                self.archivo_actual = archivo
                self.texto_modificado = False
                self.actualizar_titulo()
                self.guardar_configuracion()
                return True
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
                return False
        return False
        
    def verificar_cambios(self):
        if self.texto_modificado:
            respuesta = messagebox.askyesnocancel(
                "Cambios sin guardar",
                "¿Desea guardar los cambios antes de continuar?"
            )
            if respuesta is True:
                return self.guardar_archivo()
            elif respuesta is False:
                return True
            else:
                return False
        return True
        
    def deshacer(self):
        try:
            self.area_texto.edit_undo()
        except tk.TclError:
            pass
            
    def rehacer(self):
        try:
            self.area_texto.edit_redo()
        except tk.TclError:
            pass
            
    def cortar(self):
        try:
            self.area_texto.event_generate("<<Cut>>")
        except tk.TclError:
            pass
            
    def copiar(self):
        try:
            self.area_texto.event_generate("<<Copy>>")
        except tk.TclError:
            pass
            
    def pegar(self):
        try:
            self.area_texto.event_generate("<<Paste>>")
        except tk.TclError:
            pass
            
    def buscar(self):
        texto_buscar = simpledialog.askstring("Buscar", "Ingrese el texto a buscar:")
        if texto_buscar:
            start_pos = self.area_texto.search(texto_buscar, tk.INSERT, tk.END)
            if start_pos:
                end_pos = f"{start_pos}+{len(texto_buscar)}c"
                self.area_texto.tag_remove(tk.SEL, "1.0", tk.END)
                self.area_texto.tag_add(tk.SEL, start_pos, end_pos)
                self.area_texto.mark_set(tk.INSERT, end_pos)
                self.area_texto.see(start_pos)
            else:
                messagebox.showinfo("Buscar", "Texto no encontrado")
                
    def reemplazar(self):
        texto_buscar = simpledialog.askstring("Reemplazar", "Texto a buscar:")
        if texto_buscar:
            texto_reemplazar = simpledialog.askstring("Reemplazar", "Reemplazar con:")
            if texto_reemplazar is not None:
                contenido = self.area_texto.get("1.0", tk.END)
                nuevo_contenido = contenido.replace(texto_buscar, texto_reemplazar)
                self.area_texto.delete("1.0", tk.END)
                self.area_texto.insert("1.0", nuevo_contenido)

    def toggle_ajuste_linea(self):
        """Alterna el ajuste de línea (wrap) entre NONE y WORD.

        Cuando el ajuste está activado se usa wrap='word' y se oculta la barra horizontal.
        Cuando está desactivado se usa wrap='none' y se muestra la barra horizontal.
        """
        # Obtener el estado actual de la variable (ya modificado por el checkbutton)
        nuevo_estado = self.ajuste_linea_var.get()
        self.ajuste_linea = nuevo_estado

        if nuevo_estado:
            self.area_texto.config(wrap=tk.WORD)
            # ocultar scrollbar horizontal
            self.scrollbar_h.grid_remove()
        else:
            self.area_texto.config(wrap=tk.NONE)
            # volver a mostrar scrollbar horizontal
            self.scrollbar_h.grid(row=1, column=0, sticky="ew")

        # Guardar configuración al cambiar
        self.guardar_configuracion()

    def toggle_toolbar(self):
        """Muestra u oculta la barra de herramientas."""
        if self.toolbar_visible_var.get():
            self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2, before=self.area_texto.master)
        else:
            self.toolbar.pack_forget()
        # Guardar configuración al cambiar
        self.guardar_configuracion()

    def cargar_configuracion(self):
        """Carga la configuración desde el archivo .cfg"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # Aplicar configuraciones
                self.ajuste_linea_var.set(config.get('ajuste_linea', False))
                self.toolbar_visible_var.set(config.get('toolbar_visible', True))
                self.archivo_actual = config.get('ultimo_archivo', None)
                self.fuente_actual = config.get('fuente', 'Consolas')
                self.tamanio_fuente = config.get('tamanio_fuente', 11)
                self.color_fuente = config.get('color_fuente', 'black')
                self.color_fondo = config.get('color_fondo', 'white')

        except Exception as e:
            # Si hay error al cargar, usar valores por defecto
            print(f"Error al cargar configuración: {e}")

    def guardar_configuracion(self):
        """Guarda la configuración actual en el archivo .cfg"""
        try:
            config = {
                'ajuste_linea': self.ajuste_linea_var.get(),
                'toolbar_visible': self.toolbar_visible_var.get(),
                'ultimo_archivo': self.archivo_actual,
                'fuente': self.fuente_actual,
                'tamanio_fuente': self.tamanio_fuente,
                'color_fuente': self.color_fuente,
                'color_fondo': self.color_fondo
            }

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)

        except Exception as e:
            print(f"Error al guardar configuración: {e}")

    def aplicar_configuracion_interfaz(self):
        """Aplica la configuración cargada a la interfaz"""
        # Aplicar ajuste de línea
        if self.ajuste_linea_var.get():
            self.area_texto.config(wrap=tk.WORD)
            self.scrollbar_h.grid_remove()
        else:
            self.area_texto.config(wrap=tk.NONE)
            self.scrollbar_h.grid(row=1, column=0, sticky="ew")

        # Aplicar visibilidad de toolbar
        if not self.toolbar_visible_var.get():
            self.toolbar.pack_forget()

        # Cargar el último archivo si existe
        if self.archivo_actual and os.path.exists(self.archivo_actual):
            try:
                with open(self.archivo_actual, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                self.area_texto.delete("1.0", tk.END)
                self.area_texto.insert("1.0", contenido)
                self.texto_modificado = False
                self.actualizar_titulo()
            except Exception:
                self.archivo_actual = None
        else:
            if self.archivo_actual:
                # El archivo no existe, limpiar la referencia
                self.archivo_actual = None

    def detectar_fuentes_mono(self):
        """Detecta las fuentes monoespaciadas disponibles en el sistema"""
        fuentes_deseadas = [
            "Consolas",
            "Courier New",
            "Lucida Console",
            "Source Code Pro",
            "Cascadia Code",
            "Cascadia Mono",
            "Segoe UI Mono",
            "Terminal",
            "Courier",
            "DejaVu Sans Mono",
            "Liberation Mono",
            "Menlo",
            "Monaco"
        ]

        # Obtener todas las fuentes del sistema
        fuentes_sistema = list(tkfont.families())

        # Filtrar solo las fuentes monoespaciadas que están disponibles
        fuentes_disponibles = []
        for fuente in fuentes_deseadas:
            if fuente in fuentes_sistema:
                fuentes_disponibles.append(fuente)

        return fuentes_disponibles if fuentes_disponibles else ["Courier New", "Courier"]

    def cambiar_fuente(self):
        """Muestra un diálogo para seleccionar la fuente"""
        # Detectar fuentes disponibles
        self.fuentes_mono_disponibles = self.detectar_fuentes_mono()

        # Crear ventana de diálogo
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Seleccionar Fuente")
        dialogo.geometry("350x200")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        # Centrar el diálogo
        dialogo.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialogo.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialogo.winfo_height()) // 2
        dialogo.geometry(f"+{x}+{y}")

        # Label
        ttk.Label(dialogo, text="Seleccione una fuente monoespaciada:").pack(pady=10)

        # Listbox con scrollbar
        frame_lista = ttk.Frame(dialogo)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, height=6)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Llenar la lista con las fuentes disponibles
        for fuente in self.fuentes_mono_disponibles:
            listbox.insert(tk.END, fuente)

        # Seleccionar la fuente actual
        try:
            idx = self.fuentes_mono_disponibles.index(self.fuente_actual)
            listbox.selection_set(idx)
            listbox.see(idx)
        except ValueError:
            listbox.selection_set(0)

        # Botones
        frame_botones = ttk.Frame(dialogo)
        frame_botones.pack(pady=10)

        def aplicar():
            seleccion = listbox.curselection()
            if seleccion:
                self.fuente_actual = self.fuentes_mono_disponibles[seleccion[0]]
                self.area_texto.config(font=(self.fuente_actual, self.tamanio_fuente))
                self.guardar_configuracion()
                dialogo.destroy()

        ttk.Button(frame_botones, text="Aceptar", command=aplicar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=dialogo.destroy).pack(side=tk.LEFT, padx=5)

        # Permitir doble clic para seleccionar
        listbox.bind('<Double-Button-1>', lambda _: aplicar())

    def cambiar_tamanio_fuente(self):
        """Muestra un diálogo para seleccionar el tamaño de fuente"""
        # Crear ventana de diálogo
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Tamaño de Fuente")
        dialogo.geometry("300x150")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        # Centrar el diálogo
        dialogo.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialogo.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialogo.winfo_height()) // 2
        dialogo.geometry(f"+{x}+{y}")

        # Label
        ttk.Label(dialogo, text="Seleccione el tamaño de fuente:").pack(pady=10)

        # Frame para el spinbox
        frame_tamanio = ttk.Frame(dialogo)
        frame_tamanio.pack(pady=10)

        spinbox = ttk.Spinbox(
            frame_tamanio,
            from_=6,
            to=72,
            width=10,
            justify=tk.CENTER
        )
        spinbox.set(self.tamanio_fuente)
        spinbox.pack()

        # Botones
        frame_botones = ttk.Frame(dialogo)
        frame_botones.pack(pady=10)

        def aplicar():
            try:
                nuevo_tamanio = int(spinbox.get())
                if 6 <= nuevo_tamanio <= 72:
                    self.tamanio_fuente = nuevo_tamanio
                    self.area_texto.config(font=(self.fuente_actual, self.tamanio_fuente))
                    self.guardar_configuracion()
                    dialogo.destroy()
                else:
                    messagebox.showerror("Error", "El tamaño debe estar entre 6 y 72")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

        ttk.Button(frame_botones, text="Aceptar", command=aplicar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=dialogo.destroy).pack(side=tk.LEFT, padx=5)

    def cambiar_color_fuente(self):
        """Muestra un diálogo para seleccionar el color de la fuente"""
        from tkinter import colorchooser

        # Mostrar el selector de color
        color = colorchooser.askcolor(
            color=self.color_fuente,
            title="Seleccionar color de fuente"
        )

        # color devuelve una tupla: ((R, G, B), '#RRGGBB')
        if color[1]:
            self.color_fuente = color[1]
            self.area_texto.config(fg=self.color_fuente, insertbackground=self.color_fuente)
            self.guardar_configuracion()

    def cambiar_color_fondo(self):
        """Muestra un diálogo para seleccionar el color de fondo"""
        from tkinter import colorchooser

        # Mostrar el selector de color
        color = colorchooser.askcolor(
            color=self.color_fondo,
            title="Seleccionar color de fondo"
        )

        # color devuelve una tupla: ((R, G, B), '#RRGGBB')
        if color[1]:
            self.color_fondo = color[1]
            self.area_texto.config(bg=self.color_fondo)
            self.guardar_configuracion()

    def salir(self):
        if self.verificar_cambios():
            self.root.quit()
            
    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    editor = EditorTexto()
    editor.ejecutar()
