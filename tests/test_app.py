import pytest
import os
import json
from app import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["DB_PATH"] = "test_tasks.db"
    init_db()
    with app.test_client() as client:
        yield client
    if os.path.exists("test_tasks.db"):
        os.remove("test_tasks.db")

# Test 1: Verificar el Endpoint Index
def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"To-Do API" in res.data

# Test 2: Crear una tarea exitosamente
def test_create_task(client):
    res = client.post('/tasks', json={"title": "Test Task", "description": "DevOps"})
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data["title"] == "Test Task"

# Test 3: Intentar crear una tarea sin título (Error 400)
def test_create_task_invalid(client):
    res = client.post('/tasks', json={"description": "No title"})
    assert res.status_code == 400

# Test 4: Obtener el Healthcheck de la app
def test_healthcheck(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["status"] == "UP"

# Test 5: Intentar buscar una tarea inexistente (Error 404)
def test_get_task_not_found(client):
    res = client.get('/tasks/999')
    assert res.status_code == 404