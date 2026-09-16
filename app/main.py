from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Student(BaseModel):
    id: int
    name: str
    department: str
    semester: str
    cgpa: float

students_db = {}

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    if student.id in students_db:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    students_db[student.id] = student
    return student

@app.get("/students", response_model=List[Student])
def get_all_students():
    return list(students_db.values())

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    students_db[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    return None