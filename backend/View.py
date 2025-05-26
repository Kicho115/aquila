import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Importa las funciones del backend
from Screen import process_screen
from Masks import acceder_camara_con_filtros

# Variables de control para evitar ejecuciones múltiples
screen_running = False
camera_running = False

def run_screen():
    global screen_running, camera_running
    if screen_running:
        messagebox.showinfo("Aviso", "La captura de pantalla ya está en ejecución.")
        return
    if camera_running:
        messagebox.showwarning(
            "Funcionalidad activa",
            "La cámara está en uso.\nPor favor, cierra la ventana de la cámara antes de iniciar la captura de pantalla."
        )
        return
    screen_running = True
    try:
        process_screen()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al capturar la pantalla:\n{e}")
    finally:
        screen_running = False

def run_camera():
    global camera_running, screen_running
    if camera_running:
        messagebox.showinfo("Aviso", "La cámara ya está en ejecución.")
        return
    if screen_running:
        messagebox.showwarning(
            "Funcionalidad activa",
            "La captura de pantalla está en uso.\nPor favor, cierra la ventana de la pantalla antes de iniciar la cámara."
        )
        return
    camera_running = True
    try:
        acceder_camara_con_filtros()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al acceder a la cámara:\n{e}")
    finally:
        camera_running = False

def start_thread(target):
    t = threading.Thread(target=target)
    t.daemon = True
    t.start()

root = tk.Tk()
root.title("Aquila - Filtros de Imagen")
root.geometry("400x250")

label = ttk.Label(root, text="Selecciona una opción:", font=("Arial", 14))
label.pack(pady=20)

btn_screen = ttk.Button(root, text="Capturar Pantalla con Filtros", command=lambda: start_thread(run_screen))
btn_screen.pack(pady=10, ipadx=10, ipady=5)

btn_camera = ttk.Button(root, text="Cámara con Filtros", command=lambda: start_thread(run_camera))
btn_camera.pack(pady=10, ipadx=10, ipady=5)

info = ttk.Label(
    root,
    text="Usa los controles de OpenCV para cambiar filtros y parámetros.\nPresiona 'q' para cerrar la ventana de filtros.",
    font=("Arial", 9)
)
info.pack(pady=20)

root.mainloop()