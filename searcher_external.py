from module import RGBHistogram
from searcher import Searcher
import cv2
import pickle
import os


class SearcherExternal:
    def __init__(self):
        # stocke le nombre de cases que l’histogramme utilisera
        self.index = 'index.cpickle'
        self.dataset = 'static/pictures'
        self.paths = []

    def search(self, image):
        queryImage = cv2.imread(image)
        desc = RGBHistogram([8, 8, 8])
        queryFeatures = desc.describe(queryImage)
        index = pickle.loads(open(self.index, "rb").read())
        searcher = Searcher(index)
        results = searcher.search(queryFeatures)
        for j in range(0, 10):
            # saisir le résultat (nous utilisons l’ordre row-major) et
            # charger l’image du résultat
            (score, imageName) = results[j]
            path = os.path.join(self.dataset, imageName)
            result = cv2.imread(path)
            #result = cv2.resize(result, (300,300))
            print("\t{}. {} : {:.3f}".format(j + 1, imageName, score))
            # vérifier si le premier montage doit être utilisé
            if j < 5:
                self.paths.append(imageName)
                
        return self.paths