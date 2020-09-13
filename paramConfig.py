import configparser
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

# read all the key value pairs from GSHEET section
gs_fileName = config['GSHEET']['filename']
gs_fileID = config['GSHEET']['fileId']

# read all the key value pairs from ALSITE section
al_Sheet_Name = config['ALSITE']['sheetName']
al_client = config['ALSITE']['client']
al_mail = config['ALSITE']['mail']
al_pwd = config['ALSITE']['pwd']
al_status = config['ALSITE']['status']
al_tgt_status = config['ALSITE']['tgt_status']

# read all the key value pairs from PRSITE section
pr_Sheet_Name = config['PRSITE']['sheetName']

