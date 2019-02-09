import unittest
import sys
sys.path.append('../../api_rest')
from servidor import back_end


class Test(unittest.TestCase):

    def tearDown(self):
        pass


    def test__cargar_db(self):
        """
        Se tiene una carpeta con las bases de datos, pero se debe cargar la ultima base de datos creada.
        """
        lobe = back_end.BackEnd("./db_tests_1")
        self.assertTrue(lobe._cargar_db("./db_tests_1"))
        
    def test__cargar_db_2(self):
        """
        Si la extension no es .db, debe levantar una excepcion.
        """
        with self.assertRaises(ValueError):
            back_end.BackEnd("./db_tests_2")
            
    def tests_query_todo(self):
        """
        Debe devolver el nombre de todas las tecnologías disponibles en la base de datos.
        """
        # local back end
        lobe = back_end.BackEnd("./db_tests_3")
        # resultado del query
        lista = lobe.query_todo()
        self.assertTrue("django" in lista)
        self.assertTrue("haskell" in lista)
        self.assertTrue("python" in lista)
        
    def tests_query_tecnologia_python_1(self):
        """
        Hace un query a la base de datos y debe devolver: nombre de tecnología, porcentaje de positivos vs negativos vs neutro, total de aspectos evaluados.
        En forma de un objeto json (un dict python al parsearlo).
        """
        lobe = back_end.BackEnd("./db_tests_3")
        diccionario = lobe.query_tecnologia("python")

        # totales
        self.assertTrue("python" == diccionario["nombre"])
        self.assertTrue(isinstance(diccionario["total"], int))
        self.assertTrue(isinstance(diccionario["total_pos"], int))
        self.assertTrue(isinstance(diccionario["total_neu"], int))
        self.assertTrue(isinstance(diccionario["total_neg"], int))
        self.assertTrue(isinstance(diccionario["p_pos"], float))
        self.assertTrue(isinstance(diccionario["p_neg"], float))
        
    def tests_query_tecnologia_python_2(self):
        """
        avail_scal
        """
        lobe = back_end.BackEnd("./db_tests_3")
        diccionario = lobe.query_tecnologia("python")
        diccionario = diccionario["avail_scal"]

        # totales
        self.assertTrue(isinstance(diccionario["total"], int))
        self.assertTrue(isinstance(diccionario["total_pos"], int))
        self.assertTrue(isinstance(diccionario["total_neg"], int))
        self.assertTrue(isinstance(diccionario["p_pos"], float), msg="{}: quizas wea?".format(diccionario["p_pos"]))
        self.assertTrue(isinstance(diccionario["p_neg"], float))
        
    def tests_query_tecnologia_python_3(self):
        """
        avail_scal
        """
        lobe = back_end.BackEnd("./db_tests_3")
        diccionario = lobe.query_tecnologia("python")
        diccionario = diccionario["maintainability"]

        # totales
        self.assertTrue(isinstance(diccionario["total"], int))
        self.assertTrue(isinstance(diccionario["total_pos"], int))
        self.assertTrue(isinstance(diccionario["total_neg"], int))
        self.assertTrue(isinstance(diccionario["p_pos"], float))
        self.assertTrue(isinstance(diccionario["p_neg"], float))
        
    def tests_query_tecnologia_python_4(self):
        """
        avail_scal
        """
        lobe = back_end.BackEnd("./db_tests_3")
        diccionario = lobe.query_tecnologia("python")
        diccionario = diccionario["performance"]

        # totales
        self.assertTrue(isinstance(diccionario["total"], int))
        self.assertTrue(isinstance(diccionario["total_pos"], int))
        self.assertTrue(isinstance(diccionario["total_neg"], int))
        self.assertTrue(isinstance(diccionario["p_pos"], float))
        self.assertTrue(isinstance(diccionario["p_neg"], float))
        
    def tests_query_tecnologia_python_5(self):
        """
        avail_scal
        """
        lobe = back_end.BackEnd("./db_tests_3")
        diccionario = lobe.query_tecnologia("python")
        diccionario = diccionario["reliability"]

        # totales
        self.assertTrue(isinstance(diccionario["total"], int))
        self.assertTrue(isinstance(diccionario["total_pos"], int))
        self.assertTrue(isinstance(diccionario["total_neg"], int))
        self.assertTrue(isinstance(diccionario["p_pos"], float))
        self.assertTrue(isinstance(diccionario["p_neg"], float))
        
    def tests_query_tecnologia_python_6(self):
        """
        avail_scal
        """
        lobe = back_end.BackEnd("./db_tests_3")
        diccionario = lobe.query_tecnologia("python")
        diccionario = diccionario["deployability"]

        # totales
        self.assertTrue(isinstance(diccionario["total"], int))
        self.assertTrue(isinstance(diccionario["total_pos"], int))
        self.assertTrue(isinstance(diccionario["total_neg"], int))
        self.assertTrue(isinstance(diccionario["p_pos"], float))
        self.assertTrue(isinstance(diccionario["p_neg"], float))
        
    def tests_query_tecnologia_python_7(self):
        """
        avail_scal
        """
        lobe = back_end.BackEnd("./db_tests_3")
        diccionario = lobe.query_tecnologia("python")
        diccionario = diccionario["securability"]

        # totales
        self.assertTrue(isinstance(diccionario["total"], int))
        self.assertTrue(isinstance(diccionario["total_pos"], int))
        self.assertTrue(isinstance(diccionario["total_neg"], int))
        self.assertTrue(isinstance(diccionario["p_pos"], float))
        self.assertTrue(isinstance(diccionario["p_neg"], float))
        
    def tests_query_tecnologia_python_8(self):
        """
        avail_scal
        """
        lobe = back_end.BackEnd("./db_tests_3")
        diccionario = lobe.query_tecnologia("python")
        diccionario = diccionario["interoperability"]

        # totales
        self.assertTrue(isinstance(diccionario["total"], int))
        self.assertTrue(isinstance(diccionario["total_pos"], int))
        self.assertTrue(isinstance(diccionario["total_neg"], int))
        self.assertTrue(isinstance(diccionario["p_pos"], float))
        self.assertTrue(isinstance(diccionario["p_neg"], float))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()