import { useState } from 'react';

export default function SchemaViewer({ schema, loading }) {
    const [expanded, setExpanded] = useState({});

    const toggle = (tableName) => {
        setExpanded((prev) => ({ ...prev, [tableName]: !prev[tableName] }));
    };

    // Build FK lookup for current table
    const getFKTarget = (table, colName) => {
        const fk = table.foreign_keys?.find((f) => f.from_column === colName);
        return fk ? `→ ${fk.to_table}.${fk.to_column}` : null;
    };

    if (loading) {
        return (
            <div className="sidebar-section">
                <div className="sidebar-section-title">Database Schema</div>
                <div className="loading-container" style={{ padding: '20px' }}>
                    <div className="loading-spinner" style={{ width: 24, height: 24 }}></div>
                    <div className="loading-text" style={{ fontSize: 11 }}>Loading schema...</div>
                </div>
            </div>
        );
    }

    if (!schema || schema.length === 0) {
        return (
            <div className="sidebar-section">
                <div className="sidebar-section-title">Database Schema</div>
                <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)', fontSize: 12 }}>
                    No tables found
                </div>
            </div>
        );
    }

    return (
        <div className="sidebar-section">
            <div className="sidebar-section-title">
                Tables ({schema.length})
            </div>
            {schema.map((table) => (
                <div key={table.table_name} className="schema-table">
                    <div className="schema-table-header" onClick={() => toggle(table.table_name)}>
                        <span className="schema-table-name">
                            {expanded[table.table_name] ? '▾' : '▸'} {table.table_name}
                        </span>
                        <span className="schema-table-badge">{table.row_count} rows</span>
                    </div>
                    {expanded[table.table_name] && (
                        <div className="schema-table-columns">
                            {table.columns.map((col) => {
                                const fkTarget = getFKTarget(table, col.name);
                                return (
                                    <div key={col.name} className="schema-column">
                                        {col.primary_key && <span className="schema-column-pk">PK</span>}
                                        {fkTarget && <span className="schema-column-fk">FK</span>}
                                        <span className="schema-column-name">{col.name}</span>
                                        <span className="schema-column-type">{col.type}</span>
                                        {fkTarget && (
                                            <span style={{ fontSize: 9, color: 'var(--warning)' }}>{fkTarget}</span>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}
