import { useState, useEffect } from 'react';
import { Brain, Zap, Database, Shield } from 'lucide-react';

export default function Header() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const resp = await fetch('/health');
        if (resp.ok) {
          const data = await resp.json();
          setHealth(data);
        } else {
          setHealth(null);
        }
      } catch {
        setHealth(null);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="app-header">
      <div className="header-inner">
        <div className="header-brand">
          <div className="header-logo">
            <Brain size={22} />
          </div>
          <div>
            <div className="header-title">Agentic AI Resume Matcher</div>
            <div className="header-subtitle">LLM-Powered Resume Evaluation & Optimization</div>
          </div>
        </div>

        <div className="header-badges">
          <span className="badge badge-indigo">
            <Zap size={11} />
            LangGraph
          </span>
          <span className="badge badge-emerald">
            <Database size={11} />
            FAISS RAG
          </span>
          <span className="badge badge-rose">
            <Shield size={11} />
            HITL
          </span>
          <span className="badge badge-amber">
            <span className={`health-dot ${health ? 'online' : 'offline'}`} />
            {health ? 'API Online' : 'API Offline'}
          </span>
        </div>
      </div>
    </header>
  );
}
