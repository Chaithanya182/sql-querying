"""
Smart Bridge — Intelligent SQL Querying
FastAPI Backend Server
"""

import os
import json
import shutil
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_schema, get_schema_text, execute_query, set_db_path, get_db_path, DB_DIR
from gemini_service import generate_sql, is_configured

app = FastAPI(
    title="Smart Bridge SQL API",
    description="Intelligent natural language to SQL querying",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory query history
query_history: list[dict] = []


# ── Models ──────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str
    execute: bool = True  # whether to also execute the generated SQL


class DirectSQLRequest(BaseModel):
    sql: str


# ── Endpoints ───────────────────────────────────────────

@app.get("/")
def root():
    return {
        "app": "Smart Bridge — Intelligent SQL Querying",
        "status": "running",
        "gemini_configured": is_configured(),
    }


@app.get("/api/schema")
def api_get_schema():
    """Return the database schema (tables, columns, types, foreign keys)."""
    try:
        schema = get_schema()
        return {"success": True, "schema": schema, "db_path": os.path.basename(get_db_path())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query")
async def api_query(req: QueryRequest):
    """
    Accept a natural language question, generate SQL via Gemini, and optionally execute it.
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Step 1: Generate SQL
    schema_text = get_schema_text()
    result = await generate_sql(req.question, schema_text)

    if not result["success"]:
        return {
            "success": False,
            "error": result["error"],
            "question": req.question,
            "sql": "",
            "explanation": "",
            "results": None,
        }

    sql = result["sql"]
    explanation = result["explanation"]

    # Step 2: Execute if requested
    exec_result = None
    if req.execute and sql:
        exec_result = execute_query(sql)

    # Step 3: Save to history
    history_entry = {
        "id": len(query_history) + 1,
        "question": req.question,
        "sql": sql,
        "explanation": explanation,
        "success": exec_result["success"] if exec_result else True,
        "row_count": exec_result["row_count"] if exec_result else 0,
        "timestamp": datetime.now().isoformat(),
    }
    query_history.insert(0, history_entry)

    return {
        "success": True,
        "question": req.question,
        "sql": sql,
        "explanation": explanation,
        "results": exec_result,
    }


@app.post("/api/execute")
def api_execute_sql(req: DirectSQLRequest):
    """Execute a SQL query directly (for editing/re-running)."""
    if not req.sql.strip():
        raise HTTPException(status_code=400, detail="SQL query cannot be empty.")

    result = execute_query(req.sql)
    return result


@app.get("/api/history")
def api_get_history():
    """Return query history."""
    return {"success": True, "history": query_history}


@app.delete("/api/history")
def api_clear_history():
    """Clear query history."""
    query_history.clear()
    return {"success": True, "message": "History cleared."}


@app.post("/api/upload-db")
async def api_upload_db(file: UploadFile = File(...)):
    """Upload a custom SQLite database file."""
    if not file.filename.endswith((".db", ".sqlite", ".sqlite3")):
        raise HTTPException(status_code=400, detail="Only .db, .sqlite, .sqlite3 files are accepted.")

    os.makedirs(DB_DIR, exist_ok=True)
    dest_path = os.path.join(DB_DIR, file.filename)

    try:
        with open(dest_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate it's a real SQLite file
        try:
            test_schema = get_schema(dest_path)
            if not test_schema:
                os.remove(dest_path)
                raise HTTPException(status_code=400, detail="Database file contains no tables.")
        except Exception as e:
            if os.path.exists(dest_path):
                os.remove(dest_path)
            raise HTTPException(status_code=400, detail=f"Invalid SQLite file: {str(e)}")

        set_db_path(dest_path)
        query_history.clear()

        return {
            "success": True,
            "message": f"Database '{file.filename}' loaded successfully.",
            "schema": test_schema,
            "db_name": file.filename,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
def api_status():
    """Health check and configuration status."""
    return {
        "status": "healthy",
        "gemini_configured": is_configured(),
        "current_db": os.path.basename(get_db_path()),
        "history_count": len(query_history),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
