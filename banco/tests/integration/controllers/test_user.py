from http import HTTPStatus
from src.app import db, User, Role

def test_get_user_success(client):
    #GIVEN
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="Digjoe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()
    
    #WHEN
    response = client.get(f"/users/{user.id}")

    #THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username
    }


def test_get_user_not_found(client):
     #GIVEN
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user_id = 1
    
    #WHEN
    response = client.get(f"/users/{user_id}")

    #THEN
    assert response.status_code == HTTPStatus.NOT_FOUND
