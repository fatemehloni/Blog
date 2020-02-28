from sqlalchemy import  Integer, String,Column
from app import db
from werkzeug.security import generate_password_hash



class User(db.Model):
    __tablename__='users'
    id = Column(Integer(), primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False, unique=False)
    role = Column(Integer(), nullable=False, default=0)
    fullname = Column(String(128), nullable=True, unique=False)

    def set_password(self,password):
        self.password=generate_password_hash(password)
