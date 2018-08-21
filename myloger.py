import logging
import logging.config
import os.path as path
from datetime import datetime

def create_file():
    return datetime.now().strftime('%Y%m%d') + '.log'
    
logs_url = path.abspath(path.join(path.dirname(__file__), 'logs', create_file()))
logconf = {
        "version": 1,
        "disable_existing_loggers" : True,
        "formatters":{
            'file':{
                'class': 'logging.Formatter',
                'format': '%(asctime)s[%(levelname)s] :  %(name)s : %(message)s'
            }
        },
        "handlers": {
            'file_logs':{
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'filename': logs_url,
                'mode': 'w',
                'formatter': 'file'
            }
        },
        "loggers":{
            'flog':{
                "level": 'DEBUG',
                "handlers": ['file_logs'],
                "propagate": 0
            }
        },
        "root":{
            "level": 'DEBUG',
            "handlers": ['file_logs']
        }
    }

logging.config.dictConfig(logconf)
flog = logging.getLogger('flog')
