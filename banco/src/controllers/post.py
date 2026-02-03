from flask import Blueprint, request
from src.app import Post, db
from http import HTTPStatus
from sqlalchemy import inspect


app = Blueprint('post', __name__, url_prefix='/posts')

def _create_post():
    data = request.json
    if not all(key in data for key in ["title", "body", "author_id"]):
        return {"mensagem": "Dados incompletos. Certifique-se de incluir 'title', 'body' e 'author_id'."}, HTTPStatus.BAD_REQUEST

    post = Post(
        title=data["title"],
        body=data["body"],
        author_id=data["author_id"]
    )
    db.session.add(post)
    db.session.commit()
    return {"mensagem": "Post criado com sucesso!"}, HTTPStatus.CREATED


def _list_posts():
    query = db.select(Post)
    posts = db.session.execute((query).order_by(Post.id)).scalars()
    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "author_id": post.author_id,
        }
        for post in posts
    ]


@app.route('/', methods=["GET", "POST"])
def handle_post():
    if request.method == "POST":
        resultado = _create_post()
        return resultado
    else:
        return {"posts": _list_posts()}
    

@app.route("/<int:post_id>")
def get_post(user_id):
    post = db.get_or_404(Post, user_id)
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "author_id": post.author_id,
    }


@app.route("/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    """
    if "username" in data:
        user.username = data["username"]
        db.session.commit()
    """
    # VERSÃO DINÂMICA
    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()
   
    """ 
    attrs = ["username", "first_name", "last_name", "address"]
    for attr in attrs:
        setattr(user, attr, data[attr])
    db.session.commit()
    """
    
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "author_id": post.author_id,
    }


@app.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()

    return "Post was deleted!", HTTPStatus.NO_CONTENT
