import cv2
import numpy as np

def apply_high_pass_filter(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    high_pass_image = cv2.filter2D(gray_image, -1, kernel)
    return high_pass_image


def reduce_noise(image):
    noise_reduced_image = cv2.bilateralFilter(image, d=3, sigmaColor=100, sigmaSpace=75)
    return noise_reduced_image


def gamma_correction(image):
    gamma = 0.7
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype("uint8")
    corrected_image = cv2.LUT(image, table)
    return corrected_image


def enhance_image_clahe(image, s=4, cL=2.5):
    """
    Mejora imágenes a color utilizando CLAHE para ajustar el contraste.
    s: tamaño del bloque para CLAHE (tileGridSize)
    cL: límite de contraste para CLAHE (clipLimit)
    """
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=cL, tileGridSize=(s, s))
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge((l_clahe, a, b))
    enhanced_image = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    return enhanced_image


def enhance_winter_image(image, s=4, cL=2.5):
    # Paso 1: Aplicar CLAHE
    image_clahe = enhance_image_clahe(image, s=s, cL=cL)
    # Paso 2: Reducir el ruido con un filtro bilateral
    noise_reduced_image = reduce_noise(image_clahe)
    # Paso 3: Ajustar el brillo con corrección gamma
    enhanced_image = gamma_correction(noise_reduced_image)
    return enhanced_image


def reduced_rain_noise_BiHi(image, s=8, cL=2.0):
    # Aplicar CLAHE usando la función unificada
    image_clahe = enhance_image_clahe(image, s=s, cL=cL)

    # Reducir resolución
    small_image = cv2.resize(image_clahe, (0, 0), fx=0.5, fy=0.5)
    denoised = cv2.bilateralFilter(small_image, d=4, sigmaColor=100, sigmaSpace=50)

    # Aplicar filtro de paso alto
    high_pass_image = apply_high_pass_filter(small_image)
    high_pass_colored = cv2.cvtColor(high_pass_image, cv2.COLOR_GRAY2BGR)

    # Combinar imágenes con pesos ajustados
    combined_image = cv2.addWeighted(denoised, 0.9, high_pass_colored, 0.25, 0)

    # Restaurar el tamaño original
    restored_image = cv2.resize(combined_image, (image.shape[1], image.shape[0]))
    return restored_image


def adaptive_filter(image, condition, s=4, cL=2.5):
    """
    Aplica un filtro adaptativo basado en la condición atmosférica.
    s y cL se usan para los filtros que aplican CLAHE.
    """
    if condition in ["neblina", "noche", "sol"]:
        return enhance_image_clahe(image, s=s, cL=cL)
    elif condition == "lluvia":
        return reduced_rain_noise_BiHi(image, s=s, cL=cL)
    elif condition == "nieve":
        return enhance_winter_image(image, s=s, cL=cL)
    else:
        return image  # Sin cambios si no se especifica condición


def main():
    image_path = "Imagenes_Pruebas/sol.png"
    image = cv2.imread(image_path)
    condition = "sol"
    filtered_image = adaptive_filter(image, condition, s=8, cL=2.0)
    cv2.imshow("Imagen Original", image)
    cv2.imshow("Imagen Filtrada", filtered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()