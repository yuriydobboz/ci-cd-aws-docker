from flask import session
from flask_login import LoginManager,login_user,logout_user,login_required,current_user


def login_user(Usuario):
    session["id"]=Usuario.id
    session["username"]=Usuario.username
    session["admin"]=Usuario.admin

def logout_user():
    session.pop("id",None)
    session.pop("username",None)
    session.pop("admin",None)

def is_login():
    if "id" in session:
        return True
    else:
        return False

def is_admin():
    return session.get("admin",False)