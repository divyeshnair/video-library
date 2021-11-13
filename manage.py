from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from extensions import session
from web_app import app

manager = Manager(app)
migrate = Migrate(app, session)

manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()