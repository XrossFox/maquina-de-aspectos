# maquina-de-aspectos
Sistema de análisis de sentimientos basado en aspectos para evaluar atributos de calidad de comentarios de software (de stackoverflow y hackernews).
___
## Consideraciones
+ Este sistema fue desarrollado para mi proyecto de tesis __Evaluación de Atributos de Calidad Sobre Tecnologías a Partir de Comentarios de Usuarios Usando
Técnicas de Minería de Opiniones y Análisis de Sentimientos__ (nombre sujeto a cambios).
+ Este sistema consta de cuatro modulos. Dos de ellos funcionan de manera independiente (_recolector de comentarios_ y _preprocesador_),
los otros dos dependen el uno del otro (_api_rest_ tiene como dependencia _extractor de aspectos_).
___

## Uso de los Modulos:

Nota: se incluye un archivo _requirements.txt_ con la lista de dependencias necesarias.

### Recolector de Comentarios
Este modulo permite descargar comentarios de _StackOverflow_ y _HackerNews_ utilizando una sencilla interfaz de CLI. 

Para _hacker_news_query.py_:
> hacker_news_query.py SEARCH_STRING MAX_PAGES OUTPUT_PATH 

Donde: _search_string_ es la cadena de texto a buscar, _max_pages_ es la cantidad de páginas y _output_path_ es el directorio donde se
guardara el archivo .json con la respuesta.

Para _stackapi_harvester.py_:
> stackapi_harvester.py [OPTIONS] INTEXT TAGGED OUTPUT_PATH

Donde _intext_ es la cadena de texto a buscar, _tagged_ son el o los tags que deben tener las preguntas, _output_path_ es el directorio de salida donde
se guarda el archivo .json.

Permite las siguientes opciones:
+ -s: cantidad de páginas.
+ -p: cantidad de preguntas por página, entre 1 y 100.
+ -v: modo verboso, imprime todo el árbol de la respuesta mientras se parsea.

### Preprocesador
+ Requiere Java instalado, debido a que puede realizar resolución de correferencias usando el _Stanford CoreNLP_
+ Descargar _Stanford CoreNLP_. Tambien es una dependencia del _Extractor de Aspectos_. Descomprimir contenidos del .zip.
+ Para el Preprocesador primero es necesario descargar _wordnet_ y _punkt_. Dentro de la consola de python:
```
  import nltk
  nltk.download("wordnet")
  nltk.download("punkt")
```
+ Es necesario configurar la dirección de Stanford CoreNLP en el archivo __conf_pp.py__ en la linea 5:
```
self._dir_corenlp = "path/a/corenlp"
```


