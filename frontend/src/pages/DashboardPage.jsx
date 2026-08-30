import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Users,
  Activity,
  PlusCircle,
  Cpu,
  ArrowRight,
  ShieldCheck
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { patientService } from '../services/patientService';
import { analysisService } from '../services/analysisService';
import { Card, Badge, Loader } from '../components/Card';
import { Button } from '../components/Button';

export const DashboardPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);
  const [analyses, setAnalyses] = useState([]);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [patientsData, analysesData, healthData] = await Promise.allSettled([
          patientService.getPatients('', 0, 5),
          analysisService.getAnalyses(),
          analysisService.getSystemHealth()
        ]);
        if (patientsData.status === 'fulfilled') setPatients(patientsData.value);
        if (analysesData.status === 'fulfilled') setAnalyses(analysesData.value);
        if (healthData.status === 'fulfilled') setHealth(healthData.value);
      } catch (err) {
        console.error("Error loading dashboard data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <Loader message="Loading dashboard & system status..." />;
  }

  const completedCount = analyses.filter(a => a.status === 'COMPLETED').length;
  const recentAnalyses = analyses.slice(0, 6);

  return (
    <div className="space-y-8">
      {/* Top Welcome Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-brand-950 to-purple-950 rounded-2xl p-6 sm:p-8 text-white shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-400/30 text-xs font-semibold">
              Hybrid Intelligence Platform
            </span>
            <span className="text-xs text-slate-400">
              System Active
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome back, {user?.full_name || 'User'}
          </h2>
          <p className="text-sm text-slate-300 max-w-xl">
            Classical Vision (Swin-T) & PennyLane {health?.quantum_qubits || 4}-Qubit Variational Quantum Layer active.
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <Button
            variant="quantum"
            size="md"
            icon={PlusCircle}
            onClick={() => navigate('/analyses/new')}
          >
            New Analysis
          </Button>
          <Button
            variant="secondary"
            size="md"
            icon={Users}
            onClick={() => navigate('/patients')}
          >
            Manage Patients
          </Button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-500">Registered Patients</p>
            <h3 className="text-2xl font-black text-slate-900 mt-1">{patients.length}</h3>
            <p className="text-[11px] text-brand-600 mt-0.5">Active records</p>
          </div>
          <div className="p-3 bg-brand-50 text-brand-600 rounded-xl">
            <Users className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-500">Completed Analyses</p>
            <h3 className="text-2xl font-black text-slate-900 mt-1">{completedCount}</h3>
            <p className="text-[11px] text-emerald-600 mt-0.5">Evaluations performed</p>
          </div>
          <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
            <Activity className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-500">Quantum Processing</p>
            <h3 className="text-2xl font-black text-slate-900 mt-1">4 Qubits</h3>
            <p className="text-[11px] text-purple-600 mt-0.5">PennyLane VQC Layer</p>
          </div>
          <div className="p-3 bg-purple-50 text-purple-600 rounded-xl">
            <Cpu className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-500">System Status</p>
            <h3 className="text-2xl font-black text-slate-900 mt-1">Online</h3>
            <p className="text-[11px] text-slate-500 mt-0.5">PyTorch • VQC Active</p>
          </div>
          <div className="p-3 bg-blue-50 text-blue-600 rounded-xl">
            <ShieldCheck className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Recent Analyses Section */}
      <Card
        title="Recent QuantumCare Analyses"
        subtitle="Recent hybrid image evaluations and quantum expectation measurements"
        action={
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/history')}
            icon={ArrowRight}
          >
            View All
          </Button>
        }
      >
        {recentAnalyses.length === 0 ? (
          <div className="text-center py-12 space-y-3">
            <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-400">
              <Activity className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-semibold text-slate-700">No analyses generated yet</h4>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Initiate your first hybrid Swin Transformer + PennyLane quantum evaluation.
            </p>
            <Button
              variant="quantum"
              size="sm"
              icon={PlusCircle}
              onClick={() => navigate('/analyses/new')}
            >
              Start New Analysis
            </Button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-100 text-slate-500 uppercase tracking-wider font-semibold">
                  <th className="pb-3 px-2">Analysis Ref</th>
                  <th className="pb-3 px-2">Patient</th>
                  <th className="pb-3 px-2">Condition</th>
                  <th className="pb-3 px-2">Prediction Outcome</th>
                  <th className="pb-3 px-2">Confidence</th>
                  <th className="pb-3 px-2">Risk Level</th>
                  <th className="pb-3 px-2 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {recentAnalyses.map((item) => {
                  const pred = item.prediction;
                  const isHigh = pred?.risk_category === 'High';
                  const isModerate = pred?.risk_category === 'Moderate';
                  return (
                    <tr key={item.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3 px-2 font-mono text-slate-700 font-semibold">
                        {item.analysis_code}
                      </td>
                      <td className="py-3 px-2 text-slate-900">
                        {item.patient?.name || `Patient #${item.patient_id}`}
                      </td>
                      <td className="py-3 px-2 text-slate-600 truncate max-w-[140px]">
                        {item.target_condition}
                      </td>
                      <td className="py-3 px-2 text-slate-900 font-semibold">
                        {pred ? pred.prediction_label : 'Pending'}
                      </td>
                      <td className="py-3 px-2 text-slate-700">
                        {pred ? `${(pred.confidence_score * 100).toFixed(1)}%` : '—'}
                      </td>
                      <td className="py-3 px-2">
                        {pred ? (
                          <Badge
                            variant={isHigh ? 'danger' : isModerate ? 'warning' : 'success'}
                            size="sm"
                          >
                            {pred.risk_category}
                          </Badge>
                        ) : (
                          <Badge variant="slate" size="sm">Evaluating</Badge>
                        )}
                      </td>
                      <td className="py-3 px-2 text-right">
                        <Button
                          variant="secondary"
                          size="sm"
                          onClick={() => navigate(`/analyses/${item.id}/result`)}
                        >
                          View Result
                        </Button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
};
