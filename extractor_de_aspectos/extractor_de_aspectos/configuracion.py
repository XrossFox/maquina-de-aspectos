import json

class Configuracion(object):
    '''
    Clase de condifuracion para el programa.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #Aqui debe poner la direccion de la carpeta raiz de CoreNLP (donde se encuentra stanford-corenlp-3.9.1.jar)
        self._direccion_corenlp = "/home/david/Desktop/tesis/corenlp"
        self._path_dict_aspectos = "/home/david/Desktop/tesis/Tesis-Analisis-Aspectos/extractor_de_aspectos/extractor_de_aspectos/diccionario_de_aspectos.json"
    
    def get_direccion_corenlp(self): return self._direccion_corenlp
    
    def get_dict_aspectos(self):
        if hasattr(self, "_dict_aspectos"):
            return self._dict_aspectos
        with open(self._path_dict_aspectos, mode="r", encoding="utf-8") as w:
            self._dict_aspectos = json.load(w) 
            return self._dict_aspectos
    
    direccion_corenlp = property(get_direccion_corenlp)
    dict_aspectos = property(get_dict_aspectos)
        