import { useState } from 'react';

const HINT_QUERIES = [
    'Show all products under ₹1000',
    'Top 5 customers by total spend',
    'Average rating per category',
    'Orders from last 30 days',
    'Products with low stock',
];

function highlightSQL(sql) {
    if (!sql) return '';
    const keywords = [
        'SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER',
        'ON', 'AND', 'OR', 'NOT', 'IN', 'AS', 'ORDER', 'BY', 'GROUP', 'HAVING',
        'LIMIT', 'OFFSET', 'ASC', 'DESC', 'DISTINCT', 'UNION', 'ALL', 'INSERT',
        'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 'ALTER',
        'DROP', 'INDEX', 'VIEW', 'WITH', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
        'NULL', 'IS', 'LIKE', 'BETWEEN', 'EXISTS', 'COUNT', 'SUM', 'AVG', 'MIN',
        'MAX', 'CAST', 'COALESCE', 'IFNULL', 'ROUND',
    ];

    const parts = sql.split(/(\s+|,|\(|\)|'[^']*'|\d+\.?\d*)/g);
    return parts.map((part, i) => {
        if (keywords.includes(part.toUpperCase())) {
            return <span key={i} className="sql-keyword">{part}</span>;
        }
        if (/^'[^']*'$/.test(part)) {
            return <span key={i} className="sql-string">{part}</span>;
        }
        if (/^\d+\.?\d*$/.test(part) && part.trim()) {
            return <span key={i} className="sql-number">{part}</span>;
        }
        if (['COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'ROUND', 'COALESCE', 'IFNULL', 'CAST']
            .includes(part.toUpperCase())) {
            return <span key={i} className="sql-function">{part}</span>;
        }
        return <span key={i}>{part}</span>;
    });
}

export default function QueryPanel({ onSubmit, loading, result, error }) {
    const [question, setQuestion] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (question.trim() && !loading) {
            onSubmit(question.trim());
        }
    };

    const handleHintClick = (hint) => {
        setQuestion(hint);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    const copySQL = () => {
        if (result?.sql) {
            navigator.clipboard.writeText(result.sql);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20, flex: 1, overflow: 'hidden', minHeight: 0 }}>
            {/* Query Input Section */}
            <div className="query-section">
                <form onSubmit={handleSubmit}>
                    <div className="query-input-container">
                        <div className="query-label">
                            <span className="icon">💬</span>
                            Ask a question in plain English
                        </div>
                        <textarea
                            className="query-textarea"
                            placeholder="e.g., Show me all products with a rating above 4.5 sorted by price..."
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            onKeyDown={handleKeyDown}
                            rows={2}
                        />
                        <div className="query-actions">
                            <div className="query-hints">
                                {HINT_QUERIES.map((hint) => (
                                    <span
                                        key={hint}
                                        className="hint-chip"
                                        onClick={() => handleHintClick(hint)}
                                    >
                                        {hint}
                                    </span>
                                ))}
                            </div>
                            <button type="submit" className="submit-btn" disabled={loading || !question.trim()}>
                                {loading ? (
                                    <>
                                        <div className="loading-spinner" style={{ width: 16, height: 16, borderWidth: 2 }}></div>
                                        Generating...
                                    </>
                                ) : (
                                    <>
                                        <span className="icon">▶</span>
                                        Run Query
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </form>
            </div>

            {/* Results Area */}
            <div className="results-section">
                {/* Error Display */}
                {error && (
                    <div className="error-display">
                        <span className="icon">⚠️</span>
                        <div>{error}</div>
                    </div>
                )}

                {/* Loading State */}
                {loading && (
                    <div className="loading-container">
                        <div className="loading-spinner"></div>
                        <div className="loading-text">Translating your question to SQL with AI...</div>
                    </div>
                )}

                {/* SQL Display */}
                {!loading && result?.sql && (
                    <div className="sql-display">
                        <div className="sql-header">
                            <div className="sql-header-left">
                                <span className="icon">⚡</span>
                                Generated SQL
                            </div>
                            <div className="sql-actions">
                                <button className="sql-action-btn" onClick={copySQL}>
                                    📋 Copy
                                </button>
                            </div>
                        </div>
                        <div className="sql-body">
                            <div className="sql-code">{highlightSQL(result.sql)}</div>
                            {result.explanation && (
                                <div className="sql-explanation">
                                    <span className="icon">💡</span>
                                    {result.explanation}
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* Results Table */}
                {!loading && result?.results?.success && (
                    <div className="results-container">
                        <div className="results-header">
                            <div className="results-header-left">
                                📊 Results
                                <span className="results-count">
                                    ({result.results.row_count} row{result.results.row_count !== 1 ? 's' : ''})
                                    {result.results.truncated && ' — truncated'}
                                </span>
                            </div>
                        </div>
                        {result.results.rows.length > 0 ? (
                            <div className="results-table-wrapper">
                                <table className="results-table">
                                    <thead>
                                        <tr>
                                            {result.results.columns.map((col) => (
                                                <th key={col}>{col}</th>
                                            ))}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {result.results.rows.map((row, i) => (
                                            <tr key={i}>
                                                {result.results.columns.map((col) => (
                                                    <td key={col}>{row[col] !== null ? String(row[col]) : 'NULL'}</td>
                                                ))}
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        ) : (
                            <div className="empty-state" style={{ padding: 30 }}>
                                <p>Query executed successfully but returned no results.</p>
                            </div>
                        )}
                    </div>
                )}

                {/* SQL execution error */}
                {!loading && result?.results && !result.results.success && (
                    <div className="error-display">
                        <span className="icon">⚠️</span>
                        <div>
                            <strong>SQL Execution Error:</strong> {result.results.error}
                        </div>
                    </div>
                )}

                {/* Empty State */}
                {!loading && !result && !error && (
                    <div className="empty-state">
                        <span className="icon">🔍</span>
                        <h3>Ask anything about your data</h3>
                        <p>
                            Type a question in natural language above, and AI will generate the SQL query
                            and show you the results instantly.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
