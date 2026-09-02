from fastapi import APIRouter
from sqlalchemy import inspect

from app.db.session import engine

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/tables", summary="List database tables (Temporary Debug)")
async def list_tables():
    """Lists all tables and columns currently created in the SQLite database."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    columns_by_table = {
        table: [
            {"name": col["name"], "type": str(col["type"]), "nullable": col.get("nullable", True)}
            for col in inspector.get_columns(table)
        ]
        for table in tables
    }
    return {
        "status": "ok",
        "tables": tables,
        "schema": columns_by_table,
    }
