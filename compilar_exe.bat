@echo off
echo ========================================
echo    Compilando Editor de Texto a EXE
echo ========================================
echo.

REM Limpiar compilaciones anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist editor_texto.spec del /f /q editor_texto.spec

echo Compilando con PyInstaller...
echo.

REM Compilar con PyInstaller
REM --onefile: Crea un solo archivo ejecutable
REM --windowed: Sin ventana de consola (solo la GUI)
REM --name: Nombre del ejecutable
REM --icon: Icono (opcional, comentado por ahora)
REM --clean: Limpiar cache antes de compilar

python -m PyInstaller --onefile --windowed --name "Editor_Texto" --clean editor_texto.py

echo.
echo ========================================
echo    Compilacion completada
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\Editor_Texto.exe
echo.
echo Puedes copiar ese archivo a cualquier lugar y ejecutarlo sin instalacion.
echo.
pause
