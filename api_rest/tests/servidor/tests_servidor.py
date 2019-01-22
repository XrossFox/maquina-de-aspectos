import sys
import threading
import os
import requests
sys.path.append('../../api_rest')
import unittest
import subprocess

class Test(unittest.TestCase):


    def setUp(self):
        """
        El servidor se inicia en su propio hilo y se termina al final de los tests. revisar ejemplo 2 en:
        https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
        Se altero levemente para aumentar legibilidad en las lineas y hacer el código un poco mas evidente.
        """
        print(os.getcwd())
        self.proceso = subprocess.Popen(["python", "iniciar_servidor.py"], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        self.hilo = threading.Thread(target=self.lector_stdout)
        self.hilo.start()


    def tearDown(self):
        self.proceso.terminate()
        try:
            print('Se termino el proceso:', self.proceso.returncode)
        except subprocess.TimeoutExpired:
            print('El subproceso no se cerro a tiempo')
        self.hilo.join()

    def test_query_todo_code_200(self):
        """
        Este url debe devolver una lista con todas las tecnologias disponibles en la base de datos.
        """
        #se envia un request al url base
        req = requests.get('http://localhost:9999')
        
        self.assertEqual(req.status_code, 200)
        
    def test_query_todo_json(self):
        """
        Este url debe devolver una lista (json array) con todas las tecnologias disponibles en la base de datos.
        """
        #se envia un request al url base
        req = requests.get('http://localhost:9999')
        data = req.json()
        self.assertTrue("django" in data)
        self.assertTrue("haskell" in data)
        self.assertTrue("python" in data)
        
    def test_query_tecnologia_1(self):
        """
        Este URL debe devolver: nombre de tecnología, porcentaje de positivos vs negativos (de cada aspecto), total
        de aspectos evaluados (de cada aspecto).
        En forma de un objeto json (un dict python al parsearlo).
        """
        req = requests.get('http://localhost:9999/python')
        data = req.json()
        
        self.assertTrue("python" == data["nombre"])
        self.assertTrue(isinstance(data["total"], int))
        self.assertTrue(isinstance(data["total_pos"], int))
        self.assertTrue(isinstance(data["total_neg"], int))
        self.assertTrue(isinstance(data["p_pos"], float))
        self.assertTrue(isinstance(data["p_neg"], float))
        
    def test_query_tecnologia_2(self):
        """
        Este URL debe devolver: nombre de tecnología, porcentaje de positivos vs negativos (de cada aspecto), total
        de aspectos evaluados (de cada aspecto).
        En forma de un objeto json (un dict python al parsearlo).
        """
        req = requests.get('http://localhost:9999/python')
        data = req.json()
        data = data["avail_scal"]

        # totales
        self.assertTrue(isinstance(data["total"], int))
        self.assertTrue(isinstance(data["total_pos"], int))
        self.assertTrue(isinstance(data["total_neg"], int))
        self.assertTrue(isinstance(data["p_pos"], float), msg="{}: quizas wea?".format(data["p_pos"]))
        self.assertTrue(isinstance(data["p_neg"], float))
        
    def test_query_tecnologia_3(self):
        """
        Este URL debe devolver: nombre de tecnología, porcentaje de positivos vs negativos (de cada aspecto), total
        de aspectos evaluados (de cada aspecto).
        En forma de un objeto json (un dict python al parsearlo).
        """
        req = requests.get('http://localhost:9999/python')
        data = req.json()
        data = data["maintainability"]

        # totales
        self.assertTrue(isinstance(data["total"], int))
        self.assertTrue(isinstance(data["total_pos"], int))
        self.assertTrue(isinstance(data["total_neg"], int))
        self.assertTrue(isinstance(data["p_pos"], float), msg="{}: quizas wea?".format(data["p_pos"]))
        self.assertTrue(isinstance(data["p_neg"], float))
        
    def test_query_tecnologia_4(self):
        """
        Este URL debe devolver: nombre de tecnología, porcentaje de positivos vs negativos (de cada aspecto), total
        de aspectos evaluados (de cada aspecto).
        En forma de un objeto json (un dict python al parsearlo).
        """
        req = requests.get('http://localhost:9999/python')
        data = req.json()
        data = data["performance"]

        # totales
        self.assertTrue(isinstance(data["total"], int))
        self.assertTrue(isinstance(data["total_pos"], int))
        self.assertTrue(isinstance(data["total_neg"], int))
        self.assertTrue(isinstance(data["p_pos"], float), msg="{}: quizas wea?".format(data["p_pos"]))
        self.assertTrue(isinstance(data["p_neg"], float))
        
    def test_query_tecnologia_5(self):
        """
        Este URL debe devolver: nombre de tecnología, porcentaje de positivos vs negativos (de cada aspecto), total
        de aspectos evaluados (de cada aspecto).
        En forma de un objeto json (un dict python al parsearlo).
        """
        req = requests.get('http://localhost:9999/python')
        data = req.json()
        data = data["reliability"]

        # totales
        self.assertTrue(isinstance(data["total"], int))
        self.assertTrue(isinstance(data["total_pos"], int))
        self.assertTrue(isinstance(data["total_neg"], int))
        self.assertTrue(isinstance(data["p_pos"], float), msg="{}: quizas wea?".format(data["p_pos"]))
        self.assertTrue(isinstance(data["p_neg"], float))
        
    def test_query_tecnologia_6(self):
        """
        Este URL debe devolver: nombre de tecnología, porcentaje de positivos vs negativos (de cada aspecto), total
        de aspectos evaluados (de cada aspecto).
        En forma de un objeto json (un dict python al parsearlo).
        """
        req = requests.get('http://localhost:9999/python')
        data = req.json()
        data = data["deployability"]

        # totales
        self.assertTrue(isinstance(data["total"], int))
        self.assertTrue(isinstance(data["total_pos"], int))
        self.assertTrue(isinstance(data["total_neg"], int))
        self.assertTrue(isinstance(data["p_pos"], float), msg="{}: quizas wea?".format(data["p_pos"]))
        self.assertTrue(isinstance(data["p_neg"], float))
        
    def test_query_tecnologia_7(self):
        """
        Este URL debe devolver: nombre de tecnología, porcentaje de positivos vs negativos (de cada aspecto), total
        de aspectos evaluados (de cada aspecto).
        En forma de un objeto json (un dict python al parsearlo).
        """
        req = requests.get('http://localhost:9999/python')
        data = req.json()
        data = data["securability"]

        # totales
        self.assertTrue(isinstance(data["total"], int))
        self.assertTrue(isinstance(data["total_pos"], int))
        self.assertTrue(isinstance(data["total_neg"], int))
        self.assertTrue(isinstance(data["p_pos"], float), msg="{}: quizas wea?".format(data["p_pos"]))
        self.assertTrue(isinstance(data["p_neg"], float))
        
    def test_query_tecnologia_8(self):
        """
        Este URL debe devolver: nombre de tecnología, porcentaje de positivos vs negativos (de cada aspecto), total
        de aspectos evaluados (de cada aspecto).
        En forma de un objeto json (un dict python al parsearlo).
        """
        req = requests.get('http://localhost:9999/python')
        data = req.json()
        data = data["interoperability"]

        # totales
        self.assertTrue(isinstance(data["total"], int))
        self.assertTrue(isinstance(data["total_pos"], int))
        self.assertTrue(isinstance(data["total_neg"], int))
        self.assertTrue(isinstance(data["p_pos"], float), msg="{}: quizas wea?".format(data["p_pos"]))
        self.assertTrue(isinstance(data["p_neg"], float))
        
    def test_query_tecnologia_9(self):
        """
        cuando hay una tecnología que no esta en la base de datos
        """
        req = requests.get('http://localhost:9999/nothing')
        self.assertEqual(req.status_code, 404)
        
    def lector_stdout(self):
        """
        Imprime la salida estandar del servidor en tiempo real como va apareciendo.
        """
        for linea in iter(self.proceso.stdout.readline, b''):
            print('>>>>>: {0}'.format(linea.decode('utf-8')), end='')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()