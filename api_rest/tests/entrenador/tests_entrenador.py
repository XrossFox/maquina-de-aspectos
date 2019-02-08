import sys
sys.path.append('../../api_rest')
import unittest
from entrenador import entrenador
import os.path
import configuracion_api_rest

class Test(unittest.TestCase):


    def setUp(self):
        self.entrenador = entrenador.Entrenador()
        self.test_data_path_correcto = "./datasets_tests_1"
        self.test_data_path_con_txt = "./datasets_tests_2"
        self.test_data_path_con_errores = "./datasets_tests_3"
        self.test_data_path_con_errores_0 = "./datasets_tests_4"
        self.test_data_path_con_errores_1 = "./datasets_tests_5"
        self.test_data_path_con_errores_int = "./datasets_tests_6"
        self.test_data_path_con_errores_index = "./datasets_tests_7"
        self.test_data_path_comentarios = "./datasets_tests_8"


    def tearDown(self):
        self.entrenador.cerrar()


    def test__lector_len(self):
        """
        El mÃ©todo lector debe leer todos los archivos con extension .json en la carpeta indicada.
        Los datasets son una lista tienen la siguiente sinaxis:
            
            [[sentimiento,"comentario"],[sentimiento2, "comentario2"]]
            
        En donde sentimiento es 1 si su polaridad es positiva, o 0 si su polaridad es negativa.
        
        Se prueba que lea todos los archivos con extension .json en una carpeta
        """
        res = self.entrenador._lector(self.test_data_path_correcto)
        self.assertEqual(len(res), 6)
        
    def test__lector_len_2(self):
        """       
        Se prueba que lea todos los archivos con extension .json en una carpeta en donde hay un archvio txt
        """
        res = self.entrenador._lector(self.test_data_path_con_txt)
        self.assertEqual(len(res), 6)
    
    def test__lector_syn(self):
        """
        El mÃ©todo lector debe leer todos los archivos con extension .json en la carpeta indicada.
        Los datasets es una lista tienen la siguiente sinaxis:
            
            [[sentimiento,"comentario"],[sentimiento2, "comentario2"]]
            
        En donde sentimiento es 1 si su polaridad es positiva, o 0 si su polaridad es negativa.
        
        Se prueba que sea una lista de listas con esta syntaxis
        """
        
        res = self.entrenador._lector(self.test_data_path_correcto)
        self.assertTrue(isinstance(res, list))
            
        for comentario in res:
            self.assertTrue((comentario[0] == 0 or comentario[0] == 1) and isinstance(comentario[1], str))
            
    def test__lector_syn_ex(self):
        """
        Prueba que solo existan haya listas en la lista.
        """
        with self.assertRaises(TypeError):
            self.entrenador._lector(self.test_data_path_con_errores)
            
    def test__lector_syn_ex_1(self):
        """
        Prueba que el indice 0 sea un int.
        """
        with self.assertRaises(TypeError):
            self.entrenador._lector(self.test_data_path_con_errores_0)
            
    def test__lector_syn_ex_2(self):
        """
        Prueba que el indice 0 sea un int entre 0 y 1.
        """
        with self.assertRaises(ValueError):
            self.entrenador._lector(self.test_data_path_con_errores_int)
            
    def test__lector_syn_ex_3(self):
        """
        Prueba que el indice 1 sea un str.
        """
        with self.assertRaises(TypeError):
            self.entrenador._lector(self.test_data_path_con_errores_1)
            
    def test__lector_syn_ex_4(self):
        """
        Prueba que las listas solo tengan 2 indices
        """
        with self.assertRaises(IndexError):
            self.entrenador._lector(self.test_data_path_con_errores_index)
            
    def test__limpiar_palabras(self):
        """
        El segundo paso es deja solo los adverbios, adjetivos y negaciones de los comentarios leidos
        """
        self.maxDiff = None
        l_esperado = [
                        [1, 'very simple effective new'],
                        [1, 'easy even first highly'],
                        [1, 'brilliant brilliant challenging great only good together other fantastic'],
                        [1, 'good several new out'],
                        [0, 'too often too often no other'], 
                        [0, "n't n't even new always even really correct many still n't"], 
                        [0, 'well now indirect even mid san'], 
                        [0, 'good']
                    ]
        
        res = self.entrenador._limpiar_palabras(self.entrenador._lector(self.test_data_path_comentarios))
        self.assertEqual(res, l_esperado)
        
    def test__crear_dataframe(self):
        """
        Antes de vectorizar se necesita convertir la lista a dataframe
        """
        res = self.entrenador._limpiar_palabras(self.entrenador._lector(self.test_data_path_comentarios))
        self.entrenador._crear_dataframe(res)
        
    def test__vectorizacion(self):
        """
        La vectorizacion representa los comentarios de texto con los que se entrena el modelo.
        """
        res = self.entrenador._limpiar_palabras(self.entrenador._lector(self.test_data_path_comentarios))
        df_palabras = self.entrenador._crear_dataframe(res)
        self.entrenador._vectorizacion(df_palabras)
        
        
    def test__entrenar_modelo(self):
        """
        Se entrena el clasificador Naive Bayes Multinomial a partir de los vectores.
        """
        res = self.entrenador._limpiar_palabras(self.entrenador._lector(self.test_data_path_comentarios))
        df_palabras = self.entrenador._crear_dataframe(res)
        vectores = self.entrenador._vectorizacion(df_palabras)
        self.entrenador._entrenar_modelo(vectores, df_palabras)
        
    def test__escribir_modelo(self):
        """
        Se guarda el objeto modelo_entrenado serializado al disco duro
        """
        res = self.entrenador._limpiar_palabras(self.entrenador._lector(self.test_data_path_comentarios))
        df_palabras = self.entrenador._crear_dataframe(res)
        vectores = self.entrenador._vectorizacion(df_palabras)
        modelo = self.entrenador._entrenar_modelo(vectores, df_palabras)
        dir_completo = self.entrenador._escribir_modelo("./test__escribir_modelo", modelo)
        self.assertTrue(os.path.isfile(dir_completo))
        
    def test_inicio(self):
        """
        MÃ©todo de control que maneja el flujo del proceso
        """
        conf = configuracion_api_rest.Configuracion()
        directorio = self.entrenador.inicio(dir_datasets_entrenamiento="./test_iniciar",
                                            dir_modelos_entrenados=conf.dir_modelos_entrenados)
        self.assertTrue(os.path.isfile(directorio))

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
