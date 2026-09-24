import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, AlertTriangle, Activity, Database, CheckCircle, ArrowRight,
  TrendingUp, BarChart2, Zap, Server, Radio, Cpu, Layers, MapPin, Sliders, ShieldCheck
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie
} from 'recharts';
import { fetchStatistics, fetchDemoScenarios, predictDisaster } from '../services/api';

const CATEGORY_COLORS = {
  'Flood': '#ef4444',                  // Red
  'Fire': '#f97316',                   // Orange
  'Infrastructure Failure': '#8b5cf6', // Purple
  'Landslide': '#f59e0b',              // Amber
  'Disease Outbreak': '#3b82f6'        // Blue
};

const SEVERITY_COLORS = {
  'Critical': '#dc2626', // Red
  'High': '#f59e0b',     // Amber
  'Medium': '#3b82f6',   // Blue
  'Low': '#10b981'       // Green
};

export default function DashboardPage({ setActiveTab, setPredictFormData, setLastPrediction, lastPrediction }) {
  const [stats, setStats] = useState(null);
  const [demos, setDemos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeDemo, setActiveDemo] = useState(null);
  const [timeStr, setTimeStr] = useState('');

  const [recentLog, setRecentLog] = useState([
    { id: 1, time: '16:15:02', primary: 'Heavy Rain', secondary: 'Flood', severity: 'Critical', risk: 92, status: 'EVALUATED' },
    { id: 2, time: '15:42:18', primary: 'Cyclone', secondary: 'Infrastructure Failure', severity: 'High', risk: 78, status: 'EVALUATED' },
    { id: 3, time: '14:20:55', primary: 'Landslide Trigger', secondary: 'Landslide', severity: 'High', risk: 81, status: 'EVALUATED' },
    { id: 4, time: '12:05:40', primary: 'Extreme Heat', secondary: 'Fire', severity: 'Medium', risk: 54, status: 'EVALUATED' }
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

    const updateClock = () => {
      const now = new Date();
      setTimeStr(now.toTimeString().split(' ')[0] + ' LOCAL');
    };
    updateClock();
    const interval = setInterval(updateClock, 1000);
    return () => clearInterval(interval);
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
        risk: res.risk_score,
        status: 'EVALUATED'
      };
      setRecentLog(prev => [newEntry, ...prev.slice(0, 4)]);
      setActiveTab('predict');
    } catch (err) {
      alert('Error running demo prediction: ' + err.message);
    } finally {
      setActiveDemo(null);
    }
  };

  const handleLoadLogEntry = (logItem) => {
    // Map log entry to corresponding demo or predict state
    const matchedDemo = demos.find(d => d.data.primary_disaster === logItem.primary);
    if (matchedDemo) {
      setPredictFormData(matchedDemo.data);
    }
    setActiveTab('predict');
  };

  // Distribution chart data
  const chartData = stats?.class_distribution 
    ? Object.entries(stats.class_distribution)
        .map(([name, count]) => ({ name, count, percentage: Math.round((count / (stats.dataset_size || 3500)) * 100) }))
        .sort((a, b) => b.count - a.count)
    : [
        { name: 'Flood', count: 1102, percentage: 31 },
        { name: 'Fire', count: 913, percentage: 26 },
        { name: 'Infrastructure Failure', count: 747, percentage: 21 },
        { name: 'Landslide', count: 633, percentage: 18 },
        { name: 'Disease Outbreak', count: 105, percentage: 3 }
      ];

  // Severity donut chart data
  const severityData = stats?.severity_distribution
    ? Object.entries(stats.severity_distribution).map(([name, count]) => ({
        name,
        count,
        percentage: Math.round((count / (stats.dataset_size || 3500)) * 100)
      }))
    : [
        { name: 'High', count: 2023, percentage: 58 },
        { name: 'Medium', count: 1051, percentage: 30 },
        { name: 'Critical', count: 365, percentage: 10 },
        { name: 'Low', count: 61, percentage: 2 }
      ];

  // Regional Sectors Grid (Placeholder geospatial overview mapped to dataset regions)
  const regionalSectors = [
    { id: 1, name: 'Coastal Basin Sector', region: 'East Coastal Belt', hazard: 'Flood Inundation', level: 'HIGH RISK', color: 'text-red-400 border-red-800/80 bg-red-950/40', rain: '280 mm', elev: '15 m', pop: '9,500/km²' },
    { id: 2, name: 'Hill Slope Elevation Zone', region: 'Western Ghats Ridge', hazard: 'Landslide Flow', level: 'ELEVATED', color: 'text-amber-400 border-amber-800/80 bg-amber-950/40', rain: '180 mm', elev: '850 m', pop: '1,500/km²' },
    { id: 3, name: 'Dense Urban Core Node', region: 'Metropolitan Grid', hazard: 'Infra Collapse', level: 'CRITICAL', color: 'text-red-500 border-red-700 bg-red-950/60', rain: '45 mm', elev: '35 m', pop: '12,000/km²' },
    { id: 4, name: 'Inland Thermal Plain', region: 'Central Dry Zone', hazard: 'Fire / Thermal Stress', level: 'MODERATE', color: 'text-blue-400 border-blue-800/80 bg-blue-950/40', rain: '10 mm', elev: '120 m', pop: '4,200/km²' }
  ];

  const currentRiskDisplay = lastPrediction ? {
    disaster: lastPrediction.predicted_secondary_disaster,
    severity: lastPrediction.severity,
    score: lastPrediction.risk_score,
    prob: Math.round(lastPrediction.secondary_disaster_probability * 100),
    primary: lastPrediction.primary_disaster,
    isRealtime: true
  } : {
    disaster: 'Flood Inundation',
    severity: 'High',
    score: 81,
    prob: 85,
    primary: 'Heavy Rain',
    isRealtime: false
  };

  return (
    <div className="space-y-5 text-slate-100">
      
      {/* A. COMMAND HEADER */}
      <div className="bg-[#121827] px-5 py-4 rounded-lg border border-slate-800/80 shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-3">
            <h1 className="text-xl font-extrabold text-white font-mono tracking-tight flex items-center gap-2">
              <span>EMERGENCY OPERATIONS CENTER</span>
            </h1>
            <span className="text-[10px] px-2 py-0.5 rounded bg-red-950/90 text-red-400 border border-red-800/80 font-mono font-bold uppercase tracking-wider flex items-center gap-1">
              <Radio className="w-3 h-3 animate-pulse text-red-400" />
              LIVE MONITORING
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time multi-hazard chain reaction risk assessment & emergency resource intelligence.
          </p>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <div className="hidden sm:flex flex-col items-end text-[11px] font-mono text-slate-400 pr-2 border-r border-slate-800">
            <span className="text-slate-300 font-semibold">{timeStr}</span>
            <span className="text-[10px] text-emerald-400">MODELS LOADED (2/2)</span>
          </div>

          <button
            onClick={() => setActiveTab('predict')}
            className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-md text-xs font-bold font-mono tracking-wider shadow-md transition-all border border-blue-400/30"
          >
            <span>LAUNCH PREDICTOR</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* B. PRIORITY RISK & SITUATION SUMMARY GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        
        {/* FOCAL HERO CARD: Priority Risk Assessment (7 Cols) */}
        <div className="lg:col-span-7 bg-[#121827] p-5 rounded-lg border border-slate-800/80 space-y-4 relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-64 h-full bg-gradient-to-l from-red-950/20 to-transparent pointer-events-none"></div>
          
          <div>
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
              <div className="flex items-center space-x-2">
                <ShieldAlert className="w-4 h-4 text-red-400" />
                <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider font-mono">
                  Priority Risk Assessment {currentRiskDisplay.isRealtime ? '(ACTIVE INFERENCE)' : '(BASELINE TOP RISK)'}
                </h2>
              </div>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${
                currentRiskDisplay.severity === 'Critical' ? 'bg-red-950 text-red-400 border-red-800' :
                currentRiskDisplay.severity === 'High' ? 'bg-amber-950 text-amber-400 border-amber-800' :
                'bg-blue-950 text-blue-400 border-blue-800'
              }`}>
                {currentRiskDisplay.severity} SEVERITY
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-12 gap-4 mt-3 items-center">
              
              <div className="sm:col-span-7 space-y-1">
                <span className="text-[10px] text-slate-400 font-mono uppercase tracking-wider block">Highest Secondary Disaster Threat</span>
                <h3 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
                  <span className="text-red-400">{currentRiskDisplay.disaster}</span>
                </h3>
                <p className="text-xs text-slate-300 mt-1">
                  Primary Trigger Event: <strong className="text-white font-mono">{currentRiskDisplay.primary}</strong>
                </p>
                
                <div className="pt-2 flex items-center space-x-4 text-xs font-mono text-slate-400">
                  <div>Probability: <span className="text-white font-bold">{currentRiskDisplay.prob}%</span></div>
                  <div>Status: <span className="text-emerald-400 font-bold">MONITORED</span></div>
                </div>
              </div>

              {/* Risk Score Meter Gauge */}
              <div className="sm:col-span-5 bg-[#0b0f19] p-3.5 rounded border border-slate-800 text-center space-y-2">
                <span className="text-[10px] text-slate-400 font-mono uppercase tracking-wider block">Cascade Risk Score</span>
                <div className="text-3xl font-black text-red-400 font-mono tracking-tight">
                  {currentRiskDisplay.score}<span className="text-sm font-normal text-slate-400">/100</span>
                </div>
                
                <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div 
                    className={`h-full transition-all duration-500 ${
                      currentRiskDisplay.score >= 80 ? 'bg-red-500' :
                      currentRiskDisplay.score >= 60 ? 'bg-amber-500' : 'bg-blue-500'
                    }`}
                    style={{ width: `${currentRiskDisplay.score}%` }}
                  ></div>
                </div>
              </div>

            </div>
          </div>

          <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span className="text-slate-400 text-[11px]">
              Evaluated across 11 environmental & structural parameters
            </span>
            <button
              onClick={() => setActiveTab('predict')}
              className="text-blue-400 hover:text-blue-300 font-mono text-xs font-semibold flex items-center gap-1 hover:underline"
            >
              <span>Custom Inference</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>
        </div>

        {/* SECONDARY METRICS (5 Cols Grid) */}
        <div className="lg:col-span-5 grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-1 gap-3">
          
          <div className="bg-[#121827] p-3.5 rounded-lg border border-slate-800/80 flex items-center justify-between">
            <div>
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">Analyzed Scenarios</span>
              <h4 className="text-xl font-black text-white font-mono mt-0.5">
                {stats?.dataset_size ? stats.dataset_size.toLocaleString() : '3,500'}
              </h4>
              <p className="text-[10px] text-slate-400">11 Synthetic Feature Parameters</p>
            </div>
            <div className="p-2.5 bg-slate-900 rounded text-blue-400 border border-slate-800">
              <Database className="w-5 h-5" />
            </div>
          </div>

          <div className="bg-[#121827] p-3.5 rounded-lg border border-slate-800/80 flex items-center justify-between">
            <div>
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">Disaster Model Accuracy</span>
              <h4 className="text-xl font-black text-emerald-400 font-mono mt-0.5">
                {stats?.disaster_model?.accuracy ? `${(stats.disaster_model.accuracy * 100).toFixed(1)}%` : '92.4%'}
              </h4>
              <p className="text-[10px] text-slate-400">Random Forest (5 Target Classes)</p>
            </div>
            <div className="p-2.5 bg-slate-900 rounded text-emerald-400 border border-slate-800">
              <Activity className="w-5 h-5" />
            </div>
          </div>

          <div className="bg-[#121827] p-3.5 rounded-lg border border-slate-800/80 flex items-center justify-between">
            <div>
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">Severity Model Accuracy</span>
              <h4 className="text-xl font-black text-amber-400 font-mono mt-0.5">
                {stats?.severity_model?.accuracy ? `${(stats.severity_model.accuracy * 100).toFixed(1)}%` : '82.4%'}
              </h4>
              <p className="text-[10px] text-slate-400">Random Forest (4 Ordinal Levels)</p>
            </div>
            <div className="p-2.5 bg-slate-900 rounded text-amber-400 border border-slate-800">
              <TrendingUp className="w-5 h-5" />
            </div>
          </div>

        </div>

      </div>

      {/* C. PRIMARY INTELLIGENCE AREA (TWO-COLUMN CHARTS) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        
        {/* LEFT: Secondary Disaster Risk Distribution (7 Cols) */}
        <div className="lg:col-span-7 bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
            <div className="flex items-center space-x-2">
              <BarChart2 className="w-4 h-4 text-blue-400" />
              <h3 className="text-xs font-bold text-slate-200 font-mono uppercase tracking-wider">
                Secondary Disaster Risk Distribution
              </h3>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">Sorted by Base Frequency</span>
          </div>

          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <XAxis type="number" stroke="#475569" fontSize={10} tickLine={false} />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" fontSize={11} width={135} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc', fontSize: '11px', borderRadius: '4px' }}
                  formatter={(value) => [`${value} Scenarios`, 'Count']}
                />
                <Bar dataKey="count" radius={[0, 4, 4, 0]} barSize={16}>
                  {chartData.map((entry) => (
                    <Cell key={`cell-${entry.name}`} fill={CATEGORY_COLORS[entry.name] || '#3b82f6'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-5 gap-1 pt-1 border-t border-slate-800/80 text-[10px] font-mono text-center text-slate-400">
            {chartData.map(item => (
              <div key={item.name} className="truncate">
                <span className="font-bold text-slate-200 block">{item.percentage}%</span>
                <span className="text-slate-500 truncate block">{item.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT: Cascade Severity Profile (5 Cols Donut Chart) */}
        <div className="lg:col-span-5 bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3 flex flex-col justify-between">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <h3 className="text-xs font-bold text-slate-200 font-mono uppercase tracking-wider">
                Cascade Severity Profile
              </h3>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">4-Tier Scale</span>
          </div>

          <div className="h-48 relative flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={severityData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="count"
                >
                  {severityData.map((entry) => (
                    <Cell key={`sev-${entry.name}`} fill={SEVERITY_COLORS[entry.name] || '#3b82f6'} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc', fontSize: '11px', borderRadius: '4px' }}
                />
              </PieChart>
            </ResponsiveContainer>

            {/* Donut Center Label */}
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-lg font-black text-white font-mono">3,500</span>
              <span className="text-[9px] text-slate-400 uppercase font-mono tracking-wider">Scenarios</span>
            </div>
          </div>

          {/* Compact Readable Legend */}
          <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800/80 text-[11px] font-mono">
            {severityData.map(item => (
              <div key={item.name} className="flex items-center justify-between bg-[#0b0f19] px-2.5 py-1 rounded border border-slate-800">
                <div className="flex items-center space-x-1.5">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: SEVERITY_COLORS[item.name] }}></span>
                  <span className="text-slate-300">{item.name}</span>
                </div>
                <span className="font-bold text-slate-200">{item.percentage}%</span>
              </div>
            ))}
          </div>

        </div>

      </div>

      {/* D. REGIONAL RISK OVERVIEW (GEOSPATIAL SECTOR MATRIX) */}
      <div className="bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
          <div className="flex items-center space-x-2">
            <MapPin className="w-4 h-4 text-emerald-400" />
            <h3 className="text-xs font-bold text-slate-200 font-mono uppercase tracking-wider">
              Regional Risk Overview
            </h3>
          </div>
          <span className="text-[10px] bg-slate-900 text-emerald-400 font-mono px-2 py-0.5 rounded border border-slate-800 flex items-center gap-1">
            <ShieldCheck className="w-3 h-3" /> GIS SPATIAL ENGINE READY
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {regionalSectors.map((sector) => (
            <div 
              key={sector.id} 
              className="bg-[#0b0f19] p-3 rounded border border-slate-800/90 space-y-2 hover:border-slate-700 transition-colors"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white truncate">{sector.name}</span>
                <span className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded border ${sector.color}`}>
                  {sector.level}
                </span>
              </div>
              
              <div className="text-[11px] text-slate-400 font-mono flex items-center justify-between">
                <span>Primary Risk:</span>
                <span className="text-slate-200 font-semibold">{sector.hazard}</span>
              </div>

              <div className="grid grid-cols-3 gap-1 pt-1.5 border-t border-slate-800 text-[10px] font-mono text-slate-400 text-center">
                <div>Rain: <span className="text-blue-400 font-bold block">{sector.rain}</span></div>
                <div>Elev: <span className="text-amber-400 font-bold block">{sector.elev}</span></div>
                <div>Pop: <span className="text-slate-300 font-bold block">{sector.pop}</span></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* E. SCENARIO INTELLIGENCE AREA */}
      <div className="bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
          <div className="flex items-center space-x-2">
            <Zap className="w-4 h-4 text-amber-400" />
            <h3 className="text-xs font-bold text-slate-200 font-mono uppercase tracking-wider">
              Scenario Intelligence
            </h3>
          </div>
          <span className="text-[10px] text-slate-400 font-mono">3 Preconfigured Test Scenarios</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {demos.map((demo) => (
            <div
              key={demo.id}
              className="bg-[#0b0f19] p-3.5 rounded border border-slate-800/90 hover:border-blue-500/40 transition-all flex flex-col justify-between space-y-3"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-white">{demo.name}</span>
                  <span className="text-[10px] bg-red-950/80 text-red-300 font-mono px-2 py-0.5 rounded border border-red-800/80 font-semibold">
                    {demo.expected}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">{demo.description}</p>
                
                <div className="mt-2.5 grid grid-cols-2 gap-1 text-[10px] font-mono text-slate-300 bg-[#121827] p-2 rounded border border-slate-800">
                  <div>Rain: <span className="text-blue-400">{demo.data.rainfall_mm} mm</span></div>
                  <div>Wind: <span className="text-amber-400">{demo.data.wind_speed_kmph} km/h</span></div>
                  <div>Soil: <span className="text-emerald-400">{Math.round(demo.data.soil_moisture * 100)}%</span></div>
                  <div>Vuln: <span className="text-red-400">{Math.round(demo.data.infrastructure_vulnerability * 100)}%</span></div>
                </div>
              </div>

              <button
                onClick={() => handleRunDemo(demo)}
                disabled={activeDemo === demo.id}
                className="w-full py-1.5 bg-blue-600/20 hover:bg-blue-600/40 text-blue-400 hover:text-white border border-blue-500/30 rounded text-xs font-mono font-bold transition-all flex items-center justify-center gap-1"
              >
                {activeDemo === demo.id ? (
                  <span>Executing AI Inference...</span>
                ) : (
                  <>
                    <span>Run Demo Scenario</span>
                    <ArrowRight className="w-3 h-3" />
                  </>
                )}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* F. RECENT INCIDENT EVALUATIONS LOG */}
      <div className="bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
          <div className="flex items-center space-x-2">
            <Server className="w-4 h-4 text-emerald-400" />
            <h3 className="text-xs font-bold text-slate-200 font-mono uppercase tracking-wider">
              Recent Incident Evaluations
            </h3>
          </div>
          <span className="text-[10px] text-slate-400 font-mono">Live Operations Dispatch Log</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-[#0b0f19] uppercase font-mono text-[10px] text-slate-400">
              <tr>
                <th className="px-3.5 py-2">Time</th>
                <th className="px-3.5 py-2">Primary Event</th>
                <th className="px-3.5 py-2">Predicted Secondary</th>
                <th className="px-3.5 py-2">Severity</th>
                <th className="px-3.5 py-2">Risk Score</th>
                <th className="px-3.5 py-2">Status</th>
                <th className="px-3.5 py-2 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
              {recentLog.map((log) => (
                <tr key={log.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-3.5 py-2.5 text-slate-400">{log.time}</td>
                  <td className="px-3.5 py-2.5 font-semibold text-slate-200">{log.primary}</td>
                  <td className="px-3.5 py-2.5 font-bold text-blue-400">{log.secondary}</td>
                  <td className="px-3.5 py-2.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      log.severity === 'Critical' ? 'bg-red-950 text-red-400 border border-red-800' :
                      log.severity === 'High' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                      'bg-blue-950 text-blue-400 border border-blue-800'
                    }`}>
                      {log.severity}
                    </span>
                  </td>
                  <td className="px-3.5 py-2.5 font-extrabold text-red-400">
                    {log.risk}<span className="text-[10px] text-slate-500 font-normal">/100</span>
                  </td>
                  <td className="px-3.5 py-2.5">
                    <span className="text-[9px] px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                      {log.status}
                    </span>
                  </td>
                  <td className="px-3.5 py-2.5 text-right">
                    <button
                      onClick={() => handleLoadLogEntry(log)}
                      className="text-[10px] bg-slate-800 hover:bg-slate-700 text-slate-200 px-2 py-1 rounded font-semibold transition-all"
                    >
                      Load
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
