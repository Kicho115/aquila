import cv2
import numpy as np
from filtros import adaptive_filter

def nothing(x):
    pass

def acceder_camara_con_filtros():
    # Inicializa la cámara (0 es generalmente la cámara predeterminada)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return

    # Crear una ventana para los controles
    cv2.namedWindow("Controles")
    
    # Crear barras deslizantes para ajustar parámetros
    cv2.createTrackbar("Filtro", "Controles", 0, 4, nothing)  # 0: Sin filtro, 1: Neblina, 2: Lluvia, 3: Sol, 4: Nieve
    cv2.createTrackbar("Intensidad", "Controles", 50, 100, nothing)  # Intensidad del filtro (0-100)

    print("Presiona 'q' para salir.")

    while True:
        # Captura frame por frame
        ret, frame = cap.read()

        if not ret:
            print("Error: No se pudo leer el frame.")
            break

        # Leer los valores de las barras deslizantes
        filtro = cv2.getTrackbarPos("Filtro", "Controles")
        intensidad = cv2.getTrackbarPos("Intensidad", "Controles") / 100.0  # Normalizar a rango 0-1

        # Mapear el índice del filtro a una condición
        condiciones = ["", "neblina", "lluvia", "sol", "nieve"]
        condicion = condiciones[filtro]

        # Aplicar el filtro adaptativo si se selecciona uno
        if condicion:
            frame = adaptive_filter(frame, condicion)

        # Mostrar el frame con el filtro aplicado
        cv2.imshow('Camara con Filtros', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera la cámara y cierra las ventanas
    cap.release()
    cv2.destroyAllWindows()

# Llama a la función para acceder a la cámara con filtros
if __name__ == "__main__":
    acceder_camara_con_filtros()