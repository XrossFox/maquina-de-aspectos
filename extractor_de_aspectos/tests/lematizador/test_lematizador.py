import sys
sys.path.append('../../extractor_de_aspectos')

import unittest
from lematizador import lematizador


class Test(unittest.TestCase):


    def setUp(self):
        self.lem = lematizador.Lematizador()

    def test_lematizar_palabra_parametros(self):
        """
        Prueba que lematizar_palabra reciba dos parametros: palabra y etiqueta_pos.
        """
        
        palabra = "person"
        pos = "NN"
        
        self.lem.lematizar_palabra(palabra=palabra,etiqueta_pos_stanford=pos)
        
    def test_lematizar_palabra_devuelve_string(self):
        """
        Prueba que lematizar_palabra devuelva un string
        """
        palabra = "person"
        pos = "NN"
        
        resultado = self.lem.lematizar_palabra(palabra=palabra,etiqueta_pos_stanford=pos)
        
        self.assertTrue(isinstance(resultado, str))
        
    def test_lematizar_palabra_noun_1(self):
        """
        Prueba que lematizar_palabra acepte sustantivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ('potatoes', 'NNS')
        
        palabra_esperada = 'potato'
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(resultado, palabra_esperada)
        
        
    def test_lematizar_palabra_noun_2(self):
        """
        Prueba que lematizar_palabra acepte sustantivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ('people', 'NNS')
        
        palabra_esperada = 'people'
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(resultado, palabra_esperada)
        
    def test_lematizar_palabra_noun_3(self):
        """
        Prueba que lematizar_palabra acepte sustantivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ('kitty', 'NNp')
        
        palabra_esperada = 'kitty'
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(resultado, palabra_esperada)
        
    def test_lematizar_palabra_noun_4(self):
        """
        Prueba que lematizar_palabra acepte sustantivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ('jumper', 'NN')
        
        palabra_esperada = 'jumper'
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(resultado, palabra_esperada)
        
    def test_lematizar_palabra_noun_5(self):
        """
        Prueba que lematizar_palabra acepte sustantivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ('assailant', 'NN')
        
        palabra_esperada = 'assailant'
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(resultado, palabra_esperada)
        
    def test_lematizar_palabra_noun_6(self):
        """
        Prueba que lematizar_palabra acepte sustantivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ('projectors', 'NN')
        
        palabra_esperada = 'projector'
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(resultado, palabra_esperada)
        
    def test_lematizar_palabra_verb_1(self):
        """
        Prueba que lematizar_palabra acepte verbos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ("jumping", "VBG")
        
        palabra_esperada = "jump"
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(resultado, palabra_esperada)
        
    def test_lematizar_palabra_verb_2(self):
        """
        Prueba que lematizar_palabra acepte verbos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ("assailing", "VBG")
        
        palabra_esperada = "assail"
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(resultado, palabra_esperada)
        
    def test_lematizar_palabra_verb_3(self):
        """
        Prueba que lematizar_palabra acepte verbos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ("projecting", "VBG")
        
        palabra_esperada = "project"
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(resultado, palabra_esperada)
        
    def test_lematizar_palabra_adjetivo_1(self):
        """
        Prueba que lematizar_palabra acepte adjetivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ("agreeable", "JJ")
        
        palabra_esperada = "agreeable"
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_lematizar_palabra_adjetivo_2(self):
        """
        Prueba que lematizar_palabra acepte adjetivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ("aggressive", "JJ")
        
        palabra_esperada = "aggressive"
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_lematizar_palabra_adjetivo_3(self):
        """
        Prueba que lematizar_palabra acepte adjetivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ("ambitious", "JJ")
        
        palabra_esperada = "ambitious"
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_lematizar_palabra_adverbio_1(self):
        """
        Prueba que lematizar_palabra acepte adjetivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ("ultimately", "RB")
        
        palabra_esperada = "ultimately"
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_lematizar_palabra_adverbio_2(self):
        """
        Prueba que lematizar_palabra acepte adjetivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ("fast", "RB")
        
        palabra_esperada = "fast"
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_lematizar_palabra_adverbio_3(self):
        """
        Prueba que lematizar_palabra acepte adjetivos con la etiqueta POS de Stanford.
        """
        tupla_stanford_pos = ("faster", "RBR")
        
        palabra_esperada = "faster"
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_mapeo_etiquetas_nouns(self):
        """
        Prueba que el método auxiliar mapeo_de_etiquetas pueda traducir las etiquetas POS de Stanford
        por las etiquetas POS de Wordnet. Prueba de sustantivos.
        """
        etiqueta_pos_stanford = "NNS"
        etiqueta_pos_wordnet = "n"
        
        resultado = self.lem.mapeo_de_etiquetas(etiqueta_pos_stanford=etiqueta_pos_stanford)
        
        self.assertEqual(etiqueta_pos_wordnet, resultado)
        
    def test_mapeo_etiquetas_verbs(self):
        """
        Prueba que el método auxiliar mapeo_de_etiquetas pueda traducir las etiquetas POS de Stanford
        por las etiquetas POS de Wordnet. Prueba de verbos.
        """
        etiqueta_pos_stanford = "VBG"
        etiqueta_pos_wordnet = "v"
        
        resultado = self.lem.mapeo_de_etiquetas(etiqueta_pos_stanford)
        
        self.assertEqual(etiqueta_pos_wordnet, resultado)
        
    def test_mapeo_etiquetas_adjectives(self):
        """
        Prueba que el método auxiliar mapeo_de_etiquetas pueda traducir las etiquetas POS de Stanford
        por las etiquetas POS de Wordnet. Prueba de adjetivos.
        """
        etiqueta_pos_stanford = "JJ"
        etiqueta_pos_wordnet = "a"
        
        resultado = self.lem.mapeo_de_etiquetas(etiqueta_pos_stanford)
        
        self.assertEqual(etiqueta_pos_wordnet, resultado)
        
    def test_mapeo_etiquetas_adverbs(self):
        """
        Prueba que el método auxiliar mapeo_de_etiquetas pueda traducir las etiquetas POS de Stanford
        por las etiquetas POS de Wordnet. Prueba de adverbios.
        """
        etiqueta_pos_stanford = "RBR"
        etiqueta_pos_wordnet = "r"
        
        resultado = self.lem.mapeo_de_etiquetas(etiqueta_pos_stanford)
        
        self.assertEqual(etiqueta_pos_wordnet, resultado)
        
    def test_mapeo_etiquetas_diferentes_uh(self):
        """
        Prueba que el método auxiliar mapeo_de_etiquetas pueda traducir las etiquetas POS de Stanford
        por las etiquetas POS de Wordnet. Prueba de etiquetas POS de Stanford no soportadas por
        wordnet. Debe regresar 'None'. Prueba de etiqueta UH
        """
        etiqueta_pos_stanford = "UH"
        etiqueta_pos_wordnet = None
        
        resultado = self.lem.mapeo_de_etiquetas(etiqueta_pos_stanford)
        
        self.assertEqual(etiqueta_pos_wordnet, resultado)
        
    def test_lematizar_palabra_intejection(self):
        """
        Prueba que lematizar_palabra regrese None con palabras de tags que no se encuentran en wordnet.
        """
        tupla_stanford_pos = ("hello", "UH")
        
        palabra_esperada = None
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_mapeo_etiquetas_diferentes_prp(self):
        """
        Prueba que el método auxiliar mapeo_de_etiquetas pueda traducir las etiquetas POS de Stanford
        por las etiquetas POS de Wordnet. Prueba de etiquetas POS de Stanford no soportadas por
        wordnet. Debe regresar 'None'. Prueba de etiqueta PRP
        """
        etiqueta_pos_stanford = "PRP"
        etiqueta_pos_wordnet = None
        
        resultado = self.lem.mapeo_de_etiquetas(etiqueta_pos_stanford)
        
        self.assertEqual(etiqueta_pos_wordnet, resultado)
        
    def test_lematizar_palabra_pronombre(self):
        """
        Prueba que lematizar_palabra regrese None con palabras de tags que no se encuentran en wordnet.
        """
        tupla_stanford_pos = ("me", "PRP")
        
        palabra_esperada = None
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_mapeo_etiquetas_diferentes_prp_pesos(self):
        """
        Prueba que el método auxiliar mapeo_de_etiquetas pueda traducir las etiquetas POS de Stanford
        por las etiquetas POS de Wordnet. Prueba de etiquetas POS de Stanford no soportadas por
        wordnet. Debe regresar 'None'. Prueba de etiqueta PRP
        """
        etiqueta_pos_stanford = "PRP$"
        etiqueta_pos_wordnet = None
        
        resultado = self.lem.mapeo_de_etiquetas(etiqueta_pos_stanford)
        
        self.assertEqual(etiqueta_pos_wordnet, resultado)
        
    def test_lematizar_palabra_pronombre_peso(self):
        """
        Prueba que lematizar_palabra regrese None con palabras de tags que no se encuentran en wordnet.
        """
        tupla_stanford_pos = ("its", "PRP$")
        
        palabra_esperada = None
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_mapeo_etiquetas_diferentes_ex(self):
        """
        Prueba que el método auxiliar mapeo_de_etiquetas pueda traducir las etiquetas POS de Stanford
        por las etiquetas POS de Wordnet. Prueba de etiquetas POS de Stanford no soportadas por
        wordnet. Debe regresar 'None'. Prueba de etiqueta EX
        """
        etiqueta_pos_stanford = "EX"
        etiqueta_pos_wordnet = None
        
        resultado = self.lem.mapeo_de_etiquetas(etiqueta_pos_stanford)
        
        self.assertEqual(etiqueta_pos_wordnet, resultado)
        
    def test_lematizar_palabra_existencial(self):
        """
        Prueba que lematizar_palabra regrese None con palabras de tags que no se encuentran en wordnet.
        """
        tupla_stanford_pos = ("there", "EX")
        
        palabra_esperada = None
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_mapeo_etiquetas_diferentes_wdt(self):
        """
        Prueba que el método auxiliar mapeo_de_etiquetas pueda traducir las etiquetas POS de Stanford
        por las etiquetas POS de Wordnet. Prueba de etiquetas POS de Stanford no soportadas por
        wordnet. Debe regresar 'None'. Prueba de etiqueta WDT
        """
        etiqueta_pos_stanford = "WDT"
        etiqueta_pos_wordnet = None
        
        resultado = self.lem.mapeo_de_etiquetas(etiqueta_pos_stanford)
        
        self.assertEqual(etiqueta_pos_wordnet, resultado)
        
    def test_lematizar_palabra_determinador(self):
        """
        Prueba que lematizar_palabra regrese None con palabras de tags que no se encuentran en wordnet.
        """
        tupla_stanford_pos = ("that", "WDT")
        
        palabra_esperada = None
        
        resultado = self.lem.lematizar_palabra(tupla_stanford_pos[0], tupla_stanford_pos[1])
        
        self.assertEqual(palabra_esperada, resultado)
        
    def test_lematizar_palabra_palabra_none(self):
        """
        Prueba que levante una excepcion cuando se reciba None como parametro 'palabra'.
        """
        
        with self.assertRaises(Exception):
            self.lem.lematizar_palabra(None, "NNS")
            
    def test_lematizar_palabra_palabra_numero(self):
        """
        Prueba que levante una excepcion cuando se reciba un numero como parametro 'palabra'.
        """
        
        with self.assertRaises(Exception):
            self.lem.lematizar_palabra(15, "NNS")
            
    def test_lematizar_palabra_pos_none(self):
        """
        Prueba que levante una excepcion cuando se reciba None como parametro 'etiqueta_pos_stanford'.
        """
        
        with self.assertRaises(Exception):
            self.lem.lematizar_palabra("valid", None)
            
    def test_lematizar_palabra_pos_numero(self):
        """
        Prueba que levante una excepcion cuando se reciba un numero como parametro 'etiqueta_pos_stanford'.
        """
        
        with self.assertRaises(Exception):
            self.lem.lematizar_palabra("valid", 15)
            
    def test_lematizar_tuplas_recibe_lista(self):
        """
        Prueba que lematizar_ruplas levante una exepcion si no recibe una lista.
        """
        
        with self.assertRaises(Exception):
            self.lem.lematizar_tuplas(None)
            
    def test_lematizar_tuplas_1(self):
        """
        Prueba que regrese una tupla de la siguiente manera ("palabra", "etiqueta", "lema")
        """
        
        lista_pos = [('i', 'LS'), ('am', 'VBP'), ('a', 'DT'), ('valid', 'JJ'),
                     ('comment', 'NN'), ('.', '.')]
        
        lista_esperada = [('i', 'LS', None), ('am', 'VBP', 'be'), ('a', 'DT', None), ('valid', 'JJ', 'valid'),
                           ('comment', 'NN', 'comment'), ('.', '.', None)]
        
        res = self.lem.lematizar_tuplas(lista_pos)
        
        self.assertEqual(res, lista_esperada)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()