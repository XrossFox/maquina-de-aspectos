import os
import sys
sys.path.append('../')

import preprocesador
import unittest
import json
from pathlib import Path
from conf_pp import Configuracion

class TestEngine(unittest.TestCase):
    
    def setUp(self):
        conf = Configuracion()
        self.pre = preprocesador.Preprocesador(conf.dir_corenlp, conf.stopwords)
    
    def test_engine_leer_json(self):
        
        
        """Prueba si el modulo leer_json lee un archivo json y l oconvierte a lista"""
        test_list = ["Test String 2", "Test String 2", "123 Test String 3"]
        direccion = os.getcwd()+"/test2.json"
        
        
        
        lista = self.pre.leer_json(direccion)
        
        for i in range(len(test_list)):
            self.assertEqual(lista[i], test_list[i])
            
    def test_engine_escribir_a_json_1(self):
        """Prueba si el modulo escribir_lista_a_json escribe una lista a un archivo .json >.>"""
        
        test_list = ["Test String 3", "Test String 3", "123 Test String 3"]
        self.pre.escribir_a_json(test_list,direccion="./",nombre="test3.json")
        ar = Path("./test3.json")
        self.assertTrue(ar.is_file())
        lec = self.pre.leer_json("./test3.json")
        for i in range(len(test_list)):
            self.assertEqual(test_list[i], lec[i])
            
    def test_main_stem(self):
        """Probar que modulo engine.main integra los modulos y usa la opcion de stemming."""
        
        salida = [
            "blue shirt awesom realli like blue shirt blue shirt also expens",
            "cat small cat fit hand",
            "radioact danger radioact kill radioact make grow third arm stay away radioact",
            "hand cold hand trembl",
            "thing weird ugli thing make eye sore go burn thing furnac",
            "tall also exercis daili",
            "favorit food hamburg favorit color green",
            "like rose like rose",
            "obviou no way miss",
            "car red car color live",
            "paragraph",
            "titl",
            "badli close tag"
        ]
        
        self.pre.main("test4_in.json", "", stem=True, coref=True, punct=True, num=True,
                     html=True, urls=True, stp_wrds=True)
        to_test = self.pre.leer_json("./coref_stem_test4_in.json")
        
        for i in range(len(to_test)):
            self.assertEqual(to_test[i], salida[i])
            
    def test_main_lem(self):
        """Probar que modulo engine.main integra los modulos y usa la opcion de lemmatizacion."""
        
        salida = [
            "blue shirt awesome really like blue shirt blue shirt also expensive",
            "cat small cat fit hand",
            "radioactivity dangerous radioactivity kill radioactivity make grow third arm stay away radioactivity",
            "hand cold hand trembling",
            "thing weird ugly thing make eye sore going burn thing furnace",
            "tall also exercise daily",
            "favorite food hamburger favorite color green",
            "like rose like rose",
            "obvious no way miss",
            "car red car color lively",
            "paragraph",
            "title",
            "badly closed tag"
        ]
        
        self.pre.main("test4_in.json", "", lemmatize=True, coref=True, punct=True, num=True,
                     html=True, urls=True, stp_wrds=True)
        to_test = self.pre.leer_json("./coref_lem_test4_in.json")
        
        for i in range(len(to_test)):
            self.assertEqual(to_test[i], salida[i])
            
    def test_main_no(self):
        """Probar que modulo engine.main integra los modulos sin usar ninguna opcion de raices."""
        
        salida = [
            "blue shirt awesome really like blue shirt blue shirts also expensive",
            "cat small cat fits hand",
            "radioactivity dangerous radioactivity kill radioactivity make grow third arm stay away radioactivity",
            "hands cold hands trembling",
            "thing weird ugly thing makes eyes sore going burn thing furnace",
            "tall also exercise daily",
            "favorite food hamburgers favorite color green",
            "like roses like roses",
            "obvious no way miss",
            "car red cars color lively",
            "paragraph",
            "title",
            "badly closed tag"
        ]
        
        self.pre.main("test4_in.json", "", coref=True, punct=True, num=True,
                     html=True, urls=True, stp_wrds=True)
        to_test = self.pre.leer_json("./coref_no_test4_in.json")
        
        for i in range(len(to_test)):
            self.assertEqual(to_test[i], salida[i])
            
    def test_no_correferencias_no_raiz(self):
        
        salida = [
            "blue shirt awesome really like also expensive",
            "cat small fits hand",
            "radioactivity dangerous kill make grow third arm stay away",
            "hands cold trembling",
            "thing weird ugly makes eyes sore going burn furnace",
            "tall also exercise daily",
            "favorite food hamburgers favorite color green",
            "like roses like",
            "obvious no way miss",
            "car red color lively",
            "paragraph",
            "title",
            "badly closed tag"
        ]        
        
        self.pre.main("test4_in.json", "", coref=False, punct=True, num=True,
                     html=True, urls=True, stp_wrds=True)
        to_test = self.pre.leer_json("./no_coref_no_test4_in.json")
        
        for i in range(len(to_test)):
            self.assertEqual(to_test[i], salida[i]) 
            
    def tearDown(self):
        self.pre._cerrar()
        
            
if __name__ == "__main__":
    unittest.main()
        