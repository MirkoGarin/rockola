import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from mutagen.mp3 import MP3
import pygame
import time
import threading
import random

# Clase principal de la Rockola
class Rockola:
    def __init__(self, music_folder):
        # Inicialización de la clase Rockola
        self.music_folder = music_folder
        self.bands = self.load_bands()
        pygame.mixer.init()
        self.current_song = None
        self.current_start_time = None
        self.queue = []
        self.playing = threading.Event()
        self.current_album_info = None

    def load_bands(self):
        # Cargar las bandas desde la carpeta de música
        bands = []
        for band in os.listdir(self.music_folder):
            band_path = os.path.join(self.music_folder, band)
            if os.path.isdir(band_path):
                if 'Álbumes de estudio' in os.listdir(band_path) or 'Álbumes en vivo' in os.listdir(band_path):
                    bands.append(band)
        bands.sort()
        return bands

    def get_albums(self, band):
        # Obtener los álbumes de una banda específica
        albums = []
        band_path = os.path.join(self.music_folder, band)
        for album_type in ['Álbumes de estudio', 'Álbumes en vivo']:
            album_path = os.path.join(band_path, album_type)
            if os.path.exists(album_path):
                albums += [(album, album_type, band) for album in os.listdir(album_path) if os.path.isdir(os.path.join(album_path, album))]
        albums.sort(key=lambda x: x[0])
        return albums

    def get_album_details(self, band, album_type, album):
        # Obtener los detalles de un álbum específico
        album_details = {'cover': None, 'songs': []}
        album_path = os.path.join(self.music_folder, band, album_type, album)
        if not os.path.exists(album_path):
            print(f"Ruta no encontrada: {album_path}")
            return album_details
        for item in os.listdir(album_path):
            item_path = os.path.join(album_path, item)
            if item.lower().endswith(('.jpg', '.jpeg', '.png')):
                album_details['cover'] = item_path
            elif item.lower().endswith('.mp3'):
                album_details['songs'].append(item_path)
        return album_details

    def play_song(self, song_path):
        # Reproducir una canción específica
        if self.current_song:
            self.stop_song()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.current_song = song_path
        self.current_start_time = time.time()
        self.playing.set()

    def stop_song(self):
        # Detener la reproducción de la canción actual
        pygame.mixer.music.stop()
        self.current_song = None
        self.current_start_time = None
        self.playing.clear()

    def get_song_length(self, song_path):
        # Obtener la duración de una canción
        try:
            audio = MP3(song_path)
            return audio.info.length
        except Exception as e:
            print(f"Error loading {song_path}: {e}")
            return 0

    def get_elapsed_time(self):
        # Obtener el tiempo transcurrido de la canción actual
        if self.current_start_time:
            return time.time() - self.current_start_time
        return 0

    def add_to_queue(self, song_path, album_info):
        # Agregar una canción a la cola de reproducción
        self.queue.append((song_path, album_info))
        if not self.current_song:
            self.play_next_in_queue()

    def play_next_in_queue(self):
        # Reproducir la siguiente canción en la cola
        if self.queue:
            next_song, album_info = self.queue.pop(0)
            self.current_album_info = album_info
            self.play_song(next_song)
        else:
            self.play_random_song()

    def play_random_song(self):
        # Reproducir una canción aleatoria
        all_songs = []
        for band in self.bands:
            albums = self.get_albums(band)
            for album, album_type, _ in albums:
                album_details = self.get_album_details(band, album_type, album)
                all_songs.extend(album_details['songs'])
        if all_songs:
            random_song = random.choice(all_songs)
            band, album_type, album = self.get_song_album_info(random_song)
            self.current_album_info = (band, album_type, album)
            self.play_song(random_song)

    def get_song_album_info(self, song_path):
        # Obtener la información del álbum de una canción específica
        for band in self.bands:
            albums = self.get_albums(band)
            for album, album_type, _ in albums:
                album_details = self.get_album_details(band, album_type, album)
                if song_path in album_details['songs']:
                    return band, album_type, album
        return None, None, None

    def start_playback_thread(self):
        # Iniciar el hilo de reproducción
        threading.Thread(target=self.playback_thread, daemon=True).start()

    def playback_thread(self):
        # Hilo de reproducción para gestionar la cola de canciones
        while True:
            if self.playing.is_set() and not pygame.mixer.music.get_busy():
                self.play_next_in_queue()
            time.sleep(1)

# Interfaz gráfica de la Rockola
class RockolaGUI:
    def __init__(self, root, rockola):
        # Inicialización de la interfaz gráfica
        self.root = root
        self.rockola = rockola
        self.current_band = None
        self.current_album_index = 0
        self.albums = []
        self.song_number_buffer = ""
        self.selected_song_label = None
        self.artist_selection_index = {}

        self.root.title("Rockola")
        self.root.geometry("800x620")
        self.root.resizable(False, False)

        icon_path = "icono.ico"  # Cambia esto si el archivo está en otra ubicación
        if os.path.exists(icon_path):
            icon = ImageTk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon)  # Usar iconphoto para establecer el icono

        self.root.configure(bg="black")  # Fondo de la ventana principal

        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.album_frame = tk.Frame(self.main_frame, bg="black", bd=0)
        self.album_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.album_canvas = tk.Canvas(self.album_frame, height=220, bg="black", highlightthickness=0, bd=0)
        self.album_canvas.pack(expand=True, fill=tk.BOTH)

        self.album_info_label = tk.Label(self.album_frame, text="", bg="black", fg="white", bd=0, font=("Helvetica", 14))
        self.album_info_label.pack(pady=(10, 0))

        self.song_frame = tk.Frame(self.main_frame, bg="black", bd=0)
        self.song_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(10, 0))

        self.footer_frame = tk.Frame(self.main_frame, bg="black", bd=0)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.song_info_label = tk.Label(self.footer_frame, text="", bg="black", fg="white", bd=0, font=("Helvetica", 14))
        self.song_info_label.pack()

        self.time_label = tk.Label(self.footer_frame, text="", bg="black", fg="white", bd=0, font=("Helvetica", 14))
        self.time_label.pack()

        self.album_images = {}  # Para mantener una referencia a las imágenes

        self.placeholder_image = self.create_placeholder_image()

        self.load_bands()
        self.update_time()

        self.root.bind("<Left>", self.scroll_left)
        self.root.bind("<Right>", self.scroll_right)
        self.root.bind("<Key>", self.on_key_press)  # Vincular el evento de teclado

        self.rockola.start_playback_thread()

        # Hacer invisible el cursor del mouse
        self.root.config(cursor="none")

    def create_placeholder_image(self, size=(220, 220)):
        # Crear una imagen de marcador de posición
        image = Image.new('RGB', size, color='gray')
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        text = "Sin Carátula"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (image.width - text_width) // 2
        text_y = (image.height - text_height) // 2
        draw.text((text_x, text_y), text, font=font, fill="white")
        return ImageTk.PhotoImage(image)

    def load_bands(self):
        # Cargar las bandas en la interfaz gráfica
        for band in self.rockola.bands:
            self.albums += self.rockola.get_albums(band)
        self.show_album()

    def show_album(self):
        # Mostrar los álbumes en la interfaz gráfica
        if not self.albums:
            return
        self.album_canvas.delete("all")

        prev_index = (self.current_album_index - 1) % len(self.albums)
        next_index = (self.current_album_index + 1) % len(self.albums)

        album_prev, album_type_prev, band_prev = self.albums[prev_index]
        album_current, album_type_current, band_current = self.albums[self.current_album_index]
        album_next, album_type_next, band_next = self.albums[next_index]

        self.show_album_cover(album_prev, album_type_prev, band_prev, 100, 50, 140, 140)
        self.show_album_cover(album_current, album_type_current, band_current, 280, 0, 220, 220)
        self.show_album_cover(album_next, album_type_next, band_next, 540, 50, 140, 140)

        self.album_info_label.config(text=f"{band_current} - {album_current}")
        self.current_band = band_current
        self.update_song_list()  # Actualiza la lista de canciones al mostrar un álbum

    def show_album_cover(self, album, album_type, band, x, y, width, height):
        # Mostrar la portada del álbum
        album_details = self.rockola.get_album_details(band, album_type, album)
        cover_path = album_details.get('cover')
        if cover_path:
            try:
                image = Image.open(cover_path)
                image = image.resize((width, height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.album_canvas.create_image(x, y, anchor=tk.NW, image=photo)
                self.album_images[f"{band}/{album}"] = photo  # Mantener una referencia a la imagen para evitar la recolección de basura
            except Exception as e:
                print(f"Error loading cover image: {e}")
                placeholder_photo = self.create_placeholder_image((width, height))
                self.album_canvas.create_image(x, y, anchor=tk.NW, image=placeholder_photo)
                self.album_images[f"{band}/{album}"] = placeholder_photo
        else:
            placeholder_photo = self.create_placeholder_image((width, height))
            self.album_canvas.create_image(x, y, anchor=tk.NW, image=placeholder_photo)
            self.album_images[f"{band}/{album}"] = placeholder_photo

    def scroll_left(self, event):
        # Desplazar hacia la izquierda en la lista de álbumes
        self.current_album_index = (self.current_album_index - 1) % len(self.albums)
        self.show_album()

    def scroll_right(self, event):
        # Desplazar hacia la derecha en la lista de álbumes
        self.current_album_index = (self.current_album_index + 1) % len(self.albums)
        self.show_album()

    def update_song_list(self):
        # Actualizar la lista de canciones del álbum seleccionado
        for widget in self.song_frame.winfo_children():
            widget.destroy()
        
        album, album_type, band = self.albums[self.current_album_index]
        self.current_album = (band, album_type, album)
        album_details = self.rockola.get_album_details(band, album_type, album)
        
        songs = album_details['songs']
        songs.sort(key=lambda x: os.path.basename(x))
        
        columns = max(1, (len(songs) + 9) // 10)
        
        for col in range(columns):
            frame = tk.Frame(self.song_frame, bg="black")
            frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
            
            listbox = tk.Listbox(frame, bg="black", fg="white", selectbackground="gray", selectforeground="black", highlightthickness=0, bd=0, activestyle="none")
            listbox.pack(expand=True, fill=tk.BOTH)
            
            start_index = col * 10
            end_index = min(start_index + 10, len(songs))
            
            for i in range(start_index, end_index):
                song = songs[i]
                song_name = os.path.splitext(os.path.basename(song))[0]  # Eliminar la extensión del archivo
                length = self.rockola.get_song_length(song)
                minutes, seconds = divmod(length, 60)
                listbox.insert(tk.END, f"{song_name} ({int(minutes)}:{int(seconds):02d})")
                
            listbox.bind('<<ListboxSelect>>', self.on_song_select)
        
        self.album_info_label.config(text=f"{band} - {album}")

    def on_song_select(self, event):
        # Manejar la selección de una canción (deshabilitado)
        listbox = event.widget
        selected_index = listbox.curselection()
        if not selected_index:
            return
        selected_song = listbox.get(selected_index)
        song_name = selected_song.split(' (', 1)[0]
        band, album_type, album = self.current_album
        album_details = self.rockola.get_album_details(band, album_type, album)
        for song in album_details['songs']:
            if os.path.basename(song) == song_name:
                album_info = (band, album_type, album)
                self.rockola.add_to_queue(song, album_info)
                break

    def on_key_press(self, event):
        # Manejar las pulsaciones de teclas
        if event.char.isdigit():
            self.song_number_buffer += event.char
            self.highlight_song_entry()  # Resaltar la entrada de la canción
        elif event.char.isalpha():
            self.select_artist_by_letter(event.char.upper())
        if len(self.song_number_buffer) == 2:
            self.selected_song_label = self.song_number_buffer
        if event.keysym == 'Return':
            self.process_song_entry()
            self.song_number_buffer = ""
            self.selected_song_label = None
        if event.keysym == 'Escape':
            self.clear_song_selection()
            self.song_number_buffer = ""

    def select_artist_by_letter(self, letter):
        # Seleccionar artista por letra
        if letter not in self.artist_selection_index:
            self.artist_selection_index[letter] = 0
        else:
            self.artist_selection_index[letter] += 1
        
        matching_bands = [band for band in self.rockola.bands if band.upper().startswith(letter)]
        if matching_bands:
            index = self.artist_selection_index[letter] % len(matching_bands)
            selected_band = matching_bands[index]
            self.current_album_index = next((i for i, album in enumerate(self.albums) if album[2] == selected_band), 0)
            self.show_album()

    def highlight_song_entry(self):
        # Resaltar la canción seleccionada
        song_number = self.song_number_buffer
        for widget in self.song_frame.winfo_children():
            listbox = widget.winfo_children()[0]
            for index in range(listbox.size()):
                song = listbox.get(index)
                if song.startswith(song_number):
                    listbox.itemconfig(index, {'bg': 'green', 'fg': 'black'})
                else:
                    listbox.itemconfig(index, {'bg': 'black', 'fg': 'white'})

    def clear_song_selection(self):
        # Limpiar la selección de la canción
        for widget in self.song_frame.winfo_children():
            listbox = widget.winfo_children()[0]
            for index in range(listbox.size()):
                listbox.itemconfig(index, {'bg': 'black', 'fg': 'white'})

    def process_song_entry(self):
        # Procesar la entrada de número de canción
        song_number = self.selected_song_label
        if not song_number:
            return
        band, album_type, album = self.current_album
        album_details = self.rockola.get_album_details(band, album_type, album)
        for song in album_details['songs']:
            if os.path.basename(song).startswith(song_number):
                album_info = (band, album_type, album)
                self.rockola.add_to_queue(song, album_info)
                break

    def update_song_info(self):
        # Actualizar la información de la canción que se está reproduciendo
        if self.rockola.current_song:
            song_name = os.path.basename(self.rockola.current_song).replace('.mp3', '')
            song_name = song_name.split(' - ', 1)[1] if ' - ' in song_name else song_name
            song_length = self.rockola.get_song_length(self.rockola.current_song)
            minutes, seconds = divmod(song_length, 60)
            if self.rockola.current_album_info:
                band, album_type, album = self.rockola.current_album_info
                self.song_info_label.config(text=f"Banda: {band}\nÁlbum: {album}\nCanción: {song_name}\nDuración: {int(minutes)}:{int(seconds):02d}")

    def update_time(self):
        # Actualizar el tiempo transcurrido de la canción que se está reproduciendo
        if self.rockola.current_song:
            elapsed_time = self.rockola.get_elapsed_time()
            minutes, seconds = divmod(elapsed_time, 60)
            self.time_label.config(text=f"Tiempo transcurrido: {int(minutes)}:{int(seconds):02d}")
        self.update_song_info()  # Asegura que la información de la canción actual se actualice
        self.root.after(1000, self.update_time)

if __name__ == "__main__":
    # Código principal para iniciar la aplicación
    music_folder = "/home/duff/Music"  # Ruta actualizada
    rockola = Rockola(music_folder)

    root = tk.Tk()
    app = RockolaGUI(root, rockola)
    root.mainloop()
