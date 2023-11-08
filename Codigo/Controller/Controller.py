from Codigo.Controller.TextHandlerAdmin import TextHandlerAdmin
from Codigo.Controller.NetworkAdmin import NetworkAdmin


# HOLAMUNDO PRUEBA 5

class MainController:
    def __init__(self):
        self.textHandlerAdmin = TextHandlerAdmin()
        self.networkAdmin = NetworkAdmin()

    def addFiles(self, filepath):
        if filepath == "":
            return {
                'response': True,
                'message': "Ruta del archivo inválida",

            }
        return self.textHandlerAdmin.add_file(filepath)

    def textAnalysis(self):
        return self.textHandlerAdmin.lexical_analysis()

    def cleanText(self):
        self.textHandlerAdmin.setTextBlank()

    def setIgnoreWords(self, iwords):
        self.textHandlerAdmin.setIgnoreWords(iwords)

    def addwordstoignore(self, iwords):
        self.textHandlerAdmin.addwordstoignore(iwords)

    def getStatistics(self):
        return self.textHandlerAdmin.statistics()

    def combine_roots(self, roots):
        self.textHandlerAdmin.combine_roots(roots)

    def get_cloud_words(self, number):
        return self.textHandlerAdmin.get_cloud_words(number)

    def alphabeticSort(self):
        self.textHandlerAdmin.alphabeticSort()

    def weigthSort(self):
        self.textHandlerAdmin.weigthSort()

    # METODOS DEL NETWORK ADMIN

    def set_network_data(self):
        self.networkAdmin.set_data(self.textHandlerAdmin.roots_words, self.textHandlerAdmin.structure_stemming)

    def create_network(self):
        self.networkAdmin.create_network()

    def create_relation(self, step=1):
        self.networkAdmin.create_relation(step)

    def get_graph(self,type_word):
        return self.networkAdmin.get_graph(type_word)

    def get_graph_by_filters(self, node_weight, edge_weight, node_grade, type_word):
        return self.networkAdmin.get_graph_by_filters(node_weight, edge_weight, node_grade, type_word)

    def get_weight_of_heaviest_node(self):
        return self.networkAdmin.get_weight_of_heaviest_node()

    def get_weight_of_heaviest_edge(self):
        return self.networkAdmin.get_weight_of_heaviest_edge()

    def get_weight_of_heaviest_grade(self):
        return self.networkAdmin.get_weight_of_heaviest_grade()

    def delete_graph(self):
        self.networkAdmin.delete_graph()

    def get_text2(self):
        return self.textHandlerAdmin.get_text2()

    def get_phrases(self):
        return self.textHandlerAdmin.getPhrases()

    def get_web_pages(self):
        return self.textHandlerAdmin.getUrls()
