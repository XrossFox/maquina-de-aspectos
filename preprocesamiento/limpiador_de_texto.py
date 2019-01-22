import string
import re
import nltk

class LimpiadorDeTexto():
    
    def __init__(self,dir_stopwords):
        """
        Inicializa y carga lista de stopwords desde el path recibido
        """
        
        arc = open(dir_stopwords, "r", encoding='utf-8')
        self.stp_wrds = [line.strip() for line in arc]
        arc.close()
    
    def remocion_de_espacios(self, texto):
        """
        Remueve todos los espacios en blanco duplicados y al inicio/fin de un texto
        """
        
        texto = re.sub('  +', ' ', texto)
        return texto.strip()
    
    def remocion_de_urls(self, texto):
        """
        Remueve los urls de un texto
        """
        
        texto = re.sub(r'http\S+', '', texto)
        return texto
    
    def remocion_de_numeros(self, texto):
        """
        Remueve todos los números en un texto
        """
    
        translator = str.maketrans(dict.fromkeys("0123456789"))
        texto = texto.translate(translator)
        return texto  
    
    def remocion_de_puntuaciones(self, texto):
        """
        Remueve todos los signos de puntuación de un texto
        """
        
        translator = str.maketrans(dict.fromkeys(string.punctuation + "¿¡´’"))
        texto = texto.translate(translator)
        return texto
    
    
    def remocion_de_stopwords(self,texto):
        """
        Remueve las stopwords dentro de un cuerpo de texto.
        """
        
        tok = nltk.tokenize
        palabras = tok.word_tokenize(texto)
        
        palabras_salida = []
        
        for palabra in palabras:
            if palabra not in self.stp_wrds:
                palabras_salida.append(palabra)
        
        salida = ""
        for i in range(len(palabras_salida)):
            if palabras_salida[i] in string.punctuation:
                salida = salida.strip()+palabras_salida[i] + " "
            else:
                salida += palabras_salida[i] + " "
        
        salida = self.remocion_de_espacios(salida)
        return salida
        

    
    