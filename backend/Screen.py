import cv2
import numpy as np
import pyautogui
from filters import adaptive_filter

def process_screen():
    """
    Captura la pantalla en tiempo real, aplica un filtro adaptativo y muestra el resultado.
    Permite cambiar dinámicamente entre filtros, ajustar su intensidad y modificar el tamaño de las ventanas.
    También permite capturar toda la pantalla o una región seleccionada.
    """
    # Filtros disponibles
    filters = ["Sin Filtro", "neblina", "noche", "lluvia", "sol", "nieve"]
    current_filter_index = 0
    intensity = 1.0  # Intensidad inicial del filtro

    # Tamaño inicial de las ventanas
    window_width = 800
    window_height = 600

    # Región de captura (None para capturar toda la pantalla)
    region = None  # Cambiar a (x, y, width, height) para capturar una región específica

    # Crear ventana de controles y sliders
    cv2.namedWindow("Controles")
    cv2.createTrackbar("Filtro", "Controles", 0, 5, lambda x: None)
    cv2.createTrackbar("CLAHE s", "Controles", 4, 16, lambda x: None)
    cv2.createTrackbar("CLAHE cL", "Controles", 20, 80, lambda x: None)

    # Valores predeterminados para cada filtro: [s, cL]
    presets = {
        1: (4, 25),   # Neblina: s=4, cL=2.5
        2: (4, 25),   # Noche:   s=4, cL=2.5
        3: (8, 20),   # Lluvia:  s=8, cL=2.0
        4: (10, 40),  # Sol:     s=10, cL=4.0
        5: (8, 30),   # Nieve:   s=8, cL=3.0
    }

    prev_filter = -1

    while True:
        # Capturar la pantalla o una región específica
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()

        screen_image = np.array(screenshot)
        screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)

        # Leer sliders
        filtro = cv2.getTrackbarPos("Filtro", "Controles")
        s = cv2.getTrackbarPos("CLAHE s", "Controles")
        cL = cv2.getTrackbarPos("CLAHE cL", "Controles") / 10.0

        # Si el filtro cambió, actualiza sliders a los valores predeterminados
        if filtro != prev_filter and filtro in presets:
            preset_s, preset_cL = presets[filtro]
            cv2.setTrackbarPos("CLAHE s", "Controles", preset_s)
            cv2.setTrackbarPos("CLAHE cL", "Controles", preset_cL)
            s = preset_s
            cL = preset_cL / 10.0
        prev_filter = filtro

        # Aplicar el filtro adaptativo con los parámetros actuales
        condition = filters[filtro]
        filtered_image = adaptive_filter(screen_image, condition, s=s, cL=cL)

        # Ajustar la intensidad del filtro (si es necesario)
        filtered_image = cv2.addWeighted(screen_image, 1 - intensity, filtered_image, intensity, 0)

        # Mostrar el nombre del filtro en la imagen filtrada
        filtro_nombre = condition.capitalize() if condition else "Sin filtro"
        cv2.putText(
            filtered_image,
            f"Filtro: {filtro_nombre}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        # Redimensionar la ventana filtrada
        cv2.namedWindow("Pantalla Filtrada", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Pantalla Filtrada", window_width, window_height)

        # Mostrar la imagen filtrada
        cv2.imshow("Pantalla Filtrada", filtered_image)

        # Detectar teclas presionadas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('n'):
            current_filter_index = (current_filter_index + 1) % len(filters)
            cv2.setTrackbarPos("Filtro", "Controles", current_filter_index)
            print(f"Filtro cambiado a: {filters[current_filter_index]}")
        elif key == ord('b'):
            current_filter_index = (current_filter_index - 1) % len(filters)
            cv2.setTrackbarPos("Filtro", "Controles", current_filter_index)
            print(f"Filtro cambiado a: {filters[current_filter_index]}")
        elif key == ord('+'):
            intensity = min(intensity + 0.1, 1.0)
            print(f"Intensidad aumentada a: {intensity:.1f}")
        elif key == ord('-'):
            intensity = max(intensity - 0.1, 0.0)
            print(f"Intensidad disminuida a: {intensity:.1f}")
        elif key == ord('r'):
            region = None
            print("Capturando toda la pantalla")
        elif key == ord('m'):
            # Seleccionar región con el mouse
            temp_img = np.array(pyautogui.screenshot())
            temp_img = cv2.cvtColor(temp_img, cv2.COLOR_RGB2BGR)
            r = cv2.selectROI("Selecciona region", temp_img, showCrosshair=True, fromCenter=False)
            cv2.destroyWindow("Selecciona region")
            if r[2] > 0 and r[3] > 0:
                region = (int(r[0]), int(r[1]), int(r[2]), int(r[3]))
                print(f"Región seleccionada: {region}")
        elif key == ord('w'):
            window_height += 50
            print(f"Tamaño de ventana ajustado a: {window_width}x{window_height}")
        elif key == ord('s'):
            window_height = max(100, window_height - 50)
            print(f"Tamaño de ventana ajustado a: {window_width}x{window_height}")
        elif key == ord('a'):
            window_width = max(100, window_width - 50)
            print(f"Tamaño de ventana ajustado a: {window_width}x{window_height}")
        elif key == ord('d'):
            window_width += 50
            print(f"Tamaño de ventana ajustado a: {window_width}x{window_height}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_screen()