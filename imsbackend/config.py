import configparser
import os

app_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(app_dir, "config.ini")
config_parsor = configparser.ConfigParser()

default_log_path = app_dir + '/logs/'


# run this if config.ini doesn't exits.
def create_config_file(cfg_parser):
    """
    Create config.ini with defaults if this file doesn't exist.
    """

    cfg_parser.add_section('MONGODB')
    cfg_parser.set('MONGODB', 'MONGODB_URL', '10.189.132.143')
    cfg_parser.set('MONGODB', 'MONGODB_PORT', '27017')
    cfg_parser.set('MONGODB', 'MONGODB_DB_NAME', 'InstituteManagement')
    cfg_parser.add_section('LOGGER')
    cfg_parser.set('LOGGER', 'LOG_LEVEL', 'DEBUG')
    cfg_parser.set('LOGGER', 'CRITICAL', '50')
    cfg_parser.set('LOGGER', 'FATAL', 'CRITICAL')
    cfg_parser.set('LOGGER', 'ERROR', '40')
    cfg_parser.set('LOGGER', 'WARNING', '30')
    cfg_parser.set('LOGGER', 'WARN', 'WARNING')
    cfg_parser.set('LOGGER', 'INFO', '20')
    cfg_parser.set('LOGGER', 'DEBUG', '10')
    cfg_parser.set('LOGGER', 'NOTSET', '0')
    cfg_parser.set('LOGGER', 'MAXBYTES', '209715200')
    cfg_parser.set('LOGGER', 'BACKUPCOUNT', '5')
    try:
        with open(config_file, 'w') as configfile:
            cfg_parser.write(configfile)
    except:
        pass


if not os.path.isfile(config_file):
    create_config_file(config_parsor)

config_parsor.read(config_file)

mongo = config_parsor['MONGO']
MONGODB_URL = mongo.get('mongodb_url', 'localhost')
MONGODB_PORT = mongo.get('mongodb_port', '27017')
MONGODB_DB_NAME = mongo.get('mongodb_db_name', 'InstituteManagement')


log = config_parsor['LOGGER']
LOGNAME = log.get('LOGNAME', 'imslog')
CRITICAL = log.get('CRITICAL', '50')
FATAL = log.get('FATAL', 'CRITICAL')
ERROR = log.get('ERROR', '40')
WARNING = log.get('WARNING', '30')
WARN = log.get('WARN', 'WARNING')
INFO = log.get('INFO', '20')
DEBUG = log.get('DEBUG', '10')
NOTSET = log.get('NOTSET', '0')
LOG_LEVEL = log.get('LOG_LEVEL', 'DEBUG')
MAXBYTES = log.get('MAXBYTES', '209715200')
BACKUPCOUNT = log.get('BACKUPCOUNT', '5')

LOG_FORMAT = "'%(asctime)s [%(levelname)-8s] [%(filename)s:%(lineno)-4d] [%(funcName)s] %(message)s'"
