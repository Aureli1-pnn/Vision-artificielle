import os
import shutil
import requests

from tqdm import tqdm
from bs4 import BeautifulSoup

DOSSIER_IMAGE = 'Shoes/'

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def extension_img(url):
    _, extension = os.path.splitext(url)
    return extension

if __name__ == '__main__':

    # Création du dossier Crab
    if os.path.exists(DOSSIER_IMAGE): shutil.rmtree(DOSSIER_IMAGE)
    os.makedirs(DOSSIER_IMAGE)
    
    # Création de l'agent Web
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    # Création des URL
    URL = [
        "https://www.shutterstock.com/fr/search/shoes?consentChanged=true&image_type=photo",        
        "https://fr.freepik.com/search?format=search&last_filter=query&last_value=shoes&query=shoes&type=photo",
        "https://fr.dreamstime.com/photos-images/shoes.html",
        "https://www.pexels.com/fr-fr/chercher/shoes/"
        ]

    PAGINATION = []
    for url in URL:
        if 'shutterstock.com' in url or "freepik.com" in url:
            for page in range(2, 25):
                PAGINATION.append(url + '&page=' + str(page))
        if 'dreamstime.com' in url:
            for page in range(2, 25):
                PAGINATION.append(url + '?pg=' + str(page))
    
    for url in PAGINATION: URL.append(url)

    # Création d'un tableau contenant les sources des images
    sources = []

    # Partie web scrapping
    clear_console()
    with tqdm(total=len(URL), desc='Récupération des pages web') as pbar:
        for url in URL:
            try:
                # Récupération de la page web correspondant à URL
                page = requests.get(url, headers=headers)
                soup = BeautifulSoup(page.text, 'html.parser')
                # Récupération de toutes les balises <img>
                imgs = soup.find_all('img')
                # Extraction des sources 
                src = [img['src'] for img in imgs if 'src' in img.attrs]
                for s in src: sources.append(s)
            except:
                pass
            pbar.update(1)
    sources = list(set(sources))
    
    # Récupération des images
    img_index = 0
    with tqdm(total=len(sources), desc='Récupération des images') as pbar:
        for src in sources:
            try:
                # Récupération de l'entension
                extension = extension_img(src)
                if extension != '.webp':
                    # Récupération de l'image src
                    img = requests.get(src)
                    # Création du fichier
                    file_name = DOSSIER_IMAGE + str(img_index) + extension
                    with open(file_name, 'wb') as file:
                        file.write(img.content)
                        file.close()
                    img_index+=1
            except:
                pass
            pbar.update(1)
    