import logging
import os
from flask import Flask
from imsbackend import config
from flask_cors import CORS
from logging.handlers import RotatingFileHandler

program_name = "[ims]: "
module_name = "__init__.py: "


def create_app(test_config=None):
    function_name = "create_app(): "
    print(f"{program_name} {module_name} {function_name} DEBUG: Enter")

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from imsbackend.api import branches
    from imsbackend.api import batches
    from imsbackend.api import students
    from imsbackend.api import accounts
    from imsbackend.api import allstores

    app.register_blueprint(branches.bp)
    app.register_blueprint(batches.bp)
    app.register_blueprint(students.bp)
    app.register_blueprint(accounts.bp)
    app.register_blueprint(allstores.bp)

    return app


def create_dir(dirname):
    try:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return True
    except OSError as excp:
        return False


def setup_logging(logger_name, file_name):
    """
    :param logger_name:
    :param file_name:
    :return: logger with logger_name as specified and writes to file
    """
    function_name = "setup_logging(): "
    print(f"{program_name} {module_name} {function_name} DEBUG: "
          f"Setting up logging")

    log_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + \
               '/logs/'

    if not create_dir(log_path):
        print(f"{program_name} {module_name} {function_name} DEBUG: "
              f"Unable to create {log_path}.")

    formatter = logging.Formatter(config.LOG_FORMAT)

    logger = logging.getLogger('flask_cors')
    logger.setLevel(config.LOG_LEVEL)
    handler = RotatingFileHandler(log_path + file_name,
                                  maxBytes=int(config.MAXBYTES),
                                  backupCount=int(config.BACKUPCOUNT))
    handler.setLevel(config.LOG_LEVEL)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


LOGGER = setup_logging('ims-logger', config.LOGNAME)
