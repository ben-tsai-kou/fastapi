from src.todo import models as todo_models
from tests.utils import engine, text
import pytest


@pytest.fixture
def test_todo(db):
    todo = todo_models.Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
