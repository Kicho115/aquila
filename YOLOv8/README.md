# YOLOv8

Este directorio contiene scripts y configuraciones para el entrenamiento y validación de modelos de detección de objetos usando YOLOv8 con el dataset COCO.

## Estructura

- `coco.yaml`: Configuración de clases y rutas para el dataset COCO.
- `convtrain.py`: Convierte anotaciones de COCO (entrenamiento) al formato YOLO.
- `convval.py`: Convierte anotaciones de COCO (validación) al formato YOLO.
- `requirements.txt`: Lista de dependencias necesarias para el entorno.

## Estructura de carpetas recomendada

Para que los scripts funcionen correctamente, asegúrate de que la estructura de carpetas dentro de `YOLOv8` sea la siguiente:

```
YOLOv8/
├── coco.yaml
├── convtrain.py
├── convval.py
├── requirements.txt
├── data/
│   └── coco/
│       ├── images/
│       │   ├── train2017/
│       │   └── val2017/
│       ├── annotations/
│       │   ├── instances_train2017.json
│       │   └── instances_val2017.json
│       └── labels/
│           ├── train2017/   # Se genera tras la conversión
│           └── val2017/     # Se genera tras la conversión
```

- Las imágenes de entrenamiento deben estar en `data/coco/images/train2017/`.
- Las imágenes de validación deben estar en `data/coco/images/val2017/`.
- Los archivos de anotaciones de COCO deben estar en `data/coco/annotations/`.
- Las etiquetas en formato YOLO se generarán en `data/coco/labels/train2017/` y `data/coco/labels/val2017/` tras ejecutar los scripts de conversión.

Asegúrate de mantener esta estructura para evitar errores de rutas y facilitar el entrenamiento y validación del modelo.

## Requisitos previos

### CUDA (opcional, recomendado para entrenamiento con GPU)

Para aprovechar la aceleración por GPU, instala CUDA (CUDA toolkit y cuDNN) y los drivers de NVIDIA compatibles con tu tarjeta gráfica.
Aquí puedes revisar la compatibilidad de CUDA con tu equipo de computo https://developer.nvidia.com/cuda-gpus 
Puedes descargar CUDA desde: https://developer.nvidia.com/cuda-downloads  
Asegúrate de que la versión de CUDA sea compatible con la versión de PyTorch que vas a instalar.

### Instalación de dependencias

Desde la carpeta `YOLOv8`, instala todas las dependencias necesarias ejecutando:

```sh
pip install -r requirements.txt
```

Esto instalará PyTorch, pycocotools y otras librerías requeridas.

## Conversión de anotaciones

Para convertir las anotaciones de COCO al formato YOLO:

1. Instala las dependencias necesarias (ver sección anterior).
2. Ejecuta los scripts de conversión **dentro de la carpeta `YOLOv8`** (En terminal utiliza: cd YOLOv8):
   ```sh
   python convtrain.py
   python convval.py
   ```

Esto generará los archivos de etiquetas en `YOLOv8/data/coco/labels/train2017` y `YOLOv8/data/coco/labels/val2017`.

## Entrenamiento

Asegúrate de tener los datos y anotaciones convertidas. Luego, puedes entrenar tu modelo YOLOv8 usando la configuración de `coco.yaml`.  
Ejecuta los comandos de entrenamiento **dentro de la carpeta `YOLOv8`** para evitar problemas de rutas.

En Terminal ejecuta lo siguiente dentro de la carpeta del proyecto para dirigirte a la carpeta de YOLOv8.
```sh
cd YOLOv8
```

Ya que estes en la carpeta de YOLOv8 trata ejecutando de la siguiente forma en la Terminal:
```sh
python train_yolov8.py
```

Si no funciona, ejecuta dirigiendote al boton de ejecutar de arriba y seleciona: "Run Python File in Dedicated Terminal" (debes estar dentro de la carpeta de YOLOv8 para esto también).

## Notas

- Asegúrate de que las rutas en `coco.yaml` coincidan con la ubicación real de tus datos.
- Los scripts asumen la estructura estándar del dataset COCO.
- Si tienes problemas con CUDA, puedes entrenar en CPU, pero será más lento.
