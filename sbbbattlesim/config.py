import logging
import logging.config
import os
import traceback

config = {
    'logging': {
        'logging_conf': os.getenv('LOGGING_CONF', 'logging.ini'),
        'logging_level': os.getenv('LOGGING_LEVEL', 'DEBUG'),
        'pretty_print': os.getenv('LOG_PRETTY_PRINT', False)
    }
}


def configure_logging():
    try:
        program_logging_config = get_config('logging')
        python_logging_config = program_logging_config['logging_conf']
        python_logging_level = program_logging_config['logging_level']

        # Configure logging config
        if python_logging_config is not None:
            logging.config.fileConfig(python_logging_config, disable_existing_loggers=False)

        # Configure logging level
        if python_logging_level:
            logging.basicConfig(level=python_logging_level)
    except:
        traceback.print_exc()
        pass


def get_config(*args):
    current_config = config

    for idx in args:
        current_config = config[idx]

    return current_config
