from nltk.stem import WordNetLemmatizer

class Lematizador(object):
    '''
    Clase para lematizar texto
    '''
    
    def lematizar_palabra(self, palabra, etiqueta_pos_stanford):
        """
        Lematiza una palabra de acuerdo a asu etiqueta POS.
        @param palabra: Un string.
        @param etiqueta_pos_stanford: Etiqueta Part-Of-Speech (adjectives a, nouns n, adverbs r, verbs v).
        @return: un string lematizado | 'None', si la etiqueta POS de Stanford no se encuentra en wordnet.
        """
        if not isinstance(palabra, str):
            raise Exception("El parametro 'palabra' recibio un argumento inválido: {}".format(str(palabra)))
        
        if not isinstance(etiqueta_pos_stanford, str):
            raise Exception("El parametro 'etiqueta_pos_stanford' recibio un argumento inválido: {}".format(str(etiqueta_pos_stanford)))
        
        lema = WordNetLemmatizer()
        
        etiqueta_pos_wordnet = self.mapeo_de_etiquetas(etiqueta_pos_stanford)
        
        if not etiqueta_pos_wordnet:
            return None
        
        palabra = lema.lemmatize(palabra, etiqueta_pos_wordnet)
        
        return palabra
    
    def mapeo_de_etiquetas(self, etiqueta_pos_stanford):
        """
        Mapea las etiquetas POS de Stanford a las etiquetas POS de Wordnet.
        @param etiqueta_pos_stanford: La etiqueta POS de Stanford. ej NN, NNS, JJ, etc.
        @return: etiqueta pos de wordnet.
        """
        if etiqueta_pos_stanford.startswith("N"):
            return "n"
        elif etiqueta_pos_stanford.startswith("V"):
            return "v"
        elif etiqueta_pos_stanford.startswith("J"):
            return "a"
        elif etiqueta_pos_stanford.startswith("R"):
            return "r"
        else:
            return None
        
    def lematizar_tuplas(self, lista_tuplas):
        if not isinstance(lista_tuplas, list):
            raise Exception("Error, se esperaba una lista.")
        
        lista_tuplas_pos = list()
        
        for palabra, etiqueta in lista_tuplas:
            
            tupla = (palabra, etiqueta, self.lematizar_palabra(palabra, etiqueta))
            lista_tuplas_pos.append(tupla)
            
        return lista_tuplas_pos