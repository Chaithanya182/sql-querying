import { useState, useEffect, useRef } from 'react';
import './index.css';
import SchemaViewer from './components/SchemaViewer';
import QueryPanel from './components/QueryPanel';
import QueryHistory from './components/QueryHistory';
import { fetchSchema, submitQuery, fetchHistory, clearHistory, uploadDatabase } from './api';

function App() {
  const [schema, setSchema] = useState([]);
  const [schemaLoading, setSchemaLoading] = useState(true);
  const [dbName, setDbName] = useState('sample.db');

  const [queryLoading, setQueryLoading] = useState(false);
  const [queryResult, setQueryResult] = useState(null);
  const [queryError, setQueryError] = useState(null);

  const [history, setHistory] = useState([]);
  const [historyOpen, setHistoryOpen] = useState(false);

  const [toast, setToast] = useState(null);
  const fileInputRef = useRef(null);

  // Load schema on mount
  useEffect(() => {
    loadSchema();
  }, []);

  const loadSchema = async () => {
    setSchemaLoading(true);
    try {
      const data = await fetchSchema();
      setSchema(data.schema || []);
      setDbName(data.db_path || 'sample.db');
    } catch (err) {
      showToast('Failed to connect to backend. Is the server running?', 'error');
    } finally {
      setSchemaLoading(false);
    }
  };

  const handleQuery = async (question) => {
    setQueryLoading(true);
    setQueryError(null);
    setQueryResult(null);

    try {
      const data = await submitQuery(question);
      if (data.success) {
        setQueryResult(data);
      } else {
        setQueryError(data.error || 'Failed to generate SQL');
      }
      // Refresh history
      loadHistory();
    } catch (err) {
      setQueryError('Connection error. Is the backend server running?');
    } finally {
      setQueryLoading(false);
    }
  };

  const loadHistory = async () => {
    try {
      const data = await fetchHistory();
      setHistory(data.history || []);
    } catch (err) {
      // silent fail
    }
  };

  const handleClearHistory = async () => {
    try {
      await clearHistory();
      setHistory([]);
      showToast('History cleared', 'success');
    } catch (err) {
      showToast('Failed to clear history', 'error');
    }
  };

  const handleHistorySelect = (question) => {
    setHistoryOpen(false);
    handleQuery(question);
  };

  const handleUploadDB = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      showToast('Uploading database...', 'success');
      const data = await uploadDatabase(file);
      if (data.success) {
        setSchema(data.schema || []);
        setDbName(data.db_name || file.name);
        setQueryResult(null);
        setQueryError(null);
        showToast(`Database "${file.name}" loaded!`, 'success');
      }
    } catch (err) {
      showToast('Failed to upload database', 'error');
    }

    // Reset file input
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <div className="logo-icon">⚡</div>
            <span className="logo-text">Smart Bridge</span>
          </div>
          <div className="logo-subtitle">Intelligent SQL Querying</div>
        </div>

        <div className="sidebar-content">
          <SchemaViewer schema={schema} loading={schemaLoading} />
        </div>

        <div className="upload-section">
          <input
            ref={fileInputRef}
            type="file"
            accept=".db,.sqlite,.sqlite3"
            style={{ display: 'none' }}
            onChange={handleUploadDB}
          />
          <button className="upload-btn" onClick={() => fileInputRef.current?.click()}>
            <span className="icon">📁</span>
            Upload Custom Database
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header className="header">
          <div className="header-left">
            <h1 className="header-title">Query Console</h1>
          </div>
          <div className="header-right">
            <div className="db-badge">
              🗄 {dbName}
            </div>
            <div className="status-badge">
              <span className={`status-dot ${schemaLoading ? 'disconnected' : ''}`}></span>
              {schemaLoading ? 'Connecting...' : 'Connected'}
            </div>
            <button
              className={`icon-btn ${historyOpen ? 'active' : ''}`}
              onClick={() => {
                setHistoryOpen(!historyOpen);
                if (!historyOpen) loadHistory();
              }}
              title="Query History"
            >
              🕒
            </button>
          </div>
        </header>

        {/* Content */}
        <div className="content-area">
          <QueryPanel
            onSubmit={handleQuery}
            loading={queryLoading}
            result={queryResult}
            error={queryError}
          />
        </div>

        {/* History Panel */}
        <QueryHistory
          history={history}
          isOpen={historyOpen}
          onClose={() => setHistoryOpen(false)}
          onClear={handleClearHistory}
          onSelect={handleHistorySelect}
        />
      </main>

      {/* Toast */}
      {toast && (
        <div className={`toast ${toast.type}`}>
          {toast.type === 'success' ? '✅' : '❌'} {toast.message}
        </div>
      )}
    </div>
  );
}

export default App;
