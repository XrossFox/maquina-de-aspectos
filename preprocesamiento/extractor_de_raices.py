import nltk

class ExtractorDeRaices():

    def _stem_palabra(self, palabra):
        """
        Extrae la parte no cambiante de una palabra.
        """
        
        stm = nltk.PorterStemmer()
        return stm.stem(palabra)
    
    def _lem_palabra(self, palabra):
        """
        Extrae la raiz de la palabra según su significado de diccionario.
        """
        
        lem = nltk.WordNetLemmatizer()
        return lem.lemmatize(palabra)
    
    def stem_texto(self, texto):
        """
        Devuelve un texto donde cada palabra ha sido extraida la parte no cambiante.
        """
        
        tok = nltk.tokenize
        palabras = tok.word_tokenize(texto)
        tmp = []
        
        for palabra in palabras:
            tmp.append(self._stem_palabra(palabra))
        
        salida = ""
        for i in range(len(tmp)):
            salida += tmp[i] + " "
            
        return salida.strip()
    
    def lem_texto(self, texto):
        """
        Devuelve un texto con cada palabra lematizada.
        """
        
        tok = nltk.tokenize
        palabras = tok.word_tokenize(texto)
        tmp = []
        
        for palabra in palabras:
            tmp.append(self._lem_palabra(palabra))
            
        salida = ""
        for i in range(len(tmp)):
            salida += tmp[i] + " "
            
        return salida.strip()
    
    