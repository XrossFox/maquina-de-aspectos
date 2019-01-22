import sys
sys.path.append('../')

import unittest
from bs4 import BeautifulSoup
import json

import eliminador_de_etiquetas as el_et

class TestEliminacionDeEtiquetas(unittest.TestCase):
    """Clase que prueba el m�todo de eliminaci�n de etiquetas html/xml y urls"""
    
    def setUp(self):
        self.el = el_et.EliminadorDeEtiquetas()
    
    def test_elimina_etiquetas(self):
        """Este test prueba que se eliminaron las etiquetas"""
        #https://stackoverflow.com/questions/24856035/how-to-detect-with-python-if-the-string-contains-html-code
        #https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
        json_file = open("test.json", mode="r", encoding="utf-8")
        test_text = json.load(json_file)
        json_file.close()
        
        for text in test_text:
            self.assertFalse(self.prueba_etiqueta(self.el.remover_etiquetas(text)),"Tag html presente en: {}".format(text))
        
    def prueba_etiqueta(self, text):
        """Si encuentra una etiqute HTML, regresa True. False si es el caso contrario"""
        return bool(BeautifulSoup(text, "html.parser").find())
    
    def test_reemplaza_etiqueta_code(self):
        string = "Este es <code>codigo</code>"
        resultado = "Este es code_removed"
        
        self.assertEqual(self.el.remover_codigo(string), resultado)
        
    def test_reemplaza_etiqueta_code_2(self):
        string = "Este es <code>codigo.codigo()</code>."
        resultado = "Este es code_removed."
        
        self.assertEqual(self.el.remover_codigo(string), resultado)
        
    def test_reemplaza_etiquetas_code(self):
        string = "multiples etiquetas code <code>Este es</code> <code>codigo</code>"
        resultado = "multiples etiquetas code code_removed code_removed"
        
        self.assertEqual(self.el.remover_codigo(string), resultado)
    
    def test_remover_escaper(self):
        string = "\nun\bmonton\\de\a\fescapes\rde\tcaracteres"
        resultado = " un monton de  escapes de caracteres"
        
        self.assertEqual(self.el.remover_escapes(string), resultado)
    
if __name__ == "__main__":
    unittest.main()
        