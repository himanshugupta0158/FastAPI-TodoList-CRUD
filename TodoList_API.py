from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uuid
from sqllite_database import SQLiteDatabase


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()))  # Store UUID as string
    name: str
    description: str | None = None
    is_completed: bool = False
    date_created: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat())  # Store as ISO string

class UpdateTaskFields(BaseModel):
    description: str | None = None
    is_completed: bool = False

table_name = "tasks"


def initiate_db():
    db = SQLiteDatabase("todo_list.db")
    # Define table schema as a dictionary
    task_schema = {
        "id": "TEXT PRIMARY KEY",  # Use TEXT for UUID
        "name": "TEXT NOT NULL",
        "description": "TEXT",
        "is_completed": "BOOLEAN",
        "date_created": "TEXT NOT NULL"  # Store date as text
    }

    # Create table using the schema dictionary
    db.create_table_from_schema(table_name, task_schema)
    return db


db = initiate_db()
app = FastAPI()


@app.get("/")
async def get_all_tasks():
    return db.select(f"select * from {table_name}")


@app.post("/add/")
async def add_task(task: Task):
    # Convert Task model data to a dictionary with correct types
    task_data = task.model_dump()
    task_data["id"] = str(task.id)  # Ensure UUID is stored as a string
    task_data["date_created"] = task.date_created  # Store as ISO-formatted string
    db.insert(table_name, task_data)
    return db.select(f"SELECT * FROM {table_name} WHERE id='{task_data['id']}'")


@app.put("/update_task/{task_id}")
async def update_task(task_id: str, task: UpdateTaskFields):
    task_data = task.model_dump()
    db.update(table_name, task_data, f"id = '{task_id}'")
    return db.select(f"SELECT * FROM {table_name} WHERE id='{task_id}'")


@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: str):
    db.delete(table_name, f"id = '{task_id}'")
    return {"message": f"{task_id} successfully deleted!"}


@app.on_event("shutdown")
def shutdown_event():
    db.close_connection()
