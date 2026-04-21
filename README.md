# 🚀 Smart Task Architect (Django 5.x + AI)
A professional-grade Django backend demonstrating **Agentic AI** integration, **Ninja API** performance, and **uv** dependency management.

## 🛠 Tech Stack (2026 Standards)
- **Orchestrator:** [uv](https://astral.sh/uv) (Rust-backed dependency management)
- **Framework:** Django 5.x + [Django Ninja](https://django-ninja.rest-framework.com/) (FastAPI-style speed)
- **AI Engine:** Claude 3.5 Sonnet (Agentic task breakdown)
- **Validation:** Pydantic v2
- **Code Quality:** Ruff (Linting & Formatting)

## 🌟 Key Features
- **Semantic Task Optimization:** Uses Claude to automatically break down high-level goals into 3 actionable steps.
- **Auto-Documented API:** Interactive Swagger docs available at `/api/docs`.
- **Type-Safe Data:** Every request is validated via Pydantic schemas before hitting the database.

## ⚡ Quick Start (The 'uv' Way)
```bash
# Clone and enter
git clone <your-repo-url> && cd my_first_app

# Install and Sync in one command
uv sync

# Setup Environment
cp .env.example .env  # Add your ANTHROPIC_API_KEY

# Run
uv run python manage.py migrate
uv run python manage.py runserver