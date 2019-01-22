import sys
sys.path.append('../')

import unittest
import extractor_de_raices

class TestRaices(unittest.TestCase):
    
    def setUp(self):
        self. ra = extractor_de_raices.ExtractorDeRaices()
    
    def test_stem(self):
        """
        Prueba la funcion _stem_palabra del modulo raices. Extrae la parte no cambiante de una palabra.
        """
        
        test_strings = ['computer', 'computation', 'comparison', 'parse', 'parser', 'parsing',
                         'involment', 'involved', 'involve', 'jumper', 'jumping', 'jumped', 'jump',]
        
        stemmed_strings = ['comput', 'comput', 'comparison', 'pars', 'parser', 'pars',
                           'invol', 'involv', 'involv', 'jumper', 'jump', 'jump', 'jump',]
        
        for i, j in zip(test_strings, stemmed_strings):
            self.assertEqual(self.ra._stem_palabra(i), j)
            
    def test_text_lemmatization(self):
        """
        Prueba la funcion _lem_palabra del modulo raices. Extrae la raiz de la palabra según su significado de diccionario.
        """
        
        test_strings = ['gets', 'potatoes', 'cats', 'women', 'words', 'reads', 'computers', 'processes', 'jumpers', 'felines', 'getting']
        
        lem_strings = ['get', 'potato', 'cat', 'woman', 'word', 'read', 'computer', 'process', 'jumper', 'feline', 'getting']
        
        for i, j in zip(test_strings, lem_strings):
            self.assertEqual(self.ra._lem_palabra(i), j)
            
    def test_stem_string(self):
        """
        Prueba la funcion stem_texto. Devuelve un string donde cada palabra ha sido extraida la parte no cambiante.
        """
        
        test_string = "computer computation comparison parse parser parsing involment involved involve jumper jumping jumped jump"
        
        stem_string = "comput comput comparison pars parser pars invol involv involv jumper jump jump jump"
        
        self.assertEqual(self.ra.stem_texto(test_string), stem_string)
    
    def test_lem_string(self):
        """
        Prueba la funcion lem_texto. Devuelve un string con cada palabra lematizada.
        """
        
        test_string = "gets potatoes cats women words reads computers processes jumpers felines"
        
        lem_string = "get potato cat woman word read computer process jumper feline" 
        
        self.assertEqual(self.ra.lem_texto(test_string), lem_string)
        
            
if __name__ == '__main__':
    unittest.main()