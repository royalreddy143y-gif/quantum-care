# Alembic Database Migrations

This folder contains the auto-generated database migration revisions.

To generate a new migration after modifying SQLAlchemy models:
```bash
alembic revision --autogenerate -m "Add new field or table"
alembic upgrade head
```
