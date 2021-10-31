import logging
import logging.config
import os

config = {
    'logging': {
        'logging_conf': os.getenv('LOGGING_CONF', None),
        'logging_level': os.getenv('LOGGING_LEVEL', 'DEBUG'),
        'pretty_print': os.getenv('LOG_PRETTY_PRINT', False)
    }
}

def configure_logging():
    program_logging_config = get_config('logging')
    python_logging_config = program_logging_config['logging_conf']
    python_logging_level = program_logging_config['logging_level']

    # Configure logging config
    if python_logging_config is not None:
        logging.config.fileConfig(python_logging_config, disable_existing_loggers=False)
    else:
        formatter = logging.Formatter('%(asctime)-15s %(name)-25s %(funcName)-20s %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        for logger_name in ['sbbbattlesim.characters', 'sbbbattlesim.heros', 'sbbbattlesim.treasures',
                            'sbbbattlesim.combat', 'sbbbattlesim.events', 'sbbbattlesim.player']:
            logger = logging.getLogger(logger_name)
            logger.addHandler(stream_handler)

    # Configure logging level
    if python_logging_level:
        logging.basicConfig(level=python_logging_level)

def get_config(*args):
    current_config = config

    for idx in args:
        current_config = config[idx]

    return current_config
