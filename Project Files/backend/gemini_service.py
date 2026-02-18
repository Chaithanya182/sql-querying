"""
Gemini AI service for natural language to SQL translation.
"""

import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=GEMINI_API_KEY)


def is_configured() -> bool:
    """Check if Gemini API is properly configured."""
    return bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here")


def extract_sql(response_text: str) -> str:
    """Extract SQL query from Gemini response text."""
    # Try to find SQL in code blocks first
    code_block = re.search(r"```(?:sql)?\s*\n?(.*?)```", response_text, re.DOTALL | re.IGNORECASE)
    if code_block:
        return code_block.group(1).strip()

    # Look for lines that look like SQL
    lines = response_text.strip().split("\n")
    sql_lines = []
    capture = False
    for line in lines:
        stripped = line.strip()
        if any(stripped.upper().startswith(kw) for kw in ["SELECT", "WITH", "EXPLAIN"]):
            capture = True
        if capture:
            sql_lines.append(stripped)
            if stripped.endswith(";"):
                break

    if sql_lines:
        return "\n".join(sql_lines).rstrip(";")

    # Fallback: return the whole response (cleaned)
    return response_text.strip().rstrip(";")


async def generate_sql(natural_language: str, schema_text: str) -> dict:
    """
    Use Gemini to convert natural language question to SQL query.

    Returns:
        dict with keys: sql, explanation, success, error
    """
    if not is_configured():
        return {
            "sql": "",
            "explanation": "",
            "success": False,
            "error": "Gemini API key is not configured. Please add your key to the .env file.",
        }

    prompt = f"""You are an expert SQL query generator. Given the following SQLite database schema and a natural language question, generate the appropriate SQL query.

DATABASE SCHEMA:
{schema_text}

RULES:
1. Generate ONLY valid SQLite SELECT queries. Never generate INSERT, UPDATE, DELETE, DROP, or any write operations.
2. Use proper JOINs when querying across related tables.
3. Use aliases for readability.
4. Limit results to 100 rows unless the user specifies otherwise.
5. Use aggregate functions (COUNT, SUM, AVG, etc.) when the question implies summarization.
6. Return the SQL query inside a ```sql code block.
7. After the SQL block, provide a brief one-line explanation of what the query does.

USER QUESTION: {natural_language}

Generate the SQL query:"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        response_text = response.text

        sql = extract_sql(response_text)

        # Extract explanation (text after the code block)
        explanation = ""
        parts = response_text.split("```")
        if len(parts) >= 3:
            explanation = parts[-1].strip()
            # Clean up the explanation
            explanation = re.sub(r"^\*\*.*?\*\*\s*", "", explanation)
            explanation = explanation.strip()
            if not explanation:
                explanation = "Query generated successfully."
        else:
            explanation = "Query generated successfully."

        return {
            "sql": sql,
            "explanation": explanation,
            "success": True,
            "error": None,
        }

    except Exception as e:
        return {
            "sql": "",
            "explanation": "",
            "success": False,
            "error": f"Gemini API error: {str(e)}",
        }
