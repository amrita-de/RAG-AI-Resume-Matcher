import { useState, useCallback } from 'react';
import Header from './components/Header';
import InputSection from './components/InputSection';
import ScoreGauge from './components/ScoreGauge';
import SkillsChips from './components/SkillsChips';
import BulletComparison from './components/BulletComparison';
import SimilarJDsCard from './components/SimilarJDsCard';
import RecruiterVerdict from './components/RecruiterVerdict';

const PIPELINE_STEPS = {
  standard: ['Extracting Skills', 'Computing Match Score', 'Optimizing Bullets', 'Generating Report'],
  rag: ['Extracting Skills', 'Retrieving Context (FAISS)', 'Computing Match Score', 'RAG-Grounded Optimization', 'Generating Report'],
  hitl: ['Extracting Skills', 'Computing Match Score', 'Optimizing Bullets', 'Awaiting Human Review'],
};

export default function App() {
  const [results, setResults] = useState(null);
  const [similarJDs, setSimilarJDs] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState('');
  const [isHITL, setIsHITL] = useState(false);
  const [hitlThreadId, setHitlThreadId] = useState(null);

  const simulateProgress = useCallback((pipeline) => {
    const steps = PIPELINE_STEPS[pipeline] || PIPELINE_STEPS.standard;
    let currentStep = 0;
    const stepInterval = setInterval(() => {
      if (currentStep < steps.length) {
        setStatusText(steps[currentStep] + '...');
        setProgress(Math.min(((currentStep + 1) / steps.length) * 90, 90));
        currentStep++;
      }
    }, 800);
    return () => clearInterval(stepInterval);
  }, []);

  const handleSubmit = useCallback(async ({ mode, file, resumeText, jdText, targetRole, pipeline }) => {
    setIsLoading(true);
    setProgress(5);
    setStatusText('Initializing pipeline...');
    setResults(null);
    setSimilarJDs(null);
    setIsHITL(pipeline === 'hitl');
    setHitlThreadId(null);

    const stopProgress = simulateProgress(pipeline);

    try {
      let data;

      if (mode === 'file') {
        // Multipart file upload
        const formData = new FormData();
        formData.append('resume_file', file);
        formData.append('jd_text', jdText);
        formData.append('target_role', targetRole);
        formData.append('pipeline_type', pipeline);

        const resp = await fetch('/api/v1/upload-and-evaluate', {
          method: 'POST',
          body: formData,
        });
        data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Upload evaluation failed');
      } else {
        // Text-based evaluation
        let endpoint = '/api/v1/evaluate';
        let body = { resume_text: resumeText, jd_text: jdText, target_role: targetRole };

        if (pipeline === 'rag') {
          endpoint = '/api/v1/evaluate/rag';
        } else if (pipeline === 'hitl') {
          endpoint = '/api/v1/evaluate/hitl';
        }

        const resp = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
        data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Evaluation failed');
      }

      // Handle HITL thread_id
      if (pipeline === 'hitl' && data.thread_id) {
        setHitlThreadId(data.thread_id);
      }
      if (data.human_review?.thread_id) {
        setHitlThreadId(data.human_review.thread_id);
      }

      setResults(data);
      setProgress(100);
      setStatusText('Evaluation complete!');

      // Fetch similar JDs for RAG pipeline
      if (pipeline === 'rag' || pipeline === 'standard') {
        try {
          const jdResp = await fetch('/api/v1/similar-jds', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_text: resumeText || 'AI Engineer Python', k: 3 }),
          });
          if (jdResp.ok) {
            const jdData = await jdResp.json();
            setSimilarJDs(jdData.similar_jds);
          }
        } catch {
          // Similar JDs are optional
        }
      }
    } catch (err) {
      console.error('Evaluation error:', err);
      setStatusText(`Error: ${err.message}`);
    } finally {
      stopProgress();
      setTimeout(() => setIsLoading(false), 500);
    }
  }, [simulateProgress]);

  const handleHITLApprove = useCallback(async (approval) => {
    if (!hitlThreadId) return;

    setIsLoading(true);
    setStatusText('Submitting human review...');
    setProgress(50);

    try {
      const resp = await fetch(`/api/v1/evaluate/hitl/${hitlThreadId}/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          approval,
          feedback: approval === 'approved'
            ? 'Rewrites approved — strong action verbs and quantified metrics.'
            : 'Please refine rewrites with more specific metrics.',
        }),
      });
      const data = await resp.json();
      if (!resp.ok) throw new Error(data.detail || 'Review submission failed');

      setResults(data);
      setIsHITL(false);
      setProgress(100);
      setStatusText('HITL review complete — final report generated.');
    } catch (err) {
      setStatusText(`Error: ${err.message}`);
    } finally {
      setTimeout(() => setIsLoading(false), 500);
    }
  }, [hitlThreadId]);

  // Normalize results for display — handle different response shapes
  const matchResults = results?.match_results || {};
  const rewrites = results?.rewrites || results?.pending_rewrites || {};

  return (
    <div className="app-container">
      <Header />

      <InputSection
        onSubmit={handleSubmit}
        isLoading={isLoading}
        progress={progress}
        statusText={statusText}
      />

      {results && (
        <div className="results-grid">
          <div className="results-top-row">
            <ScoreGauge matchResults={matchResults} />
            <SkillsChips matchResults={matchResults} />
          </div>

          <BulletComparison
            rewrites={rewrites}
            isHITL={isHITL}
            onApprove={handleHITLApprove}
          />

          {similarJDs && <SimilarJDsCard similarJDs={similarJDs} />}

          <RecruiterVerdict report={results} />
        </div>
      )}
    </div>
  );
}
