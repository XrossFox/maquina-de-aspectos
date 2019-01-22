import os

from stanfordcorenlp import StanfordCoreNLP
import nltk
import re

class SolucionadorDeCorreferencias():
    
    def __init__(self, direccion_nlp):
        """Inicializa CoreNLP, requiere el path hacia la carpeta raiz"""
        self.lista_pronombres = ["i","you", "he", "she", "it", "we", "you", "they",
                              "my", "your", "his", "her", "its", "our", "their",
                              "mine", "yours", "hers", "ours", "yours", "theirs",
                              "myself", "yourself", "himself", "herself", "itself",
                              "ourselves", "yourselves", "themselves", "me",
                              "him", "it", "us", "them", "that"]
    
        #Iniciar servidor de CoreNLP
        self.nlp = StanfordCoreNLP(direccion_nlp)
    
    def cerrar(self):
        """Termina el proceso de CoreNLP."""
        self.nlp.close()
    
    def resolver_y_reemplazar(self, texto, verbose=False):
        """Reemplaza todos los pronombres de objetos por el objeto en cuestion.
        No reemplaza pronombres por otros pronombres. El string 'texto' se convierte a minusculas."""
        
        texto = texto.lower()
        if verbose: print("-"*30)
        if verbose: print("Texto Base: {}\n ".format(texto))
        # refs es una lista de listas. El primer indice indica una lista de correferencias
        # ref es una lista de correferencias, cada elemento es asi: (sentence_index, start_index, end_index, text).
        # El objetivo consiste en buscar el sustantivo y reemplazar todos los pronombres por el. No se reemplazan
        # pronombres por otros pronombres
        l_refs = self.nlp.coref(texto)
        if verbose: print("Correferencias encontradas: \n{}\n ".format(str(l_refs)))
        texto = self._reemplazar(texto, l_refs)
        if verbose: print("Texto Resuelto: {}\n ".format(texto))
        if verbose: print("+"*30)
        return texto
    
    def _reemplazar(self, texto, *l_refs):
        """Reemplaza pronombres por sustantivos en el texto dado."""
        # Recorremos lista de referencias
        tk_tx = nltk.sent_tokenize(texto)
        
        for refs in l_refs:
            # inicializamos sustantivo como None
            # recorremos referencias
            for ref in refs:
                sustantivo = None
                pronombres = []
                i_sent = set()
                for tup_i in range(len(ref)):
                    # si el texto en ref no es un pronombre, es un sustantivo
                    if ref[tup_i][3] not in self.lista_pronombres:
                        sustantivo = ref[tup_i][3]
                    # si es un pronombre, lo agregamos a nuestra lista de pronombres
                    else: 
                        pronombres.append(ref[tup_i][3])
                        i_sent.add(ref[tup_i][0])
                    
                # si se encontro un sustantivo...
                if sustantivo:
                    # ...revisamos cada sentencia...
                    for i in i_sent:
                        # ...y reemplazamos cada pronombre en nuestra lista por el sutantivo
                        for pro in pronombres:
                            tk_tx[i-1] = re.sub(r"\b"+pro+r"\b", sustantivo, tk_tx[i-1])
                            
        reemplazo = ""
        for i in range(len(tk_tx)):
            reemplazo += tk_tx[i] + " "
                    
        return reemplazo.strip()
                