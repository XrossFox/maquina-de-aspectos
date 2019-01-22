from html.parser import HTMLParser
from bs4 import BeautifulSoup
import re

class EliminadorDeEtiquetas():

    def remover_etiquetas(self, texto):
        """Elimina tags HTML de un string"""
        etiquetador = Etiquetador()
        etiquetador.feed(texto)
        return etiquetador.get_data()
    
    def remover_escapes(self, texto):
        """Remueve los caracteres escapables de un string"""
        texto = texto.replace('\n', ' ')
        texto = texto.replace("\\", " ")
        texto = texto.replace("\a", " ")
        texto = texto.replace("\b", " ")
        texto = texto.replace("\f", " ")
        texto = texto.replace("\r", " ")
        texto = texto.replace("\t", " ")
        return texto
    
    def remover_codigo(self, texto):
        """Remueve los tags html de codigo y su contenido."""
        texto = re.sub(r"<code>.*?<\/code>", "code_removed", texto).strip()
        texto = re.sub(r"\s(?=[\.\,\?\!\:\;])", "", texto).strip()
        return texto
    
class Etiquetador(HTMLParser):
    """Extiende de HTMLParser para extraer contenido de tags html"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)