import { GitCompare, Check, ThumbsUp, Pencil } from 'lucide-react';

export default function BulletComparison({ rewrites, isHITL, onApprove }) {
  const bullets = rewrites?.rewritten_bullets ?? [];

  if (!bullets.length) return null;

  return (
    <div className="bullets-card glass-card fade-in stagger-3">
      <div className="section-title">
        <GitCompare size={18} />
        Bullet Point Optimizations (Google XYZ Formula)
      </div>

      {bullets.map((bullet, idx) => (
        <div key={idx} className="bullet-item">
          <div className="bullet-header">
            <span>
              <span className="bullet-number">#{idx + 1}</span> Bullet Rewrite
            </span>
            {bullet.action_verb && (
              <span className="badge badge-indigo">{bullet.action_verb}</span>
            )}
          </div>

          <div className="bullet-columns">
            <div className="bullet-col bullet-col-original">
              <div className="bullet-col-label original">Original</div>
              {bullet.original || bullet.original_bullet || '—'}
            </div>
            <div className="bullet-col bullet-col-rewritten">
              <div className="bullet-col-label rewritten">Rewritten (XYZ)</div>
              {bullet.rewritten || bullet.improved || '—'}
            </div>
          </div>

          {(bullet.reasoning || bullet.explanation) && (
            <div className="bullet-reasoning">
              💡 {bullet.reasoning || bullet.explanation}
              {bullet.metrics_added && (
                <span className="bullet-metric">📊 {bullet.metrics_added}</span>
              )}
            </div>
          )}
        </div>
      ))}

      {rewrites?.strategic_summary && (
        <div style={{ marginTop: 16, padding: '12px 16px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-sm)', fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.7 }}>
          <strong style={{ color: 'var(--accent-indigo-light)' }}>Strategic Summary:</strong>{' '}
          {rewrites.strategic_summary}
        </div>
      )}

      {isHITL && (
        <div className="hitl-bar">
          <button className="btn btn-emerald btn-small" onClick={() => onApprove?.('approved')}>
            <ThumbsUp size={14} />
            Approve All Rewrites
          </button>
          <button className="btn btn-ghost btn-small" onClick={() => onApprove?.('edited')}>
            <Pencil size={14} />
            Request Edits
          </button>
        </div>
      )}
    </div>
  );
}
