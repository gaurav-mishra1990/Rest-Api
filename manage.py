from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import config

from app import app, db
from models import *


app.config.from_object(config)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    # print(app.config)
    manager.run()