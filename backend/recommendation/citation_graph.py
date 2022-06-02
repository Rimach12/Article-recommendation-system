from backend.models import Article


class CitationGraph: 
    def create_graph(self, xid, graph, index, max_level):
        """
        Description :
        --------------
        Créer un graphique de références pour une requête à plusieurs niveaux.

        Attribut :
        ------------
        - xid : identifiant de l'article de la requête.
        - graph : Iterable de listes. Chaque sous-liste représente un niveau du graphe.
        - data : cadre de données pandas.
        - index : niveau actuel du graphique.
        - max_level : niveau maximum du graphique à créer.

        Sortie : Retourne une liste d'identifiants d'articles.

        """
        # le niveau du graphique a atteint le niveau maximal autorisé
        if len(graph) >= max_level:
            return graph

        # obtenir l'identifiant des articles du niveau actuel (index)
        children = []
        for vertex in graph[index]:
            # vertex_row = data.filter("id == '%s'" % vertex).select("references").collect()
            vertex_row = Article.query.filter_by(id=vertex).first()
            references = vertex_row.references

            if references is not None:
                for ref in references:
                    # tmp = data.filter("id == '%s'" % ref).collect()
                    tmp = Article.query.filter_by(id=ref).first()
                    if (
                        ref != xid
                        and not any(ref in subl for subl in graph)
                        and tmp is not None
                    ):
                        children.append(ref)

        # pas de données pour le niveau actuel du graphique
        if len(children) == 0:
            return graph
        else:
            graph.append(children)
            return self.create_graph(xid, graph, len(graph) - 1, max_level)

    def get_graph_data(self, graph):
        """
        Description :
        --------------
        Récupère les identifiants de tous les articles du graphe de citation.

        Attribut :
        ------------
        - Graphique : Liste de listes d'objets. Chaque élément du graphe représente un niveau.
        - level : Entier. Représente le niveau du graphique dont on veut extraire les données.

        Sortie : Retourne une liste d'objets.
        """
        references = []
        # exclure le niveau 0 puisqu'il représente la requête
        for subl in graph[1:]:
            for xid in subl:
                references.append(xid)

        return references
