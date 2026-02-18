"""
Database management module for Smart Bridge SQL Querying.
Handles SQLite connections, schema introspection, and query execution.
"""

import sqlite3
import os
from typing import Any

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DEFAULT_DB = os.path.join(DB_DIR, "sample.db")
CURRENT_DB_PATH = DEFAULT_DB
MAX_ROWS = 500


def get_db_path() -> str:
    """Return the current active database path."""
    global CURRENT_DB_PATH
    return CURRENT_DB_PATH


def set_db_path(path: str):
    """Set the active database path."""
    global CURRENT_DB_PATH
    CURRENT_DB_PATH = path


def get_connection(db_path: str = None) -> sqlite3.Connection:
    """Create a new SQLite connection with row factory."""
    path = db_path or get_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def get_schema(db_path: str = None) -> list[dict]:
    """
    Introspect the database and return schema info.
    Returns a list of tables with their columns, types, and primary keys.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

    schema = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info('{table}')")
        columns = []
        for col in cursor.fetchall():
            columns.append({
                "name": col[1],
                "type": col[2],
                "nullable": not col[3],
                "primary_key": bool(col[5]),
            })

        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM '{table}'")
        row_count = cursor.fetchone()[0]

        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list('{table}')")
        foreign_keys = []
        for fk in cursor.fetchall():
            foreign_keys.append({
                "from_column": fk[3],
                "to_table": fk[2],
                "to_column": fk[4],
            })

        schema.append({
            "table_name": table,
            "columns": columns,
            "row_count": row_count,
            "foreign_keys": foreign_keys,
        })

    conn.close()
    return schema


def get_schema_text(db_path: str = None) -> str:
    """
    Return schema as formatted text for LLM prompt context.
    """
    schema = get_schema(db_path)
    lines = []
    for table in schema:
        cols = ", ".join(
            [f"{c['name']} {c['type']}{'  PRIMARY KEY' if c['primary_key'] else ''}" for c in table["columns"]]
        )
        lines.append(f"CREATE TABLE {table['table_name']} ({cols});")
        if table["foreign_keys"]:
            for fk in table["foreign_keys"]:
                lines.append(
                    f"  -- FK: {table['table_name']}.{fk['from_column']} -> {fk['to_table']}.{fk['to_column']}"
                )
        lines.append(f"  -- {table['row_count']} rows")
        lines.append("")
    return "\n".join(lines)


def execute_query(sql: str, db_path: str = None) -> dict[str, Any]:
    """
    Safely execute a SQL query and return results.
    Only SELECT statements are allowed for safety.
    """
    sql_stripped = sql.strip().rstrip(";").strip()

    # Basic safety check — only allow SELECT and certain read-only statements
    first_word = sql_stripped.split()[0].upper() if sql_stripped else ""
    if first_word not in ("SELECT", "WITH", "EXPLAIN"):
        return {
            "success": False,
            "error": "Only SELECT queries are allowed for safety. Write operations are disabled.",
            "columns": [],
            "rows": [],
            "row_count": 0,
        }

    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(sql_stripped)
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = [dict(row) for row in cursor.fetchmany(MAX_ROWS)]
        total = len(rows)

        return {
            "success": True,
            "columns": columns,
            "rows": rows,
            "row_count": total,
            "truncated": total >= MAX_ROWS,
        }
    except sqlite3.Error as e:
        return {
            "success": False,
            "error": str(e),
            "columns": [],
            "rows": [],
            "row_count": 0,
        }
    finally:
        conn.close()
