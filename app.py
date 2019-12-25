from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from apis.Log.routes import api as log_api
from config import config


app = Flask(__name__)
app.config.from_object(config)


if app.config['STORAGE_TYPE'] != 'file_storage':
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)
else:
    pass


def initialize_app(flask_app):
    api = Api(title='Any Title', version='1.0', description='A description')
    api.add_namespace(log_api)
    api.init_app(flask_app)


def main():
    initialize_app(app)
    import logging
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format=logFormatStr, filename="global.log", level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr, '%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("summary.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")
    app.run(debug=True)


if __name__ == "__main__":
    main()
