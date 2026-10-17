import { useEffect, useState } from 'react';
import { Target } from 'lucide-react';

export default function ScoreGauge({ matchResults }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  const overallScore = matchResults?.overall_score ?? 0;
  const skillsScore = matchResults?.skills_score ?? 0;
  const experienceScore = matchResults?.experience_score ?? 0;
  const impactScore = matchResults?.quantified_impact_score ?? 0;

  // Animate score counter
  useEffect(() => {
    if (overallScore === 0) return;
    let start = 0;
    const duration = 1200;
    const startTime = performance.now();
    const animate = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      start = Math.round(eased * overallScore);
      setAnimatedScore(start);
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [overallScore]);

  // SVG gauge
  const radius = 72;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (overallScore / 100) * circumference;

  const getColor = (score) => {
    if (score >= 80) return 'var(--accent-emerald)';
    if (score >= 60) return 'var(--accent-amber)';
    return 'var(--accent-rose)';
  };

  const getGlow = (score) => {
    if (score >= 80) return 'var(--accent-emerald-glow)';
    if (score >= 60) return 'rgba(245, 158, 11, 0.25)';
    return 'rgba(244, 63, 94, 0.25)';
  };

  const subScores = [
    { label: 'Skills Coverage', value: skillsScore },
    { label: 'Experience Relevance', value: experienceScore },
    { label: 'Quantified Impact', value: impactScore },
  ];

  return (
    <div className="score-gauge-card glass-card fade-in stagger-1">
      <div className="section-title">
        <Target size={18} />
        Match Score
      </div>

      <div className="gauge-container">
        <svg className="gauge-svg" width="180" height="180" viewBox="0 0 180 180">
          <circle className="gauge-bg" cx="90" cy="90" r={radius} />
          <circle
            className="gauge-fill"
            cx="90"
            cy="90"
            r={radius}
            stroke={getColor(overallScore)}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            style={{ filter: `drop-shadow(0 0 8px ${getGlow(overallScore)})` }}
          />
        </svg>
        <div className="gauge-score">
          <div className="gauge-number" style={{ color: getColor(overallScore) }}>
            {animatedScore}
          </div>
          <div className="gauge-label">out of 100</div>
        </div>
      </div>

      <div className="sub-scores">
        {subScores.map((s) => (
          <div key={s.label}>
            <div className="sub-score-item">
              <span className="sub-score-label">{s.label}</span>
              <span className="sub-score-value" style={{ color: getColor(s.value) }}>
                {s.value}
              </span>
            </div>
            <div className="sub-score-bar">
              <div
                className="sub-score-bar-fill"
                style={{
                  width: `${s.value}%`,
                  background: getColor(s.value),
                  boxShadow: `0 0 8px ${getGlow(s.value)}`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
