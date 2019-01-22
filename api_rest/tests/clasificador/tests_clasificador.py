import sys
sys.path.append('../../api_rest')
from clasificador import clasificador
import bd_aspectos
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        self.clasificador = clasificador.Clasificador()


    def tearDown(self):
        self.clasificador._terminar()


    def test__cargar_modelo_entrenado(self):
        """
        El primer paso es cargar el modelo entrenado serializado. En este caso se espera que este en la
        carpeta test_modelos_entrenados dentro de esta misma carpeta.
        """
        self.clasificador._cargar_modelo_entrenado("./test_modelos_entrenados")
        
    def test__cargar_modelo_entrenado_excep(self):
        """
        Cuando la carpeta no contiene archivos con la extension .clasif salta una excepcion ValueError
        """
        with self.assertRaises(ValueError):
            self.clasificador._cargar_modelo_entrenado("./test_modelos_entrenados_2")
            
    def test__cargar_comentarios(self):
        """
        Se leen todos los comentarios en una capeta especificada. Los comentarios deben estar en formato json array
        y deben tener extension .json. Los comentarios deben estar categorizados por carpeta para cada tecnología.
        Solo los comentarios en su carpeta son usados y el nombre de la carpeta es usado para identificar la tecnología
        a la que pertenecen. Debe regresar un diccionario con una lista de comentarios. la llave es la tecnologia, el valor
        es una lista con los comentarios encontrados.
        """
        direccion = "./test_comentarios"
        res = self.clasificador._cargar_comentarios(direccion)
        
        # se esperan 3 llaves por que hay 3 carpetas
        self.assertTrue(res["test_1"])
        self.assertTrue(res["test_2"])
        self.assertTrue(res["test_3"])
        
        # cada carpeta tiene 2000 comentarios cada una en dos archivos .json
        self.assertEqual(len(res["test_1"]), 2000)
        self.assertEqual(len(res["test_2"]), 2000)
        self.assertEqual(len(res["test_3"]), 2000)
        
    def test__cargar_comentarios_exc_1(self):
        """
        Si hay una carpeta vacia, se debe recibir una lista vacia.
        """
        direccion = "./test_comentarios_2"
        res = self.clasificador._cargar_comentarios(direccion)
        
        # se esperan 3 llaves por que hay 3 carpetas
        self.assertTrue(res["test_1"])
        self.assertTrue(res["test_2"])
        self.assertTrue(res["test_3"])
        self.assertFalse(res["test_4"])
        
        # cada carpeta tiene 2000 comentarios cada una en dos archivos .json
        self.assertEqual(len(res["test_1"]), 2000)
        self.assertEqual(len(res["test_2"]), 2000)
        self.assertEqual(len(res["test_3"]), 2000)
        self.assertEqual(len(res["test_4"]), 0)
        
    def test__cargar_comentarios_exc_2(self):
        """
        Debe levantar una excepcions si el archivo .json no es un json array.
        """
        with self.assertRaises(ValueError):
            self.clasificador._cargar_comentarios("./test_comentarios_3")
            
    def test__cargar_comentarios_exc_3(self):
        """
        Debe ingorar otros archivos que no sean json
        """
        direccion = "./test_comentarios_4"
        res = self.clasificador._cargar_comentarios(direccion)
        
        # se esperan 3 llaves por que hay 3 carpetas
        self.assertTrue(res["test_1"])
        self.assertTrue(res["test_2"])
        self.assertTrue(res["test_3"])
        
        # cada carpeta tiene 2000 comentarios cada una en dos archivos .json
        self.assertEqual(len(res["test_1"]), 2000)
        self.assertEqual(len(res["test_2"]), 2000)
        self.assertEqual(len(res["test_3"]), 2000)
        
    def test__extraer_aspectos(self):
        """
        Una vez los comentarios han sido leidos, se debe usar el modulo extractor_de_aspectos para dejar solo los
        adjetivos, adverbio y negciones.
        """
        esperado = {"java":[
                                {"AvailabilityAndScalability":["no"],
                                 "Maintainability":[],
                                 "Performance":["bad"],
                                 "Reliability":[],
                                 "Deployability":[],
                                 "Securability":[],
                                 "Interoperability":[]
                                 },
                                {"AvailabilityAndScalability":[],
                                 "Maintainability":[],
                                 "Performance":[],
                                 "Reliability":[],
                                 "Deployability":["hard"],
                                 "Securability":[],
                                 "Interoperability":[]
                                 },
                                {"AvailabilityAndScalability":[],
                                 "Maintainability":[],
                                 "Performance":["really nice"],
                                 "Reliability":[],
                                 "Deployability":[],
                                 "Securability":[],
                                 "Interoperability":[]
                                 },
                                {"AvailabilityAndScalability":[],
                                 "Maintainability":[],
                                 "Performance":[],
                                 "Reliability":["no"],
                                 "Deployability":[],
                                 "Securability":[],
                                 "Interoperability":[]
                                 },
                                {"AvailabilityAndScalability":[],
                                 "Maintainability":[],
                                 "Performance":[],
                                 "Reliability":[],
                                 "Deployability":[],
                                 "Securability":["bad"],
                                 "Interoperability":[]
                                 },
                                {"AvailabilityAndScalability":[],
                                 "Maintainability":[],
                                 "Performance":[],
                                 "Reliability":[],
                                 "Deployability":[],
                                 "Securability":[],
                                 "Interoperability":["not", "good"]
                                 },
                                {"AvailabilityAndScalability":[],
                                 "Maintainability":["very high"],
                                 "Performance":[],
                                 "Reliability":[],
                                 "Deployability":[],
                                 "Securability":[],
                                 "Interoperability":[]
                                 },
                            ]
                    }
        comentarios = self.clasificador._cargar_comentarios("./test_extractor_comentarios")
        res = self.clasificador._extraer_aspectos(comentarios)
        self.assertEqual(res, esperado)
        
    def test__clasificar_aspectos(self):
        """
        Los aspectos extraidos se deben pasar por el clasificador Naive Bayes para encontrar su polaridad.
        """
        esperado = {"java":[
                                {"AvailabilityAndScalability":0,
                                 "Maintainability":None,
                                 "Performance":0,
                                 "Reliability":None,
                                 "Deployability":None,
                                 "Securability":None,
                                 "Interoperability":None
                                 },
                                {"AvailabilityAndScalability":None,
                                 "Maintainability":None,
                                 "Performance":None,
                                 "Reliability":None,
                                 "Deployability":1,
                                 "Securability":None,
                                 "Interoperability":None
                                 },
                                {"AvailabilityAndScalability":None,
                                 "Maintainability":None,
                                 "Performance":1,
                                 "Reliability":None,
                                 "Deployability":None,
                                 "Securability":None,
                                 "Interoperability":None
                                 },
                                {"AvailabilityAndScalability":None,
                                 "Maintainability":None,
                                 "Performance":None,
                                 "Reliability":0,
                                 "Deployability":None,
                                 "Securability":None,
                                 "Interoperability":None
                                 },
                                {"AvailabilityAndScalability":None,
                                 "Maintainability":None,
                                 "Performance":None,
                                 "Reliability":None,
                                 "Deployability":None,
                                 "Securability":0,
                                 "Interoperability":None
                                 },
                                {"AvailabilityAndScalability":None,
                                 "Maintainability":None,
                                 "Performance":None,
                                 "Reliability":None,
                                 "Deployability":None,
                                 "Securability":None,
                                 "Interoperability":0
                                 },
                                {"AvailabilityAndScalability":None,
                                 "Maintainability":1,
                                 "Performance":None,
                                 "Reliability":None,
                                 "Deployability":None,
                                 "Securability":None,
                                 "Interoperability":None
                                 },
                            ]
                    }
        self.maxDiff = None
        modelo = self.clasificador._cargar_modelo_entrenado("./test_modelos_entrenados_3")
        comentarios = self.clasificador._cargar_comentarios("./test_extractor_comentarios")
        dict_aspectos = self.clasificador._extraer_aspectos(comentarios)
        dict_polaridades = self.clasificador._clasificar_aspectos(dict_aspectos, modelo)
        self.assertEqual(dict_polaridades, esperado)
        
    def test__aspectos_a_bd(self):
        """
        Cuando los aspectos son clasificados, estos se introducen en la base de datos SQlite
        """
        modelo = self.clasificador._cargar_modelo_entrenado("./test_modelos_entrenados_3")
        comentarios = self.clasificador._cargar_comentarios("./test_extractor_comentarios")
        dict_aspectos = self.clasificador._extraer_aspectos(comentarios)
        dict_polaridades = self.clasificador._clasificar_aspectos(dict_aspectos, modelo)
        base_datos = bd_aspectos.BDAspectos()
        base_datos.insertar_a_tabla(dict_polaridades)
        
    def test_iniciar_clasificacion(self):
        """
        Método que maneja el flujo del proceso.
        """
        self.clasificador.iniciar_clasificacion(dir_modelos_entrenados="./test_modelos_entrenados_3",
                                                dir_comentarios="./test_iniciar")

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()