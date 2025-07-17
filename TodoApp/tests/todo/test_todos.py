from src.todo.router import get_db
from src.auth.router import get_current_user
from fastapi import status
from src.todo import models as todo_models
from tests.utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "complete": False,
            "description": "Need to learn everyday!",
            "id": 1,
            "owner_id": 1,
            "priority": 5,
            "title": "Learn to code!",
        }
    ]


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "complete": False,
        "description": "Need to learn everyday!",
        "id": 1,
        "owner_id": 1,
        "priority": 5,
        "title": "Learn to code!",
    }


def test_read_one_authenticated_not_fount():
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo, db):
    request_data = {
        "title": "New Todo!",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }
    response = client.post("/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    model = db.query(todo_models.Todos).order_by(todo_models.Todos.id.desc()).first()
    # model = db.query(todo_models.Todos).filter(todo_models.Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo, db):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    model = db.query(todo_models.Todos).filter(todo_models.Todos.id == 1).first()
    assert model.title == "Change the title of the todo already saved!"


def test_update_todo_not_found(test_todo, db):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "todo not found."}


def test_delete_todo(test_todo, db):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    model = db.query(todo_models.Todos).filter(todo_models.Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "todo not found"}
