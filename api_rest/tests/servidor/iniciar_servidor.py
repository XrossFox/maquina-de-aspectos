import sys
sys.path.append('../../api_rest')
from servidor import servidor

s = servidor.Servidor()
s.iniciar_servidor(dir_bases_datos="./db_tests_3")