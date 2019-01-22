class Configuracion():

    def __init__(self):
        # path/a/core/nlp
        self._dir_corenlp = "path/a/corenlp"
        # path/a/stopwords.txt
        self._stopwords = "./stopwords.txt"

    def get_dir_corenlp(self): return self._dir_corenlp
    def get_stopwords(self): return self._stopwords

    dir_corenlp = property(fget=get_dir_corenlp)
    stopwords = property(fget=get_stopwords)