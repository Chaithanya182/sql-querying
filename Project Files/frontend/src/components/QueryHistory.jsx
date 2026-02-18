export default function QueryHistory({ history, isOpen, onClose, onClear, onSelect }) {
    const formatTime = (timestamp) => {
        if (!timestamp) return '';
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) return `${diffHours}h ago`;
        return date.toLocaleDateString();
    };

    return (
        <div className={`history-panel ${isOpen ? 'open' : ''}`}>
            <div className="history-header">
                <h3>
                    🕒 Query History
                </h3>
                <div className="history-actions">
                    {history.length > 0 && (
                        <button className="history-clear-btn" onClick={onClear}>
                            🗑 Clear
                        </button>
                    )}
                    <button className="history-close-btn" onClick={onClose}>
                        ✕
                    </button>
                </div>
            </div>
            <div className="history-list">
                {history.length === 0 ? (
                    <div className="empty-state" style={{ padding: '40px 20px' }}>
                        <span className="icon" style={{ fontSize: 32 }}>📝</span>
                        <p style={{ fontSize: 12 }}>No queries yet. Ask a question to get started!</p>
                    </div>
                ) : (
                    history.map((item) => (
                        <div
                            key={item.id}
                            className="history-item"
                            onClick={() => onSelect(item.question)}
                        >
                            <div className="history-item-question">{item.question}</div>
                            <div className="history-item-meta">
                                <span>{formatTime(item.timestamp)}</span>
                                <div className="history-item-status">
                                    <span className={`dot ${item.success ? 'success' : 'error'}`}></span>
                                    <span>{item.success ? `${item.row_count} rows` : 'Error'}</span>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
