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

___
### Recolector de Comentarios
Este modulo permite descargar comentarios de _StackOverflow_ y _HackerNews_ utilizando una sencilla interfaz de CLI. 

Para _hacker_news_query.py_:
> hacker_news_query.py SEARCH_STRING MAX_PAGES OUTPUT_PATH 

Donde: _search_string_ es la cadena de texto a buscar, _max_pages_ es la cantidad de páginas y _output_path_ es el directorio donde se
guardara el archivo .json con la respuesta.

Para _stackapi_harvester.py_:
```
stackapi_harvester.py [OPTIONS] INTEXT TAGGED OUTPUT_PATH

Options:
 -s: cantidad de páginas.
 -p: cantidad de preguntas por página, entre 1 y 100.
 -v: modo verboso, imprime todo el árbol de la respuesta mientras se parsea.
```

Donde _intext_ es la cadena de texto a buscar, _tagged_ son el o los tags que deben tener las preguntas, _output_path_ es el directorio de salida donde
se guarda el archivo .json.

Permite las siguientes opciones:


___
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

+ Tambien es posible editar la dirección del archivo con stopwords. El archivo stopwords.txt es un simple archivo de texto
con un stopword por linea.

Preprocesador tiene una interfaz CLI para el usuario a traves del archivo python _launcher_preprocesador.py_:
```
launcher_preprocesar.py [OPTIONS] OUTPUT

Options:
  -t TEXT            Dirección del archivo .json
  -b TEXT            Dirección de archivo .txt con direcciones a archivo .json
  -stem / --no-stem  Stemming activado, o desactivado
  -lem / --no-lem    Lemmatizacion activada, o desactivada
  -c / --no-c        Resolucion de correferencias activada, o desactivada
  -p / --no-p        Remover puntuación, activado o desactivado
  -n / --no-n        Remover numeros, activado o desactivado
  -h / --no-h        Remover tags HTML/XML, activado o desactivado
  -u / --no-u        Remover URLs, activado o desactivado
  -s / --no-s        Remover stop words, activado o desactivado
  --help             Show this message and exit.
```

___
### Extractor de Aspectos
Este modulo es una dependencia para _Api Rest_.
+ Para el correcto funcionamiento de este modulo solo es necesario editar la dirección a _Stanford CoreNLP_ en _configuracion.py_ en la linea 14:

```
self._direccion_corenlp = "path/a/corenlp"
```

+ Tambien es posible editar la dirección al archivo .json con los aspectos a extraer. El diccionario de aspectos es un simple objeto JSON con la siguiente estructura:

```
{
"Aspecto1":["sinonimo1","sinonimo2","sinonimoN"],
"Aspecto2":["sinonimo1","sinonimo2","sinonimoN"]
}
```
Notese que un diccionario de aspectos es provisto _por default_. Este diccionario esta hecho para extraer los aspectos de atributos de calidad de software.

Este modulo fue pensado para funcionar de manera independiente de ser necesario, como una libreria adicional. Es posible implementarla en otros sistemas de ser necesario.

___
### Api REST
Este modulo permite entrenar clasificadores Naïve Bayes, clasificar comentarios de texto y guardarlos en una base de datos SQLite3 y servir peticiones http a traves de una interfaz API REST para recuperar los resultados. Para su funcionamiento primero es necesario configurar las siguientes direcciones en _configuracion_api_rest.py_.

#### Extractor de Aspectos
+ Dirección a la raíz del modulo _Extractor de Aspectos:
```
self._dir_extractor_de_aspectos = "path/hacia/extractor_de_aspectos/extractor_de_aspectos"
```
#### Datasets de Entrenamiento
+ Dirección hacia directorio con datasets de entrenamiento para el clasificador Naïve Bayes.
```
self._dir_datasets_entrenamiento = "./data/dataset_entrenamiento"
```
+ Los datasets de entrenamiento deben estar etiquetados y estar formateados en _JSON Array_. Tambien tomar en cuenta que los comentarios
fueron procesados por el modulo _Extractor de Aspectos_ y las cadenas de texto solo contienen __adverbios__, __adjetivos__ y __negaciones__.
```
[
[0,"comentario negativo"],
[1,"comentario positivo"],
]
```
+ Se cargan todos los archivo con extensión .json que se encuentren en la carpeta como dataset de entrenamiento.

### Modelos Entrenados
+ Dirección hacia el directorio donde se almacenan los Modelos Naïve Bayes.
```
self._dir_modelos_entrenados = "./data/modelos_entrenados"
```
+ Cuando se carga un modelo, solo se carga el más reciente.
### Bases de Datos
+ Dirección hacia el directorio donde se almacenan.
```
self._dir_bases_datos = "./data/bases_datos"
```
+ Solo se carga la base de datos más reciente.

### Comentarios de texto
+ La dirección hacia el directorio con los comentarios de texto.
```
self._dir_comentarios = "./data/comentarios"
```
+ Los comentarios de texto se almacenan en sub-directorios de tal manera que cada uno lleva el nombre de la tecnología y los archivos tienen extension .json.:
```
Comentarios
--- tecnología_1:
------ comentarios_1.json
------ comentarios_2.json
--- tecnología_2:
------ comentarios_1.json
```
+ Los comentarios son simples _JSON Arrays_:
```
["comentario_1", "comentario_2"]
```
+ Los comentarios deben estar limpios de toda etiqueta HTML/XML y de ser posible, no contener código de programación.
+ Los comentarios deben tener las negaciones (no, not, n't, etc.) intactas.

La Api REST tene una interfaz CLI para el usuario a traves del archivo _launcher.py_:
```
launcher.py [OPTIONS]

Options:
  -e      Entrena el clasificador Naive Bayes usando los datasets de
          entrenamiento.
  -c      Clasifica los comentarios y los agrega a una base de datos SQlite3.
  -s      Inicia el servidor REST.
  --help  Show this message and exit.
```
