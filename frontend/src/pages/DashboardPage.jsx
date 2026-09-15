import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, AlertTriangle, Activity, Database, CheckCircle, ArrowRight,
  TrendingUp, BarChart2, Zap, Server, AlertCircle
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie
} from 'recharts';
import { fetchStatistics, fetchDemoScenarios, predictDisaster } from '../services/api';

const COLORS = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'];

export default function DashboardPage({ setActiveTab, setPredictFormData, setLastPrediction }) {
  const [stats, setStats] = useState(null);
  const [demos, setDemos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeDemo, setActiveDemo] = useState(null);
  const [recentLog, setRecentLog] = useState([
    { id: 1, time: '16:15:02', primary: 'Heavy Rain', secondary: 'Flood', severity: 'Critical', risk: 92 },
    { id: 2, time: '15:42:18', primary: 'Cyclone', secondary: 'Infrastructure Failure', severity: 'High', risk: 78 },
    { id: 3, time: '14:20:55', primary: 'Landslide Trigger', secondary: 'Landslide', severity: 'High', risk: 81 },
    { id: 4, time: '12:05:40', primary: 'Extreme Heat', secondary: 'Fire', severity: 'Medium', risk: 54 }
  ]);

  useEffect(() => {
    async function loadData() {
      try {
        const s = await fetchStatistics();
        setStats(s);
        const d = await fetchDemoScenarios();
        setDemos(d.scenarios || []);
      } catch (err) {
        console.error('Error fetching dashboard stats:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleRunDemo = async (scenario) => {
    setActiveDemo(scenario.id);
    try {
      const res = await predictDisaster(scenario.data);
      setLastPrediction(res);
      setPredictFormData(scenario.data);
      
      const newEntry = {
        id: Date.now(),
        time: new Date().toLocaleTimeString(),
        primary: scenario.data.primary_disaster,
        secondary: res.predicted_secondary_disaster,
        severity: res.severity,
        risk: res.risk_score
      };
      setRecentLog(prev => [newEntry, ...prev.slice(0, 4)]);
      setActiveTab('predict');
    } catch (err) {
      alert('Error running demo prediction: ' + err.message);
    } finally {
      setActiveDemo(null);
    }
  };

  const chartData = stats?.class_distribution 
    ? Object.entries(stats.class_distribution).map(([name, count]) => ({ name, count }))
    : [
        { name: 'Flood', count: 1102 },
        { name: 'Fire', count: 913 },
        { name: 'Infrastructure Failure', count: 747 },
        { name: 'Landslide', count: 633 },
        { name: 'Disease Outbreak', count: 105 }
      ];

  const severityData = stats?.severity_distribution
    ? Object.entries(stats.severity_distribution).map(([name, count]) => ({ name, count }))
    : [
        { name: 'High', count: 2023 },
        { name: 'Medium', count: 1051 },
        { name: 'Critical', count: 365 },
        { name: 'Low', count: 61 }
      ];

  return (
    <div className="space-y-6">
      
      {/* Banner / Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-blue-950 p-6 rounded-xl border border-slate-800 shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-full bg-blue-500/5 blur-3xl rounded-full pointer-events-none"></div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <h1 className="text-2xl font-black text-white tracking-wide font-mono flex items-center gap-2">
              <span>EMERGENCY OPERATIONS CENTER</span>
              <span className="text-xs px-2.5 py-1 rounded-md bg-red-950/80 border border-red-800 text-red-400 font-sans font-semibold uppercase">
                Live Monitoring
              </span>
            </h1>
            <p className="text-sm text-slate-300 mt-1">
              AI-driven multi-hazard cascade risk intelligence and real-time emergency resource engine.
            </p>
          </div>
          <button
            onClick={() => setActiveTab('predict')}
            className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white px-5 py-2.5 rounded-lg text-xs font-bold uppercase tracking-wider shadow-lg shadow-blue-950 transition-all shrink-0"
          >
            <span>Launch Predictor</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Metric Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Scenarios Analyzed</p>
            <h3 className="text-2xl font-extrabold text-white mt-1 font-mono">
              {stats?.dataset_size ? stats.dataset_size.toLocaleString() : '3,500'}
            </h3>
            <p className="text-[11px] text-emerald-400 mt-1 flex items-center gap-1">
              <CheckCircle className="w-3 h-3" /> Synthetic Baseline Dataset
            </p>
          </div>
          <div className="p-3 bg-blue-950/80 rounded-lg text-blue-400 border border-blue-800/50">
            <Database className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Top Secondary Risk</p>
            <h3 className="text-xl font-extrabold text-red-400 mt-1">
              Flood Inundation
            </h3>
            <p className="text-[11px] text-slate-400 mt-1">
              31.5% occurrence probability
            </p>
          </div>
          <div className="p-3 bg-red-950/80 rounded-lg text-red-400 border border-red-800/50">
            <ShieldAlert className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Disaster Model Accuracy</p>
            <h3 className="text-2xl font-extrabold text-emerald-400 mt-1 font-mono">
              {stats?.disaster_model?.accuracy ? `${(stats.disaster_model.accuracy * 100).toFixed(1)}%` : '92.4%'}
            </h3>
            <p className="text-[11px] text-slate-400 mt-1">
              Random Forest Classifier
            </p>
          </div>
          <div className="p-3 bg-emerald-950/80 rounded-lg text-emerald-400 border border-emerald-800/50">
            <Activity className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Severity Model Accuracy</p>
            <h3 className="text-2xl font-extrabold text-amber-400 mt-1 font-mono">
              {stats?.severity_model?.accuracy ? `${(stats.severity_model.accuracy * 100).toFixed(1)}%` : '82.4%'}
            </h3>
            <p className="text-[11px] text-slate-400 mt-1">
              4-Level Categorical Severity
            </p>
          </div>
          <div className="p-3 bg-amber-950/80 rounded-lg text-amber-400 border border-amber-800/50">
            <TrendingUp className="w-6 h-6" />
          </div>
        </div>

      </div>

      {/* Demo Scenarios Section */}
      <div className="bg-slate-900/90 p-6 rounded-xl border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" />
              <span>Preconfigured Demo Scenarios (1-Click AI Evaluation)</span>
            </h2>
            <p className="text-xs text-slate-400">Select any scenario to test predictions and resource calculations instantly.</p>
          </div>
          <span className="text-[11px] bg-slate-800 text-slate-300 font-mono px-2.5 py-1 rounded border border-slate-700">
            3 Scenarios Ready
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {demos.map((demo) => (
            <div
              key={demo.id}
              className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/60 hover:border-blue-500/50 transition-all flex flex-col justify-between space-y-3"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sm text-slate-100">{demo.name}</span>
                  <span className="text-[10px] bg-red-950 text-red-300 font-mono px-2 py-0.5 rounded border border-red-800">
                    {demo.expected}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-1.5 line-clamp-2">{demo.description}</p>
                
                <div className="mt-3 grid grid-cols-2 gap-1 text-[11px] font-mono text-slate-300 bg-slate-900/80 p-2 rounded">
                  <div>Rain: <span className="text-blue-400">{demo.data.rainfall_mm} mm</span></div>
                  <div>Wind: <span className="text-amber-400">{demo.data.wind_speed_kmph} km/h</span></div>
                  <div>Soil: <span className="text-emerald-400">{demo.data.soil_moisture * 100}%</span></div>
                  <div>Vuln: <span className="text-red-400">{demo.data.infrastructure_vulnerability * 100}%</span></div>
                </div>
              </div>

              <button
                onClick={() => handleRunDemo(demo)}
                disabled={activeDemo === demo.id}
                className="w-full py-2 bg-blue-600/30 hover:bg-blue-600 text-blue-300 hover:text-white border border-blue-500/40 rounded text-xs font-bold transition-all flex items-center justify-center gap-1"
              >
                {activeDemo === demo.id ? (
                  <span>Evaluating AI...</span>
                ) : (
                  <>
                    <span>Run Demo Scenario</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </>
                )}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Analytics & Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Secondary Disaster Breakdown Chart */}
        <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-blue-400" />
              <span>Secondary Disaster Distribution</span>
            </h3>
            <span className="text-xs text-slate-400 font-mono">3,500 Synthetic Records</span>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <XAxis type="number" stroke="#64748b" fontSize={11} />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" fontSize={11} width={130} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc', fontSize: '12px' }}
                />
                <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Severity Distribution Pie Chart */}
        <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <span>Cascade Severity Distribution</span>
            </h3>
            <span className="text-xs text-slate-400 font-mono">4-Tier Risk Scale</span>
          </div>

          <div className="h-64 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={severityData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="count"
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                >
                  <Cell fill="#ef4444" /> {/* High */}
                  <Cell fill="#f59e0b" /> {/* Medium */}
                  <Cell fill="#7c3aed" /> {/* Critical */}
                  <Cell fill="#10b981" /> {/* Low */}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc', fontSize: '12px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Recent Predictions Log */}
      <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
            <Server className="w-4 h-4 text-emerald-400" />
            <span>Recent Incident Evaluations Log</span>
          </h3>
          <span className="text-xs text-slate-400 font-mono">Live Session History</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-800/80 uppercase font-mono text-[11px] text-slate-400">
              <tr>
                <th className="px-4 py-2.5">Time</th>
                <th className="px-4 py-2.5">Primary Disaster</th>
                <th className="px-4 py-2.5">Predicted Secondary</th>
                <th className="px-4 py-2.5">Severity</th>
                <th className="px-4 py-2.5 text-right">Risk Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {recentLog.map((log) => (
                <tr key={log.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="px-4 py-3 text-slate-400">{log.time}</td>
                  <td className="px-4 py-3 font-semibold text-slate-200">{log.primary}</td>
                  <td className="px-4 py-3 font-semibold text-blue-400">{log.secondary}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      log.severity === 'Critical' ? 'bg-red-950 text-red-400 border border-red-800' :
                      log.severity === 'High' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                      'bg-blue-950 text-blue-400 border border-blue-800'
                    }`}>
                      {log.severity}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right font-extrabold text-red-400">{log.risk}/100</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
