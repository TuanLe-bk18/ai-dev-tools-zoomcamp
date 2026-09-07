# Project Backlog: ChoreWheel

Based on `_docs/plan.md`, here is the ordered backlog for building the ChoreWheel Django application:

## Task 1: Define core data models (Member, Chore, Assignment) and run migrations
- Create `Member` model (name, email, is_active).
- Create `Chore` model (title, description, frequency_days, effort_points).
- Create `Assignment` model (chore, member, due_date, is_completed, completed_at).
- Generate and run Django migrations.

## Task 2: Implement weekly rotation algorithm
- Implement rotation service helper to assign chores to active household members in round-robin order for a target week.
- Prevent duplicate assignments for the same period.

## Task 3: Build web UI for chore board and check-in
- Create view and template to display current week's chores grouped by assigned member.
- Add toggle action/view to check off completed chores with timestamps.

## Task 4: Automated tests
- Unit tests for models validation.
- Unit tests for round-robin assignment rotation logic.
- Integration tests for chore listing and check-in views.
