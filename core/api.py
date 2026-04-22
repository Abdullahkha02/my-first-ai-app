import os
from typing import List
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from .models import Task
from anthropic import Anthropic

api = NinjaAPI()

# --- SCHEMAS ---
class TaskIn(Schema):
    title: str
    description: str

class TaskOut(Schema):
    id: int
    title: str
    description: str
    is_ai_generated: bool

# --- ENDPOINTS ---

@api.post("/tasks", response=TaskOut)
def create_task(request, data: TaskIn):
    # This creates the task and returns the whole object
    task = Task.objects.create(
        title=data.title, 
        description=data.description,
        is_ai_generated=False
    )
    return task

@api.get("/tasks/{task_id}/optimize", response=List[str])
def optimize_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return ["Error: Missing Anthropic API Key in Railway."]

    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": f"5 steps for: {task.title}"}]
    )

    ai_text = message.content[0].text
    return [t.strip("- 123456789. ") for t in ai_text.strip().split("\n") if t.strip()]