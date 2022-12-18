# importer les paquets nécessaires
from module import RGBHistogram
from searcher import Searcher
import numpy as np
import argparse
import os
import pickle
import cv2

# construit l’argument parser et analyse les arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
help = "Path to the directory that contains the images we just indexed")
ap.add_argument("-i", "--index", required = True,
help = "Path to where we stored our index")
ap.add_argument("-q", "--query", required = True,
help = "Path to query image")
args = vars(ap.parse_args())

# charge l’image de la requête et la montre
queryImage = cv2.imread(args["query"])
cv2.imshow("Query", queryImage)
print("query: {}".format(args["query"]))

# décrire la requête de la même manière que nous l’avons fait index.py - un histogramme 3D RVB avec 8 bins par
# canal
desc = RGBHistogram([8, 8, 8])
queryFeatures = desc.describe(queryImage)

# charger l’index effectuer la recherche
index = pickle.loads(open(args["index"], "rb").read())
searcher = Searcher(index)
results = searcher.search(queryFeatures)

# initialise les deux montages pour afficher nos résultats -
# nous avons un total de 25 images dans l’index, mais seulement
# afficher les 10 premiers résultats; 5 images par montage, avec
# images de 400 x 166 pixels
montageA = np.zeros((300 * 5, 300, 3), dtype = "uint8")
montageB = np.zeros((300 * 5, 300, 3), dtype = "uint8")
# charger l’index effectuer la recherche
paths = []

for j in range(0, 10):
    # saisir le résultat (nous utilisons l’ordre row-major) et
    # charger l’image du résultat
    (score, imageName) = results[j]
    path = os.path.join(args["dataset"], imageName)
    result = cv2.imread(path)
    result = cv2.resize(result, (300,300))
    print("\t{}. {} : {:.3f}".format(j + 1, imageName, score))
    # vérifier si le premier montage doit être utilisé
    if j < 5:
        paths.append(imageName)
        montageA[j * 300:(j + 1) * 300, :] = result
        print(paths)
    # sinon, le second montage doit être utilisé
    else:
        montageB[(j - 5) * 300:((j - 5) + 1) * 300, :] = result

print(montageA)
print(paths)
cv2.imshow("Results 1-5", montageA)
cv2.imshow("Results 6-10", montageB)
cv2.waitKey(0)
