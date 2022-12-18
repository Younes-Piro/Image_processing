# importer les paquets nécessaires
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
args = vars(ap.parse_args())
# charge l’index et initialise notre chercheur
index = pickle.loads(open(args["index"], "rb").read())
searcher = Searcher(index)

# boucle sur les images dans l’index - nous allons utiliser chacun comme
# une image de requête
for (query, queryFeatures) in index.items():
# effectue la recherche en utilisant la requête en cours
    results = searcher.search(queryFeatures)
    # charger l’image de la requête et l’afficher
    path = os.path.join(args["dataset"], query)
    queryImage = cv2.imread(path)
    cv2.resize(queryImage, (0,0))
    cv2.imshow("Query", queryImage)
    print("query: {}".format(query))
    print('/*********************/')
    print(results)
    # initialise les deux montages pour afficher nos résultats -
    # nous avons un total de 25 images dans l’index, mais seulement
    # afficher les 10 premiers résultats; 5 images par montage, avec
    # images de 400 x 166 pixels
    montageA = np.zeros((166 * 5, 400, 3), dtype = "uint8")
    montageB = np.zeros((166 * 5, 400, 3), dtype = "uint8")
# boucle sur les dix premiers résultats
    for j in range(0, 10):
        # saisir le résultat (nous utilisons l’ordre row-major) et
        # charger l’image du résultat
        (score, imageName) = results[j]
        path = os.path.join(args["dataset"], imageName)
        result = cv2.imread(path)
        print("\t{}. {} : {:.3f}".format(j + 1, imageName, score))
        print(result)
        if j < 5:
            montageA[j * 166:(j + 1) * 166, :] = result     
            # sinon, le second montage doit être utilisé
        else:
            montageB[(j - 5) * 166:((j - 5) + 1) * 166, :] = result

    # afficher les résultats
    cv2.imshow("Results 1-5", montageA)
    cv2.imshow("Results 6-10", montageB)
    cv2.waitKey(0)

