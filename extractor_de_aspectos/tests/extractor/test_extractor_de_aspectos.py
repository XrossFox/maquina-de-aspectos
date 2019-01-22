import sys
sys.path.append('../../extractor_de_aspectos')

import unittest
from extractor import extractor_de_aspectos
from cliente_corenlp import cliente_corenlp
from lematizador import lematizador
import nltk

class Test(unittest.TestCase):


    def setUp(self):
        self.ex = extractor_de_aspectos.ExtractorDeAspectos()
        self.cliente = cliente_corenlp.ClienteCoreNLP()
        self.lemas = lematizador.Lematizador()        
        
    def test_extractor_recibe_arbol_de_dependencias(self):
        """
        Para poder extraer los aspectos, primero se necesita pasar como argumento el arbol de dependencias
        que resuelve el Stanford CoreNLP.
        
        Prueba que el método extraer levante una excepcion si no recibe el arbol de aspectos en fora de una lista
        (la salida que ofrece cliente_corenlp.resolver_dependencias).
        """
        
        com = "i am a valid comment."
        diccionario = dict()
        arbol = None
        pos_lem = list()
        
        with self.assertRaises(Exception):
            self.ex.extraer(com, diccionario, arbol, pos_lem)
        
    def test__buscar_en_tupla_pos_lem(self):
        """
        Prueba el método auxiliar que es usado para buscar el lema o la palabra de una tupla pos_lem
        dado una posición.
        Se espera que de la tupla en la posición 1, devuelve el lema 'be'.
        """
        tupla_pos_lem = [('i', 'LS', None), ('am', 'VBP', 'be'), ('a', 'DT', None), ('valid', 'JJ', 'valid'),
                          ('comment', 'NN', 'comment'), ('.', '.', None)]
        
        indice = 1
        resultado = self.ex._buscar_en_tupla_pos_lem(indice, tupla_pos_lem)
        
        resultado_esperado = 'be'
        
        self.assertEqual(resultado, resultado_esperado)
        
    def test__buscar_en_tupla_pos_lem_2(self):
        """
        Prueba el método auxiliar que es usado para buscar el lema o la palabra de una tupla pos_lem
        dado una posición.
        Se espera que de la tupla en la posición 3, devuelve la palabra 'a', ya que el lema es None.
        """
        tupla_pos_lem = [('i', 'LS', None), ('am', 'VBP', 'be'), ('a', 'DT', None), ('valid', 'JJ', 'valid'),
                          ('comment', 'NN', 'comment'), ('.', '.', None)]
        
        indice = 3
        resultado = self.ex._buscar_en_tupla_pos_lem(indice-1, tupla_pos_lem)
        
        resultado_esperado = 'a'
        
        self.assertEqual(resultado, resultado_esperado)
        
    def test__es_aspecto_1(self):
        """
        Prueba el método auxiliar que es usado para determinar si una palabra esta en el diccionario de aspectos.
        Se espera que la palabra 'comment' sea determinado como aspecto 'comment'.
        """
        
        palabra = 'comment'
        
        diccionario = {"comment":["comment"]}
        
        resultado = self.ex._es_aspecto(palabra, diccionario)
        
        self.assertEqual("comment", resultado)
        
    def test__es_aspecto_2(self):
        """
        Prueba el método auxiliar que es usado para determinar si una palabra esta en el diccionario de aspectos.
        Se espera que la palabra 'review' sea determinado como aspecto 'comment'.
        """
        
        palabra = 'comment'
        
        diccionario = {"comment":["comment", "review"]}
        
        resultado = self.ex._es_aspecto(palabra, diccionario)
        
        self.assertEqual("comment", resultado)
        
    def test__es_aspecto_3(self):
        """
        Prueba el método auxiliar que es usado para determinar si una palabra esta en el diccionario de aspectos.
        Se espera que la palabra 'review' no sea determinado como aspecto y devuelva None.
        """
        
        palabra = 'review'
        
        diccionario = {"comment":["comment"]}
        
        resultado = self.ex._es_aspecto(palabra, diccionario)
        
        self.assertEqual(None, resultado)
        
    def test__amod_1(self):
        """
        Prueba el método auxiliar _extraer_dependencia que se ejecuta cuando se encuentra una dependencia con la etiqueta "amod".
        Se espera una tupla ("comment", "valid")
        """
        indice_raiz = 5
        indice_nodo = 4
        lista_pos_lem = [('i', 'LS', None), ('am', 'VBP', 'be'), ('a', 'DT', None), ('valid', 'JJ', 'valid'),
                          ('comment', 'NN', 'comment'), ('.', '.', None)]
        diccionario_de_aspectos = {"comment":["comment"]}
        
        res = self.ex._extraer_dependencia(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos)
        
        res_esperado = ("comment", "valid")
        
        self.assertEqual(res, res_esperado)
        
    def test__amod_2(self):
        """
        Prueba el método auxiliar _extraer_dependencia que se ejecuta cuando se encuentra una dependencia con la etiqueta "amod".
        Se espera una tupla ("cyclone", "red")
        """
        indice_raiz = 4
        indice_nodo = 3
        lista_pos_lem = [('im', 'VB', None), ('the', 'DT', None), ('red', 'JJ', None),
                          ('cyclone', 'NN', None), ('.', '.', None)]

        diccionario_de_aspectos = {"cyclone":["cyclone"]}
        
        res = self.ex._extraer_dependencia(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos)
        
        res_esperado = ("cyclone", "red")
        
        self.assertEqual(res, res_esperado)
        
    def test__amod_3(self):
        """
        Prueba el método auxiliar _extraer_dependencia que se ejecuta cuando se encuentra una dependencia con la etiqueta "amod".
        Se espera None
        """
        indice_raiz = 4
        indice_nodo = 3
        lista_pos_lem = [('im', 'VB', None), ('the', 'DT', None), ('red', 'JJ', None),
                          ('cyclone', 'NN', None), ('.', '.', None)]

        diccionario_de_aspectos = {"not":["ok"]}
        
        res = self.ex._extraer_dependencia(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos)
        
        res_esperado = None
        
        self.assertEqual(res, res_esperado)
        
    def test__amod_4(self):
        """
        Prueba el método auxiliar _extraer_dependencia que se ejecuta cuando se encuentra una dependencia con la etiqueta "amod".
        Se espera None
        """
        indice_raiz = 4
        indice_nodo = 3
        lista_pos_lem = [('im', 'VB', None), ('the', 'DT', None), ('red', 'JJ', None),
                          ('cyclone', 'NN', None), ('.', '.', None)]
        arbol_de_dependencias = [('ROOT', 0, 1), ('det', 4, 2), ('amod', 4, 3),
                                 ('dobj', 1, 4), ('punct', 1, 5)]


        diccionario_de_aspectos = {"not":["ok"]}
        
        res = self.ex._extraer_dependencia(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos,
                                           arbol_de_dependencias=arbol_de_dependencias)
        
        res_esperado = None
        
        self.assertEqual(res, res_esperado)
        
    def test__amod_5(self):
        """
        Prueba el método auxiliar _extraer_dependencia que se ejecuta cuando se encuentra una dependencia con la etiqueta "amod".
        Se espera una tupla ("cyclone", "red")
        """
        indice_raiz = 4
        indice_nodo = 3
        lista_pos_lem = [('im', 'VB', None), ('the', 'DT', None), ('red', 'JJ', None),
                          ('cyclone', 'NN', None), ('.', '.', None)]
        arbol_de_dependencias = [('ROOT', 0, 1), ('det', 4, 2), ('amod', 4, 3),
                                 ('dobj', 1, 4), ('punct', 1, 5)]

        diccionario_de_aspectos = {"cyclone":["cyclone"]}
        
        res = self.ex._extraer_dependencia(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos)
        
        res_esperado = ("cyclone", "red")
        
        self.assertEqual(res, res_esperado)
        
    def test__advmod_1(self):
        """
        Prueba el método auxiliar _extraer_dependencia que se ejecuta cuando se encuentra una dependencia con la etiqueta "advmod".
        Se espera que regrese el adverbio del sustantivo en una tupla: ('sustantivo', 'dependencia').
        """
        # ultimately, it's a sheep
        indice_raiz = 6
        indice_nodo = 1
        lista_pos_lem = [('ultimately', 'RB', None), (',', ',', None), ('it', 'PRP', None),
                          ("'s", 'VBZ', None), ('a', 'DT', None), ('sheep', 'NN', None)]
        diccionario_de_aspectos = {"sheep": ["sheep"]}
        
        res = self.ex._extraer_dependencia(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos)
        
        res_esperado = ("sheep","ultimately")
        
        self.assertEqual(res_esperado, res)
        
    def test__advmod_2(self):
        """
        Prueba el método auxiliar _extraer_dependencia que se ejecuta cuando se encuentra una dependencia con la etiqueta "advmod".
        Se espera que regrese el adverbio del sustantivo en una tupla: ('sustantivo', 'dependencia').
        """
        # do you dream of perfectly electric sheep, lately?
        indice_raiz = 3
        indice_nodo = 9
        lista_pos_lem = [('do', 'VB', None), ('you', 'PRP', None), ('dream', 'NN', None),
                         ('of', 'IN', None), ('perfectly', 'RB', None), ('electric', 'JJ', None),
                         ('sheep', 'NN', None), (',', ',', None), ('lately', 'RB', None),
                         ('?', '.', None)]

        diccionario_de_aspectos = {"Dream": ["dream"]}
        
        res = self.ex._extraer_dependencia(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos)
        
        res_esperado = ("Dream","lately")
        
        self.assertEqual(res_esperado, res)
        
    def test__amod_advmod(self):
        """
        En algunas ocaciones, adjetivos de un sustantivo poseen su propio adverbio. Esta prueba espera que 
        al encontrar una dependencia amod que tiene su propio advmod, se devuelvan ambos en un solo string.
        Se espera ("sheep", "perfectly electric") 
        """
        # do you dream of perfectly electric sheep, lately?
        indice_raiz = 7
        indice_nodo = 6
        lista_pos_lem = [('do', 'VB', None), ('you', 'PRP', None), ('dream', 'NN', None),
                         ('of', 'IN', None), ('perfectly', 'RB', None), ('electric', 'JJ', None),
                         ('sheep', 'NN', None), (',', ',', None), ('lately', 'RB', None),
                         ('?', '.', None)]
        arbol_de_dependencias = [('ROOT', 0, 3), ('aux', 3, 1), ('nsubj', 3, 2), ('case', 7, 4),
                                 ('advmod', 6, 5), ('amod', 7, 6), ('nmod', 3, 7), ('punct', 3, 8),
                                 ('advmod', 3, 9), ('punct', 3, 10)]

        diccionario_de_aspectos = {"Sheep": ["sheep"]}
        
        res = self.ex._extraer_dependencia(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos,
                                           arbol_de_dependencias=arbol_de_dependencias)
        
        res_esperado = ("Sheep","perfectly electric")
        
        self.assertEqual(res_esperado, res)
        
    def test_extraer_dependencia_doble_1(self):
        """
        Prueba el método auxiliar que busca dependencias de dependencias. Debe encontrar el advmod
        del adjetivo 'electric'. Se espera que devuelva 'perfectly'.
        """
        indice_nodo = 6
        lista_pos_lem = [('do', 'VB', None), ('you', 'PRP', None), ('dream', 'NN', None),
                         ('of', 'IN', None), ('perfectly', 'RB', None), ('electric', 'JJ', None),
                         ('sheep', 'NN', None), (',', ',', None), ('lately', 'RB', None),
                         ('?', '.', None)]    
        arbol_de_dependencias = [('ROOT', 0, 3), ('aux', 3, 1), ('nsubj', 3, 2), ('case', 7, 4),
                                 ('advmod', 6, 5), ('amod', 7, 6), ('nmod', 3, 7), ('punct', 3, 8),
                                 ('advmod', 3, 9), ('punct', 3, 10)]
        
        res_esperado = "perfectly"
        
        res = self.ex._extraer_dependencia_doble(indice_nodo, lista_pos_lem, arbol_de_dependencias)
        
        self.assertEqual(res_esperado, res)
        
    def test__neg_1(self):
        """
        Prueba el método auxiliar que busca negaciones. Debe encontrar la negacion
        del sustantivos 'example'. Se espera que devuelva ('example','not').
        """
        lista_pos_lem = [('this', 'DT', None), ('is', 'VBZ', None), ('not', 'RB', None),
                         ('a', 'DT', None), ('good', 'JJ', None), ('example', 'NN', None),
                          ('.', '.', None)]
        arbol_de_dependencias = [('ROOT', 0, 6), ('nsubj', 6, 1), ('cop', 6, 2),
                                ('neg', 6, 3), ('det', 6, 4), ('amod', 6, 5), ('punct', 6, 7)]
        diccionario_de_aspectos = {"example": ["example"]}
        indice_raiz = 6
        indice_nodo = 3
        
        res_esperado = ("example", "not")
        
        res = self.ex._extraer_dependencia(indice_raiz=indice_raiz, indice_nodo=indice_nodo,
                                           lista_pos_lem=lista_pos_lem,
                                           diccionario_de_aspectos=diccionario_de_aspectos,
                                           arbol_de_dependencias=arbol_de_dependencias)
        
        self.assertEqual(res,res_esperado)
        
    def test__nsub_1(self):
        """
        Prueba el método auxiliar que busca sujetos nominales. Debe encontrar el adjetivo y adverbio
        del sustantivo 'cats'. Se espera que devuelva ('cats', "really cute").
        """
        lista_pos_lem = [('black', 'JJ', None), ('cats', 'NNS', None), ('are', 'VBP', None),
                         ('really', 'RB', None),
                         ('cute', 'JJ', None), ('.', '.', None)]
        arbol_de_dependencias = [('ROOT', 0, 5), ('amod', 2, 1), ('nsubj', 5, 2),
                                 ('cop', 5, 3), ('advmod', 5, 4), ('punct', 5, 6)]
        diccionario_de_aspectos = {"cats":["cats"]}
        indice_raiz = 5
        indice_nodo = 2
        
        res_esperado = ("cats", "really cute")
        
        res = self.ex._extraer_nsubj(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos, arbol_de_dependencias)
        self.assertEqual(res_esperado, res)
        
    def test__nsub_2(self):
        """
        Prueba el método auxiliar que busca sujetos nominales. Como el sujeto nominas no va de un adjetivo
        a un sustantivo, debe regresar None.
        """
        lista_pos_lem = [('this', 'DT', None), ('is', 'VBZ', None), ('not', 'RB', None),
                         ('a', 'DT', None), ('good', 'JJ', None), ('example', 'NN', None),
                          ('.', '.', None)]
        arbol_de_dependencias = [('ROOT', 0, 6), ('nsubj', 6, 1), ('cop', 6, 2),
                                ('neg', 6, 3), ('det', 6, 4), ('amod', 6, 5), ('punct', 6, 7)]
        diccionario_de_aspectos = {"example": ["example"]}
        indice_raiz = 6
        indice_nodo = 1
        
        res_esperado = None
        
        res = self.ex._extraer_nsubj(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos, arbol_de_dependencias)
        
        self.assertEqual(res_esperado, res)

    def test_extractor_1(self):
        """
        Dado el siguiente comentario: i am a valid comment.
        Debe devolver el adjetivo 'valid' del aspecto 'comment'
        """
        
        com = "i am a valid comment."
        diccionario = {"comment":["comment"]}
        arbol = self.cliente.resolver_dependencias(com)
        etiquetas_pos = self.cliente.etiquetar_texto(com)
        lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
        
        diccionario_esperado = {"comment":["valid"]}
        
        dic_resultado = self.ex.extraer(diccionario, arbol, lista_pos_lem)
        
        self.assertEqual(diccionario_esperado, dic_resultado)
        
    def test_extractor_2(self):
        """
        Dado el siguiente comentario: im the red cyclone.
        Debe devolver {"cyclone":["red"]}
        """
        
        com = "im the red cyclone."
        diccionario = {"cyclone":["cyclone"]}
        arbol = self.cliente.resolver_dependencias(com)
        etiquetas_pos = self.cliente.etiquetar_texto(com)
        lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
        
        diccionario_esperado = {"cyclone":["red"]}
        
        dic_resultado = self.ex.extraer(diccionario, arbol, lista_pos_lem)
        
        self.assertEqual(diccionario_esperado, dic_resultado)
        
    def test_extractor_3(self):
        """
        Dado el siguiente comentario: do you dream of perfectly electric sheep, lately?
        Debe devolver {"dream":["dream"],"sheep":["sheep"]}
        """
        
        com = "do you dream of perfectly electric sheep, lately?"
        diccionario = {"dream":["dream"],
                       "sheep":["sheep"]}
        arbol = self.cliente.resolver_dependencias(com)
        etiquetas_pos = self.cliente.etiquetar_texto(com)
        lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
        
        diccionario_esperado = {"dream":["lately"], "sheep":["perfectly electric"]}
        
        dic_resultado = self.ex.extraer(diccionario, arbol, lista_pos_lem)
        
        self.assertEqual(diccionario_esperado, dic_resultado)
        
    def test_extractor_4(self):
        """
        Dado el siguiente comentario: ultimately, it's a sheep
        Debe devolver {"sheep":["ultimately"]}
        """
        
        com = "ultimately, it's a sheep"
        diccionario = {"sheep":["sheep"]}
        arbol = self.cliente.resolver_dependencias(com)
        etiquetas_pos = self.cliente.etiquetar_texto(com)
        lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
        
        diccionario_esperado = {"sheep":["ultimately"]}
        
        dic_resultado = self.ex.extraer(diccionario, arbol, lista_pos_lem)
        
        self.assertEqual(diccionario_esperado, dic_resultado)
     
    def test_extractor_5(self):
        """
        Dado el siguiente comentario: black cats are really cute.
        Debe devolver {"cats":["black"," really cute"]}
        """
        
        com = "black cats are really cute."
        diccionario = {"cats":["cat", "cats"]}
        arbol = self.cliente.resolver_dependencias(com)
        etiquetas_pos = self.cliente.etiquetar_texto(com)
        lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
        
        diccionario_esperado = {"cats":["black","really cute"]}
        
        dic_resultado = self.ex.extraer(diccionario, arbol, lista_pos_lem)
        
        self.assertEqual(diccionario_esperado, dic_resultado)
        
    def test_extractor_6(self):
        """
        Dado el siguiente comentario: i really love black cats.
        Debe devolver {"cats":["black"}
        """
        
        com = "i really love black cats."
        diccionario = {"cats":["cat", "cats"]}
        arbol = self.cliente.resolver_dependencias(com)
        etiquetas_pos = self.cliente.etiquetar_texto(com)
        lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
        
        diccionario_esperado = {"cats":["black"]}
        
        dic_resultado = self.ex.extraer(diccionario, arbol, lista_pos_lem)
        
        self.assertEqual(diccionario_esperado, dic_resultado)
        
    def test_extractor_7(self):
        """
        Dado el siguiente comentario: this is not a good example.
        Debe devolver {"example":["not good"]}
        """
        
        com = "this is not a good example."
        diccionario = {"example":["example"]}
        arbol = self.cliente.resolver_dependencias(com)
        etiquetas_pos = self.cliente.etiquetar_texto(com)
        lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
        
        diccionario_esperado = {"example":["not", "good"]}
        
        dic_resultado = self.ex.extraer(diccionario, arbol, lista_pos_lem)
        
        self.assertEqual(diccionario_esperado, dic_resultado)
        
    def test_extractor_8(self):
        """
        Dado el siguiente comentario: They sent him the same, wrong item.
        Debe devolver {"item":["same","wrong"]}
        """
        
        com = "They sent him the same, wrong item."
        diccionario = {"item":["item", "items"]}
        arbol = self.cliente.resolver_dependencias(com)
        etiquetas_pos = self.cliente.etiquetar_texto(com)
        lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
        
        diccionario_esperado = {"item":["same","wrong"]}
        
        dic_resultado = self.ex.extraer(diccionario, arbol, lista_pos_lem)
        print(diccionario_esperado)
        self.assertEqual(diccionario_esperado, dic_resultado)
        
    def test_extractor_9(self):
        """
        Pruebas con comentarios reales
        """
        
        com = "Usually I have good experiences with Amazon and its customer service reps, but after todays online customer service chat I am horrified at some of the people Amazon employs. Enter employee Ruchitha. I was trying to get a print out label for my roommate since he doesn't have Prime and isn't really internet savvy. After he had bought a dvd that wasn't playable in the country, he called customer service and a rep said they were going to send him the correct one. They sent him the same, wrong item. So he had 2 returns to do."
        diccionario = {"experience":["experiences","experience"],"Amazon":["Amazon","amazon"],
                       "item":["item","items"]}
        sentencias = nltk.sent_tokenize(com)
        
        dic_resultado = dict()
        
        for sentencia in sentencias:
            arbol = self.cliente.resolver_dependencias(sentencia)
            etiquetas_pos = self.cliente.etiquetar_texto(sentencia)
            lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
            
            res = self.ex.extraer(diccionario, arbol, lista_pos_lem)
            dic_resultado = self._combinar_dict(res, dic_resultado)
        
        diccionario_esperado = {"experience":["good"],
                                "Amazon":[],
                                "item":["same","wrong"]
                                }
        
        self.assertEqual(diccionario_esperado, dic_resultado)
        
    def test_extractor_10(self):
        """
        Pruebas con comentarios reales
        """
        
        com = "There was a time I was a super-Amazon fan-boy, but those days are long past. If AMZ is good at one thing these days, it is finding new and innovated ways to anger their customers. I try to find the best deal with products all the time and use what discounts where I can. Apparently, AMZ does not like this and has taken to locking people out of their ability to comment on products if they feel you are not paying the top price. Today I had the simplest question about a feature on an item I bought on AMZ, but cannot ask the question as apparently, I am persona non grata these days. I got the product with a discount via research on the net."
        diccionario = {"fan-boy":["fan-boy"],"Amazon":["Amazon","amazon","AMZ"],
                       "question":["question"], "thing":["thing", "things"],
                       "way":["way","ways"], "deal":["deal","deals"],
                       "price":["prices", "price"],}
        sentencias = nltk.sent_tokenize(com)
        
        dic_resultado = dict()
        
        for sentencia in sentencias:
            arbol = self.cliente.resolver_dependencias(sentencia)
            etiquetas_pos = self.cliente.etiquetar_texto(sentencia)
            lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
            
            res = self.ex.extraer(diccionario, arbol, lista_pos_lem)
            dic_resultado = self._combinar_dict(res, dic_resultado)
        
        diccionario_esperado = {"fan-boy":["super-Amazon"],
                                "Amazon":["good"],
                                "question":["simple"],
                                "thing":["good"],
                                "way":["new"],
                                "deal":["best"],
                                "price":["top"]
                                }
        
        self.assertEqual(diccionario_esperado, dic_resultado)
        
    def test__conj_1(self):
        """
        Método aúxiliar para manejar las conjunciones de un sustantivo a un adverbio/adjetivo
        """
        lista_pos_lem = [('I', 'PRP', None), ('have', 'VBP', None), ('been', 'VBN', None),
                        ('a', 'DT', None), ('Prime', 'JJ', None), ('member', 'NN', None),
                        ('for', 'IN', None), ('years', 'NNS', None), ('and', 'CC', None),
                        ('always', 'RB', None), ('received', 'VBD', None), ('my', 'PRP$', None),
                        ('merchandise', 'NN', None), ('in', 'IN', None), ('the', 'DT', None),
                        ('desired', 'JJ', None), ('time', 'NN', None), ('frame', 'NN', None),
                        (',', ',', None), ('but', 'CC', None), ('no', 'DT', None),
                        ('more', 'JJR', None), ('!!', '.', None)]

        arbol_de_dependencias = [('ROOT', 0, 6), ('nsubj', 6, 1), ('aux', 6, 2),
                                ('cop', 6, 3), ('det', 6, 4), ('amod', 6, 5),
                                ('case', 8, 7), ('nmod', 6, 8), ('cc', 6, 9),
                                ('advmod', 11, 10), ('conj', 6, 11), ('nmod:poss', 13, 12),
                                ('dobj', 11, 13), ('case', 18, 14), ('det', 18, 15),
                                ('amod', 18, 16), ('compound', 18, 17), ('nmod', 11, 18),
                                ('punct', 6, 19), ('cc', 6, 20), ('neg', 22, 21),
                                ('conj', 6, 22), ('punct', 6, 23)]
        diccionario_de_aspectos = {"Member":["member"]}
        indice_raiz = 6
        indice_nodo = 22
        
        res_esperado = ("Member", "no more")
        
        res = self.ex._extraer_conj(indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos, arbol_de_dependencias)
        self.assertEqual(res_esperado, res)
     
    def test_extractor_11(self):
        """
        Pruebas con comentarios reales
        """
        
        com = "Prime 2 day shipping seems to be a thing of the past. I have been a Prime member for years and always received my merchandise in the desired time frame, but no more!! I have had numerous conversations with customer service and supervisors. All they do is give me the runaround and tell me their policy has not changed. \"Two day shipping starts when the item leaves the warehouse\". They can't ship if the items are not in their warehouses, seemly blaming the vendors. Shame on you Amazon for not telling the truth. To save money, Amazon no longer uses reliable trucking companies to move merchandise from vendors warehousing to Amazon warehouses. They can't ship what's not available. Nice way to save a buck. But keep taking our membership money for services you no longer can provide."
        diccionario = {"Member":["member","Member"],
                       "Shipping":["shipping","Shipping"],
                       }
        sentencias = nltk.sent_tokenize(com)
        
        dic_resultado = dict()
        
        for sentencia in sentencias:
            arbol = self.cliente.resolver_dependencias(sentencia)
            etiquetas_pos = self.cliente.etiquetar_texto(sentencia)
            lista_pos_lem = self.lemas.lematizar_tuplas(etiquetas_pos)
            
            res = self.ex.extraer(diccionario, arbol, lista_pos_lem)
            dic_resultado = self._combinar_dict(res, dic_resultado)
        
        diccionario_esperado = {"Member":["Prime", "no more"],
                                "Shipping":["day"],
                                }
        
        self.assertEqual(diccionario_esperado, dic_resultado)
    
    def test_quitar_palabras(self):
        """
        Prueba el metodo quitar_palabras. Se espera que elimine toda palabra que no tenga una etiqueta POS
        de adverbio, sustantivo o negacion.
        """
        texto = "do you dream of perfectly electric sheep, lately?"
        res = self.ex.quitar_palabras(texto)
        
        texto_esperado = "perfectly electric lately"
        
        self.assertEqual(res, texto_esperado)
        
    def test_quitar_palabras_2(self):
        """
        Prueba el metodo quitar_palabras. Se espera que elimine toda palabra que no tenga una etiqueta POS
        de adverbio, sustantivo o negacion.
        """
        texto = "don't say no to cookies, never again"
        res = self.ex.quitar_palabras(texto)
        
        texto_esperado = "n't no never again"
        
        self.assertEqual(res, texto_esperado)
        
    def test_quitar_palabras_3(self):
        """
        Prueba el metodo quitar_palabras. Se espera que elimine toda palabra que no tenga una etiqueta POS
        de adverbio, sustantivo o negacion.
        """
        texto = "black cats are really cute."
        res = self.ex.quitar_palabras(texto)
        
        texto_esperado = "black really cute"
        
        self.assertEqual(res, texto_esperado)
        
    def test__purgar_palabras_pos(self):
        """
        Método auxiliar que es el que recorre las lista de tuplas para eliminar las palabras innecesarias.
        """
        texto = "don't say no to cookies, never again"
        lista_pos_lem = self.lemas.lematizar_tuplas(self.cliente.etiquetar_texto(texto))
        res = self.ex._purgar_palabras_pos(lista_pos_lem)
        tupla_esperada = [("n't", 'RB', "n't"),('no', 'DT', None),
                          ('never', 'RB', "never"), ('again', 'RB', "again")]
        
        self.assertEqual(res, tupla_esperada)
        
    def test__unir_palabras(self):
        """
        Método auxiliar que une las palabras de la lista de tuplas.
        """        
        texto = "don't say no to cookies, never again"
        lista_pos_lem = self.lemas.lematizar_tuplas(self.cliente.etiquetar_texto(texto))
        tupla_purgada = self.ex._purgar_palabras_pos(lista_pos_lem)
        res = self.ex._unir_palabras(tupla_purgada)
        
        texto_esperado = "n't no never again"
        
        self.assertEqual(res, texto_esperado)
    
    def _combinar_dict(self, dict1, dict2):
        for llave in dict1:
            if llave in dict2.keys():
                dict2[llave].extend(dict1[llave])
            else:
                dict2[llave] = dict1[llave]
        return dict2
    
    def tearDown(self):
        self.cliente.cerrar_servicio()
        self.ex.cerrar()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()