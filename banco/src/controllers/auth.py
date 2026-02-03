from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from src.app import User, db


app = Blueprint("auth", __name__, url_prefix="/auth")

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    # Aqui você deve validar o usuário e a senha (exemplo simplificado)
    if not user or user.password != password:
        return {"messsagem": "Bad username or password"}, HTTPStatus.UNAUTHORIZED 
    # Cria o token de acesso
    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}, HTTPStatus.OK