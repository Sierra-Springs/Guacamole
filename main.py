import pandas as pd

from pprint import pprint
from src.APIRequester import APIRequester
from Utils.pathDefinitions import *
from Graph.Graph import Graph
from Graph.GraphBuilder import *
from Graph.Embedder import *
import io
from tqdm import tqdm

if __name__ == '__main__':
    apiRequester = APIRequester()
    #pprint(apiRequester.request_articles("Romain Deveaud"))
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df = pd.read_csv(csvPath, header=0, delimiter="	")
    #print(df)

    #print(df["query_text"][0])
    #pprint(apiRequester.request(df["query_text"][0], size=1000))

    # Récupère les articles pour les query_text correspondant à G01

    res = dict()
    researches = df[df["topic_id"] == "G01"]["query_text"]
    print(researches)
    for research in tqdm(researches):
        res[research] = apiRequester.request_articles(df["query_text"][0], size=1000)


    apiRequester = APIRequester()
    # g = Graph(apiRequester.request_articles("Romain Deveaud"))

    #res = apiRequester.request_articles("Romain Deveaud", size=1000)


    graphBuilder = GraphBuilder(res,
                                embedder=LatentDirichletAllocationEmbedder(),
                                childs_depth=0,
                                parent_depth=0,
                                verbose=True)
    graph = graphBuilder.build_graph()
    print(graph.graph_correlation())
    graph.graph_to_file()

