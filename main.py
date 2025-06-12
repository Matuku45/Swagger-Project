from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy data
students = [{"id": 1, "name": "John", "age": 20}]
next_id = 2

class Student(BaseModel):
    name: str
    age: int

@app.get("/students", response_model=List[dict])
def get_students():
    return students

@app.post("/students", status_code=201)
def add_student(student: Student):
    global next_id
    new_student = {"id": next_id, "name": student.name, "age": student.age}
    students.append(new_student)
    next_id += 1
    return new_student

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    for s in students:
        if s["id"] == student_id:
            s["name"] = student.name
            s["age"] = student.age
            return s
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    global students
    students = [s for s in students if s["id"] != student_id]
    return {"message": f"Student {student_id} deleted"}
