import React, { useState, useEffect } from 'react';
import { Brain, Loader2, AlertTriangle, AlertCircle, Info, CheckCircle } from 'lucide-react';
import { aiAPI } from '../api';

const Insights = () => {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInsights();
  }, []);

  const fetchInsights = async () => {
    try {
      const res = await aiAPI.getInsights();
      setInsights(res.data);
    } catch (err) {
      console.error('Failed to fetch insights:', err);
    } finally {
      setLoading(false);
    }
  };

  const getIcon = (type) => {
    switch (type) {
      case 'danger': return <AlertTriangle className="w-5 h-5 text-danger" />;
      case 'warning': return <AlertCircle className="w-5 h-5 text-warning" />;
      case 'success': return <CheckCircle className="w-5 h-5 text-success" />;
      default: return <Info className="w-5 h-5 text-primary" />;
    }
  };

  const getStyles = (type) => {
    switch (type) {
      case 'danger': return 'bg-danger/10 border-danger';
      case 'warning': return 'bg-warning/10 border-warning';
      case 'success': return 'bg-success/10 border-success';
      default: return 'bg-primary/10 border-primary';
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
      <div className="flex items-center gap-3">
        <div className="p-3 bg-primary/20 rounded-xl">
          <Brain className="w-6 h-6 text-primary" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white">AI Insights</h1>
          <p className="text-slate-400">AI-powered recommendations and predictions</p>
        </div>
      </div>

      {insights.length === 0 ? (
        <div className="card text-center py-12">
          <Brain className="w-12 h-12 text-slate-500 mx-auto mb-4" />
          <p className="text-slate-400">No insights available yet. Upload activity data to get AI-powered recommendations.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {insights.map((insight, index) => (
            <div key={index} className={`card border-l-4 ${getStyles(insight.insight_type)}`}>
              <div className="flex items-start gap-4">
                <div className="mt-1">{getIcon(insight.insight_type)}</div>
                <div className="flex-1">
                  <p className="text-white">{insight.message}</p>
                  {insight.module_name && (
                    <p className="text-sm text-slate-400 mt-2">
                      <span className="font-medium">Module:</span> {insight.module_name}
                    </p>
                  )}
                  <p className="text-xs text-slate-500 mt-2">
                    {new Date(insight.created_at).toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="card bg-gradient-to-r from-primary/20 to-secondary/20">
        <h3 className="text-lg font-semibold text-white mb-2">How AI Insights Work</h3>
        <p className="text-sm text-slate-300">
          Our AI analyzes your development activity data to identify patterns and predict potential risks. 
          The system considers factors like code churn, commit frequency, bug density, and module instability 
          to generate actionable insights for your team.
        </p>
      </div>
    </div>
  );
};

export default Insights;
