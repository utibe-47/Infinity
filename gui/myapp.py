from os.path import dirname, abspath
import sys
# from flask_script import Manager
from flask_migrate import Migrate

sys.path.append(dirname(dirname(abspath(__file__))))

from gui.user_interface.models import TaskMessage, User
from gui.user_interface import db
from gui.app import app


# app = apply_monkey_patch(app)
# manager = Manager(app)

migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(debug=True)
