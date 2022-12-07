from Graph.Graph import Graph
from APIRequester import APIRequester
from tqdm import tqdm


class GraphBuilder:
    def __init__(self, json_graph, embedder, childs_depth=0, parent_depth=0, verbose=False):
        """
        :param json_graph: de la forme {"query_text" : [article1, article2, ...]}
        :param childs_depth: profondeur de la récupération des articles cités
        Exemples :  0 : Pas de récupération d'articles cités.
                    1 : Récupération des articles cités
                    2 : Récupération des articles cités et des articles cités par ces articles
        :param childs_depth: profondeur de la récupération des articles qui citent nos articles
        :param verbose: True / False
        """
        self.embedder = embedder
        self.verbose = verbose
        self.apiRequester = APIRequester()
        self.child_depth = childs_depth
        self.parent_depth = parent_depth
        self.articles = tuple()

        for query_text in json_graph:
            self.articles += tuple(json_graph[query_text])  # Ajout de la liste totale des articles (childs_depth = 0)

        root_articles = self.articles
        self.add_child_articles(root_articles)
        print(f"len articles {len(self.articles)}")
        print(f"len root articles {len(root_articles)}")

        self.add_parent_articles(root_articles)

    def add_child_articles(self, articles, step=0):
        if step == self.child_depth: return

        if self.verbose:
            print(f"__add_child_articles step {step}__ (nb all articles : {len(self.articles)})")
            nb_sub_articles = sum([len(article["_source"]["references"]) for article in articles])
            print(f"nb_sub_articles for step={step} : {nb_sub_articles}")
            print()

        new_articles = tuple()
        for num_article, articles in enumerate(articles):
            for reference in tqdm(articles["_source"]["references"]):
                new_articles + tuple(self.apiRequester.request_by_doc_id(reference))
        self.articles += tuple(new_articles)
        self.add_child_articles(new_articles, step + 1)

    def add_parent_articles(self, articles, step=0):
        if step == self.parent_depth: return

        if self.verbose:
            print(f"__add_parent_articles step {step}__ (nb all articles : {len(self.articles)})")

        new_articles = tuple()
        for num_article, articles in enumerate(articles):
            print(articles["_id"])
            parents = self.apiRequester.request_doc_references_by_id(id=articles["_id"])
            print(parents)
            new_articles += tuple(self.apiRequester.request_doc_references_by_id(id=articles["_id"]))
        if self.verbose == True:
            print(f"nb_sub_articles for step={step} : {len(new_articles)}")
            print()
        self.articles += tuple(new_articles)
        self.add_parent_articles(new_articles, step + 1)



    def build_graph(self):
        return Graph(self.articles, self.embedder)
