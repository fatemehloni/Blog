from . import admin
from flask import session
@admin.route('/')
def index():
    return "hello from admin index"

@admin.route('/login/')
def login():
    session['name']='fafa'
    print(session)
    return "1"
