from os import listdir
from os.path import join
import sys
import json

import configuracion_api_rest
conf = configuracion_api_rest.Configuracion()
sys.path.append(conf.dir_extractor_de_aspectos)

from extractor import extractor_de_aspectos
from modelo_entrenado import ModeloEntrenado
import pandas
from sklearn.feature_extraction.text  import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score
import pickle
import datetime

class Entrenador(object):
    '''
    Esta clase produce un clasificador de Machine Learning Naive Bayes Multinomial
    '''
    def __init__(self):
        self.ex = extractor_de_aspectos.ExtractorDeAspectos()
    
    def inicio(self, dir_datasets_entrenamiento, dir_modelos_entrenados):
        """
        Inicia el proceso de entrenar un modelo. Requiere configurar entradas y salidas en configuracio_api_rest.py
        @return: la direccion del modelo entrenado en disco.
        """
        comentarios = self._lector(dir_datasets_entrenamiento)
        comentarios = self._limpiar_palabras(comentarios)
        df_comentarios = self._crear_dataframe(comentarios)
        vectores = self._vectorizacion(df_comentarios)
        modelo = self._entrenar_modelo(vectores, df_comentarios)
        dir_modelo = self._escribir_modelo(dir_modelos_entrenados, modelo)
        
        return dir_modelo
    
    def _lector(self, directorio):
        """
        Lee todos los archivos con extension .json en un directorio y que cumplan con el squiete formato:
        [[0,"comentario1"], [1,"comentario2"]]
        @param directorio: la dirección de un directorio.
        @return: una lista de listas de comentarios con el sentimiento en la posicion 0 y el comentario en 1.
        Los sentimientos son: 0 si es negativo y 1 si es positivo. El comentario es un str.
        """
        comentarios = list()
        archivos = list(listdir(directorio))
        
        for archivo in archivos:
            fname = join(directorio,archivo)
            if not archivo.endswith(".json"):
                continue
            with open(file=fname, mode="r", encoding="utf-8") as op:
                tmp = json.load(op)
                for el in tmp:
                    if not isinstance(el, list):
                        raise(TypeError("Uno de los elementos en '{}' no es un json array.".format(fname)))
                    if not isinstance(el[0], int):
                        raise(TypeError("Uno de los elementos en '{}' en la posicion 0 no es un 'int'.".format(fname)))
                    if not (el[0] == 1 or el[0] == 0):
                        raise(ValueError("Uno de los elementos en '{}' en la posicion 0 no es un '1' o '0'.".format(fname)))
                    if not isinstance(el[1], str):
                        raise(TypeError("Uno de los elementos en {} en la posicion 1 no es un 'str'.".format(fname)))
                    if not len(el) == 2:
                        raise(IndexError("Uno de los elementos en {} no contiene solo 2 posiciones".format(fname)))
                    
                comentarios.extend(tmp)
            
        return comentarios
    
    def _limpiar_palabras(self, palabras):
        """
        Extrae las palabras que sean adverbios, adjetivos y negaciones, elimina el resto. Hace uso del modulo 
        'extractor_de_aspectos'.
        @param palabras: una lista de [sentimiento, "palabras"]
        @return: una lista de [sentimiento, "adjetivos/adverbios/negaciones de las palabras"]
        """
        palabras_limpias = list()
        for palabra in palabras:
            tmp = self.ex.quitar_palabras(palabra[1].lower())
            if tmp:
                palabras_limpias.append([palabra[0], tmp])
        return palabras_limpias
    
    def _crear_dataframe(self, palabras):
        """
        Convierte la lista de palabras en un dataframe de pandas.
        @param palabras: una lista de listas de [sentimiento, "adjetivos/adverbios/negaciones"]
        @return: un objeto DataFrame de Pandas
        """
        df_palabras = pandas.DataFrame({"label":[tx[0] for tx in palabras],"message":[tx[1] for tx in palabras]})
        return df_palabras
    
    def _vectorizacion(self, df_palabras):
        """
        Vectoriza y devuelve las respectivas transformaciones necesarias para entrenar y hacer uso del
        clasificador Naive Bayes.
        @param df_palabras: el dataframe generado a partid de la lista de palabras
        @return: un dict con "vocabulario", "dtm", "idf_vector", "tfidf_repr"
        """
        vecto = CountVectorizer()
        
        vocabulario = vecto.fit(df_palabras['message'])
        dtm = vocabulario.transform(df_palabras['message'])
        idf_vector = TfidfTransformer().fit(dtm)
        tfidf_repr = idf_vector.transform(dtm)
        return {"vocabulario":vocabulario, "dtm":dtm, "idf_vector":idf_vector, "tfidf_repr":tfidf_repr}
    
    def _entrenar_modelo(self, vectores, df_palabras):
        """
        Entrena el modelo.
        @param vectores: dict con los vectores de entrenamiento
        @param df_palabras: DataFrame de las palabras.
        @return: un objeto modelo_entrenado.
        """
        X_train, X_test, y_train, y_test = train_test_split(vectores["tfidf_repr"], df_palabras['label'],
                                                            test_size=0.1, random_state=69)
        model_tf_idf = MultinomialNB().fit(X_train, y_train)
        predicted_tfidf = model_tf_idf.predict(X_test)
        f_score = f1_score(y_test, predicted_tfidf, average="binary")
        mod_en = ModeloEntrenado(vectores, model_tf_idf, f_score)
        return mod_en
        
    def _escribir_modelo(self, directorio, mod_en):
        """
        Serializa y escribe el modelo entrenado a disco duro para usarse posteriormente.
        @param directorio: directorio de salida para el archivo.
        @param mod_en: el objeto ModeloEntrenado.
        @return: el directorio y nombre del archivo escrito. 
        """
        fecha = datetime.datetime.now()
        nombre = "mul_nb_{}-{}-{}-{}-{}.clasif".format(fecha.year, fecha.month, fecha.day, fecha.hour,
                                                   fecha.minute, fecha.second)
        dir_completo = join(directorio,nombre)
        with open(file=dir_completo, mode="wb") as fl:
            pickle.dump(mod_en, fl)
        return dir_completo
                
    def cerrar(self):
        self.ex.cerrar()
