from fastapi import FastAPI
from pydantic import BaseModel

class Task(BaseModel):
    counter: int
    title: str
    description: str | None = None
app = FastAPI()





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


@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_tasks_by_ID(task_id:int):
    for t in  tasks:
        if t["id"] == task_id:
            return t
    
@app.put("/tasks/{task_id}")
def put_tasks_by_ID(task_id: int, task: Task):
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = task.title
            t["description"] = task.description
            return t



@app.delete("/tasks/{task_id}")
def delete_tasks_by_ID(task_id: int):
    for i, t in enumerate(tasks):
        if  t["id"] == task_id:
            del tasks(i)
            return {"message": "Task deleted"}