class Configuracion():
    """
    Clase de configuarcion del la aplicacion REST
    """
    def __init__(self):
        """
        Modificar esto de acuerdo al sistema.
        """
        # path del modulo extractor_de_aspectos
        self._dir_extractor_de_aspectos = "/home/david/Desktop/tesis/Tesis-Analisis-Aspectos/extractor_de_aspectos/extractor_de_aspectos"
        self._dir_datasets_entrenamiento = "/home/david/Desktop/tesis/Tesis-Analisis-Aspectos/api_rest/api_rest/data/dataset_entrenamiento"
        self._dir_modelos_entrenados = "/home/david/Desktop/tesis/Tesis-Analisis-Aspectos/api_rest/api_rest/data/modelos_entrenados"
        self._dir_bases_datos = "/home/david/Desktop/tesis/Tesis-Analisis-Aspectos/api_rest/api_rest/data/bases_datos"
        self._dir_comentarios = "/home/david/Desktop/tesis/Tesis-Analisis-Aspectos/api_rest/api_rest/data/comentarios"
    
    def get_dir_extractor_de_aspectos(self): return self._dir_extractor_de_aspectos
    def get_dir_datasets_entrenamiento(self): return self._dir_datasets_entrenamiento
    def get_dir_modelos_entrenados(self): return self._dir_modelos_entrenados
    def get_dir_bases_datos(self): return self._dir_bases_datos
    def get_dir_comentarios(self): return self._dir_comentarios
    
    dir_extractor_de_aspectos = property(fget=get_dir_extractor_de_aspectos)
    dir_datasets_entrenamiento = property(fget=get_dir_datasets_entrenamiento)
    dir_modelos_entrenados = property(fget=get_dir_modelos_entrenados)
    dir_bases_datos = property(fget=get_dir_bases_datos)
    dir_comentarios = property(fget=get_dir_comentarios)
    