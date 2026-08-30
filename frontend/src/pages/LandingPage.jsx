import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Cpu,
  Activity,
  ArrowRight,
  Sparkles,
  Microscope
} from 'lucide-react';
import { Navbar } from '../components/Navbar';
import { Button } from '../components/Button';

export const LandingPage = () => {
  const navigate = useNavigate();

  const steps = [
    { num: '01', title: 'Patient Data', desc: 'Secure clinical metadata & optional biomarker intake' },
    { num: '02', title: 'Medical Image', desc: 'High-resolution histopathology or radiologic scan upload' },
    { num: '03', title: 'Image Preprocessing', desc: 'Standardization to 224×224 RGB with ImageNet normalization' },
    { num: '04', title: 'Classical ML', desc: 'Swin Transformer hierarchical shifted-window feature extraction' },
    { num: '05', title: 'Feature Extraction', desc: 'Projection from 768-D vision representation to 4-D latent vector' },
    { num: '06', title: 'Quantum ML', desc: 'Angle embedding & 4-qubit Variational Quantum Circuit execution' },
    { num: '07', title: 'Hybrid Prediction', desc: 'Pauli-Z expectation synthesis & decision layer' },
    { num: '08', title: 'Clinical Report', desc: 'Instant risk stratification and PDF report generation' }
  ];

  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-28 bg-gradient-to-b from-slate-50 to-white border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 border border-brand-200 text-brand-700 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              <span>Hybrid Classical-Quantum AI Platform</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight">
              Early Disease Detection with <span className="bg-gradient-to-r from-brand-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">Hybrid Quantum AI</span>
            </h1>

            <p className="text-lg text-slate-600 leading-relaxed">
              Explore the computational frontier of early pathology detection. Combining the visual representation power of <strong>Swin Transformers</strong> with the high-dimensional Hilbert-space transformations of <strong>PennyLane Variational Quantum Circuits</strong>.
            </p>

            <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
              <Button
                variant="quantum"
                size="lg"
                icon={ArrowRight}
                onClick={() => navigate('/register')}
              >
                Get Started
              </Button>
              <Button
                variant="secondary"
                size="lg"
                onClick={() => navigate('/login')}
              >
                Sign In to Platform
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section id="problem" className="py-16 lg:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto text-center mb-12">
            <h2 className="text-xs font-bold uppercase tracking-wider text-brand-600">The Clinical Challenge</h2>
            <h3 className="text-3xl font-bold text-slate-900 mt-2">
              Why Early Disease Screening Demands Advanced Computational Assistance
            </h3>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:shadow-md transition-all">
              <div className="p-3 bg-rose-50 text-rose-600 rounded-xl w-fit mb-4">
                <Microscope className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-slate-900 mb-2">Early Detection is Challenging</h4>
              <p className="text-sm text-slate-600 leading-relaxed">
                Subtle micro-structural tissue cellular alterations in early-stage lesions are often imperceptible in initial screenings, requiring high-sensitivity feature extraction.
              </p>
            </div>

            <div className="p-6 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:shadow-md transition-all">
              <div className="p-3 bg-amber-50 text-amber-600 rounded-xl w-fit mb-4">
                <Activity className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-slate-900 mb-2">Time-Intensive Image Auditing</h4>
              <p className="text-sm text-slate-600 leading-relaxed">
                Pathologists and radiologists review thousands of scan slices daily. Computational assistance tools provide rapid preliminary categorization to prioritize reviews.
              </p>
            </div>

            <div className="p-6 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:shadow-md transition-all">
              <div className="p-3 bg-brand-50 text-brand-600 rounded-xl w-fit mb-4">
                <Cpu className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-slate-900 mb-2">Augmenting Medical Professionals</h4>
              <p className="text-sm text-slate-600 leading-relaxed">
                Quantum neural network layers map subtle features into quantum Hilbert spaces, discovering subtle correlations beyond classical feature representations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section id="solution" className="py-16 lg:py-24 bg-slate-900 text-white relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <span className="text-xs font-bold uppercase tracking-wider text-purple-400">Architecture</span>
            <h3 className="text-3xl sm:text-4xl font-black mt-2">
              Hybrid Classical-Quantum Architecture
            </h3>
            <p className="text-sm text-slate-300 mt-3 leading-relaxed">
              Bridging the best of deep visual representations and variational quantum circuit topology.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div className="space-y-6">
              <div className="p-6 rounded-2xl bg-slate-800/80 border border-slate-700 space-y-2">
                <h4 className="text-lg font-bold text-white flex items-center gap-2">
                  <Cpu className="w-5 h-5 text-brand-400" />
                  Swin Transformer Vision Backbone
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Processes raw 224×224 RGB pathology images via shifted windows to extract rich 768-dimensional latent representations.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-slate-800/80 border border-slate-700 space-y-2">
                <h4 className="text-lg font-bold text-white flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-purple-400" />
                  PennyLane Variational Quantum Circuit
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Encodes reduced features via angle embedding on 4 qubits, entangled via CNOT gates, measuring Pauli-Z expectations.
                </p>
              </div>
            </div>

            <div className="bg-slate-950 p-6 rounded-2xl border border-slate-800 font-mono text-xs text-slate-300 space-y-3">
              <div className="flex justify-between items-center text-slate-400 border-b border-slate-800 pb-2">
                <span>Computational Pipeline Trace</span>
                <span className="text-emerald-400">● LIVE</span>
              </div>
              <div className="space-y-2 text-[11px]">
                <div className="bg-slate-900 p-3 rounded-lg border border-slate-700 flex justify-between items-center">
                  <span className="text-slate-300">Image Tensor [3, 224, 224]</span>
                  <span className="text-brand-400">Preprocessed</span>
                </div>
                <div className="flex justify-center text-slate-500">↓</div>
                <div className="bg-slate-900 p-3 rounded-lg border border-slate-700 flex justify-between items-center">
                  <span className="text-slate-300">Swin-T Patch Embeddings</span>
                  <span className="text-purple-400">768-D Vector</span>
                </div>
                <div className="flex justify-center text-slate-500">↓</div>
                <div className="bg-slate-900 p-3 rounded-lg border border-slate-700 flex justify-between items-center">
                  <span className="text-slate-300">Angle Encoding & PennyLane VQC</span>
                  <span className="text-emerald-400">4 Qubits (Ring CNOT)</span>
                </div>
                <div className="flex justify-center text-slate-500">↓</div>
                <div className="bg-slate-900 p-3 rounded-lg border border-slate-700 flex justify-between items-center">
                  <span className="text-slate-300">Pauli-Z Observable Measurement ⟨Z_i⟩</span>
                  <span className="text-amber-400">Expectation [-1, 1]</span>
                </div>
                <div className="flex justify-center text-slate-500">↓</div>
                <div className="bg-brand-950 p-3 rounded-lg border border-brand-700 flex justify-between items-center">
                  <span className="text-white font-bold">Hybrid Decision Layer</span>
                  <span className="text-brand-300 font-bold">Risk Stratification</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-16 lg:py-24 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto text-center mb-16">
            <h2 className="text-xs font-bold uppercase tracking-wider text-brand-600">End-to-End Workflow</h2>
            <h3 className="text-3xl font-bold text-slate-900 mt-2">How QuantumCare Operates</h3>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((step, idx) => (
              <div key={idx} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm relative">
                <span className="text-3xl font-black text-slate-200 absolute top-4 right-4">{step.num}</span>
                <div className="w-8 h-8 rounded-lg bg-brand-50 text-brand-600 flex items-center justify-center font-bold text-xs mb-4">
                  {idx + 1}
                </div>
                <h4 className="text-base font-bold text-slate-900 mb-1">{step.title}</h4>
                <p className="text-xs text-slate-500 leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-brand-600 text-white">
                <Cpu className="w-4 h-4" />
              </div>
              <span className="font-bold text-slate-900">QuantumCare Platform</span>
            </div>
            <p className="text-xs text-slate-500">
              © {new Date().getFullYear()} QuantumCare Platform. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};
