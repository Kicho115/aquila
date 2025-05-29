import cv2
import numpy as np
from filters import adaptive_filter
from detection import detect_y_draw

def nothing(x):
    pass

def acceder_camara_con_filtros():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return

    cv2.namedWindow("Controles")
    cv2.createTrackbar("Filtro", "Controles", 0, 5, nothing)  # 0: Sin filtro, 1: Neblina/Noche, 2: Lluvia, 3: Sol, 4: Nieve
    cv2.createTrackbar("CLAHE s", "Controles", 4, 16, nothing)  # tileGridSize (s)
    cv2.createTrackbar("CLAHE cL", "Controles", 20, 80, nothing)  # clipLimit (cL*0.1)

    # Valores predeterminados para cada filtro: [s, cL]
    presets = {
        1: (4, 25),   # Neblina: s=4, cL=2.5
        2: (4, 25),   # Noche:   s=4, cL=2.5
        3: (8, 20),   # Lluvia:  s=8, cL=2.0
        4: (10, 40),  # Sol:     s=10, cL=4.0
        5: (8, 30),   # Nieve:   s=8, cL=3.0
    }

    print("Presiona 'q' para salir.")

    prev_filtro = -1

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el frame.")
            break

        filtro = cv2.getTrackbarPos("Filtro", "Controles")
        s = cv2.getTrackbarPos("CLAHE s", "Controles")
        cL = cv2.getTrackbarPos("CLAHE cL", "Controles") / 10.0

        # Si el filtro cambió, actualiza sliders a los valores predeterminados
        if filtro != prev_filtro and filtro in presets:
            preset_s, preset_cL = presets[filtro]
            cv2.setTrackbarPos("CLAHE s", "Controles", preset_s)
            cv2.setTrackbarPos("CLAHE cL", "Controles", preset_cL)
            s = preset_s
            cL = preset_cL / 10.0
        prev_filtro = filtro

        condiciones = ["", "neblina", "noche", "lluvia", "sol", "nieve"]
        condicion = condiciones[filtro]

        if condicion in ["neblina", "lluvia", "sol", "noche", "nieve"]:
            frame = adaptive_filter(frame, condicion, s=s, cL=cL)
        elif condicion:
            frame = adaptive_filter(frame, condicion)

        # Mostrar el nombre del filtro en la imagen de la cámara
        filtro_nombre = condicion.capitalize() if condicion else "Sin filtro"
        cv2.putText(
            frame,
            f"Filtro: {filtro_nombre}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        # --- Detección de objetos ---
        frame = detect_y_draw(frame)

        cv2.imshow('Camara con Filtros', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    acceder_camara_con_filtros()