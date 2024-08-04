#!/bin/bash

# Verificar si Python 3.6 o superior está instalado
if ! command -v python3 &> /dev/null
then
    echo "Python 3.6 o superior no está instalado. Instalando..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
fi

# Verificar si tkinter está instalado
if ! python3 -c "import tkinter" &> /dev/null
then
    echo "Tkinter no está instalado. Instalando..."
    sudo apt install -y python3-tk
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null
then
    echo "pip no está instalado. Instalando..."
    sudo apt install -y python3-pip
fi

# Crear y activar el entorno virtual
python3 -m venv env
source env/bin/activate

# Instalar las dependencias
pip install pillow mutagen pygame

# Ejecutar la aplicación
python rockola.py &

# Crear archivo .desktop
DESKTOP_FILE=~/.local/share/applications/rockola.desktop

echo "[Desktop Entry]
Version=1.0
Name=Rockola
Comment=Rockola Music Player
Exec=$(pwd)/install_and_run.sh
Icon=$(pwd)/icono.ico
Terminal=false
Type=Application
Categories=Application;AudioVideo;" > $DESKTOP_FILE

chmod +x $DESKTOP_FILE

echo "Instalación completa. Puedes encontrar Rockola en tu menú de aplicaciones."
