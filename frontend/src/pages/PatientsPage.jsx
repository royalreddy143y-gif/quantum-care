import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Users,
  Plus,
  Search,
  Eye,
  Edit,
  Trash2,
  AlertCircle
} from 'lucide-react';
import { patientService } from '../services/patientService';
import { Card, Badge, Loader } from '../components/Card';
import { Button } from '../components/Button';
import { Modal } from '../components/Modal';

export const PatientsPage = () => {
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  
  // Add modal state
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [addLoading, setAddLoading] = useState(false);
  
  // Edit modal state
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editLoading, setEditLoading] = useState(false);
  const [editingPatientId, setEditingPatientId] = useState(null);

  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    patient_id: `QC-2025-${Math.floor(100 + Math.random() * 900)}`,
    name: '',
    age: 45,
    gender: 'Female',
    symptoms: '',
    medical_history: '',
    biomarkers: { ca125: '', psa: '', cea: '' },
    genomics: { brca1_mutation: false, egfr_mutation: 'wild_type' }
  });

  const [editFormData, setEditFormData] = useState({
    name: '',
    age: 45,
    gender: 'Female',
    symptoms: '',
    medical_history: ''
  });

  const fetchPatients = async (query = '') => {
    try {
      setLoading(true);
      const data = await patientService.getPatients(query);
      setPatients(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients(search);
  }, [search]);

  const handleCreatePatient = async (e) => {
    e.preventDefault();
    setError('');
    setAddLoading(true);
    try {
      const cleanedBiomarkers = {};
      if (formData.biomarkers.ca125) cleanedBiomarkers.ca125 = parseFloat(formData.biomarkers.ca125);
      if (formData.biomarkers.psa) cleanedBiomarkers.psa = parseFloat(formData.biomarkers.psa);
      if (formData.biomarkers.cea) cleanedBiomarkers.cea = parseFloat(formData.biomarkers.cea);

      const payload = {
        patient_id: formData.patient_id,
        name: formData.name,
        age: parseInt(formData.age, 10),
        gender: formData.gender,
        symptoms: formData.symptoms || null,
        medical_history: formData.medical_history || null,
        biomarkers: Object.keys(cleanedBiomarkers).length > 0 ? cleanedBiomarkers : null,
        genomics: formData.genomics || null
      };

      await patientService.createPatient(payload);
      setIsAddModalOpen(false);
      // Reset form ID for next
      setFormData({
        patient_id: `QC-2025-${Math.floor(100 + Math.random() * 900)}`,
        name: '',
        age: 45,
        gender: 'Female',
        symptoms: '',
        medical_history: '',
        biomarkers: { ca125: '', psa: '', cea: '' },
        genomics: { brca1_mutation: false, egfr_mutation: 'wild_type' }
      });
      fetchPatients();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create patient record.');
    } finally {
      setAddLoading(false);
    }
  };

  const handleOpenEdit = (patient) => {
    setEditingPatientId(patient.id);
    setEditFormData({
      name: patient.name,
      age: patient.age,
      gender: patient.gender,
      symptoms: patient.symptoms || '',
      medical_history: patient.medical_history || ''
    });
    setError('');
    setIsEditModalOpen(true);
  };

  const handleUpdatePatient = async (e) => {
    e.preventDefault();
    setError('');
    setEditLoading(true);
    try {
      await patientService.updatePatient(editingPatientId, {
        name: editFormData.name,
        age: parseInt(editFormData.age, 10),
        gender: editFormData.gender,
        symptoms: editFormData.symptoms || null,
        medical_history: editFormData.medical_history || null
      });
      setIsEditModalOpen(false);
      fetchPatients(search);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update patient record.');
    } finally {
      setEditLoading(false);
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to delete patient record for ${name}?`)) return;
    try {
      await patientService.deletePatient(id);
      fetchPatients(search);
    } catch (err) {
      alert("Error deleting patient record.");
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Patient Directory</h2>
          <p className="text-xs text-slate-500 mt-1">
            Maintain clinical patient histories, demographics, and link imaging scans
          </p>
        </div>
        <Button
          variant="quantum"
          size="md"
          icon={Plus}
          onClick={() => {
            setError('');
            setIsAddModalOpen(true);
          }}
        >
          Add New Patient
        </Button>
      </div>

      {/* Search Bar */}
      <div className="relative max-w-md">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
          <Search className="h-4 w-4" />
        </div>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by patient name or ID..."
          className="block w-full pl-10 pr-4 py-2 text-sm border border-slate-200 rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-brand-500 shadow-xs"
        />
      </div>

      {/* Patient Table Card */}
      <Card>
        {loading ? (
          <Loader message="Fetching patient records..." />
        ) : patients.length === 0 ? (
          <div className="text-center py-12 space-y-3">
            <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-400">
              <Users className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-semibold text-slate-800">No patients found</h4>
            <p className="text-xs text-slate-500 max-w-xs mx-auto">
              Create a new patient record to initiate medical scan uploads and hybrid QML runs.
            </p>
            <Button
              variant="quantum"
              size="sm"
              icon={Plus}
              onClick={() => {
                setError('');
                setIsAddModalOpen(true);
              }}
            >
              Add First Patient
            </Button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-100 text-slate-400 uppercase tracking-wider font-semibold">
                  <th className="pb-3 px-3">Patient ID</th>
                  <th className="pb-3 px-3">Name</th>
                  <th className="pb-3 px-3">Age / Gender</th>
                  <th className="pb-3 px-3">Symptoms / History</th>
                  <th className="pb-3 px-3">Profile Type</th>
                  <th className="pb-3 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {patients.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-3 px-3 font-mono font-bold text-brand-700">
                      {p.patient_id}
                    </td>
                    <td className="py-3 px-3 font-semibold text-slate-900">
                      {p.name}
                    </td>
                    <td className="py-3 px-3 text-slate-600">
                      {p.age} yrs • {p.gender}
                    </td>
                    <td className="py-3 px-3 text-slate-500 truncate max-w-[200px]">
                      {p.symptoms || p.medical_history || 'No recorded history'}
                    </td>
                    <td className="py-3 px-3">
                      {p.biomarkers || p.genomics ? (
                        <Badge variant="quantum" size="sm">Multi-Omics</Badge>
                      ) : (
                        <Badge variant="slate" size="sm">Standard</Badge>
                      )}
                    </td>
                    <td className="py-3 px-3 text-right space-x-1">
                      <Button
                        variant="secondary"
                        size="sm"
                        icon={Eye}
                        onClick={() => navigate(`/patients/${p.id}`)}
                      >
                        Profile
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        icon={Edit}
                        onClick={() => handleOpenEdit(p)}
                        title="Edit patient"
                      >
                        Edit
                      </Button>
                      <button
                        onClick={() => handleDelete(p.id, p.name)}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                        title="Delete patient"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      {/* New Patient Modal */}
      <Modal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        title="Add New Patient Record"
        size="lg"
      >
        <form onSubmit={handleCreatePatient} className="space-y-4 text-xs">
          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2 text-rose-800 font-medium">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
              <span>{error}</span>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Patient Identifier *</label>
              <input
                type="text"
                required
                value={formData.patient_id}
                onChange={(e) => setFormData({ ...formData, patient_id: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Full Name *</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Enter patient full name"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Age *</label>
              <input
                type="number"
                required
                min="0"
                max="130"
                value={formData.age}
                onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Gender *</label>
              <select
                value={formData.gender}
                onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
              >
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Reported Symptoms</label>
            <textarea
              rows="2"
              value={formData.symptoms}
              onChange={(e) => setFormData({ ...formData, symptoms: e.target.value })}
              placeholder="e.g. Asymptomatic routine screening follow-up; mild chest pain..."
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Medical & Family History</label>
            <textarea
              rows="2"
              value={formData.medical_history}
              onChange={(e) => setFormData({ ...formData, medical_history: e.target.value })}
              placeholder="e.g. Family history of lesions, hypertension..."
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
            />
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <Button
              variant="secondary"
              size="md"
              onClick={() => setIsAddModalOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="quantum"
              size="md"
              isLoading={addLoading}
            >
              Save Patient Record
            </Button>
          </div>
        </form>
      </Modal>

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
