class Configuracion():

    def __init__(self):
        # path/a/core/nlp
        self._dir_corenlp = "/home/david/Desktop/tesis/corenlp"
        # path/a/stopwords.txt
        self._stopwords = "/home/david/Desktop/tesis/Tesis-Analisis-Aspectos/preprocesamiento/stopwords.txt"

    def get_dir_corenlp(self): return self._dir_corenlp
    def get_stopwords(self): return self._stopwords

    dir_corenlp = property(fget=get_dir_corenlp)
    stopwords = property(fget=get_stopwords)