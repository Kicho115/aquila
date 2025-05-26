import cv2
import numpy as np
import pyautogui
from filtros import adaptive_filter

def process_screen():
    """
    Captura la pantalla en tiempo real, aplica un filtro adaptativo y muestra el resultado.
    Permite cambiar dinámicamente entre filtros, ajustar su intensidad y modificar el tamaño de las ventanas.
    También permite capturar toda la pantalla o una región seleccionada.
    """
    # Filtros disponibles
    filters = ["lluvia", "noche", "sol", "nieve", "neblina"]
    current_filter_index = 0
    intensity = 1.0  # Intensidad inicial del filtro

    # Tamaño inicial de las ventanas
    window_width = 800
    window_height = 600

    # Región de captura (None para capturar toda la pantalla)
    region = None  # Cambiar a (x, y, width, height) para capturar una región específica

    while True:
        # Capturar la pantalla o una región específica
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()

        # Convertir la captura a un array de NumPy (formato compatible con OpenCV)
        screen_image = np.array(screenshot)

        # Convertir de RGB (PyAutoGUI) a BGR (OpenCV)
        screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)

        # Aplicar el filtro adaptativo con la intensidad actual
        condition = filters[current_filter_index]
        filtered_image = adaptive_filter(screen_image, condition)

        # Ajustar la intensidad del filtro (si es necesario)
        filtered_image = cv2.addWeighted(screen_image, 1 - intensity, filtered_image, intensity, 0)

        # Redimensionar las ventanas
        cv2.namedWindow("Pantalla Original", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Pantalla Filtrada", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Pantalla Original", window_width, window_height)
        cv2.resizeWindow("Pantalla Filtrada", window_width, window_height)

        # Mostrar la imagen original y la filtrada
        cv2.imshow("Pantalla Original", screen_image)
        cv2.imshow("Pantalla Filtrada", filtered_image)

        # Detectar teclas presionadas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Salir si se presiona la tecla 'q'
            break
        elif key == ord('n'):  # Cambiar al siguiente filtro
            current_filter_index = (current_filter_index + 1) % len(filters)
            print(f"Filtro cambiado a: {filters[current_filter_index]}")
        elif key == ord('b'):  # Cambiar al filtro anterior
            current_filter_index = (current_filter_index - 1) % len(filters)
            print(f"Filtro cambiado a: {filters[current_filter_index]}")
        elif key == ord('+'):  # Aumentar la intensidad
            intensity = min(intensity + 0.1, 1.0)
            print(f"Intensidad aumentada a: {intensity:.1f}")
        elif key == ord('-'):  # Disminuir la intensidad
            intensity = max(intensity - 0.1, 0.0)
            print(f"Intensidad disminuida a: {intensity:.1f}")
        elif key == ord('r'):  # Alternar entre captura de pantalla completa y región
            if region is None:
                # Cambiar a una región específica (ejemplo: esquina superior izquierda de 800x600)
                region = (0, 0, 800, 600)
                print("Capturando región: (0, 0, 800, 600)")
            else:
                # Cambiar a captura de pantalla completa
                region = None
                print("Capturando toda la pantalla")
        elif key == ord('w'):  # Aumentar el alto de las ventanas
            window_height += 50
            print(f"Tamaño de ventana ajustado a: {window_width}x{window_height}")
        elif key == ord('s'):  # Disminuir el alto de las ventanas
            window_height = max(100, window_height - 50)
            print(f"Tamaño de ventana ajustado a: {window_width}x{window_height}")
        elif key == ord('a'):  # Disminuir el ancho de las ventanas
            window_width = max(100, window_width - 50)
            print(f"Tamaño de ventana ajustado a: {window_width}x{window_height}")
        elif key == ord('d'):  # Aumentar el ancho de las ventanas
            window_width += 50
            print(f"Tamaño de ventana ajustado a: {window_width}x{window_height}")

    # Cerrar todas las ventanas
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Procesar la pantalla en tiempo real con filtros dinámicos
    process_screen()