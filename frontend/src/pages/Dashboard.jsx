import React, { useState, useEffect } from 'react';
import { 
  FolderKanban, 
  Users, 
  TrendingUp, 
  AlertTriangle,
  Brain,
  ArrowUpRight,
  ArrowDownRight,
  Loader2
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { analyticsAPI, aiAPI } from '../api';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const [dashboard, setDashboard] = useState(null);
  const [productivity, setProductivity] = useState([]);
  const [churn, setChurn] = useState([]);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [dashRes, prodRes, churnRes, insightRes] = await Promise.all([
        analyticsAPI.getDashboard(),
        analyticsAPI.getProductivity(),
        analyticsAPI.getChurn(),
        aiAPI.getInsights()
      ]);
      setDashboard(dashRes.data);
      setProductivity(prodRes.data);
      setChurn(churnRes.data);
      setInsights(insightRes.data);
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
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

  const stats = [
    { 
      label: 'Total Projects', 
      value: dashboard?.total_projects || 0, 
      icon: FolderKanban, 
      color: 'bg-primary',
      change: '+12%'
    },
    { 
      label: 'Active Developers', 
      value: dashboard?.total_developers || 0, 
      icon: Users, 
      color: 'bg-secondary',
      change: '+5%'
    },
    { 
      label: 'Avg Productivity', 
      value: `${dashboard?.avg_productivity?.toFixed(1) || 0}%`, 
      icon: TrendingUp, 
      color: 'bg-purple-500',
      change: '+8%'
    },
    { 
      label: 'High Risk Modules', 
      value: dashboard?.high_risk_modules || 0, 
      icon: AlertTriangle, 
      color: 'bg-danger',
      change: '-3%'
    },
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">
            Welcome back, {user?.username}!
          </h1>
          <p className="text-slate-400">Here's what's happening with your projects</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="card">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-slate-400 text-sm">{stat.label}</p>
                  <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-xl ${stat.color}`}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
              </div>
              <div className="flex items-center gap-1 mt-3 text-sm">
                {stat.change.startsWith('+') ? (
                  <ArrowUpRight className="w-4 h-4 text-success" />
                ) : (
                  <ArrowDownRight className="w-4 h-4 text-danger" />
                )}
                <span className={stat.change.startsWith('+') ? 'text-success' : 'text-danger'}>
                  {stat.change}
                </span>
                <span className="text-slate-500">vs last month</span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-white mb-4">Developer Productivity</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={productivity.slice(0, 6)}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="developer_name" stroke="#94a3b8" fontSize={12} tickLine={false} />
              <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }} />
              <Bar dataKey="productivity_score" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-white mb-4">Module Instability</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={churn.slice(0, 6)}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="module_name" stroke="#94a3b8" fontSize={12} tickLine={false} />
              <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }} />
              <Bar dataKey="instability_score" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <Brain className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-semibold text-white">AI Insights</h3>
          </div>
          <div className="space-y-3">
            {insights.slice(0, 4).map((insight, index) => (
              <div key={index} className={`p-3 rounded-lg border-l-4 ${insight.insight_type === 'danger' ? 'bg-danger/10 border-danger' : ''} ${insight.insight_type === 'warning' ? 'bg-warning/10 border-warning' : ''} ${insight.insight_type === 'info' ? 'bg-primary/10 border-primary' : ''} ${insight.insight_type === 'success' ? 'bg-success/10 border-success' : ''}`}>
                <p className="text-sm text-slate-200">{insight.message}</p>
                {insight.module_name && <p className="text-xs text-slate-400 mt-1">Module: {insight.module_name}</p>}
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-white mb-4">Code Churn by Module</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={churn.slice(0, 5)} dataKey="code_churn" nameKey="module_name" cx="50%" cy="50%" outerRadius={80} label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                {churn.slice(0, 5).map((entry, index) => (<Cell key={index} fill={['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][index % 5]} />))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
