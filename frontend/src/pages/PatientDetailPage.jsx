import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  PlusCircle,
  Edit,
  AlertCircle
} from 'lucide-react';
import { patientService } from '../services/patientService';
import { analysisService } from '../services/analysisService';
import { Card, Loader } from '../components/Card';
import { Button } from '../components/Button';
import { Modal } from '../components/Modal';

export const PatientDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [patient, setPatient] = useState(null);
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);

  // Edit modal
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editLoading, setEditLoading] = useState(false);
  const [error, setError] = useState('');
  const [editFormData, setEditFormData] = useState({
    name: '',
    age: 45,
    gender: 'Female',
    symptoms: '',
    medical_history: ''
  });

  const fetchProfile = async () => {
    try {
      const [patientData, analysesData] = await Promise.all([
        patientService.getPatient(id),
        analysisService.getAnalyses(id)
      ]);
      setPatient(patientData);
      setAnalyses(analysesData);
      setEditFormData({
        name: patientData.name,
        age: patientData.age,
        gender: patientData.gender,
        symptoms: patientData.symptoms || '',
        medical_history: patientData.medical_history || ''
      });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, [id]);

  const handleUpdatePatient = async (e) => {
    e.preventDefault();
    setError('');
    setEditLoading(true);
    try {
      await patientService.updatePatient(id, {
        name: editFormData.name,
        age: parseInt(editFormData.age, 10),
        gender: editFormData.gender,
        symptoms: editFormData.symptoms || null,
        medical_history: editFormData.medical_history || null
      });
      setIsEditModalOpen(false);
      fetchProfile();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update patient record.');
    } finally {
      setEditLoading(false);
    }
  };

  if (loading) {
    return <Loader message="Loading patient profile..." />;
  }

  if (!patient) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-500">Patient record not found.</p>
        <Button variant="secondary" size="sm" onClick={() => navigate('/patients')} className="mt-4">
          Back to Directory
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Back and Edit button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/patients')}
            className="p-2 rounded-xl bg-white border border-slate-200 text-slate-600 hover:text-slate-900 shadow-xs"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-2xl font-bold text-slate-900">{patient.name}</h2>
              <span className="font-mono text-xs px-2 py-0.5 rounded bg-brand-50 text-brand-700 font-bold border border-brand-200">
                {patient.patient_id}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              {patient.age} years old • {patient.gender} • Registered {new Date(patient.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="md"
            icon={Edit}
            onClick={() => setIsEditModalOpen(true)}
          >
            Edit Patient
          </Button>
          <Button
            variant="quantum"
            size="md"
            icon={PlusCircle}
            onClick={() => navigate(`/analyses/new?patient_id=${patient.id}`)}
          >
            New Analysis
          </Button>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Clinical History & Symptoms */}
        <div className="md:col-span-2 space-y-6">
          <Card title="Clinical Summary & History">
            <div className="space-y-4 text-xs">
              <div>
                <h5 className="font-semibold text-slate-700 uppercase tracking-wider text-[10px]">
                  Reported Symptoms
                </h5>
                <p className="text-slate-800 bg-slate-50 p-3 rounded-lg border border-slate-100 mt-1 leading-relaxed">
                  {patient.symptoms || "No acute symptoms reported at registration."}
                </p>
              </div>

              <div>
                <h5 className="font-semibold text-slate-700 uppercase tracking-wider text-[10px]">
                  Medical & Pathological History
                </h5>
                <p className="text-slate-800 bg-slate-50 p-3 rounded-lg border border-slate-100 mt-1 leading-relaxed">
                  {patient.medical_history || "No prior history documented in current record."}
                </p>
              </div>
            </div>
          </Card>

          {/* Previous Analyses for this Patient */}
          <Card
            title={`Analyses History (${analyses.length})`}
            subtitle="Previous evaluations for this patient"
          >
            {analyses.length === 0 ? (
              <div className="text-center py-8 text-slate-500 text-xs">
                No analyses recorded for this patient yet. Click "New Analysis" above to upload a scan.
              </div>
            ) : (
              <div className="divide-y divide-slate-100 text-xs">
                {analyses.map((an) => {
                  const pred = an.prediction;
                  return (
                    <div key={an.id} className="py-3 flex items-center justify-between hover:bg-slate-50 px-2 rounded-lg transition-colors">
                      <div className="space-y-0.5">
                        <div className="flex items-center gap-2">
                          <span className="font-mono font-bold text-slate-800">{an.analysis_code}</span>
                          <span className="text-slate-400">•</span>
                          <span className="text-slate-600">{an.target_condition}</span>
                        </div>
                        <p className="text-[11px] text-slate-400">
                          {new Date(an.created_at).toLocaleString()}
                        </p>
                      </div>

                      <div className="flex items-center gap-3">
                        {pred && (
                          <div className="text-right">
                            <span className="font-bold text-slate-900 block">{pred.prediction_label}</span>
                            <span className="text-[10px] text-slate-500">{(pred.confidence_score * 100).toFixed(1)}% conf</span>
                          </div>
                        )}
                        <Button
                          variant="secondary"
                          size="sm"
                          onClick={() => navigate(`/analyses/${an.id}/result`)}
                        >
                          View Result
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </Card>
        </div>

        {/* Multi-Omics & Biomarkers Sidebar Card */}
        <div className="space-y-6">
          <Card title="Multi-Omics Biomarkers">
            <div className="space-y-4 text-xs">
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
                  Circulating Blood Biomarkers
                </span>
                {patient.biomarkers ? (
                  <div className="space-y-2">
                    {Object.entries(patient.biomarkers).map(([key, val]) => (
                      <div key={key} className="flex justify-between p-2 rounded-lg bg-slate-50 border border-slate-100">
                        <span className="uppercase font-semibold text-slate-700">{key}</span>
                        <span className="font-mono font-bold text-brand-700">{String(val)}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-slate-400 italic">No serum biomarker assays entered.</p>
                )}
              </div>

              <div className="pt-2 border-t border-slate-100">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
                  Genomic Variant Profiling
                </span>
                {patient.genomics ? (
                  <div className="space-y-2">
                    {Object.entries(patient.genomics).map(([key, val]) => (
                      <div key={key} className="flex justify-between p-2 rounded-lg bg-purple-50/50 border border-purple-100">
                        <span className="capitalize font-semibold text-purple-900">{key.replace('_', ' ')}</span>
                        <span className="font-mono text-purple-700">{String(val)}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-slate-400 italic">No genetic markers documented.</p>
                )}
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Edit Patient Modal */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        title="Edit Patient Information"
        size="lg"
      >
        <form onSubmit={handleUpdatePatient} className="space-y-4 text-xs">
          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2 text-rose-800 font-medium">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
              <span>{error}</span>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Full Name *</label>
              <input
                type="text"
                required
                value={editFormData.name}
                onChange={(e) => setEditFormData({ ...editFormData, name: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Gender *</label>
              <select
                value={editFormData.gender}
                onChange={(e) => setEditFormData({ ...editFormData, gender: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
              >
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Age *</label>
            <input
              type="number"
              required
              min="0"
              max="130"
              value={editFormData.age}
              onChange={(e) => setEditFormData({ ...editFormData, age: e.target.value })}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Reported Symptoms</label>
            <textarea
              rows="2"
              value={editFormData.symptoms}
              onChange={(e) => setEditFormData({ ...editFormData, symptoms: e.target.value })}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Medical History</label>
            <textarea
              rows="2"
              value={editFormData.medical_history}
              onChange={(e) => setEditFormData({ ...editFormData, medical_history: e.target.value })}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
            />
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <Button
              variant="secondary"
              size="md"
              onClick={() => setIsEditModalOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="quantum"
              size="md"
              isLoading={editLoading}
            >
              Update Patient
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
