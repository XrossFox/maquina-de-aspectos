
class ModeloEntrenado(object):

    def __init__(self, vectores, mod_entrenado, f_score):
        
        self.vocabulario = vectores['vocabulario']
        self.dtm = vectores['dtm']
        self.idf_vector = vectores['idf_vector']
        self.tfidf_repr = vectores['tfidf_repr']
        self.mod_entrenado = mod_entrenado
        self.f_score = f_score
    
    def clasificar_comentario(self, comentario, neutro=False):
        """
        Clasifica un comentario asignandole una polaridad.
        @param comentario: un string.
        @return: 1 si es positivo o -1 si es negativo.| Si comentarios neutros estan activados, regresa:
        1 para positivo, 0 para neutro y -1 para negativo. 
        """
        # vocabulario del comentario de acuerdo al vocabulario del dataset
        com_voc = self.vocabulario.transform([comentario])
        # comentario vectorizado usando el vector tf_idf
        com_vec = self.idf_vector.transform(com_voc)
        # probabilidad de estar en una de dos clases. Si neg tiene mayor prob de ser negativo, regresa 0. Si  no, regresa 1
        neg, pos = self.mod_entrenado.predict_proba(com_vec)[0]
        # si se permiten neutros:
        print("comentario: {} - pos: {} - neg: {}".format(comentario, pos, neg))
        if neutro:
            print("Neutros activados")
            if pos > 0.497:
                print("positivo")
                return 1
            elif neg > 0.504:
                print("negativo")
                return -1
            else: 
                print("neutral")
                return 0
        # si solo se esperan pos y neg:
        if neg > pos:
            print("Neutros desactivados")
            return -1
        return 1
    
    
        
        