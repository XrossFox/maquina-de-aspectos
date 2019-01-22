import os

import json
import itertools

import eliminador_de_etiquetas
import solucionador_de_correferencias
import limpiador_de_texto
import extractor_de_raices


class Preprocesador():
    
    def __init__(self, direccion_nlp, direccion_stp_wrds):
        """
        Inicializa el servicio de CoreNLP y carga la lista de Stopwords.
        """
        
        self.core = solucionador_de_correferencias.SolucionadorDeCorreferencias(direccion_nlp)
        self.lim = limpiador_de_texto.LimpiadorDeTexto(direccion_stp_wrds)
        self.elim = eliminador_de_etiquetas.EliminadorDeEtiquetas()
        self.r = extractor_de_raices.ExtractorDeRaices()
    
    def leer_json(self, direccion):
        """
        Lee un archivo json y devuelve su contenido de acuerdo a su tipo. La conversion se lleva a cabo segun la
        especificacion en la API de Python del modulo json.
        """
            
        archivo = open(direccion, mode="r", encoding="utf-8")
        contenido = json.load(archivo)
        archivo.close()
        return contenido
    
    def escribir_a_json(self, ob, direccion, nombre):
        """
        Escribe un objeto python a un objeto json. La conversion se lleva a cabo segun la
        especificacion en la API de Python del modulo json.
        """

        if len(direccion) < 1:
            pass
        elif not direccion.endswith("/"):
            direccion += "/"
        archivo = open(direccion+nombre, "wt", encoding="utf-8")
        json.dump(ob, archivo)
        archivo.close()
    
    def _init_global(self, stem=False, lemmatize=False, coref=False,
        punct=False, num=False, html=False, urls=False, stp_wrds=False):
        """
        Inicializa las variables globales para evitar evitar la declaracion redundante de atributos
        en cada método que los requiera
        """
        
        self.stem=stem
        self.lemmatize=lemmatize
        self.coref=coref
        self.punct=punct
        self.num=num
        self.html=html
        self.urls=urls
        self.stp_wrds=stp_wrds
        
        if self.stem and self.lemmatize:
            raise Exception("'stem' y 'lemmatize' no pueden ser ambas True") 
     
    def main(self, dir_entrada, dir_salida, stem=False, lemmatize=False, coref=False,
        punct=False, num=False, html=False, urls=False, stp_wrds=False):
        """
        Inicia el proceso de limpieza.
        Si stem == True, utiliza stemming.
        Si lemmatize == True, utiliza lematizacion, si ambos son True, solo usa stemming.
        Si ambos == False, no usa ninguno.
        """ 
        
        self._init_global(stem, lemmatize, coref, punct, num, html, urls, stp_wrds)
                
        entrada = self.leer_json(dir_entrada)
        
        self.contador = 1
        self.tops = len(entrada)
        
        #Una lista del iterable resultado de la funcion map()
        resultado = [self._aux(texto) for texto in entrada]
            
        path = dir_entrada.split("/")
        nombre = nombre = self._gen_nombre(path[-1])
        self.escribir_a_json(resultado, dir_salida, nombre)
        
    def _gen_nombre(self, nombre):
        """
        Devuelve el nombre del archivo a escribir según si se usa stemming,
        lemmatization y resolucion de correferencias.
        """
        
        sec1 = "no_coref_"
        sec2 = "no_"
        sec3 = nombre
        
        if self.coref:
            sec1 = "coref_"
        
        if self.stem:
            sec2 = "stem_"
        elif self.lemmatize:
            sec2 = "lem_"
            
        return sec1+sec2+nombre
        
        
    def _aux(self, texto):
        """
        Aplica cada uno de los métodos de limpieza a un texto.
        """
        texto = texto.lower()
        
        texto = self.elim.remover_escapes(texto)
        if self.html:
            texto = self.elim.remover_codigo(texto)
            texto = self.elim.remover_etiquetas(texto)
            texto = self.lim.remocion_de_espacios(texto)
            
        if self.urls:
            texto = self.lim.remocion_de_urls(texto)
            texto = self.lim.remocion_de_espacios(texto)
        
        if self.coref:
            try:
                texto = self.core.resolver_y_reemplazar(texto)
            except Exception as w:
                #print(type(w))
                #print(w)
                #print(w.args)
                print("Error: saltando resolución de correferencias")
        
        if self.punct:    
            texto = self.lim.remocion_de_puntuaciones(texto)
            texto = self.lim.remocion_de_espacios(texto)
        
        if self.num:
            texto = self.lim.remocion_de_numeros(texto)
            texto = self.lim.remocion_de_espacios(texto)
        
        if self.stp_wrds:
            texto = self.lim.remocion_de_stopwords(texto)
            texto = self.lim.remocion_de_espacios(texto)
                
        if self.stem:
            texto = self.r.stem_texto(texto)
        elif self.lemmatize:
            texto = self.r.lem_texto(texto)

        print("Procesado texto {} de {}".format(self.contador,self.tops))
        self.contador += 1
        return texto
    
    def _cerrar(self):
        """
        Cierra el servicio de CoreNLP corriendo en el fondo.
        """
        self.core.cerrar()