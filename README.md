# Rockola

**Rockola** es una aplicación de reproducción de música en Python con una interfaz gráfica que permite seleccionar y reproducir canciones de forma sencilla. Navega por tus álbumes y canciones, añade pistas a la cola de reproducción y disfruta de tu música favorita. La aplicación soporta formatos de audio MP3 y muestra carátulas de los álbumes.

## Características

- Reproducción de archivos MP3.
- Navegación por bandas y álbumes.
- Muestra de carátulas de los álbumes.
- Cola de reproducción.
- Reproducción aleatoria si la cola está vacía.

## Requisitos

- Python 3.6 o superior
- Tkinter
- Pillow
- Mutagen
- Pygame

## Instalación

Sigue estos pasos para instalar y ejecutar Rockola en tu sistema:
```sh
   Clona este repositorio en tu máquina local:
   git clone https://github.com/mirkogarin/rockola.git
   cd rockola
   python -m venv env
   source env/bin/activate  # En Windows usa `env\Scripts\activate`
   pip install -r requirements.txt
   Ejecuta la aplicación: python rockola.py
   
## Formato de carpeta

Music/
├── Banda1/
│   ├── Álbumes de estudio/
│   │   ├── Álbum1/
│   │   │   ├── 01 - Canción1.mp3
│   │   │   ├── 02 - Canción2.mp3
│   │   │   └── portada.jpg
│   └── Álbumes en vivo/
│       └── Álbum1/
│           ├── 01 - Canción1.mp3
│           ├── 02 - Canción2.mp3
│           └── portada.jpg
└── Banda2/
    └── Álbumes de estudio/
        └── Álbum1/
            ├── 01 - Canción1.mp3
            ├── 02 - Canción2.mp3
            └── portada.jpg
            

Uso:

    Al abrir la aplicación, se mostrará una ventana negra con un carrusel de álbumes en el centro.
    Usa las teclas izquierda y derecha para navegar entre los álbumes.
    Selecciona un álbum y presiona Enter para ver la lista de canciones.
    Ingresa el número de la canción que deseas reproducir. La canción seleccionada se pondrá en verde.
    Presiona Enter para reproducir la canción o Escape para deseleccionarla y elegir otra.
    La información de la canción que se está reproduciendo se mostrará en la parte inferior de la ventana.
    Funcionalidad para seleccionar artistas por letra.
    Cuando se presiona una letra, seleccionará el primer artista cuyo nombre comience con esa letra.
    Al presionar la misma letra nuevamente, se avanzará al siguiente artista que comience con esa letra

Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas o mejoras, siéntete libre de abrir un issue o un pull request.
Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
