import sys
from os import listdir
from os.path import join, isdir, isfile
import configuracion_api_rest
conf = configuracion_api_rest.Configuracion()
sys.path.append(conf.dir_extractor_de_aspectos)
import pickle
import re
import json
import bd_aspectos
from extractor import extractor_de_aspectos

class Clasificador(object):
    '''
    Clasficá de los comentarios de texto y los almacena en una base de datos sqlite
    '''

    def __init__(self):
        self.ex = extractor_de_aspectos.ExtractorDeAspectos()
        
        
    def _cargar_modelo_entrenado(self, direccion):
        """
        Lee todos los archivos en el directorio recibido con extension .clasif. Si no encuentra archivos, levanta una
        excepcion. Carga el modelo mas reciente en el directorio.
        @param direccion: direccion hacia el directorio con los archivos .clasif.
        @return: una instancia de modelo_entrenado.
        """
        archivos = list(listdir(direccion))
        ult_clasif = ""
        mod_en = None
        for n in range(len(archivos)):
            # se recorre desde atras la lista de archivos
            nombre = archivos[(n+1)*-1]
            # si el ultimo elemento tiene la extension, se usa ese. Si no continua.
            if nombre.endswith(".clasif"):
                ult_clasif = join(direccion, nombre)
                break
            n += 1
        try:
            with open(file=ult_clasif, mode="rb") as fl:
                mod_en = pickle.load(fl)
        except:
            raise ValueError("No se encontro ningún archivo con extensions '.clasif'")
        return mod_en
    
    def _cargar_comentarios(self, direccion):
        """
        Lee los comentarios de cada tecnología en su respectiva carpeta, en el directorio especificado.
        @param direccion: el directorio donde se buscan los comentarios.
        @return: dict() de listas. Cada llave es una tecnologia, como valor se tiene una lista con los comentarios
        de cada tecnología encontrada.
        """
        dir_tec = [join(direccion, directorio) for directorio in listdir(direccion)]
        comentarios = dict()
        
        # revisar los directorios y remover los que no lo son
        for directorio in dir_tec:
            if not isdir(directorio):
                dir_tec.remove(directorio)
                
        # cargar los comentarios dentro de la lista de directorios en su respectiva llave
        for directorio in dir_tec:
            tmp = self._aux_cargar_comentarios(directorio)
            comentarios[tmp[0]] = tmp[1]
        
        return comentarios
        
    def _aux_cargar_comentarios(self, directorio):
        """
        Lee todos los comentarios con extension .json en un directorio, y devuelve una tupla: (nombre, [lista_comentarios])
        @param directorio: direccion del directorio
        @return: una tupla (nombre, [lista_de_comentarios])
        """
        nom_tec = re.split(r"[\\/]", directorio)
        archivos = [join(directorio, archivo) for archivo in listdir(directorio)]
        lista_res = (nom_tec[-1], list())
        
        # eliminar no-archivos y los que no tienen la extension apropiada
        for archivo in archivos:
            if not isfile(archivo):
                archivos.remove(archivo)
            if not archivo.endswith(".json"):
                archivos.remove(archivo)
        
        # leer todos los .json
        for archivo in archivos:
            with open(file=archivo, mode="r", encoding="utf-8") as fl:
                com = json.load(fl)
                for el in com:
                    if not isinstance(el, str):
                        raise ValueError("Uno de los elementos en '{}' no es un json array".format(archivo))
                if not isinstance(com, list):
                    raise ValueError("Uno de los elementos en '{}' no es un json array".format(archivo))
                lista_res[1].extend(com)
          
        return lista_res
    
    def _extraer_aspectos(self, comentarios):
        """
        Extrae los aspectos de los comentarios.
        @param comentarios: es un dict. Cada llave es el nombre de la tecnologia. Como valor se tiene una lista de
        comentarios de dicha tecnología.
        @return: un dict donde cada llave es la tecnología. El valor es un dict que tiene por llave el nombre del
        aspecto y por valor una lista de strings con adjetivos, adverbios y negaciones, o vacia.
        """
        dict_aspectos = dict()
        for tecnologia in comentarios:
            dict_aspectos[tecnologia] = list()
            for comentario in comentarios[tecnologia]:
                aspectos = self.ex.iniciar_extraccion(comentario)
                dict_aspectos[tecnologia].append(aspectos)
        return dict_aspectos
    
    def _clasificar_aspectos(self, dict_aspectos, mod_en):
        """
        Clasifica los aspectos de los comentarios.
        @param dict_aspectos: un dict donde la llave es el nombre de la tecnología y el valor es una lista de dicts, donde
        las llaves son los nombres de los aspectos y los valores son listas de strings con los adjetivos, adverbios y
        negaciones.
        @param mod_en: instancia del modelo entrenado.
        @return: dict donde la llave es el nombre de la tecnologñia y el valor es una lista de dicts, donde las llaves
        son los aspectos y los valores pueden ser 'pos', 'neg' o None.
        """
        dict_polaridades = dict()
        for tecnologia in dict_aspectos:
            dict_polaridades[tecnologia] = list()
            # aspectos es un diccionario, con los nombres de los aspectos por llave y lista de strings como valor
            for aspectos in dict_aspectos[tecnologia]:
                # el nuevo diccionario, llave: nombres de aspectos, valor: polaridad.
                tmp_aspectos = dict()
                for nombre_aspecto in aspectos:
                    polaridad = None
                    # Si la lista de strings en la llave nombre_aspecto no esta vacia.
                    if aspectos[nombre_aspecto]:
                        com_strings = " ".join(aspectos[nombre_aspecto])
                        polaridad = mod_en.clasificar_comentario(com_strings)
                    tmp_aspectos[nombre_aspecto] = polaridad
                # agregamos el dict con los aspectos evaluados al dict de tecnologias
                dict_polaridades[tecnologia].append(tmp_aspectos)
        return dict_polaridades
    
    def iniciar_clasificacion(self, dir_modelos_entrenados, dir_comentarios):
        """
        Inicia la clasificación de los comentarios, los inserta en una base de datos SQLite en disco duro.
        Requiere que se edite la dirección de la carpeta de los comentarios, las bases de datos y los modelos entrenados
        de manera manual en el archivo configuracion_api_rest.py.
        @param dir_modelos_entrenados: direccion a directorio con modelos entrenados.
        @param dir_comentarios: direccion a directorio con comentarios.
        """
        # cargar modelo
        modelo = self._cargar_modelo_entrenado(dir_modelos_entrenados)
        
        # cargar comentarios
        comentarios = self._cargar_comentarios(dir_comentarios)
        # extraer aspectos
        dict_aspectos = self._extraer_aspectos(comentarios)
        # clasificar polaridad sentimental de los aspectos
        dict_polaridades = self._clasificar_aspectos(dict_aspectos, modelo)
        # creacion e insercion en la base de datos
        base_datos = bd_aspectos.BDAspectos()
        base_datos.insertar_a_tabla(dict_polaridades)
        
        # cerrar el servicio corenlp
        self._terminar()
        
    def _terminar(self):
        self.ex.cerrar()
                
        