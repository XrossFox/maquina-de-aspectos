class Configuracion(object):

    def __init__(self):
        self._direccion_corenlp = "C:/David/Repos/Tesis-Analisis-Aspectos/preprocesamiento/corenlp/CoreNLP"
        self._direccion_stopwords = "C:/David/Repos/Tesis-Analisis-Aspectos/preprocesamiento/stopwords.txt"
        
    def get_direccion_corenlp(self): return self._direccion_corenlp
    def get_direccion_stopwords(self): return self._direccion_stopwords
    
    direccion_corenlp = property(fget=get_direccion_corenlp)
    direccion_stopwords = property(fget=get_direccion_stopwords)