import os
import sys
sys.path.append('../')

import unittest
import limpiador_de_texto as lim


class TestLimpiezaDeTexto(unittest.TestCase):
    """Pruebas para el modulo limpieza_de_texto.py"""
    
    def setUp(self):
        self.l = lim.LimpiadorDeTexto(os.getcwd()+"/../stopwords.txt")
    
    def test_remocion_de_espacios(self):
        """
        Probar que remocion_de_espacio remueve todos los espacios en blanco duplicados y al inicio/fin de un texto
        """
        
        strings_de_prueba = [
            "buenas noches",
            " buenas noches",
            " buenas noches ",
            "buenas  noches ",
            "     buenas          noches      ",
        ]
        
        strings_de_salida = [
            "buenas noches",
            "buenas noches",
            "buenas noches",
            "buenas noches",
            "buenas noches",
        ]
        
        for i in range(len(strings_de_prueba)):
            self.assertEqual(self.l.remocion_de_espacios(strings_de_prueba[i]), strings_de_salida[i])
        
    
    def test_remocion_de_urls(self):
        """
        Probar que remocion_de_urls remueve todos los urls de un string
        """
        
        strings_de_prueba = [
            "https://www.google.com/",
            "http://www.google.com/",
            "https://www.google.com/, holo"
        ]
        
        strings_de_salida = [
            "",
            "",
            " holo",
        ]
        
        for i in range(len(strings_de_prueba)):
            self.assertEqual(self.l.remocion_de_urls(strings_de_prueba[i]), strings_de_salida[i])
        
    
    def test_remocion_de_numeros(self):
        """
        Probar que remocion_de_numero remueve todos los numeros de un string
        """
        
        strings_de_prueba = [
            "uno 1",
            "dos veces dos 22",
            "nada",
            "un cero a la izquierda 0123",
            "1,222,369 de pesos",
            ]
        
        strings_de_salida = [
            "uno ",
            "dos veces dos ",
            "nada",
            "un cero a la izquierda ",
            ",, de pesos",
        ]
        
        for i in range(len(strings_de_prueba)):
            self.assertEqual(self.l.remocion_de_numeros(strings_de_prueba[i]), strings_de_salida[i])
            
    def test_remocion_de_puntuaciones(self):
        """
        Probar que remocion_de_puntuaciones remueve todos los signos de puntuación de un string
        """
        
        strings_de_prueba = [
            "Esto es una prueba",
            "aqui, otra prueba",
            "pero que rayos es esto!?",
            "signos de puntuacion ,.:;´'\"",
            "¿¡Holi, que hace!? :D",
            "what’?"
            ]
        
        strings_de_salida = [
            "Esto es una prueba",
            "aqui otra prueba",
            "pero que rayos es esto",
            "signos de puntuacion ",
            "Holi que hace D",
            "what"
        ]
        
        for i in range(len(strings_de_prueba)):
            self.assertEqual(self.l.remocion_de_puntuaciones(strings_de_prueba[i]), strings_de_salida[i])
            
    
    def _remocion_no_letras(self):
        """Prueba que se remueva cualquier caracter que no sea una letra y URLs."""
        test_strings = ["i, like2. potatos.?", "!i like potatos",
                        "i ,,''\".. enjoy. life..,;:", "::halp::", "\"oh ; noes\"",
                        "this is just fine", "123, cha cha cha!", "¿que demonios, tio? ", " probando    espacios en  blanco   ",
                        "im an url http://www.google.com"
            ]
        
        respuestas = ["i like potatos", "i like potatos", 
                      "i enjoy life", "halp", "oh noes", "this is just fine", "cha cha cha", "que demonios tio",
                      "probando espacios en blanco", "im an url"]
        
        for i in range(len(test_strings)):
            self.assertEqual(respuestas[i], self.l.limpieza(test_strings[i]))
            
    def test_remocion_stopwords(self):
        """Prueba que las stop words sean removidas del texto"""
        
        test_strings = ["im not blue", "im also tall", "dont do that", "not cool bro", "i Cato Sicarius", "i am blue",
                        "luckily, django provides checks to avoid this kind of leakage before hitting production with",
                        "this is a great concrete example why you should never run debug mode on a public server. django can only do so much for redacting private info. this is also a great example of how insecure pickle is!"]
        
        res_strings = ["not blue", "also tall", "dont", "not cool bro", "Cato Sicarius", "blue",
                       "luckily, django provides checks avoid kind leakage hitting production",
                       "great concrete example never run debug mode public server. django much redacting private info. also great example insecure pickle!"]
        
        res = []
        for string in test_strings:
            res.append(self.l.remocion_de_stopwords(string))
        
        for i in range(len(test_strings)):
            self.assertEqual(res[i], res_strings[i])
        
        
        
            
if __name__ == "__main__":
    unittest.main()
    