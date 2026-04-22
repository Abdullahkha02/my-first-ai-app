import os
from typing import List
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from .models import Task
from anthropic import Anthropic

api = NinjaAPI()

# --- SCHEMAS ---

# This defines what you see in the POST "Request Body"
# We only want the user to provide these two fields.
class TaskIn(Schema):
    title: str
    description: str

# This defines what the API sends back to you
class TaskOut(Schema):
    id: int
    title: str
    description: str
    is_ai_generated: bool

# --- ENDPOINTS ---

@api.post("/tasks", response=TaskOut)
def create_task(request, data: TaskIn):
    """
    Step 1: Create a task. 
    The 'id' and 'is_ai_generated' are handled by the database automatically.
    """
    # **data.dict() unpacks title and description into the Task model
    task = Task.objects.create(**data.dict())
    return task

@api.get("/tasks/{task_id}/optimize", response=List[str])
def optimize_task(request, task_id: int):
    """
    Step 2: Take the ID from Step 1 and generate AI sub-tasks.
    """
    # 1. Fetch the task from the DB (or 404 if ID is wrong)
    task = get_object_or_404(Task, id=task_id)

    # 2. Get API Key from Railway Environment Variables
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return ["Error: ANTHROPIC_API_KEY not found in Railway Variables."]

    # 3. Initialize Claude
    client = Anthropic(api_key=api_key)

    # 4. Ask Claude for the checklist
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[
            {"role": "user", "content": f"Provide a simple 5-step checklist for: {task.title}"}
        ]
    )

    # 5. Parse the response into a clean list
    ai_text = message.content[0].text
    lines = ai_text.strip().split("\n")
    
    # Clean up bullets, numbers, and empty lines
    return [line.strip("- 123456789. ") for line in lines if line.strip()]