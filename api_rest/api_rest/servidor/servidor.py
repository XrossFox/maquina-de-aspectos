import bottle
from servidor import back_end
import json

class Servidor(object):
    '''
    Clase (interfaz) del servidor REST.
    '''
    
    def wrap_query_todo(self):
        """
        Wrapper para el método be.query_todo. Convierte la respuesta en un objeto json. 
        """
        lista = self.be.query_todo()
        bottle.response.status = 200
        return json.dumps(lista)
    
    def wrap_query_tecnologia(self, tecnologia):
        """
        Wrapper para el método be.query_tecnologia. Convierte la respuesta en un objeto json.
        """
        diccionario = self.be.query_tecnologia(tecnologia)
        if diccionario:
            bottle.response.status = 200
            return json.dumps(diccionario)
        else:
            bottle.response.status = 404
    
    def iniciar_servidor(self, dir_bases_datos):
        self.be = back_end.BackEnd(dir_bases_datos)
        bottle.route("/")(self.wrap_query_todo)
        bottle.route("/<tecnologia>")(self.wrap_query_tecnologia)
        bottle.run(host='localhost', port=9999, debug=False)
        