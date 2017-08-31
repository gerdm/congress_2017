from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin 
from . import db, login_manager

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False)
    last_name = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=True, index=True)
    school = db.Column(db.String(64), unique=False)
    kit = db.Column(db.Boolean, unique=False)
    grade_id = db.Column(db.Integer, db.ForeignKey("school_grades.id"))
    beverage_id = db.Column(db.Integer, db.ForeignKey("beverages.id"))
    user_type_id= db.Column(db.Integer, db.ForeignKey("user_types.id"))
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"))
    round_table_id = db.Column(db.Integer, db.ForeignKey("round_tables.id"))

    def __repr__(self):
        return ("<User {first} {last}>"
                .format(first=self.first_name, last=self.last_name))


class Grade(db.Model):
    __tablename__ = "school_grades"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="grade", lazy="dynamic")

    def __repr__(self):
        return "<School Grade {grade}>".format(grade=self.name)


class User_Type(db.Model):
    __tablename__ = "user_types"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="user_type", lazy="dynamic")

    def __repr__(self):
        return "<User Type {utype}>".format(utype=self.type)


class Beverage(db.Model):
    __tablename__ = "beverages"
    id = db.Column(db.Integer, primary_key=True)
    beverage = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="beverage", lazy="dynamic")

    def __repr__(self):
        return "<Beverage {beverage}>".format(beverage=self.beverage)


class Workshop(db.Model):
    __tablename__ ="workshops"
    id = db.Column(db.Integer, primary_key=True)
    workshop = db.Column(db.String(64), unique=True)
    grade_allowed = db.Column(db.Integer, db.ForeignKey("school_grades.id"))
    users = db.relationship("User", backref="workshop", lazy="dynamic")

    def __repr__(self):
        return "<Workshop {ws}>".format(ws=self.workshop)


class Round_Table(db.Model):
    __tablename__ = "round_tables"
    id = db.Column(db.Integer, primary_key=True)
    table = db.Column(db.String)
    grade_allowed = db.Column(db.Integer, db.ForeignKey("school_grades.id"))
    users = db.relationship("User", backref="role", lazy="dynamic")
    
    def __repr__(self):
        return "<Round Table {table}>".format(table=self.table)


class Staff(UserMixin, db.Model):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Staff {staff}>".format(staff=self.username)


@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(int(user_id))
