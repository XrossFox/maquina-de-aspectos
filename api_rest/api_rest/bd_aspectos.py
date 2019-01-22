from peewee import *
import datetime
from os.path import join
import configuracion_api_rest

db = Proxy()

class Aspectos(Model):
    """
    Clase entidad de la tabla "aspectos"
    """
    id = AutoField(primary_key=True)
    tecnologia = CharField()
    avail_scal = BooleanField(null=True)
    maintainability = BooleanField(null=True)
    performance = BooleanField(null=True)
    reliability = BooleanField(null=True)
    deployability = BooleanField(null=True)
    securability = BooleanField(null=True)
    interoperability = BooleanField(null=True)
            
    class Meta:
        database = db

class BDAspectos():
    """
    Clase que permite operaciones sobre la base de datos
    """
    def __init__(self, db_dir=None):
        """
        Constructor. Carga o crea una base de datos.
        @param db_dir: si db_dir es None, crea una base de datos nueva. Si no, carga la base de datos especificada.
        """
        self.con = configuracion_api_rest.Configuracion()
        # cargar db de direccion especificada
        if db_dir:
            base_datos = SqliteDatabase(db_dir)
            # inicializar proxy
            db.initialize(base_datos)
        else:
            # nombre y direccion de la nueva db
            fecha = datetime.datetime.now()
            nombre = "sqlite_{}-{}-{}-{}-{}.db".format(fecha.year, fecha.month, fecha.day, fecha.hour,
                                                               fecha.minute, fecha.second)
            direccion = self.con.dir_bases_datos
            path_completo = join(direccion,nombre)
            # se crea db con la dirección completa
            base_datos = SqliteDatabase(path_completo)
            db.initialize(base_datos)
            # crear tabla
            Aspectos.create_table()
            
        self.json_estructura = {
            "nombre": "",
            "total": 0,
            "total_pos": 0,
            "total_neg": 0,
            "p_pos": 0.0,
            "p_neg": 0.0,
            "avail_scal": {
                "total": 0,
                "total_pos": 0,
                "total_neg": 0,
                "p_pos": 0.0,
                "p_neg": 0.0
            },
            "maintainability": {
                "total": 0,
                "total_pos": 0,
                "total_neg": 0,
                "p_pos": 0.0,
                "p_neg": 0.0
            },
            "performance": {
                "total": 0,
                "total_pos": 0,
                "total_neg": 0,
                "p_pos": 0.0,
                "p_neg": 0.0
            },
            "reliability": {
                "total": 0,
                "total_pos": 0,
                "total_neg": 0,
                "p_pos": 0.0,
                "p_neg": 0.0
            },
            "deployability": {
                "total": 0,
                "total_pos": 0,
                "total_neg": 0,
                "p_pos": 0.0,
                "p_neg": 0.0
            },
            "securability": {
                "total": 0,
                "total_pos": 0,
                "total_neg": 0,
                "p_pos": 0.0,
                "p_neg": 0.0
            },
            "interoperability": {
                "total": 0,
                "total_pos": 0,
                "total_neg": 0,
                "p_pos": 0.0,
                "p_neg": 0.0
            }
        }

            
    
    def insertar_a_tabla(self, dict_polaridades):
        """
        Inserta las polaridades de los aspectos en la tabla 'Aspectos'.
        @param dict_polaridades: un dict donde la llave es el nombre de la tecnologia. El valor es una lista de dicts donde:
        la llave es el nombre del aspecto y el valor la polaridad sentimental del aspectos (0 para negativo, 1 para positivo
        o None si  no tiene).
        """
        # por cada tecnologia...
        for tec in dict_polaridades:
            # insertar los aspectos de los comentarios a la tabla.
            for dict_comentarios in dict_polaridades[tec]:
                if dict_comentarios:
                    Aspectos.create(tecnologia=tec,
                                    avail_scal=dict_comentarios["AvailabilityAndScalability"],
                                    maintainability=dict_comentarios["Maintainability"],
                                    performance=dict_comentarios["Performance"],
                                    reliability=dict_comentarios["Reliability"],
                                    deployability=dict_comentarios["Deployability"],
                                    securability=dict_comentarios["Securability"],
                                    interoperability=dict_comentarios["Interoperability"],
                                    )
        
    def query_tecnologias_disponibles(self):
        """
        Devuelve una lista de las tecnologías en la base de datos.
        @retun: lista con las tecnologias disponibles en la base de datos. 
        """
        query = Aspectos.select().group_by(Aspectos.tecnologia)
        db.close()
        return [a.tecnologia for a in query]
    
    def _aux_totales(self, dict_aspectos, fila):
        """
        Método auxiliar para el método _aux_query_aspectos_tecnologia. Cuenta
        los atributos de calidad validos y los agrega a los contadores.
        @param dict_aspectos: El diccionario con la estructura json.
        @param fila: Una fila del 'query select'.
        @return: dict_aspectos con los contadores actualziados.
        """
        # actualiza los contadores de totales si no son None.
        if fila.avail_scal != None:
            if fila.avail_scal:
                dict_aspectos["avail_scal"]["total_pos"] += 1
            else:
                dict_aspectos["avail_scal"]["total_neg"] += 1
                
            dict_aspectos["avail_scal"]["total"] += 1
            
        if fila.maintainability != None:
            if fila.maintainability:
                dict_aspectos["maintainability"]["total_pos"] += 1
            else:
                dict_aspectos["maintainability"]["total_neg"] += 1

            dict_aspectos["maintainability"]["total"] += 1
            
        if fila.performance != None:
            if fila.performance:
                dict_aspectos["performance"]["total_pos"] += 1
            else:
                dict_aspectos["performance"]["total_neg"] += 1
                
            dict_aspectos["performance"]["total"] += 1
            
        if fila.reliability != None:
            if fila.reliability:
                dict_aspectos["reliability"]["total_pos"] += 1
            else:
                dict_aspectos["reliability"]["total_neg"] += 1
                
            dict_aspectos["reliability"]["total"] += 1
            
        if fila.deployability != None:
            if fila.deployability:
                dict_aspectos["deployability"]["total_pos"] += 1
            else:
                dict_aspectos["deployability"]["total_neg"] += 1
                
            dict_aspectos["deployability"]["total"] += 1
            
        if fila.securability != None:
            if fila.securability:
                dict_aspectos["securability"]["total_pos"] += 1
            else:
                dict_aspectos["securability"]["total_neg"] += 1
                
            dict_aspectos["securability"]["total"] += 1
            
        if fila.interoperability != None:
            if fila.interoperability:
                dict_aspectos["interoperability"]["total_pos"] += 1
            else:
                dict_aspectos["interoperability"]["total_neg"] += 1
                
            dict_aspectos["interoperability"]["total"] += 1
            
        return dict_aspectos
    
    def _aux_porcentajes(self, dict_aspectos):
        """
        Calcula los porcentajes de aspectos positivos y negativos de la estructura json.
        @param dict_aspectos: la estructura de la respuesta json.
        @return: dict_aspectos, la estructura con los porcentajes actualziados.
        """
        # porcentajes avail_scal
        dict_aspectos["avail_scal"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["avail_scal"]["total"],
                                                                    tot_pos=dict_aspectos["avail_scal"]["total_pos"])
        dict_aspectos["avail_scal"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["avail_scal"]["total"],
                                                                    tot_pos=dict_aspectos["avail_scal"]["total_neg"])
        
        # porcentajes maintainability
        dict_aspectos["maintainability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["maintainability"]["total"],
                                                                    tot_pos=dict_aspectos["maintainability"]["total_pos"])
        dict_aspectos["maintainability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["maintainability"]["total"],
                                                                    tot_pos=dict_aspectos["maintainability"]["total_neg"])
        
        # porcentajes performance
        dict_aspectos["performance"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["performance"]["total"],
                                                                    tot_pos=dict_aspectos["performance"]["total_pos"])
        dict_aspectos["performance"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["performance"]["total"],
                                                                    tot_pos=dict_aspectos["performance"]["total_neg"])

        # porcentajes reliability
        dict_aspectos["reliability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["reliability"]["total"],
                                                                    tot_pos=dict_aspectos["reliability"]["total_pos"])
        dict_aspectos["reliability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["reliability"]["total"],
                                                                    tot_pos=dict_aspectos["reliability"]["total_neg"])

        # porcentajes deployability
        dict_aspectos["deployability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["deployability"]["total"],
                                                                    tot_pos=dict_aspectos["deployability"]["total_pos"])
        dict_aspectos["deployability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["deployability"]["total"],
                                                                    tot_pos=dict_aspectos["deployability"]["total_neg"])
        
        # porcentajes securability
        dict_aspectos["securability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["securability"]["total"],
                                                                    tot_pos=dict_aspectos["securability"]["total_pos"])
        dict_aspectos["securability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["securability"]["total"],
                                                                    tot_pos=dict_aspectos["securability"]["total_neg"])
        
        # porcentajes interoperability
        dict_aspectos["interoperability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["interoperability"]["total"],
                                                                    tot_pos=dict_aspectos["interoperability"]["total_pos"])
        dict_aspectos["interoperability"]["p_pos"] = self._saca_porcentajes(total=dict_aspectos["interoperability"]["total"],
                                                                    tot_pos=dict_aspectos["interoperability"]["total_neg"])
        return dict_aspectos
    
    def _aux_totales_general(self, dict_aspectos):
        """
        Actualiza los contadores generales de la respuesta json.
        @param dict_aspectos: El dicyt con la estructura json.
        @return: la estrcutur a con los contadores actualizados.
        """
        dict_aspectos["total_pos"] = sum([dict_aspectos["avail_scal"]["total_pos"],dict_aspectos["maintainability"]["total_pos"],
                dict_aspectos["performance"]["total_pos"],dict_aspectos["reliability"]["total_pos"],
                dict_aspectos["deployability"]["total_pos"],dict_aspectos["securability"]["total_pos"],
                dict_aspectos["interoperability"]["total_pos"]])
        
        dict_aspectos["total_neg"] = sum([dict_aspectos["avail_scal"]["total_neg"],dict_aspectos["maintainability"]["total_neg"],
                dict_aspectos["performance"]["total_neg"],dict_aspectos["reliability"]["total_neg"],
                dict_aspectos["deployability"]["total_neg"],dict_aspectos["securability"]["total_neg"],
                dict_aspectos["interoperability"]["total_neg"]])
        
        dict_aspectos["total"] = dict_aspectos["total_pos"] + dict_aspectos["total_neg"]
        
        dict_aspectos["p_pos"] = self._saca_porcentajes(total=dict_aspectos["total"],
                                                        tot_pos=dict_aspectos["total_pos"])
        dict_aspectos["p_neg"] = self._saca_porcentajes(total=dict_aspectos["total"],
                                                        tot_pos=dict_aspectos["total_neg"])
        
        return dict_aspectos
    
    def query_aspectos_tecnologia(self, tecnologia):
        """
        Devuelve un diccionario con los aspectos de una tecnologia
        @param tecnologia: el nombre de la tecnologia.
        @return: dict con los aspectos y numero de aspectos.
        """
        
        dict_aspectos = self.json_estructura
        select_all = Aspectos.select().where(Aspectos.tecnologia==tecnologia)
        
        if not len(list(select_all)):
            return None
        
        dict_aspectos["nombre"] = tecnologia
        for fila in select_all:
            # Contadores
            dict_aspectos = self._aux_totales(dict_aspectos, fila)
            # porcentajes
            dict_aspectos = self._aux_porcentajes(dict_aspectos)
            # totales general
            dict_aspectos = self._aux_totales_general(dict_aspectos)
        
        return dict_aspectos
    
    def cerrar_db(self):
        db.close()
    
    def _saca_porcentajes(self, total, tot_pos):
        if total and tot_pos:
            return (tot_pos / total) * 100
        return 0.0