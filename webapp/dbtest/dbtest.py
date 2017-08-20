from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user  = db.Column(db.String(80), unique=False)
    requires_inscription = db.Column(db.Boolean, unique=False)

    def __repr__(self):
        return "<User {}>".format(self.user)

if __name__ =="__main__":
    pass
