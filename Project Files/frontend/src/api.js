const API_BASE = 'http://localhost:8000';

export async function fetchSchema() {
    const res = await fetch(`${API_BASE}/api/schema`);
    if (!res.ok) throw new Error('Failed to fetch schema');
    return res.json();
}

export async function submitQuery(question) {
    const res = await fetch(`${API_BASE}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, execute: true }),
    });
    if (!res.ok) throw new Error('Failed to submit query');
    return res.json();
}

export async function executeSQL(sql) {
    const res = await fetch(`${API_BASE}/api/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sql }),
    });
    if (!res.ok) throw new Error('Failed to execute SQL');
    return res.json();
}

export async function fetchHistory() {
    const res = await fetch(`${API_BASE}/api/history`);
    if (!res.ok) throw new Error('Failed to fetch history');
    return res.json();
}

export async function clearHistory() {
    const res = await fetch(`${API_BASE}/api/history`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to clear history');
    return res.json();
}

export async function uploadDatabase(file) {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/api/upload-db`, {
        method: 'POST',
        body: formData,
    });
    if (!res.ok) throw new Error('Failed to upload database');
    return res.json();
}

export async function fetchStatus() {
    const res = await fetch(`${API_BASE}/api/status`);
    if (!res.ok) throw new Error('Failed to fetch status');
    return res.json();
}
