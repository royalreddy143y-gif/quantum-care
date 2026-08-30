import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Printer,
  Download,
  ArrowLeft,
  Cpu
} from 'lucide-react';
import { analysisService } from '../services/analysisService';
import { Button } from '../components/Button';
import { Loader } from '../components/Card';

export const ReportViewPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const data = await analysisService.getAnalysisDetail(id);
        setAnalysis(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalysis();
  }, [id]);

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadPdf = () => {
    const pdfUrl = analysisService.getPdfDownloadUrl(id);
    window.open(pdfUrl, '_blank');
  };

  if (loading) {
    return <Loader message="Rendering analysis report..." />;
  }

  if (!analysis || !analysis.prediction) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-500">Analysis report not available.</p>
        <Button variant="secondary" size="sm" onClick={() => navigate('/dashboard')} className="mt-4">
          Return to Dashboard
        </Button>
      </div>
    );
  }

  const pred = analysis.prediction;
  const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';
  const backendBase = API_BASE.replace(/\/api\/?$/, '');
  const imageUrl = analysis.image
    ? `${backendBase}/uploads/${analysis.image.file_path.split(/[\\/]/).pop()}`
    : null;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Top Action Bar (hidden in print mode) */}
      <div className="flex items-center justify-between print:hidden">
        <button
          onClick={() => navigate(`/analyses/${analysis.id}/result`)}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Result View
        </button>

        <div className="flex items-center gap-3">
          <Button
            variant="secondary"
            size="sm"
            icon={Printer}
            onClick={handlePrint}
          >
            Print Report
          </Button>
          <Button
            variant="quantum"
            size="sm"
            icon={Download}
            onClick={handleDownloadPdf}
          >
            Download PDF
          </Button>
        </div>
      </div>

      {/* Printable Report Document Card */}
      <div className="bg-white rounded-2xl shadow-md border border-slate-200 p-8 sm:p-12 space-y-8 print:shadow-none print:border-none print:p-0">
        {/* Document Header */}
        <div className="border-b-2 border-brand-600 pb-4 flex justify-between items-start">
          <div>
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-brand-600 text-white rounded-lg">
                <Cpu className="w-5 h-5" />
              </div>
              <h1 className="text-2xl font-black tracking-tight text-slate-900">QUANTUMCARE</h1>
            </div>
            <p className="text-[11px] text-brand-700 font-semibold mt-1">
              Hybrid Quantum Machine Learning Platform for Early Disease Detection
            </p>
          </div>

          <div className="text-right text-xs">
            <span className="font-bold text-slate-900 block text-sm">CLINICAL ANALYSIS REPORT</span>
            <span className="font-mono text-slate-500 font-semibold block">{analysis.analysis_code}</span>
            <span className="text-slate-400 text-[11px]">
              {new Date(analysis.created_at).toLocaleString()}
            </span>
          </div>
        </div>

        {/* Section 1: Patient Details */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            1. Patient Information & Medical Context
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs bg-slate-50 p-4 rounded-xl border border-slate-200">
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-semibold">Patient ID</span>
              <span className="font-mono font-bold text-slate-900">{analysis.patient?.patient_id}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-semibold">Full Name</span>
              <span className="font-bold text-slate-900">{analysis.patient?.name}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-semibold">Age / Gender</span>
              <span className="text-slate-800">{analysis.patient?.age} yrs / {analysis.patient?.gender}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-semibold">Architecture</span>
              <span className="font-bold text-purple-700">Hybrid QML (Swin-T + VQC)</span>
            </div>
          </div>
        </div>

        {/* Section 2: Imaging & Classification Results */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            2. Scan Evaluation & Hybrid Predictions
          </h3>
          <div className="grid sm:grid-cols-3 gap-6 items-center">
            {imageUrl && (
              <div className="border border-slate-200 rounded-xl overflow-hidden bg-slate-50 p-2 text-center">
                <img
                  src={imageUrl}
                  alt="Medical scan"
                  className="max-h-44 mx-auto rounded object-contain"
                />
                <span className="text-[10px] text-slate-500 mt-1 block">Input Medical Scan</span>
              </div>
            )}

            <div className={`sm:col-span-2 p-5 rounded-xl border space-y-3 ${
              pred.risk_category === 'High'
                ? 'bg-rose-50 border-rose-200 text-rose-950'
                : pred.risk_category === 'Moderate'
                ? 'bg-amber-50 border-amber-200 text-amber-950'
                : 'bg-emerald-50 border-emerald-200 text-emerald-950'
            }`}>
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold uppercase tracking-wider">Classification Outcome</span>
                <span className="font-bold px-2 py-0.5 rounded bg-white border border-current text-[11px]">
                  {pred.risk_category.toUpperCase()} RISK
                </span>
              </div>
              <h4 className="text-2xl font-black">{pred.prediction_label}</h4>
              <div className="flex justify-between items-center text-xs pt-2 border-t border-current/20">
                <span>Calculated Confidence: <strong>{(pred.confidence_score * 100).toFixed(1)}%</strong></span>
                <span>Inference Latency: <strong>{pred.processing_time_ms} ms</strong></span>
              </div>
            </div>
          </div>
        </div>

        {/* Section 3: Technical Telemetry */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            3. Classical & Quantum Telemetry
          </h3>
          <div className="grid sm:grid-cols-2 gap-4 text-xs">
            <div className="p-3.5 rounded-xl border border-slate-200 bg-slate-50 space-y-1">
              <span className="font-bold text-slate-800 block">Classical Vision (Swin Transformer)</span>
              <p className="text-[11px] text-slate-600">
                Hierarchical patch embedding & windowed self-attention. Reduced 768-D representation to 4-D angular space.
              </p>
            </div>
            <div className="p-3.5 rounded-xl border border-slate-200 bg-purple-50/50 space-y-1">
              <span className="font-bold text-purple-900 block">PennyLane Variational Quantum Circuit</span>
              <p className="text-[11px] text-purple-800">
                4-Qubit simulator. Ring CNOT entanglement. Pauli-Z expectation values:
                <span className="font-mono block mt-1 font-bold">
                  {JSON.stringify(pred.quantum_features)}
                </span>
              </p>
            </div>
          </div>
        </div>

        {/* Section 4: Algorithmic Explanation */}
        <div className="space-y-2 text-xs">
          <h3 className="font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            4. Explanation Summary
          </h3>
          <p className="text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-200">
            {pred.explanation}
          </p>
        </div>

        {/* Sign-off footer */}
        <div className="pt-8 border-t border-slate-200 grid grid-cols-2 gap-8 text-xs text-slate-500">
          <div>
            <span className="block font-semibold text-slate-700">Reviewing Physician / Clinician:</span>
            <span className="block mt-4 border-b border-slate-300 w-48"></span>
          </div>
          <div className="text-right">
            <span className="block font-semibold text-slate-700">QuantumCare Platform Version:</span>
            <span className="font-mono text-[11px]">1.0.0 (Production Build)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
