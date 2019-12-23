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
    app.run(debug=True)


if __name__ == "__main__":
    main()