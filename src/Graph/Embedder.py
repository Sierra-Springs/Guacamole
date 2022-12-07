from APIRequester import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


class Embedder:
    def __init__(self, feature_extractor):
        self.feature_extractor = feature_extractor

    def generate_term_document_matrix(self, json_graph):
        texts = []
        for i in json_graph:
            article = i['_source']
            texts.append(article['abstract'])

        # https://okan.cloud/posts/2021-04-08-text-vectorization-using-python-term-document-matrix/
        vect = CountVectorizer()
        vects = vect.fit_transform(texts)

        td = pd.DataFrame(vects.todense())
        td.columns = vect.get_feature_names_out()
        term_document_matrix = td.T
        # from sklearn.datasets import make_multilabel_classification
        # X, _ = make_multilabel_classification(random_state=0)
        return term_document_matrix

    def fit_transform(self, json_graph):
        return self.feature_extractor.fit_transform(self.generate_term_document_matrix(json_graph))


class LatentDirichletAllocationEmbedder(Embedder):
    def __init__(self):
        self.num_topics = 10  # Build LDA model
        feature_extractor = LatentDirichletAllocation(n_components=self.num_topics)
        super().__init__(feature_extractor=feature_extractor)
