from cliente_corenlp import cliente_corenlp
from lematizador import lematizador
import nltk
import configuracion

class ExtractorDeAspectos(object):
    
    def __init__(self):
        self.cliente = cliente_corenlp.ClienteCoreNLP()
        self.lemas = lematizador.Lematizador()
        self.config = configuracion.Configuracion()
    
    def cerrar(self):
        self.cliente.cerrar_servicio()
    
    def quitar_palabras(self, texto):
        """
        Extrae las palabras con las siguientes etiquetas POS: Adverbios, Adjetivos, Negaciones y
        Determinantes (solo si es negacion).
        @param texto: El comentario de texto a procesar.
        @return: texto: Una cadena de texto solo con las palabras de las etiquetas deseadas y lematizadas. 
        """
        
        tuplas_pos = self.cliente.etiquetar_texto(texto)
        lista_pos_lem = self.lemas.lematizar_tuplas(tuplas_pos)
        lista_pos_lem = self._purgar_palabras_pos(lista_pos_lem)
        texto = self._unir_palabras(lista_pos_lem)
        
        return texto
    
    def _unir_palabras(self, lista_pos_lem):
        """
        Une la lista de tuplas en una cadena.
        @param lista_pos_lem: la lista de tuplas.
        @return: un string del texto concatenado
        """
        texto = ""
        for tupla in lista_pos_lem:
            if tupla[2]:
                texto += tupla[2] + " "
            else:
                texto += tupla[0] + " "
        return texto.strip()
    
    def _purgar_palabras_pos(self, lista_pos_lem):
        """
        Método auxiliar, elimina todas las palabras con etiqueta pos que no inicie con R, J,
        y D(y que sea negación).
        @param lista_pos_lem: lista de tuplas pos con lemas.
        @return: lista de tuplas con lemas sin palabras no deseadas.
        """
        nueva_lista = list()
        for tupla in lista_pos_lem:
            if tupla[1].startswith("J") or tupla[1].startswith("R"):
                nueva_lista.append(tupla)
            elif tupla[1].startswith("D") and (tupla[0] in ("no", "not")):
                nueva_lista.append(tupla)
        return nueva_lista
    
    def iniciar_extraccion(self, texto):
        """
        Inicia la extraccion de los aspectos dado un comentario.
        @param texto: el comentario de texto a procesar
        @return dict_aspectos: una lista de aspectos encontrados según su categoria.
        """
        sentencias = nltk.sent_tokenize(texto)
        
        aspectos_resultado = dict()
        
        for sentencia in sentencias:
            lista_pos_lem = self.lemas.lematizar_tuplas(self.cliente.etiquetar_texto(sentencia))
            arbol_de_dependencias = self.cliente.resolver_dependencias(sentencia)
            
            res = self.extraer(self.config.dict_aspectos, arbol_de_dependencias, lista_pos_lem)
            aspectos_resultado = self._combinar_dict(res, aspectos_resultado)
        
        return aspectos_resultado

    def extraer(self, diccionario_de_aspectos, arbol_de_dependencias, lista_pos_lem):
        """
        Extrae las dependencias (amod, advmod, neg, y ciertos nsubj) de acuerdo al diccionario de aspectos de UNA
        SOLA SENTENCIA A LA VEZ.
        @param diccionario_de_aspectos: el diccionario con los aspectos, cada llave es un aspecto y cada elemento
                                        de la lista es el aspecto mas sinonimos del mismo ej:
                                        {"performance": ["performance","latency","thoroughput"]}
        @param arbol_de_dependencias: es el producto del Standford Parser.
        @param lista_pos_lem: la lista de tuplas resultado del stanford POS Tagger
                              despues de haber agregado los lemas.
        @return: Un diccionario, cada llave es una categoria de aspecto con una lista de dependencias. ej:
                {aspecto1:[dependencias],aspecto2:{dependencias}}.
                Si no se encontraron dependenacias, las listas estaran vacias.
        """
        aspectos_encontrados = dict()
        
        for llave in diccionario_de_aspectos:
            aspectos_encontrados[llave] = list()
            
        for hoja in arbol_de_dependencias:
            if hoja[0] in ("amod", "advmod", "neg"):
                dependencia = self._extraer_dependencia(hoja[1], hoja[2], lista_pos_lem, diccionario_de_aspectos,
                                          arbol_de_dependencias)
                if dependencia:
                    aspectos_encontrados[dependencia[0]].append(dependencia[1])
            
            elif hoja[0] == "conj":
                dependencia = self._extraer_conj(hoja[1], hoja[2], lista_pos_lem,
                                                diccionario_de_aspectos, arbol_de_dependencias)
                if dependencia:
                    aspectos_encontrados[dependencia[0]].append(dependencia[1])
                
            elif hoja[0] in ("nsubj","nmod"):
                dependencia = self._extraer_nsubj(hoja[1], hoja[2], lista_pos_lem, diccionario_de_aspectos,
                                                  arbol_de_dependencias)
                if dependencia:
                    aspectos_encontrados[dependencia[0]].append(dependencia[1])
        
        return aspectos_encontrados
    
    def _extraer_dependencia(self, indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos,
                             arbol_de_dependencias=None):
        """
        Si se encuentra una dependencia que va del una raiz a un nodo, extrae la dependencia y lo devuelve si
        esta en la lista de aspectos.
        @param indice_raiz: posición de la palabra raiz (la dependencia).
        @param indice_nodo: posicion de la palabra nodo (el sustantivo).
        @param lista_pos_lem: lista de las tuplas pos_lem.
        @param diccionario_de_aspectos: diccionario con los aspectos deseados.
        @param arbol_de_dependencias: el arbol de dependencias. Si se especifica
                                    se busca si la dependencia tiene su propia dependencia.
                                    ej. Un adjetivo de un sustantivo que tiene su propio adverbio.
        @return: (aspecto, dependencia) | None si no es un aspecto.
        """
        posible_aspecto = self._buscar_en_tupla_pos_lem(indice_raiz-1, lista_pos_lem)
        dependencia = self._buscar_en_tupla_pos_lem(indice_nodo-1, lista_pos_lem)
        
        aspecto = self._es_aspecto(posible_aspecto, diccionario_de_aspectos)
        
        if aspecto:
            if arbol_de_dependencias:
                doble = self._extraer_dependencia_doble(indice_nodo, lista_pos_lem, 
                                                        arbol_de_dependencias)
                if doble:
                    dependencia = doble +" "+ dependencia
                    
            return (aspecto, dependencia)
        
        return None
    
    def _extraer_conj(self, indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos,
                             arbol_de_dependencias=None):
        """
        Si se encuentra una dependencia que va del una raiz a un nodo, extrae la dependencia y lo devuelve si
        esta en la lista de aspectos. Funciona igual que _extraer_dependencia, solo tiene checkeos especificos
        para las conjunciones.
        @param indice_raiz: posición de la palabra raiz (la dependencia).
        @param indice_nodo: posicion de la palabra nodo (el sustantivo).
        @param lista_pos_lem: lista de las tuplas pos_lem.
        @param diccionario_de_aspectos: diccionario con los aspectos deseados.
        @param arbol_de_dependencias: el arbol de dependencias. Si se especifica
                                    se busca si la dependencia tiene su propia dependencia.
                                    ej. Un adjetivo de un sustantivo que tiene su propio adverbio.
        @return: (aspecto, dependencia) | None si no es un aspecto.
        """
        posible_aspecto = self._buscar_en_tupla_pos_lem(indice_raiz-1, lista_pos_lem)
        tag_asp = lista_pos_lem[indice_raiz-1][1]
        dependencia = self._buscar_en_tupla_pos_lem(indice_nodo-1, lista_pos_lem)
        tag_dep = lista_pos_lem[indice_nodo-1][1]
        
        
        if tag_asp.startswith("N") and (tag_dep.startswith("J") or tag_dep.startswith("R")):
        
            aspecto = self._es_aspecto(posible_aspecto, diccionario_de_aspectos)
            if aspecto:
                if arbol_de_dependencias:
                    doble = self._extraer_dependencia_doble(indice_nodo, lista_pos_lem, 
                                                            arbol_de_dependencias)
                    if doble:
                        dependencia = doble +" "+ dependencia
                        
                return (aspecto, dependencia)
        
        return None
    
    def _extraer_nsubj(self, indice_raiz, indice_nodo, lista_pos_lem, diccionario_de_aspectos,
                             arbol_de_dependencias=None):
        """
        Funciona igual que extraer_dependencia pero con checkeos especificos para sujetos nominales (nsubj).
        @param indice_raiz: posición de la palabra raiz (el sustantivo).
        @param indice_nodo: posicion de la palabra nodo (la dependencia).
        @param lista_pos_lem: lista de las tuplas pos_lem.
        @param diccionario_de_aspectos: diccionario con los aspectos deseados.
        @param arbol_de_dependencias: el arbol de dependencias. Si se especifica
                                    se busca si la dependencia tiene su propia dependencia.
                                    ej. Un adjetivo de un sustantivo que tiene su propio adverbio.
        @return: (aspecto, dependencia) | None si no es un aspecto.
        """
        #Primero se revisa si el nsubj va de un adjetivo a un sustantivo
        if lista_pos_lem[indice_raiz-1][1].startswith("J") and lista_pos_lem[indice_nodo-1][1].startswith("N"):
            
            # el orden de los aspectos/dependencias viene al reves a diferencia de las dependencias normales
            posible_aspecto = self._buscar_en_tupla_pos_lem(indice_nodo-1, lista_pos_lem)
            dependencia = self._buscar_en_tupla_pos_lem(indice_raiz-1, lista_pos_lem)
            
            aspecto = self._es_aspecto(posible_aspecto, diccionario_de_aspectos)
            
            if aspecto:
                if arbol_de_dependencias:
                    # el orden viene invertido.
                    doble = self._extraer_dependencia_doble(indice_raiz, lista_pos_lem, 
                                                            arbol_de_dependencias)
                    if doble:
                        dependencia = doble +" "+ dependencia
                        
                return (aspecto, dependencia)
        
        return None
    
    
    def _extraer_dependencia_doble(self, indice_nodo, lista_pos_lem, arbol_de_dependencias):
        """
        Revisa si existe un amod o un advmod que sea dependencia de un nodo encontrado en _extraer_dependencia.
        Por ejemplo, un adjetivo de un sustantivo que tiene su propio adverbio.
        @param indice_nodo: posicion de la palabra nodo (la dependencia a revisar por otra dependencia).
        @param lista_pos_lem: lista de las tuplas pos_lem.
        @param arbol_de_dependencias: el arbol de dependencias.
        """
        for dep in arbol_de_dependencias:
            
            dep_tag, indice_raiz_d, indice_nodo_d = dep
            
            if dep_tag in ("amod", "advmod", "neg") and indice_raiz_d == indice_nodo:
                
                dependencia = self._buscar_en_tupla_pos_lem(indice_nodo_d-1, lista_pos_lem)
                return dependencia
            
        return None
    
    def _es_aspecto(self, palabra, diccionario_de_aspectos):
        """
        Recibe una palabra y la busca dentro del diccionario de aspectos para determinar
        si es uno de los aspectos deseados.
        @param palabra: la palabra a determinar.
        @param diccionario_de_aspectos: el diccionario de aspectos.
        @return: la categoría del aspecto, o None si no se encuentra. 
        """
        
        for categoria in diccionario_de_aspectos:
            if palabra in diccionario_de_aspectos[categoria]:
                return categoria
            
        return None
       
    def _buscar_en_tupla_pos_lem(self, indice, lista_pos_lem):
        """
        Recibe un número, busca la tupla en lista_pos_lem en esa posicion y devuelve el lema.
        Si el lema es None, entonces devuelve la palabra.
        @param indice: Posición de la tupla deseada.
        @param lista_pos_lem: La lista que contiene las tuplas (palabra, pos, lema)
        @return: lema || palabra.
        """
        if lista_pos_lem[indice][2]:
            return lista_pos_lem[indice][2]
        
        return lista_pos_lem[indice][0]
    
    def _combinar_dict(self, dict1, dict2):
        for llave in dict1:
            if llave in dict2.keys():
                dict2[llave].extend(dict1[llave])
            else:
                dict2[llave] = dict1[llave]
        return dict2