Rol: Eres un experto programador python 

Objetivo: Crear un editor de texto plano independiente, ligero y solo con librerias nativas de python.

## Características

- **Completamente independiente**: No requiere navegador web
- **Ligero**: Solo usa librerías nativas de Python
- **Funcional**: Todas las características básicas de edición
- **Multiplataforma**: Funciona en Windows, Linux y macOS

## Funcionalidades

### Gestión de Archivos
- Crear nuevo archivo (Ctrl+N)
- Abrir archivo desde cualquier carpeta (Ctrl+O)
- Guardar archivo (Ctrl+S)
- Guardar como (Ctrl+Shift+S)
- Guardar la configuracion automaticamente

### Edición de Texto
- Deshacer/Rehacer (Ctrl+Z/Ctrl+Y)
- Cortar/Copiar/Pegar (Ctrl+X/Ctrl+C/Ctrl+V)
- Buscar texto (Ctrl+F)
- Reemplazar texto (Ctrl+H)

### Interfaz
- Barra de herramientas con botones principales
- Barra de estado con posición del cursor y contador de caracteres
- Scrollbars horizontal y vertical
- Fuente monoespaciada para mejor legibilidad
- Ajuste de linea
- Elegir tipo de letra (Monoespaciada) y tamaño
- Elegir color de fuente y color de fondo
- Elegir visibilidad de toolbar SI/NO
- hacer undo y redo hasta 30 pasos atras o adelante, guardar los 60 pasos en el .cfg por si necesito hacerlos en la proxima sesion
- hacer autoguardado
- hacer encriptado de desencriptado con una clave para cada vez que abro la aplicacion y con la misma clave abra todos los archivos
- El metodo de encriptado tiene que tener un marcador y reiniciar cada 512 caracteres para recuperarse de un caracter corrupto con proceso de recuperacion

### Cifrado
- Metodo XOR: encripta y desencripta
- Utiliza una llave local (publica):'E1!d2#U3$a4%R5&d6=O7|r8°U9.f0_E1-i2!L3#f4$I5%o6&R7=i8|' y le agrega sobre ella la clave del usuario (privada)
- la clave la define para la sesion y encripta y desencripta todos los archivos de esa sesion con la misma clave.
- aunque el archivo encriptado estuviese corrompido no deberia perder toda la informacion, deberia desencriptar todo lo posible.

## Requisitos

- Python 3.x (tkinter incluido por defecto)
- No requiere instalación de paquetes adicionales
- Compilar el editor de texto en un ejecutable portable de Windows (.exe) que no requiere instalación.