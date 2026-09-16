import pytest
from fastapi.testclient import TestClient
from app.main import app, students_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    students_db.clear()
    yield
    students_db.clear()

# --- Successful Operations ---
def test_create_student_success():
    payload = {"id": 1, "name": "Abir", "department": "CSE", "semester": "7th", "cgpa": 3.75}
    res = client.post("/students", json=payload)
    assert res.status_code == 201
    assert res.json()["name"] == "Abir"

def test_get_all_students_success():
    payload = {"id": 1, "name": "Abir", "department": "CSE", "semester": "7th", "cgpa": 3.75}
    client.post("/students", json=payload)
    res = client.get("/students")
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_get_single_student_success():
    payload = {"id": 2, "name": "Nafis", "department": "EEE", "semester": "5th", "cgpa": 3.60}
    client.post("/students", json=payload)
    res = client.get("/students/2")
    assert res.status_code == 200
    assert res.json()["id"] == 2

def test_update_student_success():
    payload = {"id": 3, "name": "Old Name", "department": "BBA", "semester": "1st", "cgpa": 3.00}
    client.post("/students", json=payload)
    updated = {"id": 3, "name": "New Name", "department": "BBA", "semester": "2nd", "cgpa": 3.50}
    res = client.put("/students/3", json=updated)
    assert res.status_code == 200
    assert res.json()["name"] == "New Name"

def test_delete_student_success():
    payload = {"id": 4, "name": "Temp", "department": "ME", "semester": "3rd", "cgpa": 3.20}
    client.post("/students", json=payload)
    res = client.delete("/students/4")
    assert res.status_code == 204

# --- Invalid Scenarios (Required >= 2) ---
def test_create_student_duplicate_id_invalid():
    payload = {"id": 1, "name": "Abir", "department": "CSE", "semester": "7th", "cgpa": 3.75}
    client.post("/students", json=payload)
    res = client.post("/students", json=payload)
    assert res.status_code == 400
    assert res.json()["detail"] == "Student ID already exists"

def test_get_student_not_found_invalid():
    res = client.get("/students/999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Student not found"