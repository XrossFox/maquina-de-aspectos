from os import listdir
from os.path import join
import bd_aspectos

class BackEnd():
    """
    Clase que representa las rutas y los metodos del Servidor
    """
    
    def __init__(self, dir_bases_datos):
        """
        @param dir_bases_datos: dirección del directorio de bases de datos
        """
        
        base_datos = self._cargar_db(dir_bases_datos)
        self.bda = bd_aspectos.BDAspectos(base_datos)
        
    def _cargar_db(self, direccion):
        """
        Lee todos los archivos en el directorio recibido con extension .db. Si no encuentra archivos, levanta una
        excepcion. Carga la base de datos mas reciente en el directorio.
        @param direccion: direccion hacia el directorio con los archivos .db.
        @return: La direccion al archivo '.db' en disco. | None si no se encontr DB
        """
        archivos = list(listdir(direccion))
        ult_db = None
        for n in range(len(archivos)):
            # se recorre desde atras la lista de archivos
            nombre = archivos[(n+1)*-1]
            # si el ultimo elemento tiene la extension, se usa ese. Si no continua.
            if nombre.endswith(".db"):
                ult_db = join(direccion, nombre)
                break
            n += 1
        if ult_db:
            return ult_db
        else:
            raise ValueError("No se encontro ningún archivo con extensions '.db'")
    
     
    def query_todo(self):
        """
        Devuelve el query de tecnologías disponibles en la db recibida.
        @return: una lista de las tecnologías disponibles.
        """
            
        lista_tec = self.bda.query_tecnologias_disponibles()
        return lista_tec
    
    def query_tecnologia(self, tecnologia):
        """
        Hace un query que regresa el nombre de la tecnologia, el porcentaje de positividad contra negatividad, y el número
        de aspectos (por cada aspecto)
        @param tecnologia: el nombre de la tecnologia a buscar.
        @return: dict() con los siguientes valores: nombre, avail_scal, maintainability, performance, reliability, deployability,
        securability, interoperability, total_avail_scal, total_maintainability, total_performance, total_reliability,
        total_deployability, total_securability, total_interoperability.
        """       
        dict_query = self.bda.query_aspectos_tecnologia(tecnologia)
        return dict_query
        
        
        
        