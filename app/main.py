# Import FastAPI and dependencies
from fastapi import FastAPI, HTTPException, Depends
from models import Task, Base, engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from task_logic import *

# Initialize the FastAPI app
app = FastAPI(title="StoteWise Backend Assignment",
    description="Good luck with the assignment! :)",
    version="1.0.0",
    contact={
        "name": "Achal Agarwal",
        "email": "achalagarwal.01@gmail.com ",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    })



# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Basic Endpoints

# 1. Retrieve all tasks
@app.get("/tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    if tasks is None:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

# 2. Create a new task


# Define a Pydantic model for task creation
class TaskCreate(BaseModel):
    name: str
    description: str = None
    due_date: str  # Expecting a string in ISO 8601 format
    priority: int = 1
    status: str = "pending"
    parent_id: int = None
    duration: int = 0

@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Convert due_date from string to datetime object
    due_date = datetime.fromisoformat(task.due_date)
    
    db_task = Task(
        name=task.name,
        description=task.description,
        due_date=due_date,
        priority=task.priority,
        status=task.status,
        parent_id=task.parent_id,
        duration=task.duration,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# 3. Delete a task by its task_id
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}


# Level 1 


# Question 2
@app.get("/tasks/question2")
def question2_route(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question2(tasks)

# Question 3
@app.get("/tasks/question3")
def question3_route(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question3(tasks)

# Question 4
@app.get("/tasks/question4")
def question4_route(db: Session = Depends(get_db)):

    parents_without_children = []
    
    # Note: We accept any means to solve this question 4
    # But we want you to ideally use only SQL query to solve this question
    # Hint: Use a join  

    return []

# Question 5
@app.get("/tasks/question5/{task_id}")
def question5_route(task_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question5(tasks, task_id)



# Level 2

# Question 6
@app.get("/tasks/question6/{query}")
def question6_route(query: str, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question6(tasks, query)

# Question 7
@app.get("/tasks/question7")
def question7_route(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question7(tasks)

# Question 8
@app.get("/tasks/question8/")
def question8_route(criteria: dict, sort_by: str, db: Session = Depends(get_db)):
    
    # Note: Only use a SQL query to solve this question
    return None

# Question 9
@app.post("/tasks/question9/{worker_threads}")
def question9_route(worker_threads: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question9(tasks, worker_threads)


# Default route
@app.get("/")
def default_route():
    return {"message": "Welcome to the Storewise Backend Assignment!", "documentation": "Visit localhost:8000/docs"}
