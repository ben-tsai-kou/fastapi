from tests.utils import *
from src.admin.router import get_db
from src.auth.router import get_current_user
from fastapi import status
from src.todo import models as todo_models

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "id": 1,
            "priority": 5,
            "complete": False,
            "owner_id": 1,
        }
    ]


def test_admin_delete_todo(test_todo, db):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    model = db.query(todo_models.Todos).filter(todo_models.Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}
