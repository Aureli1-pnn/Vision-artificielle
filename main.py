import os
import cv2 
import sys
import json
import torch
import shutil
import numpy as np

from ultralytics import YOLO

# Utile à l'éxécution (évite de planter)
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# Créer le dossier de destination
DOSSIER_RESULTAT = 'Resultat/'
if not os.path.exists(DOSSIER_RESULTAT): os.makedirs(DOSSIER_RESULTAT)

if __name__ == '__main__':

    try:
        # Récupération du chemin de l'image
        img_path = sys.argv[1]

        # Récupération du nom du fichier 
        file_name = os.path.basename(img_path).split('.')[0]

        # Ouverture et resize de l'image au format 640*640
        img = cv2.imread(img_path)
        img = cv2.resize(img, (640, 640))
    
        # Chargement du modèle
        model   = YOLO("final_model.pt")

        # Prédiction
        results = model.predict(img, conf=0.5)

        # Génére un résultat par image fourni
        for result in results:

            # Récupération du masque
            masks = result.masks.data
            boxes = result.boxes.data
            clss = boxes[:, 5]
            obj_indices = torch.where(clss == 0)
            obj_masks = masks[obj_indices]
            obj_mask = torch.any(obj_masks, dim=0).int()

            # Application du masque
            masked_img = img*obj_mask.numpy()[:, :, np.newaxis]

            # Transformation de l'image en PNG RGBA (Ajout de la transparence du background)
            alpha   = np.sum(masked_img, axis=-1) > 0
            alpha   = np.uint8(alpha * 255)
            img_res = np.dstack((masked_img, alpha))

            # Enregistrement de l'image
            cv2.imwrite(str(f'{DOSSIER_RESULTAT}/{file_name}_all_shoes.png'), img_res)

            # Faire la même pour chaque chaussures
            for i, obj_index in enumerate(obj_indices[0].numpy()):
                
                # Récupération du masque
                obj_masks = masks[torch.tensor([obj_index])]
                obj_mask = torch.any(obj_masks, dim=0).int()
                
                # Application du masque
                masked_img = img*obj_mask.numpy()[:, :, np.newaxis]

                # Transformation de l'image en PNG RGBA
                alpha   = np.sum(masked_img, axis=-1) > 0
                alpha   = np.uint8(alpha * 255)
                img_res = np.dstack((masked_img, alpha))

                # Récupération de la bounding box
                bounding_box = result.boxes[obj_index].xyxy[0]

                # Crop de l'image
                x_min = bounding_box[0].int()
                y_min = bounding_box[1].int()
                x_max = bounding_box[2].int()
                y_max = bounding_box[3].int()
                cropped_img = img_res[y_min : y_max, x_min: x_max]

                # Enregistrement de l'image
                cv2.imwrite(str(f'{DOSSIER_RESULTAT}/{file_name}_{i+1}.png'), cropped_img)
    
    # Gestion des erreurs 
    except Exception as e:
        print(f"Erreur lors de l'éxécution {e}")