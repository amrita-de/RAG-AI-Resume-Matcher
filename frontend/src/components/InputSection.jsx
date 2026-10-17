import { useState, useRef, useCallback } from 'react';
import { Upload, FileText, X, Sparkles, Play, Beaker } from 'lucide-react';

export default function InputSection({ onSubmit, isLoading, progress, statusText }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jdText, setJdText] = useState('');
  const [targetRole, setTargetRole] = useState('Senior AI / Full Stack Engineer');
  const [pipeline, setPipeline] = useState('standard');
  const [isDragOver, setIsDragOver] = useState(false);
  const [inputMode, setInputMode] = useState('text'); // 'text' or 'file'
  const fileInputRef = useRef(null);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) setResumeFile(file);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback(() => setIsDragOver(false), []);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) setResumeFile(file);
  };

  const handleLoadSample = async () => {
    try {
      const resp = await fetch('/api/v1/sample-data');
      if (resp.ok) {
        const data = await resp.json();
        setResumeText(data.resume_text);
        setJdText(data.jd_text);
        setTargetRole(data.target_role);
        setInputMode('text');
        setResumeFile(null);
      }
    } catch (err) {
      console.error('Failed to load sample data:', err);
    }
  };

  const handleSubmit = () => {
    if (inputMode === 'file' && resumeFile) {
      onSubmit({
        mode: 'file',
        file: resumeFile,
        jdText,
        targetRole,
        pipeline,
      });
    } else if (inputMode === 'text' && resumeText.trim()) {
      onSubmit({
        mode: 'text',
        resumeText,
        jdText,
        targetRole,
        pipeline,
      });
    }
  };

  const canSubmit =
    ((inputMode === 'file' && resumeFile) || (inputMode === 'text' && resumeText.trim().length >= 50)) &&
    jdText.trim().length >= 50 &&
    !isLoading;

  const fileExt = resumeFile?.name?.split('.').pop()?.toUpperCase() || '';

  return (
    <div className="input-section glass-card fade-in">
      <div className="section-title">
        <Beaker size={18} />
        Resume Evaluation Lab
      </div>

      {/* Mode toggle */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <button
          className={`btn btn-small ${inputMode === 'text' ? 'btn-primary' : 'btn-ghost'}`}
          onClick={() => setInputMode('text')}
        >
          Paste Text
        </button>
        <button
          className={`btn btn-small ${inputMode === 'file' ? 'btn-primary' : 'btn-ghost'}`}
          onClick={() => setInputMode('file')}
        >
          <Upload size={13} /> Upload File
        </button>
        <button className="btn btn-small btn-ghost" onClick={handleLoadSample} style={{ marginLeft: 'auto' }}>
          <Sparkles size={13} /> Quick Fill Sample Data
        </button>
      </div>

      <div className="input-grid">
        {/* Left: Resume */}
        <div className="input-group">
          <label className="input-label">Candidate Resume</label>
          {inputMode === 'file' ? (
            <div
              className={`dropzone ${isDragOver ? 'drag-over' : ''} ${resumeFile ? 'has-file' : ''}`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={() => !resumeFile && fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.doc,.txt,.md"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />
              {resumeFile ? (
                <div className="file-info">
                  <FileText size={20} />
                  <span>{resumeFile.name}</span>
                  <span className="badge badge-indigo">{fileExt}</span>
                  <button
                    className="file-remove"
                    onClick={(e) => {
                      e.stopPropagation();
                      setResumeFile(null);
                    }}
                  >
                    <X size={16} />
                  </button>
                </div>
              ) : (
                <>
                  <Upload size={28} className="dropzone-icon" />
                  <div className="dropzone-text">Drop resume file here or click to browse</div>
                  <div className="dropzone-hint">PDF, DOCX, or TXT · Max 10MB</div>
                </>
              )}
            </div>
          ) : (
            <textarea
              className="jd-textarea"
              placeholder="Paste your full resume text here..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
            />
          )}
        </div>

        {/* Right: Job Description */}
        <div className="input-group">
          <label className="input-label">Target Job Description</label>
          <textarea
            className="jd-textarea"
            placeholder="Paste the full job description text here..."
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
          />
        </div>
      </div>

      {/* Controls */}
      <div className="controls-row">
        <div className="controls-left">
          <input
            className="role-input"
            placeholder="Target Role Title"
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
          />
          <div className="pipeline-selector">
            <button
              className={`pipeline-btn ${pipeline === 'standard' ? 'active' : ''}`}
              onClick={() => setPipeline('standard')}
            >
              Standard
            </button>
            <button
              className={`pipeline-btn ${pipeline === 'rag' ? 'active' : ''}`}
              onClick={() => setPipeline('rag')}
            >
              RAG Enhanced
            </button>
            <button
              className={`pipeline-btn ${pipeline === 'hitl' ? 'active' : ''}`}
              onClick={() => setPipeline('hitl')}
            >
              HITL Review
            </button>
          </div>
        </div>

        <button className="btn btn-primary" disabled={!canSubmit} onClick={handleSubmit}>
          <Play size={16} />
          {isLoading ? 'Evaluating...' : 'Run Evaluation'}
        </button>
      </div>

      {/* Progress bar */}
      {isLoading && (
        <div>
          <div className="progress-bar">
            <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
          </div>
          <div className="status-text">
            <span className="spinner" />
            {statusText}
          </div>
        </div>
      )}
    </div>
  );
}
