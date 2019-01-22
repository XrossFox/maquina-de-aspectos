import requests
import json
import click
from time import sleep

#API Ref: https://hn.algolia.com/api

@click.command()
@click.argument("search_string")
@click.argument("max_pages")
@click.argument("output_path")
def main(search_string,max_pages,output_path):
    """
    Método main, recibe 3 parametros al llamarse desde linea de comandos. Actua como CLI.
    Hace un request a la API de busqueda de hackernews y los comentarios que cuadren con
    el string de busqueda son escritos a un archivo .json en formato json array.
    
    search_string: cadena de texto a buscar en la API.
    max_pages: número máximo de paginas a extraer de la API.
    output_path: path del archivo .json a escribir
    """
    json_response_list = hack_api_request(search_string, int(max_pages))
    comment_list = json_extract(json_response_list)
    to_hdd(comment_list,search_string, output_path)
    
def to_hdd(comment_list, name, output_path):
    """
    Escribe un archivo json en formato json array desde una lista.
    comment_list: lista a convertir a json.
    name: nombre del archivo.
    output_path: path del archivo de salida.
    """
    with open('{}\\{}.json'.format(output_path,name), 'w') as file:
        json.dump(comment_list, file)
    

def json_extract(json_response_list):
    """
    Extrae los comentarios de la respuesta de la API. La respuesta es un diccionario.
    json_response_list: lista de diccionarios.
    
    return comments_list: una lista de comentarios (str). 
    """
    comments_list = []
    for json_response in json_response_list:
        for hit in json_response["hits"]:
            comments_list.append(hit["comment_text"])
    return comments_list
            
def hack_api_request(search_string,max_pages):
    """
    Realiza un request http a la API de busqueda de Hackernews.
    
    search_string: cadena de busqueda para el query.
    max_pages: cuantas páginas se deben pedir.
    
    return json_list: una lista de diccionarios (la respuesta de la API es un json convertido a diccionario)
    """
    url = "https://hn.algolia.com/api/v1/search_by_date?query={}&hitsPerPage=50&tags=comment&page={}"
    json_list = []
    for current_page in range(0,max_pages):
        req = requests.get(url.format(search_string,current_page))
        json_list.append(req.json())
        sleep(1)
    return json_list
    
    
if __name__ == "__main__":
    main()