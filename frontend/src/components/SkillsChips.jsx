import { CheckCircle, AlertTriangle, Info } from 'lucide-react';

export default function SkillsChips({ matchResults }) {
  const matched = matchResults?.matched_skills ?? [];
  const missing = matchResults?.missing_critical_skills ?? matchResults?.missing_skills ?? [];
  const niceToHave = matchResults?.missing_nice_to_have ?? matchResults?.nice_to_have ?? [];

  if (!matched.length && !missing.length && !niceToHave.length) return null;

  return (
    <div className="skills-card glass-card fade-in stagger-2">
      <div className="section-title">
        <CheckCircle size={18} style={{ color: 'var(--accent-emerald)' }} />
        Skills Gap Analysis
      </div>

      {matched.length > 0 && (
        <div className="skills-section">
          <div className="skills-section-title matched">
            <CheckCircle size={13} />
            Matched Skills ({matched.length})
          </div>
          <div className="chip-grid">
            {matched.map((skill, i) => (
              <span key={i} className="chip chip-matched">
                <CheckCircle size={11} />
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {missing.length > 0 && (
        <div className="skills-section">
          <div className="skills-section-title missing">
            <AlertTriangle size={13} />
            Missing Critical ({missing.length})
          </div>
          <div className="chip-grid">
            {missing.map((skill, i) => (
              <span key={i} className="chip chip-missing">
                <AlertTriangle size={11} />
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {niceToHave.length > 0 && (
        <div className="skills-section">
          <div className="skills-section-title nice-to-have">
            <Info size={13} />
            Nice-to-Have ({niceToHave.length})
          </div>
          <div className="chip-grid">
            {niceToHave.map((skill, i) => (
              <span key={i} className="chip chip-nice">
                <Info size={11} />
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
