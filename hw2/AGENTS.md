# Agent Guidelines for hw2 (SeatFlow)

Instructions for AI coding agents working on this module.

## Workflow Rules
1. **Spec First:** Refer to `_docs/specs.md` before making architectural or schema changes.
2. **Contract-Driven:** Keep `openapi.yaml` consistent with backend endpoints and frontend client models.
3. **Clean Code:** Write minimal, maintainable, readable code without unnecessary boilerplate or dead dependencies.
4. **Testing First:** Backend changes must have matching pytest tests. Run `uv run pytest` to ensure passes before committing.
5. **Atomic Commits:** Make descriptive, bounded commits for each milestone.
