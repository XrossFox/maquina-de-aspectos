import os
import sys
sys.path.append('../')

import unittest
import solucionador_de_correferencias as corref

class TestCorreferencias(unittest.TestCase):
    
    def setUp(self):
        print(os.getcwd())
        self.C = corref.SolucionadorDeCorreferencias(os.getcwd()+"\\..\\corenlp\\CoreNLP")
    
    def test_resolucion_de_correferencias(self):
        """Prueba si las correferencias son reemplazadas correctamente. Reemplaza pronombres de tema u objeto por su tem u objeto respectivamente"""
        
        #Entradas
        li = [
            "My blue shirt is awesome, i really like it. It's also very expensive",
            "That cat is so small, it fits in my hand",
            "Radioactivity is very dangerous, it can kill you or it can make you grow a third arm. Stay away from it",
            "My hands are cold, they are trembling",
            "That thing is weird, is so ugly it makes my eyes sore. I´m going to burn it in the furnace",
            "I'm tall. I also exercise daily.",
            "My favorite food is hamburgers. My favorite color is green.",
            "I like roses, I like them",
            "That is very obvious, no way to miss it",
            "My car is red. It's color is very lively",
        ]
        
        #Salidas esperadas
        lo = [
            "my blue shirt is awesome, i really like my blue shirt. my blue shirt's also very expensive",
            "that cat is so small, cat fits in my hand",
            "radioactivity is very dangerous, radioactivity can kill you or radioactivity can make you grow a third arm. stay away from radioactivity",
            "my hands are cold, my hands are trembling",
            "that thing is weird, is so ugly thing makes my eyes sore. i´m going to burn thing in the furnace",
            "i'm tall. i also exercise daily.",
            "my favorite food is hamburgers. my favorite color is green.",
            "i like roses, i like roses",
            "that is very obvious, no way to miss it",
            "my car is red. my car's color is very lively",
        ]
        
        
        
        for i, o in zip(li,lo):
            res = self.C.resolver_y_reemplazar(i)
            self.assertEqual(res, o)

    def tearDown(self):
        self.C.cerrar()

if __name__ == "__main__":
    unittest.main()
        
        
        
        
        
    