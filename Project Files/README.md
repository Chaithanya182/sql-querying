# 🌉 Smart Bridge — Intelligent SQL Querying

> An AI-powered web application that converts **natural language questions** into **valid SQL queries** using Google Gemini AI, making database interaction accessible to everyone.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?logo=google)

---

## 👥 Team Details

| Role | Name |
|------|------|
| **Team Leader** | C Chaithanya Prasad |
| Team Member | K Dinesh |
| Team Member | Karnam Vidhyasree |
| Team Member | Bharath Kumar |
| Team Member | Parlapalli Khandith Kumar Reddy |

**Team ID:** `LTVIP2026TMIDS80425`

---

## ✨ Features

- 🗣️ **Natural Language Querying** — Type questions in plain English, get SQL results
- 🤖 **Google Gemini AI** — Schema-aware SQL generation using Gemini 2.5 Flash
- 📊 **Interactive Schema Viewer** — Browse tables, columns, and data types
- 🛡️ **Read-Only Safety** — Only SELECT queries allowed, no accidental data changes
- 🎨 **Premium Dark Theme** — Modern UI with glassmorphism and smooth animations
- ⚡ **Real-Time Results** — Formatted tables with generated SQL and AI explanations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│              React 18 + Vite                     │
│   (Query Panel · Schema Viewer · Results Table)  │
└──────────────────────┬──────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────┐
│                   Backend                        │
│              FastAPI (Python)                    │
│   (Query Router · Schema Extractor · AI Service) │
└────────┬─────────────────────────┬──────────────┘
         │                         │
    ┌────▼────┐             ┌──────▼──────┐
    │ SQLite  │             │ Google      │
    │ Database│             │ Gemini API  │
    └─────────┘             └─────────────┘
```

---

## 📁 Project Structure

```
Project Files/
├── backend/
│   ├── main.py                 # FastAPI app & API routes
│   ├── gemini_service.py       # Google Gemini AI integration
│   ├── database.py             # SQLite database operations
│   ├── seed_db.py              # Database seeding script
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (API keys)
│   └── data/
│       └── store.db            # SQLite database file
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main application component
│   │   ├── api.js              # API communication layer
│   │   ├── main.jsx            # React entry point
│   │   ├── index.css           # Global styles & dark theme
│   │   └── components/
│   │       ├── QueryPanel.jsx  # NL query input component
│   │       ├── ResultsDisplay.jsx  # Query results table
│   │       └── SchemaViewer.jsx    # Database schema sidebar
│   ├── index.html              # HTML entry point
│   ├── package.json            # Node.js dependencies
│   └── vite.config.js          # Vite configuration
│
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 + Vite | Component-based UI with fast HMR |
| Backend | Python + FastAPI | High-performance async API server |
| AI Engine | Google Gemini 2.5 Flash | NL-to-SQL translation |
| Database | SQLite 3 | Lightweight relational database |
| Styling | CSS3 (Custom) | Dark theme with glassmorphism |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Gemini API Key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Chaithanya182/sql-querying.git
   cd sql-querying
   ```

2. **Backend setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure API Key** — Create a `.env` file in the `backend/` directory:
   ```
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

4. **Seed the database**
   ```bash
   python seed_db.py
   ```

5. **Frontend setup**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

**Terminal 1 — Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser 🚀

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/schema` | Returns database schema (tables, columns, types) |
| `POST` | `/api/query` | Accepts NL query, returns SQL, results & explanation |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/docs` | Auto-generated Swagger API documentation |

### Example Request

```bash
POST /api/query
{
    "query": "Show me the top 5 customers by total spending"
}
```

### Example Response

```json
{
    "sql": "SELECT c.first_name, c.last_name, SUM(o.total_amount) AS total_spending FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id ORDER BY total_spending DESC LIMIT 5",
    "results": {
        "columns": ["first_name", "last_name", "total_spending"],
        "rows": [["John", "Doe", 1500.00]]
    },
    "explanation": "This query joins customers and orders tables to calculate total spending per customer, sorted in descending order, limited to 5."
}
```

---

## 🗄️ Database Schema

The application comes with a sample **e-commerce database** with 4 tables:

| Table | Columns |
|-------|---------|
| `customers` | id, first_name, last_name, email, city, registration_date |
| `products` | id, name, category, price, stock_quantity |
| `orders` | id, customer_id, order_date, status, total_amount |
| `order_items` | id, order_id, product_id, quantity, unit_price |

---

## 🔒 Security

- ✅ **Read-Only Execution** — Only `SELECT` queries; `INSERT`, `UPDATE`, `DELETE`, `DROP` are blocked
- ✅ **API Key Security** — Gemini key stored in `.env`, never exposed to frontend
- ✅ **Input Sanitization** — User inputs sanitized before processing
- ✅ **CORS Configuration** — Restricted to configured frontend origins

---

## 🔮 Future Enhancements

- Multi-database support (PostgreSQL, MySQL)
- Query history & bookmarks
- Auto-generated data visualizations
- Voice input for queries
- User authentication (JWT)
- Export results as CSV/PDF
- Docker containerization

---

## 📄 License

This project is developed as part of an academic assignment.

---

<p align="center">
  Built with ❤️ by <strong>Team LTVIP2026TMIDS80425</strong>
</p>
