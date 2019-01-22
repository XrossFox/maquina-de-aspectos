import stanfordcorenlp
import configuracion

class ClienteCoreNLP(object):
    '''
    Clase que hace de cliente con el servicio de Stanoford CoreNLP.
    '''


    def __init__(self):
        '''
        Constructor: inicializa el servidor de Stanford CoreNLP
        '''
        config = configuracion.Configuracion()
        self.core_nlp = stanfordcorenlp.StanfordCoreNLP(config.direccion_corenlp)
    
    def cerrar_servicio(self):
        """
        Termina el servicio CoreNLP
        """
        self.core_nlp.close()
        
    def etiquetar_texto(self, texto):
        """
        Envia un texto al sevicio CoreNLP para ser etiquetado con el POS Tagger
        @param texto: el texto a ser etiquetado (en ingles).
        @return: una lista de tuplas de cada palabra con su etiqueta
        """
        texto = texto.strip()
        if not texto:
            raise Exception("Se recibio un string vacio.")
        return self.core_nlp.pos_tag(texto)
    
    def resolver_dependencias(self, texto):
        """
        Envia un texto al servicio CoreNLP para realizar un análisis de dependencias.
        @param texto: texto a analizar (en ingles).
        @return: lista de tuplas con el tipo de dependencia, indice de palabra rama, indice de palabra hoja.
        """
        
        texto = texto.strip()
        if not texto:
            raise Exception("Se recibio un string vacio.")
        return self.core_nlp.dependency_parse(texto)
