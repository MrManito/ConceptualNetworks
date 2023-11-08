class StructureStemming:
    def __init__(self,):
        self.stem_words = {}
        self.count_words = 0

    def add(self, root, word):
        '''Método que realiza agrega la raiz y la palabra a la estructura.
            Entradas: self, root: raiz del stemming, word: palabra que se radicalizo
            Salidas: N/A.
            Restricciones: que las entradas sean strings'''
        if root not in self.stem_words:
            self.stem_words[root] = [{word: 1}, 1]
        else:
            dic_words = self.stem_words[root][0]
            if word in dic_words.keys():
                self.stem_words[root][0][word] += 1
            else:
                self.stem_words[root][0][word] = 1
            self.stem_words[root][1] += 1
        self.count_words += 1

    def merge(self, root1, root2):
        '''Método que une dos raices que proviene de la misma.
            Entradas: self, root1, root2
            Salidas: N/A.
            Restricciones: N/A'''
        if len(root1) <= len(root2):
            aux_list_words = self.stem_words[root2]
            self.stem_words[root1][0].update(aux_list_words[0])
            self.stem_words[root1][1] += aux_list_words[1]
            del self.stem_words[root2]
        else:
            aux_list_words = self.stem_words[root1]
            self.stem_words[root2][0].update(aux_list_words[0])
            self.stem_words[root2][1] += aux_list_words[1]
            del self.stem_words[root1]

    def mergeList(self, list_roots):
        root_choice = min(list_roots, key=len)
        list_roots.remove(root_choice)
        if len(list_roots) >= 1:
            for root in list_roots:
                self.merge(root_choice, root)
        return root_choice

    def getStemWords(self):
        '''Método que devuelve la structura donde se mantiene los datos.
            Entradas: self
            Salidas: La estructura creada de stem_words.
            Restricciones: N/A'''
        return self.stem_words

    def cleanStructure(self):
        '''Método que limpia todo el diccionario.'''
        self.stem_words.clear()

    def sortStruture(self):
        '''Método que ordena segun llave de raiz de manera alfabética'''
        self.stem_words = dict(sorted(self.stem_words.items()))

    def sortStrutureWeigth(self):
        '''Método que ordena segun el cantidad de palabras que tiene una raiz'''
        self.stem_words = dict(sorted(self.stem_words.items(), key=lambda item: (item[1][1]), reverse=True))

    def get_nodes_and_weights(self):
        nodes = list(self.stem_words.keys())
        # weights = list(map(lambda x: x[1] if len(x) >= 2 else None, self.stem_words.values()))
        weights = list(map(lambda x: x[1], self.stem_words.values()))
        return nodes, weights

    def get_firts_word_and_weights(self):
        results = {}
        for key, value in self.stem_words.items():
            results[list(value[0].keys())[0]] = value[1]
        return results

    def get_valuable_word_and_weights(self):
        results = {}
        for key, value in self.stem_words.items():
            dicc = value[0]
            results[max(dicc, key=lambda key: dicc[key])] = value[1]
        return results

    def get_short_word_and_weights(self):
        results = {}
        for key_i, value in self.stem_words.items():
            dicc = value[0]
            results[sorted(dicc, key=lambda x: len(x))[0]] = value[1]
        return results

    def get_first_word(self, root):
        words = self.stem_words[root]
        word = list(words[0].keys())[0]
        return word

    def get_heaviest_word(self, root):
        words = self.stem_words[root]
        word = max(words[0], key=lambda key: words[0][key])
        return word

    def get_shortest_word(self, root):
        words = self.stem_words[root]
        word = sorted(words[0], key=lambda x: len(x))[0]
        return word
