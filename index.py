
from module import RGBHistogram
from imutils.paths import list_images
import argparse
import pickle
import cv2


# construit l’argument parser et analyse les arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
   help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True,
   help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

# initialise le dictionnaire d’index pour stocker notre notre quantifié
# images, avec la "clé"du dictionnaire étant l’image
# nom de fichier et la ’valeur’ de nos fonctionnalités calculées
index = {}

# initialise notre descripteur d’image - un histogramme 3D RVB avec
# 8 bins par canal

desc = RGBHistogram([8, 8, 8])

# utilise list_images pour saisir les chemins de l’image et les faire défiler
for imagePath in list_images(args["dataset"]):
    # extrait notre identifiant d’image unique (c’est-à-dire le nom du fichier)
    k = imagePath[imagePath.rfind("/") + 1:]
    # chargez l’image, décrivez-la en utilisant notre histogramme RVB
    # descripteur et mettre à jour l’index
    image = cv2.imread(imagePath)
    features = desc.describe(image)
    index[k] = features

# nous avons maintenant fini d’indexer notre image - maintenant nous pouvons écrire notre
#index to disk
f = open(args["index"], "wb")
f.write(pickle.dumps(index))
f.close()
# montre combien d’images nous avons indexées
print("[INFO] done...indexed {} images".format(len(index)))

