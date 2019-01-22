import sys
sys.path.append('../../extractor_de_aspectos')

import unittest
from cliente_corenlp import cliente_corenlp

class Test(unittest.TestCase):


    def setUp(self):
        self.cliente = cliente_corenlp.ClienteCoreNLP()


    def tearDown(self):
        self.cliente.cerrar_servicio()

    def test_pos_tag_regresa_lista(self):
        """
        Prueba que metodo etiquetar_texto devuelva una lista.
        """
        texto_prueba = "My name is Jose, and i like peanuts."
        
        resultado = self.cliente.etiquetar_texto(texto_prueba)
        
        self.assertTrue(isinstance(resultado, list))
        
    def test_pos_tag_contenido_1(self):
        """
        Prueba que el método etiquetar_texto devuelva una lista con el texto etiquetado apropiado.
        """

        texto_prueba = "My name is Jose, and i like peanuts."
        
        salida_esperada = [('My', 'PRP$'), ('name', 'NN'), ('is', 'VBZ'), ('Jose', 'NNP'),
                 (',', ','), ('and', 'CC'), ('i', 'FW'), ('like', 'IN'),
                 ('peanuts', 'NNS'), ('.', '.')]
        
        resultado = self.cliente.etiquetar_texto(texto_prueba)
        
        self.assertEqual(salida_esperada, resultado)
        
    def test_pos_tag_contenido_cadena_vacia(self):
        """
        Prueba que el método etiquetar_texto levante una excepcion al recibir un string vacio.
        """

        texto_prueba = ""
        
        with self.assertRaises(Exception):
            self.cliente.etiquetar_texto(texto_prueba)
            
    def test_pos_tag_contenido_espacio_vacio(self):
        """
        Prueba que el método etiquetar_texto levante una excepcion al recibir un string con un espacio vacio.
        """
        
        texto_prueba = " "
        
        with self.assertRaises(Exception):
            self.cliente.etiquetar_texto(texto_prueba)

    def test_pos_tag_contenido_espacio_vacio_2(self):
        """
        Prueba que el método etiquetar_texto levante una excepcion al recibir un string con multiples
        espacios vacios.
        """
        
        texto_prueba = "      "
        
        with self.assertRaises(Exception):
            self.cliente.etiquetar_texto(texto_prueba)

            
    def test_pos_tag_contenido_none(self):
        """
        Prueba que el método etiquetar_texto levante una excepcion al recibir none
        """
        
        texto_prueba = None
        
        with self.assertRaises(Exception):
            self.cliente.etiquetar_texto(texto_prueba)
            
    def test_pos_tag_contenido_no_string(self):
        """
        Prueba que el método etiquetar_texto levante una excepcion al recibir un objeto que
        no sea str
        """
        
        texto_prueba = 12

        with self.assertRaises(Exception):
            self.cliente.etiquetar_texto(texto_prueba)
            
    def test_resolver_dependencias_lista(self):
        """
        Prueba que el método resolver_dependencias devuelva una lista.
        """
        
        texto_prueba = "I love stanford dependency parser"
        
        resultado = self.cliente.resolver_dependencias(texto_prueba)
        
        self.assertTrue(isinstance(resultado, list))
        
    def test_resolver_dependencias_1(self):
        """
        Prueba la salida del método resolver_dependencias.
        """
        
        texto_prueba = "I love stanford dependency parser"
        
        resultado = self.cliente.resolver_dependencias(texto_prueba)
        
        resultado_esperado = [('ROOT', 0, 2), ('nsubj', 2, 1),
                               ('compound', 5, 3), ('compound', 5, 4),
                                ('dobj', 2, 5)]
        
        self.assertEqual(resultado, resultado_esperado)
        
    def test_resolver_dependencias_none(self):
        """
        Prueba que el método resolver_dependencias levante una excepcion al recibir None.
        """
        
        texto_prueba = None
        
        with self.assertRaises(Exception):
            self.cliente.resolver_dependencias(texto_prueba)
            
    def test_resolver_dependencias_string_vacio_1(self):
        """
        Prueba que el método resolver_dependencias levante una excepcion al recibir un string vacio.
        """
        
        texto_prueba = ""
        
        with self.assertRaises(Exception):
            self.cliente.resolver_dependencias(texto_prueba)
            
    def test_resolver_dependencias_string_vacio_2(self):
        """
        Prueba que el método resolver_dependencias levante una excepcion al recibir un string con
        espacios en blanco.
        """
        
        texto_prueba = "     "
        
        with self.assertRaises(Exception):
            self.cliente.resolver_dependencias(texto_prueba)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()