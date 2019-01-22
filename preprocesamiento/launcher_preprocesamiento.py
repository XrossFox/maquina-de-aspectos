import os

import click
import preprocesador
import time
import configuracion_preprocesamiento

#punct=False, num=False, html=False, urls=False, stp_wrds=False

@click.command()
@click.argument('output')
@click.option('-t', help="Dirección del archivo .json")
@click.option('-b', help="Dirección de archivo .txt con direcciones a archivo .json")
@click.option('-stem/--no-stem', help="Stemming activado, o desactivado", default=False)
@click.option('-lem/--no-lem', help="Lemmatizacion activada, o desactivada", default=False)
@click.option('-c/--no-c', help="Resolucion de correferencias activada, o desactivada", default=False)
@click.option('-p/--no-p', help="Remover puntuación, activado o desactivado", default=False)
@click.option('-n/--no-n', help="Remover numeros, activado o desactivado", default=False)
@click.option('-h/--no-h', help="Remover tags HTML/XML, activado o desactivado", default=False)
@click.option('-u/--no-u', help="Remover URLs, activado o desactivado", default=False)
@click.option('-s/--no-s', help="Remover stop words, activado o desactivado", default=False)
def main(output, t, b, stem, lem, c, p, n, h, u, s):
    config = configuracion_preprocesamiento.Configuracion()
    
    
    if t == None and b == None:
        click.echo("No hay archivo especificado, --help para ayuda (ver opciones -t y -b).")
        exit()
        
    if stem == True and lem == True:
        click.echo("Las opciones -stem y -lem no se pueden usar en conjunto.")
        exit()
    
    click.echo("+"*30+
               "\nOUTPUT: {}\nIn_Path: {}\nBatch: {}\nStemming: {},\nLemmatization: {}\nRes. de Correferencias: {}\n".format(output, t, b, stem, lem, c)+
               "Remover Puntuaciones: {}\nRemover Numeros: {}\nRemover HTML/XML: {}\nRemover URLs: {}\nRemover Stop Words: {}\n".format(p, n, h, u, s)+
               "-"*30)
    pre = preprocesador.Preprocesador(config.direccion_corenlp, config.direccion_stopwords)
    
    tiempo = time.time()
    
    if t != None:
        click.echo(t)
        _llamadas(t, output, stem, lem, c, p, n, h, u, s, pre)
        click.echo("Tiempo transcurrido: {}".format((time.time() - tiempo)))
            
    else:
        click.echo(b)
        lineas = _lectura(b)
        contador = 1
        for linea in lineas:
            click.echo("-"*30+"\n"+"Archivo .json: {}\n {} de {} archivos".format(linea, contador, len(lineas)))
            _llamadas(linea, output, stem, lem, c, p, n, h, u, s, pre)
            click.echo("Tiempo transcurrido: {}".format((time.time() - tiempo))+" Segundos\n"+"-"*30)
            contador += 1
            
    pre._cerrar()

def _lectura(direccion):
    """Lee un archivo de texto con direcciones de archivos .json"""
    archivo_texto = open(direccion, "rt", encoding="utf-8")
    lineas = [linea.strip() for linea in archivo_texto]
    return lineas
            
def _llamadas(t, output, stem, lem, c, p, n, h, u, s, pre=None):
        """Flujo principal del programa"""        
        try:
            pre.main(t, output, stem, lem, c, p, n, h, u, s)
        except Exception as w:
            print(type(w))
            print(w)
            print(w.args)
            pre._cerrar()
    
    
    
    
    
if __name__ == "__main__":
    main()


