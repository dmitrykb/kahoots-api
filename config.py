import os
import inspect
import ConfigParser

# server info
api_version = 1;
root_path = os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))

# read config.ini for specific server type
config_path = os.path.join(root_path, 'config.ini')
config_ini = ConfigParser.ConfigParser()
config_ini.read(config_path)

log_path = os.path.join(root_path, 'flikdate.log')

# main Database
db = {}
db['host'] = config_ini.get('DB_MAIN', 'DB_HOST', 0)
db['user'] = config_ini.get('DB_MAIN', 'DB_USER', 0)
db['password'] = config_ini.get('DB_MAIN', 'DB_PASSWORD', 0)
db['database'] = config_ini.get('DB_MAIN', 'DB_DATABASE', 0)
db['raise_on_warnings'] = config_ini.getboolean('DB_MAIN', 'RAISE_ON_WARNINGS')
db_url='mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(db['user'], db['password'], db['host'], db['database']) 

# facebook auth
client_id = config_ini.get('FACEBOOK_APP', 'CLIENT_ID', 0)
client_secret = config_ini.get('FACEBOOK_APP', 'CLIENT_SECRET', 0)
