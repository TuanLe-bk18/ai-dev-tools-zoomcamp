# ChoreWheel: Shared Household Chores Tool

A Django application for managing shared household chores with automated weekly rotation and check-in tracking. Built as part of [DataTalksClub AI Dev Tools Zoomcamp 2026 (Homework 1)](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp).

## Features
1. **Member & Chore Management**: Add household members and define chores.
2. **Weekly Rotation Engine**: Automatically assign tasks in round-robin order.
3. **Completion Check-in**: Mark tasks done and track activity history.

## Setup & Run
```bash
uv venv
uv run python manage.py migrate
uv run python manage.py runserver
```
