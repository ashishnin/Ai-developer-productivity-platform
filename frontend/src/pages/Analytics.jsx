import React, { useState, useEffect } from 'react';
import { Users, BarChart3, Loader2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { analyticsAPI } from '../api';

const Analytics = () => {
  const [productivity, setProductivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const res = await analyticsAPI.getProductivity();
      setProductivity(res.data);
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
    } finally {
      setLoading(false);
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
        <h1 className="text-2xl font-bold text-white">Developer Analytics</h1>
        <p className="text-slate-400">Track developer productivity and contributions</p>
      </div>

      <div className="card overflow-x-auto">
        <h3 className="text-lg font-semibold text-white mb-4">Developer Productivity Metrics</h3>
        <table className="w-full">
          <thead>
            <tr className="border-b border-dark-600">
              <th className="text-left py-3 px-4 text-slate-400 font-medium">Developer</th>
              <th className="text-right py-3 px-4 text-slate-400 font-medium">Commits</th>
              <th className="text-right py-3 px-4 text-slate-400 font-medium">Lines Added</th>
              <th className="text-right py-3 px-4 text-slate-400 font-medium">Lines Deleted</th>
              <th className="text-right py-3 px-4 text-slate-400 font-medium">Files Modified</th>
              <th className="text-right py-3 px-4 text-slate-400 font-medium">Bugs</th>
              <th className="text-right py-3 px-4 text-slate-400 font-medium">Contribution %</th>
              <th className="text-right py-3 px-4 text-slate-400 font-medium">Productivity</th>
            </tr>
          </thead>
          <tbody>
            {productivity.map((dev, index) => (
              <tr key={index} className="border-b border-dark-700 hover:bg-dark-700/50">
                <td className="py-3 px-4 text-white font-medium">{dev.developer_name}</td>
                <td className="py-3 px-4 text-right text-slate-300">{dev.total_commits}</td>
                <td className="py-3 px-4 text-right text-success">+{dev.total_lines_added}</td>
                <td className="py-3 px-4 text-right text-danger">-{dev.total_lines_deleted}</td>
                <td className="py-3 px-4 text-right text-slate-300">{dev.total_files_modified}</td>
                <td className="py-3 px-4 text-right text-warning">{dev.total_bugs}</td>
                <td className="py-3 px-4 text-right text-slate-300">{dev.contribution_percentage.toFixed(1)}%</td>
                <td className="py-3 px-4 text-right">
                  <span className={`badge ${dev.productivity_score >= 70 ? 'badge-success' : dev.productivity_score >= 40 ? 'badge-warning' : 'badge-danger'}`}>
                    {dev.productivity_score.toFixed(1)}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-white mb-4">Commits Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={productivity.slice(0, 6)}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="developer_name" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }} />
              <Bar dataKey="total_commits" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-white mb-4">Contribution Share</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={productivity.slice(0, 5)} dataKey="total_commits" nameKey="developer_name" cx="50%" cy="50%" outerRadius={100} label>
                {productivity.slice(0, 5).map((entry, index) => (<Cell key={index} fill={['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][index % 5]} />))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
