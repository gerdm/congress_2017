import os
from app import create_app, db
from app.models import User, Grade, Beverage, Workshop, Round_Table, Staff, Passcode
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv("FLASK_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Grade=Grade, Staff=Staff, Passcode=Passcode,
                Beverage=Beverage, Workshop=Workshop, Round_Table=Round_Table)
                
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
