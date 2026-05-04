import os 
os.environ['AMBIENTE_GENETICAPP'] = 'PROTOTIPO'
import sys
sys.path.insert(0, '/var/www/geneticapp/geneticapp/fuente')
from geneticapp import servidor as application
