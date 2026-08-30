import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  CheckCircle2,
  Loader2,
  Cpu,
  ShieldAlert
} from 'lucide-react';
import { analysisService } from '../services/analysisService';
import { Card } from '../components/Card';
import { ProgressBar } from '../components/Card';

export const AnalysisProcessPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state;

  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(15);
  const [statusMessage, setStatusMessage] = useState("Preparing image...");
  const [error, setError] = useState('');

  const pipelineSteps = [
    { title: "Image Preprocessing", message: "Preparing image & standardizing to 224×224 RGB..." },
    { title: "Classical ML Analysis", message: "Running classical model (Swin Transformer)..." },
    { title: "Feature Extraction", message: "Extracting features (768-D to 4-D projection)..." },
    { title: "Quantum ML Processing", message: "Running quantum model (PennyLane 4-Qubit VQC)..." },
    { title: "Hybrid Prediction", message: "Generating result & synthesizing risk score..." }
  ];

  useEffect(() => {
    if (!state?.patientId || !state?.imageId) {
      navigate('/analyses/new');
      return;
    }

    let isMounted = true;

    const executePipeline = async () => {
      try {
        // Step 1: Preprocessing
        setCurrentStep(0);
        setStatusMessage("Preparing image...");
        setProgress(20);
        await new Promise(r => setTimeout(r, 600));

        // Step 2: Classical ML Analysis
        if (!isMounted) return;
        setCurrentStep(1);
        setStatusMessage("Running classical model...");
        setProgress(40);
        await new Promise(r => setTimeout(r, 600));

        // Step 3: Feature Extraction
        if (!isMounted) return;
        setCurrentStep(2);
        setStatusMessage("Extracting features...");
        setProgress(60);

        // Call backend prediction API
        const response = await analysisService.runPrediction({
          patient_id: state.patientId,
          image_id: state.imageId,
          target_condition: state.targetCondition
        });

        // Step 4: Quantum ML Processing
        if (!isMounted) return;
        setCurrentStep(3);
        setStatusMessage("Running quantum model...");
        setProgress(85);
        await new Promise(r => setTimeout(r, 700));

        // Step 5: Hybrid Prediction Synthesis
        if (!isMounted) return;
        setCurrentStep(4);
        setStatusMessage("Generating result...");
        setProgress(100);

        // Transition to Result page
        await new Promise(r => setTimeout(r, 600));
        if (isMounted) {
          navigate(`/analyses/${response.id}/result`);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.response?.data?.detail || "Inference pipeline encountered an execution error.");
        }
      }
    };

    executePipeline();

    return () => {
      isMounted = false;
    };
  }, [state, navigate]);

  return (
    <div className="max-w-3xl mx-auto space-y-6 py-6">
      <div className="text-center space-y-2">
        <span className="px-3 py-1 rounded-full bg-purple-50 text-purple-700 border border-purple-200 text-xs font-bold uppercase tracking-wider inline-flex items-center gap-1.5">
          <Cpu className="w-3.5 h-3.5" />
          QuantumCare Hybrid Engine
        </span>
        <h2 className="text-2xl font-black text-slate-900">Executing Computational Pipeline</h2>
        <p className="text-xs text-slate-500">
          Target: {state?.targetCondition || "Tissue Lesion Analysis"}
        </p>
      </div>

      {error ? (
        <Card className="border-rose-200 bg-rose-50/50">
          <div className="text-center py-6 space-y-3">
            <ShieldAlert className="w-8 h-8 text-rose-600 mx-auto" />
            <h4 className="font-bold text-rose-900 text-sm">Pipeline Execution Error</h4>
            <p className="text-xs text-rose-700 max-w-md mx-auto">{error}</p>
            <button
              onClick={() => navigate('/analyses/new')}
              className="mt-2 px-4 py-2 bg-white border border-rose-300 rounded-lg text-xs font-semibold text-rose-800 hover:bg-rose-50 shadow-xs"
            >
              Return to Upload Form
            </button>
          </div>
        </Card>
      ) : (
        <Card className="space-y-6">
          {/* Progress Bar & Status Text */}
          <div className="space-y-2">
            <ProgressBar progress={progress} label={statusMessage} color="quantum" />
          </div>

          {/* Stepper Pipeline Visualizer */}
          <div className="space-y-3">
            {pipelineSteps.map((step, idx) => {
              const isDone = currentStep > idx;
              const isCurrent = currentStep === idx;

              return (
                <div
                  key={idx}
                  className={`flex items-center justify-between p-3.5 rounded-xl border transition-all ${
                    isCurrent
                      ? 'bg-purple-50/80 border-purple-300 shadow-xs'
                      : isDone
                      ? 'bg-slate-50/80 border-slate-200 text-slate-700'
                      : 'border-slate-100 text-slate-400 opacity-60'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-6 h-6 rounded-full font-bold text-xs">
                      {isDone ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                      ) : isCurrent ? (
                        <Loader2 className="w-5 h-5 text-purple-600 animate-spin" />
                      ) : (
                        <span className="w-5 h-5 rounded-full border border-slate-300 flex items-center justify-center text-[10px] text-slate-400">
                          {idx + 1}
                        </span>
                      )}
                    </div>
                    <div>
                      <h4 className={`text-xs font-bold ${isCurrent ? 'text-purple-950' : 'text-slate-800'}`}>
                        {step.title}
                      </h4>
                      <p className="text-[11px] text-slate-500">
                        {isCurrent ? step.message : step.title}
                      </p>
                    </div>
                  </div>

                  <span className="text-[10px] uppercase font-mono font-semibold">
                    {isDone ? 'Completed' : isCurrent ? 'Running...' : 'Queued'}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Image Thumbnail & Quantum Telemetry preview */}
          {state?.imagePreview && (
            <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
              <div className="flex items-center gap-3">
                <img
                  src={state.imagePreview}
                  alt="Scan thumbnail"
                  className="w-12 h-12 object-cover rounded-lg border border-slate-200 shadow-xs"
                />
                <div>
                  <span className="font-semibold text-slate-700 block">Active Scan Buffer</span>
                  <span className="text-[10px]">Image standardized for Swin-T patch partitioning</span>
                </div>
              </div>
              <div className="text-right">
                <span className="font-mono text-purple-600 font-bold block">default.qubit</span>
                <span className="text-[10px]">4 wires • CNOT Ring</span>
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
};
