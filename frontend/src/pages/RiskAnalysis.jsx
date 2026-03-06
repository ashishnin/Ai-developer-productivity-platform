import React, { useState, useEffect } from 'react';
import { ShieldAlert, Loader2, AlertTriangle } from 'lucide-react';
import { aiAPI } from '../api';

const RiskAnalysis = () => {
  const [riskData, setRiskData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRiskData();
  }, []);

  const fetchRiskData = async () => {
    try {
      const res = await aiAPI.getRiskAnalysis();
      setRiskData(res.data);
    } catch (err) {
      console.error('Failed to fetch risk analysis:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskBadge = (level) => {
    switch (level) {
      case 'High': return 'badge-danger';
      case 'Medium': return 'badge-warning';
      default: return 'badge-success';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h1 className="text-2xl font-bold text-white">Module Risk Analysis</h1>
        <p className="text-slate-400">AI-powered risk prediction for your modules</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {riskData.slice(0, 3).map((module, index) => (
          <div key={index} className={`card border-l-4 ${module.risk_level === 'High' ? 'border-danger' : module.risk_level === 'Medium' ? 'border-warning' : 'border-success'}`}>
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-white">{module.module_name}</h3>
              <span className={`badge ${getRiskBadge(module.risk_level)}`}>{module.risk_level}</span>
            </div>
            <div className="flex items-end gap-2">
              <span className="text-3xl font-bold text-white">{module.risk_score}</span>
              <span className="text-slate-400 text-sm mb-1">/100</span>
            </div>
            <div className="mt-3 h-2 bg-dark-600 rounded-full overflow-hidden">
              <div className={`h-full ${module.risk_level === 'High' ? 'bg-danger' : module.risk_level === 'Medium' ? 'bg-warning' : 'bg-success'}`} style={{ width: `${module.risk_score}%` }} />
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-white mb-4">Detailed Risk Analysis</h3>
        {riskData.length === 0 ? (
          <div className="text-center py-8">
            <AlertTriangle className="w-12 h-12 text-slate-500 mx-auto mb-4" />
            <p className="text-slate-400">No risk data available. Upload activity data to see analysis.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {riskData.map((module, index) => (
              <div key={index} className="p-4 bg-dark-800 rounded-lg">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <ShieldAlert className={`w-5 h-5 ${module.risk_level === 'High' ? 'text-danger' : module.risk_level === 'Medium' ? 'text-warning' : 'text-success'}`} />
                    <h4 className="font-medium text-white">{module.module_name}</h4>
                  </div>
                  <span className={`badge ${getRiskBadge(module.risk_level)}`}>{module.risk_level} Risk</span>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-3">
                  <div><span className="text-slate-400">Risk Score:</span> <span className="text-white font-medium">{module.risk_score}</span></div>
                </div>
                <div className="bg-dark-700 rounded-lg p-3 mb-3">
                  <p className="text-xs text-slate-400 mb-2">Risk Factors:</p>
                  <div className="flex flex-wrap gap-2">
                    {module.factors.map((factor, i) => (<span key={i} className="text-xs px-2 py-1 bg-dark-600 text-slate-300 rounded">{factor}</span>))}
                  </div>
                </div>
                <div className="p-3 bg-primary/10 border border-primary/30 rounded-lg">
                  <p className="text-sm text-slate-200"><span className="text-primary font-medium">AI Recommendation:</span> {module.recommendation}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default RiskAnalysis;
