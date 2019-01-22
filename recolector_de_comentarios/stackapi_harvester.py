from stackapi import StackAPI
import click
import pickle
import json


@click.command()
@click.argument('intext')
@click.argument('tagged')
@click.argument('output_path')
@click.option('-p', default=1, help="Cantidad de Páginas")
@click.option('-s', type=click.IntRange(1,100, clamp=True), default=1,
               help="Cantidad de elementos por página, mínimo 1, máximo 100",)
@click.option('-v', type= click.IntRange(0,1, clamp=True), default=0,
              help="Modo verboso = 1, default es 0")
def main(intext, tagged, output_path, p, s, v):
    """Método main del script, requiere 6 parametros al ejecutarse desde linea de comandos:\n
    intext: el texto a buscar en el cuerpo del texto.\n
    tagged: los tags con los que esta marcada la pregunta.\n
    output_path: destino del archivo .json"""
    
    if v: click.echo("Intext: {}. Tagged: {}. -p: {}. -s: {}".format(intext,tagged,p,s))
    
    response = fetch_stackapi(intext, tagged, p, s)
    dataset = maze_runner(response, v)
    #pickle_list(output_path, intext, tagged, dataset, v)
    to_hdd(dataset, "{}_{}".format(intext,tagged), output_path)
 
def to_hdd(comment_list, name, output_path):
    """
    Escribe un archivo json en formato json array desde una lista.
    comment_list: lista a convertir a json.
    name: nombre del archivo.
    output_path: path del archivo de salida.
    """
    with open('{}\\{}.json'.format(output_path,name), 'w') as file:
        json.dump(comment_list, file)  
  
def fetch_stackapi(text, tags, page_size=1, max_pages=1):
    """Método que realiza la petición a la Stack API. Recibe:
       text: = string de busqueda in-lin para para la busqueda
       tags: busca posts marcados con estos tags
       page_size: tamaño de páginas a recuperar
       max_pages: número de páginas a recuperar
       """
    tags_toks = tags.split(";")
    
    SITE = StackAPI('stackoverflow')
    SITE.page_size = page_size
    SITE.max_pages = max_pages
    return SITE.fetch('search/advanced', intext=text, tagged=tags_toks, sort="relevance",
                          filter="!7qBwspMQR3L7c4q7tesaRX(_gP(rj*U-.H")

def maze_runner(response, verbose):
    """Recorre el dict del response recuperado de la Stack API.
       Agrega a una lista todos los cuerpos de texto de las preguntas, las respuestas y todos
       sus comentarios respectivos y la devuelve. Recibe:
       response: response de la API
       verbose: modo verboso"""
    lista_comentarios = []
    #El response es un dict
    if verbose: print("Devuelve una respuesta: {}".format(type(response)))
    if verbose: print('Y contiene:')
    
    for keys in response:
        if verbose: print('-'*4+"4: {} - que es: {}".format(keys,type(response[keys])))
        
        #items es una lista que puede tener una o más preguntas
        if keys == 'items':
            items = response[keys]
            if verbose: print("-"*8+"8: Esta lista contiene preguntas:")
            
            #Preguntas
            for question in items:
                if verbose: print("-"*8+"8: question_id: {}".format(question["question_id"]))
                if verbose: print("-"*8+"8: pregunta: {} - {}".format(type(question),repr(question)[:30]))
                
                # Cada pregunta es un diccionario
                # IMPORTANTE: La llave 'body' tiene el cuerpo de la preguta
                lista_comentarios.append(question['body'])
                # IMPORTANTE: La llave 'title' tiene el nombre de la pregunta
                
                
                for q_key in question:
                    if verbose: print("-"*12+"12: {} que es: {}".format(q_key,type(question[q_key])))
                    
                    # Que puede tener una lista de comentarios
                    if q_key == 'comments':
                        
                        # Cada comentario es una lista
                        for comment in question[q_key]:
                            #print("-"*16+" elemento: {}".format(type(comment)))
                            lista_comentarios.append(comment['body'])
                            # Que contiene un diccionario
                            for c_item in comment:
                                
                                # IMPORTANTE: La llave 'body' tiene el texto del comentario
                                if verbose: print("-"*20+"20: {} que es: {}".format(c_item,type(c_item)))
                                
                    
                    # O una lista de respuestas
                    if q_key == 'answers':
                        # Cada respuesta es un diccionario
                        # IMPORTANTE: la llave 'body' tiene el cuerpo de la respuesta
                        for comment in question[q_key]:
                            if verbose: print("-"*16+"16: elemento: {}".format(type(comment)))
                            lista_comentarios.append(comment['body'])
                            
                            for c_item in comment:
                                if verbose: print("-"*20+" 20: {} que es: {}".format(c_item,type(comment[c_item])))
                                
                                # que puede tener una lista de comentarios
                                if c_item == 'comments':
                                    
                                    #Cada comentario es un diccionario
                                    for ind in comment[c_item]:
                                        if verbose: print("-"*24+'24: elemento que es: {}'.format(type(ind)))
                                        lista_comentarios.append(ind['body'])
                                        
                                        # IMPORTANTE: la llave 'body' tiene el cuerpo del comentario
                                        for key_ind in ind:
                                            if verbose: print("-"*28+"28: {} que es: {}".format(key_ind,type(ind[key_ind])))
    if verbose:
        print("-"*100)
        for comentario in lista_comentarios:
            print(comentario)
            print("-"*100)
    return lista_comentarios

def pickle_list(out_path, intext, tagged, dataset, verbose):
    """serializa la lista de comentarios en un archivo de texto
       de protocolo más alto (legible por el ser humano). Recibe:
       out_path: directorio de salida.
       intext: string de busqueda intext (para el nombre).
       tagged: string de buqueda de tags (para el nombre).
       dataset: lista de comentarios a serializar:
       verbose: modo verboso. """
       
       
    with open(file="{}\\intext_{}-tagged_{}.txt".format(out_path, intext, tagged)
              , mode="ab") as file:
        pickle.dump(dataset, file, pickle.HIGHEST_PROTOCOL)
    
    if verbose: print("Escrito/anexado una lista nativa de python 3 al archivo: {}".format("{}\\intex_{}-tagged_{}.txt".format(
        out_path, intext, tagged)))
        
                    
if __name__ == "__main__":
    main()