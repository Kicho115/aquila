import cv2
from filtros import reduced_rain_noise_s
from concurrent.futures import ThreadPoolExecutor, as_completed

def apply_filter(frame):
    try:
        # Aplica el filtro
        return reduced_rain_noise_s(frame)
    except Exception as e:
        print(f"Error al aplicar el filtro: {e}")
        return frame

def process_frame_in_thread(frame, executor):
    # Procesar el frame en un hilo separado
    return executor.submit(apply_filter, frame)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

# Crear un ThreadPoolExecutor con un número de hilos adecuado
# Usaremos la mitad de los núcleos disponibles para evitar saturar la CPU
executor = ThreadPoolExecutor(max_workers=5) # Ajusta según tu CPU y la fluidez deseada
# Entre mas hilos, mas fluido sera el video, pero mas carga en la CPU
# Maximo soportado de momento 30, sin embargo la carga de CPU es alta

# Lista para rastrear los frames en proceso
futures = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Enviar el frame al hilo para procesarlo
    future = process_frame_in_thread(frame, executor)
    futures.append(future)

    # Mostrar el frame procesado si está disponible
    completed_futures = [f for f in futures if f.done()]
    for f in completed_futures:
        processed_frame = f.result()
        cv2.imshow("Camara con Filtros", processed_frame)
        futures.remove(f)  # Eliminar el futuro completado de la lista

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
executor.shutdown()