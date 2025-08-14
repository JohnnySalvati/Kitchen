import os
from pathlib import Path
import pytest
from db.db_initializer import createDatabase
from models.action_model import Recipe

@pytest.fixture(scope="module")
def setup_db():
    db_path = "test_kitchen.db"
    createDatabase()
    yield
    if os.path.exists(db_path):
        os.remove(db_path)

        