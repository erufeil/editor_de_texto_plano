import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import os

class EditorTexto:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Editor de Texto Simple")
        self.root.geometry("800x600")
        self.root.minsize(400, 300)
        
        # Variables
        self.archivo_actual = None
        self.texto_modificado = False
        
        # Configurar interfaz
        self.crear_menu()
        self.crear_toolbar()
        self.crear_area_texto()
        self.crear_barra_estado()
        
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
        
    def crear_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        
        ttk.Button(toolbar, text="Nuevo", command=self.nuevo_archivo).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Abrir", command=self.abrir_archivo).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Guardar", command=self.guardar_archivo).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(toolbar, text="Cortar", command=self.cortar).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Copiar", command=self.copiar).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Pegar", command=self.pegar).pack(side=tk.LEFT, padx=2)
        
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
            font=("Consolas", 11),
            bg="white",
            fg="black",
            insertbackground="black",
            selectbackground="#316AC5"
        )
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(frame_texto, orient=tk.VERTICAL, command=self.area_texto.yview)
        scrollbar_h = ttk.Scrollbar(frame_texto, orient=tk.HORIZONTAL, command=self.area_texto.xview)
        
        self.area_texto.config(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Posicionar elementos
        self.area_texto.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")
        
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
                
    def salir(self):
        if self.verificar_cambios():
            self.root.quit()
            
    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    editor = EditorTexto()
    editor.ejecutar()
