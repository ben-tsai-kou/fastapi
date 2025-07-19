from tests.utils import *
from src.users.router import get_db
from src.auth.router import get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "ben"
    assert response.json()["email"] == "ben@email.com"
    assert response.json()["first_name"] == "Ben"
    assert response.json()["last_name"] == "Tsai"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "(111)-111-1111"
