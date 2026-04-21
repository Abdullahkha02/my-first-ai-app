from ninja import NinjaAPI, Schema
from .models import Task
from typing import List

api = NinjaAPI()


# This is a 'Schema' - it ensures the data is perfect
class TaskSchema(Schema):
    id: int
    title: str
    description: str
    is_ai_generated: bool


@api.get("/tasks", response=List[TaskSchema])
def list_tasks(request):
    return Task.objects.all()


@api.post("/tasks")
def create_task(request, data: TaskSchema):
    # In a real 2026 app, we'd trigger an AI call here!
    task = Task.objects.create(**data.dict())
    return {"id": task.id}


@api.get("/tasks/{task_id}/optimize")
def optimize_task(request, task_id: int):
    task = Task.objects.get(id=task_id)
    suggestions = suggest_subtasks(task.title)
    task.description = suggestions
    task.is_ai_generated = True
    task.save()
    return {"status": "optimized", "new_description": suggestions}
