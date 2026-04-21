import anthropic
from decouple import config


def suggest_subtasks(task_title):
    client = anthropic.Anthropic(api_key=config("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Break this task into 3 actionable steps: {task_title}",
            }
        ],
    )
    return response.content[0].text
