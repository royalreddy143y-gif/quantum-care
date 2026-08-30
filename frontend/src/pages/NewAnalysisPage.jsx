import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  ArrowRight,
  AlertCircle,
  Sparkles
} from 'lucide-react';
import { patientService } from '../services/patientService';
import { analysisService } from '../services/analysisService';
import { ImageUploader } from '../components/ImageUploader';
import { Card, Loader } from '../components/Card';
import { Button } from '../components/Button';

export const NewAnalysisPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const preselectedPatientId = searchParams.get('patient_id');

  const [patients, setPatients] = useState([]);
  const [selectedPatientId, setSelectedPatientId] = useState(preselectedPatientId || '');
  const [targetCondition, setTargetCondition] = useState('Histopathologic Tissue Lesion');
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetchingPatients, setFetchingPatients] = useState(true);
  const [error, setError] = useState('');

  // Sample image generator for quick testing
  const handleLoadSampleScan = async () => {
    const canvas = document.createElement('canvas');
    canvas.width = 224;
    canvas.height = 224;
    const ctx = canvas.getContext('2d');

    // Background medical scan texture
    const grad = ctx.createRadialGradient(112, 112, 10, 112, 112, 110);
    grad.addColorStop(0, '#7dd3fc');
    grad.addColorStop(0.4, '#0284c7');
    grad.addColorStop(0.8, '#0f172a');
    grad.addColorStop(1, '#020617');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 224, 224);

    // Simulate cellular clusters
    ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
    for (let i = 0; i < 25; i++) {
      const x = 50 + Math.random() * 124;
      const y = 50 + Math.random() * 124;
      const r = 4 + Math.random() * 12;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }

    canvas.toBlob((blob) => {
      const file = new File([blob], "sample_histology_scan.png", { type: "image/png" });
      setSelectedFile(file);
    }, 'image/png');
  };

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const data = await patientService.getPatients();
        setPatients(data);
        if (data.length > 0 && !selectedPatientId) {
          setSelectedPatientId(String(data[0].id));
        }
      } catch (err) {
        console.error(err);
      } finally {
        setFetchingPatients(false);
      }
    };
    fetchPatients();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!selectedPatientId) {
      setError('Please select or create a target patient record.');
      return;
    }

    if (!selectedFile) {
      setError('Please upload a valid medical image scan (JPEG or PNG).');
      return;
    }

    setLoading(true);

    try {
      // 1. Upload medical image to backend
      const uploadResp = await analysisService.uploadMedicalImage(
        selectedPatientId,
        selectedFile,
        'medical_scan'
      );

      // Navigate to the interactive pipeline processor with uploaded IDs
      navigate('/analyses/process', {
        state: {
          patientId: parseInt(selectedPatientId, 10),
          imageId: uploadResp.id,
          targetCondition,
          executionMode: 'hybrid',
          imagePreview: URL.createObjectURL(selectedFile)
        }
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload medical scan for analysis.');
      setLoading(false);
    }
  };

  if (fetchingPatients) {
    return <Loader message="Preparing clinical workspace..." />;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Initiate Hybrid Quantum Analysis</h2>
        <p className="text-xs text-slate-500 mt-1">
          Submit medical scans to the Swin Transformer and PennyLane Variational Quantum Circuit pipeline
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card title="1. Patient & Case Selection">
          {error && (
            <div className="mb-4 p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2 text-rose-800 text-xs font-medium">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
              <span>{error}</span>
            </div>
          )}

          <div className="grid sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Select Patient Record *
              </label>
              {patients.length === 0 ? (
                <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg text-amber-900 flex justify-between items-center">
                  <span>No patients available.</span>
                  <Button variant="quantum" size="sm" onClick={() => navigate('/patients')}>
                    Create Patient
                  </Button>
                </div>
              ) : (
                <select
                  value={selectedPatientId}
                  onChange={(e) => setSelectedPatientId(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white font-medium text-slate-800"
                >
                  {patients.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name} ({p.patient_id}) — {p.age}y/{p.gender}
                    </option>
                  ))}
                </select>
              )}
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Target Anomaly / Tissue Focus *
              </label>
              <select
                value={targetCondition}
                onChange={(e) => setTargetCondition(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white font-medium text-slate-800"
              >
                <option value="Histopathologic Tissue Lesion">Histopathologic Tissue Lesion</option>
                <option value="Pulmonary Nodule & Opacity">Pulmonary Nodule & Opacity (Chest X-Ray)</option>
                <option value="Dermoscopic Melanocytic Lesion">Dermoscopic Melanocytic Lesion</option>
                <option value="General Cellular & Tissue Anomaly">General Cellular & Tissue Anomaly</option>
              </select>
            </div>
          </div>
        </Card>

        <Card
          title="2. Upload Medical Scan"
          subtitle="Supports high-resolution PNG, JPG, or JPEG raster imaging (max 10MB)"
          action={
            <button
              type="button"
              onClick={handleLoadSampleScan}
              className="text-xs text-brand-600 hover:text-brand-700 font-semibold flex items-center gap-1"
            >
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              Load Sample Histology Scan
            </button>
          }
        >
          <ImageUploader
            selectedImage={selectedFile ? { name: selectedFile.name, size: selectedFile.size, preview: URL.createObjectURL(selectedFile) } : null}
            onImageSelect={(file) => setSelectedFile(file)}
            onClearImage={() => setSelectedFile(null)}
          />
        </Card>

        <Card title="3. Computational Engine Configuration">
          <div className="grid sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Quantum Simulator Backend
              </label>
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 flex items-center justify-between">
                <span>PennyLane Variational Quantum Circuit</span>
                <span className="font-mono text-purple-600 font-bold">4 Qubits</span>
              </div>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Classical Feature Backbone
              </label>
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 flex items-center justify-between">
                <span>Swin Transformer (Shifted-Window Attention)</span>
                <span className="font-mono text-brand-600 font-bold">768-D</span>
              </div>
            </div>
          </div>
        </Card>

        <div className="flex justify-end gap-3 pt-2">
          <Button
            variant="secondary"
            size="lg"
            onClick={() => navigate('/dashboard')}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            variant="quantum"
            size="lg"
            isLoading={loading}
            icon={ArrowRight}
          >
            Launch Hybrid Quantum Pipeline
          </Button>
        </div>
      </form>
    </div>
  );
};
