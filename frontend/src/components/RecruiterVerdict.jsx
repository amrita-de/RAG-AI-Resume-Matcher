import { Award } from 'lucide-react';

export default function RecruiterVerdict({ report }) {
  const advice = report?.strategic_advice || report?.rewrites?.strategic_summary;
  if (!advice) return null;

  return (
    <div className="verdict-card glass-card fade-in stagger-4">
      <div className="section-title">
        <Award size={18} style={{ color: 'var(--accent-amber)' }} />
        Strategic Recruiter Verdict
      </div>
      <div className="verdict-text">{advice}</div>
    </div>
  );
}
