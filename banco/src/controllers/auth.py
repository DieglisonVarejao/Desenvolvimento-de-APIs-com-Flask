from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from src.app import User, db


app = Blueprint('auth', __name__, url_prefix='/auth')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Aqui você deve validar o usuário e a senha (exemplo simplificado)
    if username != 'test' or password != 'test':
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED 
    
    # Cria o token de acesso
    access_token = create_access_token(identity=username)
    return {"access_token": access_token}, HTTPStatus.OK