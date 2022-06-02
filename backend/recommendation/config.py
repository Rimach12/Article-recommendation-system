import pickle

# Chemin d'accès aux fichiers
EMBEDDINGS_PATH = "backend/bin/word2vec_embeddings.pkl"
MODEL_PATH = "backend/bin/knn_model.pkl"

# Constantes de réglage de l'algorithme
THRESHOLD = 0.3
N_SIMILAR = 6
GRAPH_LEVEL = 3

# Charger les données binaires
def load_data(path):
    """
    Description : Chargement des données à partir du chemin. 
    
    Attribut : 
    ------------
        - path : Chaîne. Emplacement du fichier à charger.
    """
    with open(path, 'rb') as f:
        return pickle.load(f)
