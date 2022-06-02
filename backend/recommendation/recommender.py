from . import config
from .citation_graph import CitationGraph
from backend.models import Article

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:
    embeddings = config.load_data(config.EMBEDDINGS_PATH)
    knn = config.load_data(config.MODEL_PATH)

    def __init__(self, qid):
        self.query_id = qid
        self.query_embeddings = np.array(self.embeddings[qid]).reshape(1, -1)

    def calculate_similarity(self, query, data, n=config.N_SIMILAR, threshold=config.THRESHOLD):
        """
        Description :
        --------------
        Calcule la similarité entre les incorporations de la requête et tous les vecteurs d'articles du cadre de données.

        Attribut :
        ------------
        - query : Vecteur d'entiers. Incorporations de requêtes
        - data : liste de vecteurs. Incorporation de données.
        - Threshold : pourcentage de similarité requis.
        - n : Entier. Nombre d'articles similaires à retourner.
        """
        # calculer la similarité
        cosine = cosine_similarity(query, data)

        # le dictionnaire contient chaque article avec la similarité correspondante avec la requête
        i = 0
        similarity = dict({})
        for value in cosine[0]:
            # vérifier si l'article est similaire au seuil% avec la requête
            if value >= threshold:
                similarity[i] = value
            i += 1

        # trier les articles par ordre décroissant en fonction de leur similarité avec la requête et retourner n articles
        similarity = {
            k: v
            for k, v in [
                (key, value)
                for key, value in sorted(
                    similarity.items(), key=lambda item: item[1], reverse=True
                )
            ][:n]
        }

        return similarity

    def get_similar_articles(self):
        """
        Description :
        --------------
        Retourne les articles similaires à la requête de l'article.

        Sortie : Liste d'entiers. Index des articles
        """
        # créer un graphique de citations pour une requête de 3 niveaux
        instance = CitationGraph()
        graph = instance.create_graph(self.query_id, [[self.query_id]], 0, config.GRAPH_LEVEL)
        graph_data = instance.get_graph_data(graph)

        # retourner les articles similaires
        if len(graph_data) <= config.N_SIMILAR:
            _, index = self.knn.kneighbors(self.query_embeddings)
            index = list(index[0])

            if self.query_id in index:
                index.remove(self.query_id)
            
            return index
        else:
            # obtenir l'encastrement des noeuds du graphe
            graph_embeddings = []
            for xid in graph_data:
                tmp = Article.query.filter_by(id=xid).first()
                graph_embeddings.append(self.embeddings[tmp.id])

            index = self.calculate_similarity(self.query_embeddings, graph_embeddings)
            index = list(index.keys())

            if self.query_id in index:
                index.remove(self.query_id)
            
            return index
