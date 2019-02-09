import click
from entrenador import entrenador
from clasificador import clasificador
from servidor import servidor
import configuracion_api_rest

@click.command()
@click.option("-e", help="Entrena el clasificador Naive Bayes usando los datasets de entrenamiento.", is_flag=True)
@click.option("-c", help="Clasifica los comentarios (pos y neg) y los agrega a una base de datos SQlite3.", is_flag=True)
@click.option("-n", help="Clasifica los comentarios (pos, neu y neg) y los agrega a una base de datos SQlite3.", is_flag=True)
@click.option("-s", help="Inicia el servidor REST.", is_flag=True)
def main(e, c, s, n):
    """
    Recuerda editar las direcciones de los directorios en configuracion_api_rest.py en el constructor. Las opciones son
    mutuamente exclluyentes, y tienen la siguiente prioridad: e > c > s.
    """
    conf = configuracion_api_rest.Configuracion()
    if e:
        print("Entrenando modelo...")
        ent = entrenador.Entrenador()
        ent.inicio(dir_datasets_entrenamiento=conf.dir_datasets_entrenamiento,
                   dir_modelos_entrenados=conf.dir_modelos_entrenados)
        ent.cerrar()
        return
    if c:
        print("Clasificando comentarios...")
        cla = clasificador.Clasificador()
        cla.iniciar_clasificacion(dir_modelos_entrenados=conf.dir_modelos_entrenados,
                                  dir_comentarios=conf.dir_comentarios)
        return
    if n:
        print("Clasificando comentarios incluyendo neutrales...")
        cla = clasificador.Clasificador()
        cla.iniciar_clasificacion(dir_modelos_entrenados=conf.dir_modelos_entrenados,
                                  dir_comentarios=conf.dir_comentarios, neutro=True)
        return
    if s:
        print("Iniciando servidor REST...")
        rest = servidor.Servidor()
        rest.iniciar_servidor(dir_bases_datos=conf.dir_bases_datos)
        return
    
if __name__ == "__main__":
    main()