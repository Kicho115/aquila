import os
from pycocotools.coco import COCO

# Rutas
coco_json = "YOLOv8/data/coco/annotations/instances_val2017.json"
images_dir = "YOLOv8/data/coco/images/val2017"
labels_dir = "YOLOv8/data/coco/labels/val2017"

os.makedirs(labels_dir, exist_ok=True)

# Cargar anotaciones COCO
coco = COCO(coco_json)

# Crear un mapeo de category_id a índice (0-79)
cat_ids = coco.getCatIds()
cat_id_to_index = {cat_id: idx for idx, cat_id in enumerate(cat_ids)}

for img in coco.imgs.values():
    img_id = img['id']
    file_name = img['file_name']
    width = img['width']
    height = img['height']
    ann_ids = coco.getAnnIds(imgIds=img_id)
    anns = coco.loadAnns(ann_ids)
    label_lines = []
    for ann in anns:
        if ann.get('iscrowd', 0):
            continue
        cat_id = ann['category_id']
        if cat_id not in cat_id_to_index:
            continue  # Ignora categorías fuera de COCO80
        yolo_cat_id = cat_id_to_index[cat_id]
        bbox = ann['bbox']  # [x_min, y_min, width, height]
        x_center = (bbox[0] + bbox[2] / 2) / width
        y_center = (bbox[1] + bbox[3] / 2) / height
        w = bbox[2] / width
        h = bbox[3] / height
        label_lines.append(f"{yolo_cat_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")
    # Guardar archivo .txt
    txt_path = os.path.join(labels_dir, file_name.replace('.jpg', '.txt'))
    with open(txt_path, 'w') as f:
        f.write('\n'.join(label_lines))