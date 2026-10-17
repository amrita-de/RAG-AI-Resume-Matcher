import { Layers } from 'lucide-react';

export default function SimilarJDsCard({ similarJDs }) {
  if (!similarJDs || !similarJDs.length) return null;

  const getScoreColor = (score) => {
    if (score >= 0.8) return 'linear-gradient(135deg, var(--accent-emerald), #059669)';
    if (score >= 0.6) return 'linear-gradient(135deg, var(--accent-amber), #d97706)';
    return 'linear-gradient(135deg, var(--accent-rose), #e11d48)';
  };

  return (
    <div className="similar-jds-card glass-card fade-in stagger-3">
      <div className="section-title">
        <Layers size={18} />
        Similar Jobs from FAISS Index
      </div>

      {similarJDs.map((jd, idx) => (
        <div key={idx} className="jd-item">
          <div
            className="jd-score-badge"
            style={{ background: getScoreColor(jd.similarity_score) }}
          >
            {Math.round((jd.similarity_score || 0) * 100)}%
          </div>
          <div className="jd-info">
            <div className="jd-title">{jd.title || `Job ${idx + 1}`}</div>
            <div className="jd-company">{jd.company || 'Unknown Company'}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
