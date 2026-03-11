from fastapi import FastAPI
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str | None = None



app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}



@app.get("/tasks")
def get_tasks():
    return tasks

tasks = []
counter = 1

@app.post("/tasks")
def create_task(task: Task):
    global counter

    new_task = {
        "id": counter,
        "title": task.title,
        "description": task.description
    }

    tasks.append(new_task)
    counter += 1
    return new_task


@app.post("/tasks")
def create_task(task: dict):
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}")
@app.put("/tasks/{task_id}")
@app.delete("/tasks/{task_id}")