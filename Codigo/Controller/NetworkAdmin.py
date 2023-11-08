import networkx as nx


def get_graph_by_node_grade(graph, amount=100):
    degree_dict = dict(graph.degree())
    # nodes_sorted_by_degree = sorted(degree_dict, key=lambda x: degree_dict[x], reverse=True)
    top_x_nodes = {clave: valor for clave, valor in degree_dict.items() if valor >= amount}

    # top_x_nodes = nodes_sorted_by_degree[:amount]
    new_graph = graph.subgraph(top_x_nodes).copy()

    return new_graph


def get_graph_by_edge_weight(graph, amount=5):
    weights = nx.get_edge_attributes(graph, 'weight')
    edges = {clave: valor for clave, valor in weights.items() if valor >= amount}
    # edges=[ print((x,y, data))for x,y, data in weights if int(data) >= amount]
    new_graph = graph.edge_subgraph(edges)
    return new_graph


def get_graph_by_node_weight(graph, amount=5):
    weights = nx.get_node_attributes(graph, 'weight')
    filtered_nodes = [node for node, weight in weights.items() if weight >= amount]
    new_graph = graph.subgraph(filtered_nodes)
    return new_graph


class NetworkAdmin:
    def __init__(self):
        self.roots_words = []
        self.structure_stemming = None
        self.graph = nx.Graph()

    def set_data(self, roots_words, structure_stemming):
        self.roots_words = roots_words
        self.structure_stemming = structure_stemming

    def create_network(self):
        nodes, weights = self.structure_stemming.get_nodes_and_weights()

        for node, weight in zip(nodes, weights):
            if not self.graph.has_node(node):
                self.graph.add_node(node, weight=weight)

    def create_relation(self, step=1):
        index = 0
        amount_words = len(self.roots_words)
        for node in self.roots_words:
            if index + step < amount_words:
                u, v = node, self.roots_words[index + step]
                if self.graph.has_edge(u, v):
                    self.graph[u][v]['weight'] += 1.0
                else:
                    self.graph.add_edge(u, v, weight=1.0)
            index += 1

    def change_labels(self, new_graph, type_word):
        for node in new_graph.nodes():
            if type_word == 1:
                new_label = self.structure_stemming.get_first_word(node)
            elif type_word == 2:
                new_label = self.structure_stemming.get_heaviest_word(node)
            elif type_word == 3:
                new_label = self.structure_stemming.get_shortest_word(node)
            else:
                new_label = node

            new_graph.nodes[node]['label'] = new_label

        return new_graph

    def get_graph(self, type_word):
        weights = nx.get_node_attributes(self.graph, 'weight')
        filtered_nodes = [node for node, weight in weights.items() if weight >= 0]
        new_graph = self.graph.subgraph(filtered_nodes)
        new_graph = self.change_labels(new_graph, type_word)
        return new_graph

    def get_graph_by_filters(self, node_weight, edge_weight, node_grade, type_word):
        new_graph = self.graph

        if node_weight == 0 and edge_weight == 0 and node_grade == 0:
            return self.get_graph(type_word)

        if node_weight > 0:
            new_graph = get_graph_by_node_weight(new_graph, node_weight)
        if edge_weight > 0:
            new_graph = get_graph_by_edge_weight(new_graph, edge_weight)
        if node_grade > 0:
            new_graph = get_graph_by_node_grade(new_graph, node_grade)

        new_graph = self.change_labels(new_graph, type_word)

        return new_graph

    def get_weight_of_heaviest_node(self):
        weights = nx.get_node_attributes(self.graph, 'weight')
        max_weight = max(weights.values())
        return max_weight

    def get_weight_of_heaviest_edge(self):
        weights = nx.get_edge_attributes(self.graph, 'weight')
        max_weight = max(weights.values())
        return max_weight

    def get_weight_of_heaviest_grade(self):
        degree_dict = dict(self.graph.degree())
        max_grade = max(degree_dict.values())
        return max_grade

    def delete_graph(self):
        self.graph.clear()

    def print_network(self):
        for node, data in self.graph.nodes(data=True):
            print(f"{node}: Peso {data['weight']}")

        for u, v, data in self.graph.edges(data=True):
            print(f"{u} --> {v}: Peso {data['weight']}")
