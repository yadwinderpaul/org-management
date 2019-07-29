import os
from dotenv import load_dotenv
import logging
from organizations.adapters import PipedriveAdapter

load_dotenv()


def InitConfig(app):
    return {
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'DEBUG'),
        'ADAPTER_NAME': os.getenv('ADAPTER_NAME', 'pipedrive'),
        'PIPEDRIVE': {
            'ENDPOINT': os.getenv('PIPEDRIVE_ENDPOINT'),
            'API_TOKEN': os.getenv('PIPEDRIVE_API_TOKEN'),
            'DEFAULT_LIMIT': os.getenv('PIPEDRIVE_DEFAULT_LIMIT'),
            'NAME_FIELD_KEY': os.getenv('PIPEDRIVE_NAME_FIELD_KEY'),
            'URL_FIELD_KEY': os.getenv('PIPEDRIVE_URL_FIELD_KEY'),
            'ADDRESS_FIELD_KEY': os.getenv('PIPEDRIVE_ADDRESS_FIELD_KEY'),
            'COORDINATES_FIELD_KEY':
                os.getenv('PIPEDRIVE_COORDINATES_FIELD_KEY'),
        }
    }


def InitLogger(app):
    config = app['config']
    logging.basicConfig(
        level=config['LOG_LEVEL']
    )
    return logging.getLogger('main')


def InitAdapter(app):
    if app['config']['ADAPTER_NAME'] == 'pipedrive':
        logger = app['logger']
        pipedrive_config = app['config']['PIPEDRIVE']
        return PipedriveAdapter(pipedrive_config, {
            'logger': logger
        })
