from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory data
students = [{"id": 1, "name": "John", "age": 20}]
next_id = 2

class Student(BaseModel):
    name: str
    age: int

@app.get("/", response_class=HTMLResponse)
def homepage():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>🎓 Student API Interface</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 30px; background: #f4f4f4; }
            h1 { color: #2c3e50; }
            section { margin-bottom: 20px; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.05); }
            input, button, textarea { padding: 6px; margin-top: 5px; width: 100%; }
            code { background: #eef; padding: 3px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🎓 Student API Testing Interface</h1>
        <p><strong>Base URL:</strong> <code>/students</code></p>

        <section>
            <h3>📥 GET /students</h3>
            <button onclick="fetchStudents()">Fetch Students</button>
            <pre id="studentList"></pre>
        </section>

        <section>
            <h3>➕ POST /students</h3>
            <textarea id="newStudent" rows="2">{ "name": "Alice", "age": 23 }</textarea>
            <button onclick="createStudent()">Create Student</button>
            <pre id="createResult"></pre>
        </section>

        <section>
            <h3>✏️ PUT /students/&lt;id&gt;</h3>
            <input id="updateId" placeholder="Student ID" />
            <textarea id="updateStudent" rows="2">{ "name": "Bob", "age": 24 }</textarea>
            <button onclick="updateStudent()">Update Student</button>
            <pre id="updateResult"></pre>
        </section>

        <section>
            <h3>🗑️ DELETE /students/&lt;id&gt;</h3>
            <input id="deleteId" placeholder="Student ID" />
            <button onclick="deleteStudent()">Delete Student</button>
            <pre id="deleteResult"></pre>
        </section>

        <section>
            <h3>🔍 GET /students/&lt;id&gt;</h3>
            <input id="searchId" placeholder="Student ID" />
            <button onclick="getStudent()">Get Student</button>
            <pre id="searchResult"></pre>
        </section>

        <script>
            const base = "/students";

            async function fetchStudents() {
                const res = await fetch(base);
                const data = await res.json();
                document.getElementById("studentList").textContent = JSON.stringify(data, null, 2);
            }

            async function createStudent() {
                const body = document.getElementById("newStudent").value;
                const res = await fetch(base, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: body
                });
                const data = await res.json();
                document.getElementById("createResult").textContent = JSON.stringify(data, null, 2);
            }

            async function updateStudent() {
                const id = document.getElementById("updateId").value;
                const body = document.getElementById("updateStudent").value;
                const res = await fetch(`${base}/${id}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: body
                });
                const data = await res.json();
                document.getElementById("updateResult").textContent = JSON.stringify(data, null, 2);
            }

            async function deleteStudent() {
                const id = document.getElementById("deleteId").value;
                const res = await fetch(`${base}/${id}`, { method: "DELETE" });
                const data = await res.json();
                document.getElementById("deleteResult").textContent = JSON.stringify(data, null, 2);
            }

            async function getStudent() {
                const id = document.getElementById("searchId").value;
                const res = await fetch(`${base}/${id}`);
                const data = await res.json();
                document.getElementById("searchResult").textContent = JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/students")
def get_students():
    return students

@app.post("/students")
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
