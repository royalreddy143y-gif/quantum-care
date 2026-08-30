import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  History,
  Search,
  Eye,
  Download,
  Filter,
  PlusCircle
} from 'lucide-react';
import { analysisService } from '../services/analysisService';
import { Card, Badge, Loader } from '../components/Card';
import { Button } from '../components/Button';

export const HistoryPage = () => {
  const navigate = useNavigate();
  const [analyses, setAnalyses] = useState([]);
  const [search, setSearch] = useState('');
  const [filterRisk, setFilterRisk] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalyses = async () => {
      try {
        const data = await analysisService.getAnalyses();
        setAnalyses(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalyses();
  }, []);

  const filteredAnalyses = analyses.filter(item => {
    const matchesSearch =
      item.analysis_code.toLowerCase().includes(search.toLowerCase()) ||
      (item.patient?.name && item.patient.name.toLowerCase().includes(search.toLowerCase())) ||
      (item.patient?.patient_id && item.patient.patient_id.toLowerCase().includes(search.toLowerCase())) ||
      (item.target_condition && item.target_condition.toLowerCase().includes(search.toLowerCase()));

    const matchesRisk =
      filterRisk === 'ALL' ||
      (item.prediction && item.prediction.risk_category === filterRisk);

    return matchesSearch && matchesRisk;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Analysis Audit History</h2>
          <p className="text-xs text-slate-500 mt-1">
            Complete chronological ledger of hybrid deep learning & quantum evaluations
          </p>
        </div>

        <Button
          variant="quantum"
          size="md"
          icon={PlusCircle}
          onClick={() => navigate('/analyses/new')}
        >
          Run New Analysis
        </Button>
      </div>

      {/* Filter and Search Toolbar */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:max-w-md">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <Search className="h-4 w-4" />
          </div>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by analysis code, patient name, or condition..."
            className="block w-full pl-10 pr-4 py-2 text-xs border border-slate-200 rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-brand-500 shadow-xs"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={filterRisk}
            onChange={(e) => setFilterRisk(e.target.value)}
            className="text-xs border border-slate-200 rounded-xl px-3 py-2 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500"
          >
            <option value="ALL">All Risk Strata</option>
            <option value="Low">Low Risk Only</option>
            <option value="Moderate">Moderate Risk Only</option>
            <option value="High">High Risk Only</option>
          </select>
        </div>
      </div>

      {/* Analyses Table Card */}
      <Card>
        {loading ? (
          <Loader message="Loading historical analyses..." />
        ) : filteredAnalyses.length === 0 ? (
          <div className="text-center py-12 space-y-3">
            <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-400">
              <History className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-semibold text-slate-800">No matching analyses found</h4>
            <p className="text-xs text-slate-500 max-w-xs mx-auto">
              Execute a hybrid quantum machine learning run to populate the history ledger.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-100 text-slate-400 uppercase tracking-wider font-semibold">
                  <th className="pb-3 px-3">Analysis Code</th>
                  <th className="pb-3 px-3">Patient</th>
                  <th className="pb-3 px-3">Timestamp</th>
                  <th className="pb-3 px-3">Pipeline</th>
                  <th className="pb-3 px-3">Prediction</th>
                  <th className="pb-3 px-3">Confidence</th>
                  <th className="pb-3 px-3">Risk</th>
                  <th className="pb-3 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {filteredAnalyses.map((item) => {
                  const pred = item.prediction;
                  const isHigh = pred?.risk_category === 'High';
                  const isMod = pred?.risk_category === 'Moderate';

                  return (
                    <tr key={item.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3 px-3 font-mono font-bold text-slate-900">
                        {item.analysis_code}
                      </td>
                      <td className="py-3 px-3">
                        <span className="font-semibold text-slate-800 block">
                          {item.patient?.name || `Patient #${item.patient_id}`}
                        </span>
                        <span className="text-[10px] text-slate-400 font-mono">
                          {item.patient?.patient_id}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-slate-500">
                        {new Date(item.created_at).toLocaleString()}
                      </td>
                      <td className="py-3 px-3">
                        <Badge variant="quantum" size="sm">
                          Hybrid QML
                        </Badge>
                      </td>
                      <td className="py-3 px-3 text-slate-900 font-semibold">
                        {pred ? pred.prediction_label : 'Evaluating...'}
                      </td>
                      <td className="py-3 px-3 text-slate-700">
                        {pred ? `${(pred.confidence_score * 100).toFixed(1)}%` : '—'}
                      </td>
                      <td className="py-3 px-3">
                        {pred ? (
                          <Badge
                            variant={isHigh ? 'danger' : isMod ? 'warning' : 'success'}
                            size="sm"
                          >
                            {pred.risk_category}
                          </Badge>
                        ) : (
                          <Badge variant="slate" size="sm">Running</Badge>
                        )}
                      </td>
                      <td className="py-3 px-3 text-right space-x-1">
                        <Button
                          variant="secondary"
                          size="sm"
                          icon={Eye}
                          onClick={() => navigate(`/analyses/${item.id}/result`)}
                        >
                          Details
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          icon={Download}
                          onClick={() => window.open(analysisService.getPdfDownloadUrl(item.id), '_blank')}
                          title="Download PDF"
                        />
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
