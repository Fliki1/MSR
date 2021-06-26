import logging
'''
Gestione dei log da più moduli, che potrebbero richiedere una configurazione di log differente per ambito di lavoro
Quando si lavora con un modulo ha i suoi log
se lo si importa in un altro modulo con i suoi log configurati, ne cambia anche i connotati di quello importato

Per evitare ciò e mantenere le differenze magari, modulo solo INFO e modulo solo DEBUG, o ordine del formato ecc..

getLogger() returns a reference to a logger instance with the specified name if it is provided, or root if not.
in questo caso __name__ è il nomde del modulo corrente, nel main sarebbe stato __main__

bisogna chiamare poi logger per fare le print
'''
logger = logging.getLogger(__name__)    # nome del modulo corrente
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
# FileHandler: outputfile
file_handler = logging.FileHandler('./log/Metodo1.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# StreamHandler: console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def ciao():
    logger.info('sono dentro metodo1')