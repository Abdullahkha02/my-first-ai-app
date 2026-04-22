import os
from typing import List
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from .models import Task
from anthropic import Anthropic

api = NinjaAPI()

# This is what the USER sends (Simple)
# What the USER sends (Notice: No ID here!)
class TaskIn(Schema):
    title: str
    description: str

# What the API sends BACK to the user
class TaskOut(Schema):
    id: int
    title: str
    description: str
    is_ai_generated: bool

# --- ENDPOINTS ---

# 1. List all tasks
@api.get("/tasks", response=List[TaskOut])
def list_tasks(request):
    return Task.objects.all()

# 2. Create a new task
@api.post("/tasks", response=TaskOut)
def create_task(request, data: TaskIn):
    task = Task.objects.create(**data.dict())
    return task

# 3. Optimize a task using AI
@api.get("/tasks/{task_id}/optimize", response=List[str])
def optimize_task(request, task_id: int):
    # This prevents the "DoesNotExist" error by returning a 404 if the ID is wrong
    task = get_object_or_404(Task, id=task_id)

    # Initialize the client inside the function
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Call Claude
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[
            {"role": "user", "content": f"Provide a simple 5-step checklist for: {task.title}"}
        ]
    )

    # Convert the AI's text block into a clean Python list
    ai_text = message.content[0].text
    return [line.strip("- 123456789. ") for line in ai_text.strip().split("\n") if line.strip()]