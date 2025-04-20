import cv2
import numpy as np

'''def dehaze(image):
    # Aplica CLAHE para mejorar el contraste en imágenes con neblina.

    # Convertir la imagen de BGR a LAB
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # Crear y aplicar CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)
    # Fusionar los canales y convertir de nuevo a BGR
    lab_clahe = cv2.merge((l_clahe, a, b))
    dehazed = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    return dehazed'''

def apply_high_pass_filter(image):
    
    # Aplica un filtro de paso alto para resaltar bordes y detalles en la imagen.
    
    # Convertir la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Crear un kernel para el filtro de paso alto
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    
    # Aplicar la convolución con el kernel
    high_pass_image = cv2.filter2D(gray_image, -1, kernel)
    
    return high_pass_image


def reduce_rain_noise(image):

    # Aplica el filtro fastNlMeansDenoisingColored para reducir el ruido en una imagen a color.

    # Aplicar el filtro de reducción de ruido
    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, h=5, templateWindowSize=3, searchWindowSize=21)

    c = 1 # Variable constante
    e = 0.001 # Variable constante
    gamma = 1.3 # Variable constante

    # Aplicar un filtro de paso alto para resaltar bordes y detalles
    high_pass_image = apply_high_pass_filter(denoised_image)
    high_pass_colored = cv2.cvtColor(high_pass_image, cv2.COLOR_GRAY2BGR)

    # Combinar las dos imágenes usando una combinación ponderada
    combined_image = cv2.addWeighted(denoised_image, 1, high_pass_colored, 0.35, 0)

    # Aplicar la corrección gamma
    imagen_gamma = c*(combined_image + e)**gamma

    imagen_gamma = cv2.normalize(imagen_gamma, None, 0, 255, cv2.NORM_MINMAX, dtype = cv2.CV_8UC1)
    return imagen_gamma


def enhance_image(image):
    
    # Mejora imágenes nocturnas a color utilizando CLAHE para ajustar el contraste.
    
    # Convertir la imagen de BGR a LAB
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)

    # Crear el objeto CLAHE y aplicarlo al canal de luminancia
    s = 4 # Tamaño del bloque para CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(s, s))
    l_clahe = clahe.apply(l)

    # Fusionar los canales LAB con el canal de luminancia mejorado
    lab_clahe = cv2.merge((l_clahe, a, b))

    # Convertir de nuevo a BGR
    enhanced_image = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

    return enhanced_image

def gamma_correction(image): 
    # Corrección gamma puede funcionar para noche o sol, sin embargo disminuye la calidad entre más intenso sea el filtro
    """
    Aplica corrección gamma a una imagen.
    :param image: Imagen de entrada (en formato BGR).
    :param gamma: Factor de corrección gamma (>1 reduce el brillo, <1 lo aumenta).
    :return: Imagen con corrección gamma aplicada.
    """
    # Calcular el inverso de gamma
    gamma = 1
    inv_gamma = 1.0 / gamma

    # Crear una tabla de búsqueda para mapear los valores de píxeles
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype("uint8")

    # Aplicar la corrección gamma usando la tabla de búsqueda
    corrected_image = cv2.LUT(image, table)

    return corrected_image

def reduce_noise(image):
    
    # Aplica un filtro bilateral para reducir el ruido mientras se preservan los bordes.
    
    # Filtro bilateral para reducir ruido
    noise_reduced_image = cv2.bilateralFilter(image, d=3, sigmaColor=100, sigmaSpace=75)
    return noise_reduced_image


"""def flash_faturation(image):
    
    # Aplica CLAHE a una imagen a color para mejorar el contraste y reducir el impacto de la luz excesiva.
    
    # Convertir la imagen de BGR a LAB
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Dividir la imagen en sus canales L, A y B
    l, a, b = cv2.split(lab_image)

    # Crear el objeto CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    # Aplicar CLAHE al canal de luminancia (L)
    l_clahe = clahe.apply(l)

    # Fusionar los canales LAB con el canal L mejorado
    lab_clahe = cv2.merge((l_clahe, a, b))

    # Convertir de nuevo a BGR
    enhanced_image = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

    return enhanced_image"""

def enhance_winter_image(image):
   
    # Combina filtros: CLAHE, reducción de ruido y corrección gamma para mejorar imágenes invernales.
    
    # Paso 1: Aplicar CLAHE
    image_clahe = enhance_image(image)

    # Paso 2: Reducir el ruido con un filtro bilateral
    noise_reduced_image = reduce_noise(image_clahe)

    # Paso 3: Ajustar el brillo con corrección gamma
    enhanced_image = gamma_correction(noise_reduced_image)

    return enhanced_image

def adaptive_filter(image, condition):
   
    # Aplica un filtro adaptativo basado en la condición atmosférica.
    
    if condition == "neblina" or condition == "noche":
        return enhance_image(image)
    elif condition == "lluvia":
        return reduce_rain_noise(image)
    elif condition == "sol":
        return gamma_correction(image)
    elif condition == "nieve":
        return enhance_winter_image(image)
    else:
        return image  # Sin cambios si no se especifica condición

# def main():
#     # Cargar la imagen
#     image_path = "Imagenes_Pruebas/nieve3.jpg"  # Cambia esto por la ruta de tu imagen
#     image = cv2.imread(image_path)

#     # Especificar la condición atmosférica
#     condition = "nieve"  # Cambia a "lluvia" según la condición

#     # Aplicar el filtro adaptativo
#     filtered_image = adaptive_filter(image, condition)

#     # Mostrar la imagen original y la filtrada
#     cv2.imshow("Imagen Original", image)
#     cv2.imshow("Imagen Filtrada", filtered_image)

#     # Esperar a que se presione una tecla para cerrar
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()