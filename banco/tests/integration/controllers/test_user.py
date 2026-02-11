from http import HTTPStatus

def test_get_user_sucsses(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK