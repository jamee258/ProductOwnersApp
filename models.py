from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

product_owners = db.Table('product_owners', db.Column('product_owner_id', db.Integer, db.ForeignKey('user.id')), db.Column('application_id', db.Integer, db.ForeignKey('application.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Integer, nullable=False)
    # applications = db.relationship('Application', secondary=product_owners, backref='app_contacts')

    def __repr__(self):
        return f'{self.first_name}'

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(100))
    users = db.relationship('User', secondary=product_owners, backref='app_owners')

    def __repr__(self):
        return f'{self.name}'