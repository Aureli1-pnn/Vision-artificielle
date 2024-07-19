import numpy as np
import matplotlib.pyplot as plt

from os import listdir, remove
from os.path import join

DOSSIER_IMAGE = 'Shoes/'

if __name__ == '__main__':

    # Récupération des images à supprimer
    """img_a = plt.imread(DOSSIER_IMAGE+'56.jpg') # Logo Freepik
    img_b = plt.imread(DOSSIER_IMAGE+'57.png') # Petit carré
    img_c = plt.imread(DOSSIER_IMAGE+'62.jpg') # Etoile bleu
    img_d = plt.imread(DOSSIER_IMAGE+'71.png') # Visage 
    img_e = plt.imread(DOSSIER_IMAGE+'77.png') # Visage 
    img_f = plt.imread(DOSSIER_IMAGE+'83.png') # Visage 
    img_g = plt.imread(DOSSIER_IMAGE+'68.png') # Visage 
    img_h = plt.imread(DOSSIER_IMAGE+'86.png') # Visage 
    img_i = plt.imread(DOSSIER_IMAGE+'89.jpg') # Visage 
    img_j = plt.imread(DOSSIER_IMAGE+'101.png') # Visage 
    img_k = plt.imread(DOSSIER_IMAGE+'116.png') # Visage 
    img_l = plt.imread(DOSSIER_IMAGE+'3480.png') # Visage 
    img_m = plt.imread(DOSSIER_IMAGE+'3577.jpg') # Logo LOOK 
    img_o = plt.imread(DOSSIER_IMAGE+'2713.jpg') # Logo bleu et noir 
    img_p = plt.imread(DOSSIER_IMAGE+'2664.jpg') # Logo photo de profil 
    img_q = plt.imread(DOSSIER_IMAGE+'2315.jpg') # Logo racoolstudio """
    img_r = plt.imread(DOSSIER_IMAGE+'3160.jpg') # Logo vert
    img_s = plt.imread(DOSSIER_IMAGE+'2990.jpg') # bonhomme bleu
    img_t = plt.imread(DOSSIER_IMAGE+'2034.jpg') # Logo vert


    # Récupération de toutes les images 
    images = listdir(DOSSIER_IMAGE)

    # Analyse des images
    nb_suppression = 0
    for img in images:

        try:
            img_path = DOSSIER_IMAGE + img
            img_tab  = plt.imread(img_path)
        
            if (np.array_equal(img_tab, img_r) or
                np.array_equal(img_tab, img_s) or
                np.array_equal(img_tab, img_t)) :

                remove(img_path)
                nb_suppression += 1
        except:
            pass

    print(f"Nombre de suppression : " + str(nb_suppression))