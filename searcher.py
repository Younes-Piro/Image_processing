import numpy as np

class Searcher:
    def __init__(self, index): 
        # stocker notre index d’images 
        self.index = index 
        
    def search(self, queryFeatures):
        # initialise notre dictionnaire de résultats
        results = {}
        # boucle sur l’index
        for (k, features) in self.index.items():
        # calculer la distance du chi-carré entre les entités
        # dans notre index et nos fonctionnalités de requête - en utilisant le
        # distance chi-carré qui est normalement utilisée dans le
        # champ de vision par ordinateur pour comparer les histogrammes
            d = self.chi2_distance(features, queryFeatures)
        # maintenant que nous avons la distance entre les deux caractéristiques
        # vecteurs, nous pouvons udpate le dictionnaire de résultats - le
        # La touche # est l’identifiant d’image actuel dans l’index et le
        # valeur est la distance que nous venons de calculer, représentant
        # comment ’similaire’ l’image dans l’index est à notre
            results[k] = d
        # trier nos résultats, de sorte que les plus petites distances (c.-à-d.
        # des images plus pertinentes sont en tête de liste)
        results = sorted([(v, k) for (k, v) in results.items()])
        # retourner nos résultats
        return results
        
    def chi2_distance(self, histA, histB, eps = 1e-10):
        # calcule la distance du chi-carré
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])

        # retourne la distance du chi-carré
        return d