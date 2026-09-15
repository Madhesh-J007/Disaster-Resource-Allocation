import React, { useState } from 'react';
import { 
  Activity, ShieldAlert, Cpu, AlertTriangle, ArrowRight, Info, CheckCircle2, Sliders, Zap
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { predictDisaster } from '../services/api';

const PRIMARY_DISASTERS = [
  'Heavy Rain', 'Cyclone', 'Earthquake', 'Extreme Heat', 'Landslide Trigger'
];

export default function PredictPage({ formData, setFormData, lastPrediction, setLastPrediction, setActiveTab }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  const handlePredict = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await predictDisaster(formData);
      setLastPrediction(res);
    } catch (err) {
      setError(err.message || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (type) => {
    if (type === 'flood') {
      setFormData({
        rainfall_mm: 260.0,
        river_level_m: 8.8,
        soil_moisture: 0.90,
        wind_speed_kmph: 25.0,
        temperature_c: 25.0,
        population_density: 8500.0,
        elevation_m: 20.0,
        infrastructure_vulnerability: 0.65,
        road_accessibility: 0.60,
        distance_to_water_body: 0.5,
        primary_disaster: 'Heavy Rain'
      });
    } else if (type === 'landslide') {
      setFormData({
        rainfall_mm: 175.0,
        river_level_m: 2.8,
        soil_moisture: 0.88,
        wind_speed_kmph: 30.0,
        temperature_c: 21.0,
        population_density: 1500.0,
        elevation_m: 920.0,
        infrastructure_vulnerability: 0.55,
        road_accessibility: 0.25,
        distance_to_water_body: 5.0,
        primary_disaster: 'Landslide Trigger'
      });
    } else if (type === 'infra') {
      setFormData({
        rainfall_mm: 40.0,
        river_level_m: 2.0,
        soil_moisture: 0.30,
        wind_speed_kmph: 120.0,
        temperature_c: 28.0,
        population_density: 11000.0,
        elevation_m: 35.0,
        infrastructure_vulnerability: 0.88,
        road_accessibility: 0.45,
        distance_to_water_body: 3.5,
        primary_disaster: 'Cyclone'
      });
    }
  };

  const probChartData = lastPrediction?.class_probabilities
    ? Object.entries(lastPrediction.class_probabilities).map(([cls, prob]) => ({
        name: cls,
        probability: Math.round(prob * 100)
      }))
    : [];

  return (
    <div className="space-y-6">
      
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/90 p-5 rounded-xl border border-slate-800">
        <div>
          <h1 className="text-xl font-black text-white font-mono flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-400" />
            <span>AI SECONDARY DISASTER PREDICTOR</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Input primary disaster conditions to compute cascade risk probabilities, severity classification, and transparent feature explanations.
          </p>
        </div>

        {/* Preset quick buttons */}
        <div className="flex items-center space-x-2">
          <span className="text-[11px] text-slate-400 uppercase font-mono hidden lg:inline">Presets:</span>
          <button onClick={() => loadPreset('flood')} className="px-2.5 py-1 text-xs bg-slate-800 hover:bg-blue-900/40 text-blue-300 rounded border border-slate-700 font-mono">
            Severe Flood
          </button>
          <button onClick={() => loadPreset('landslide')} className="px-2.5 py-1 text-xs bg-slate-800 hover:bg-emerald-900/40 text-emerald-300 rounded border border-slate-700 font-mono">
            Landslide
          </button>
          <button onClick={() => loadPreset('infra')} className="px-2.5 py-1 text-xs bg-slate-800 hover:bg-purple-900/40 text-purple-300 rounded border border-slate-700 font-mono">
            Infra Failure
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Form Inputs (5 cols) */}
        <div className="lg:col-span-5 bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <Sliders className="w-4 h-4 text-blue-400" />
              <span>Environmental & Geographical Inputs</span>
            </h2>
            <span className="text-[10px] text-slate-400 font-mono">11 Parameters</span>
          </div>

          <form onSubmit={handlePredict} className="space-y-3">
            
            {/* Primary Disaster Select */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Primary Disaster Type</label>
              <select
                name="primary_disaster"
                value={formData.primary_disaster}
                onChange={handleChange}
                className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-xs font-mono text-white focus:outline-none focus:border-blue-500"
              >
                {PRIMARY_DISASTERS.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>

            {/* Grid 2 Columns for numerical inputs */}
            <div className="grid grid-cols-2 gap-3 text-xs">
              
              <div>
                <label className="block font-medium text-slate-300 mb-1">Rainfall (mm)</label>
                <input
                  type="number"
                  step="0.1"
                  name="rainfall_mm"
                  value={formData.rainfall_mm}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">River Level (m)</label>
                <input
                  type="number"
                  step="0.1"
                  name="river_level_m"
                  value={formData.river_level_m}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Soil Moisture (0 - 1)</label>
                <input
                  type="number"
                  step="0.01"
                  max="1.0"
                  min="0.0"
                  name="soil_moisture"
                  value={formData.soil_moisture}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Wind Speed (km/h)</label>
                <input
                  type="number"
                  step="1"
                  name="wind_speed_kmph"
                  value={formData.wind_speed_kmph}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Temperature (°C)</label>
                <input
                  type="number"
                  step="0.5"
                  name="temperature_c"
                  value={formData.temperature_c}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Population Density</label>
                <input
                  type="number"
                  step="100"
                  name="population_density"
                  value={formData.population_density}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Elevation (m)</label>
                <input
                  type="number"
                  step="10"
                  name="elevation_m"
                  value={formData.elevation_m}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Infra Vulnerability (0 - 1)</label>
                <input
                  type="number"
                  step="0.01"
                  max="1.0"
                  min="0.0"
                  name="infrastructure_vulnerability"
                  value={formData.infrastructure_vulnerability}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Road Access (0 - 1)</label>
                <input
                  type="number"
                  step="0.01"
                  max="1.0"
                  min="0.0"
                  name="road_accessibility"
                  value={formData.road_accessibility}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Dist to Water (km)</label>
                <input
                  type="number"
                  step="0.1"
                  name="distance_to_water_body"
                  value={formData.distance_to_water_body}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-700 rounded p-2 font-mono text-white focus:outline-none focus:border-blue-500"
                />
              </div>

            </div>

            {error && (
              <div className="p-3 bg-red-950/80 border border-red-800 text-red-300 text-xs rounded">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-extrabold text-xs uppercase tracking-wider rounded-lg shadow-lg shadow-blue-950 transition-all flex items-center justify-center space-x-2"
            >
              {loading ? (
                <span>Executing Random Forest Inference...</span>
              ) : (
                <>
                  <Zap className="w-4 h-4 text-amber-300" />
                  <span>Run AI Secondary Prediction</span>
                </>
              )}
            </button>

          </form>
        </div>

        {/* Right Column: Prediction Results & Explanations (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          
          {lastPrediction ? (
            <>
              {/* Primary Output Cards */}
              <div className="bg-slate-900/90 p-6 rounded-xl border border-slate-800 space-y-4 relative overflow-hidden">
                <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                  <span className="text-xs text-slate-400 font-mono uppercase tracking-wider">AI Inference Results</span>
                  <span className="px-2.5 py-0.5 rounded bg-emerald-950 text-emerald-400 text-[10px] font-mono border border-emerald-800">
                    Confidence: {(lastPrediction.secondary_disaster_probability * 100).toFixed(1)}%
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  
                  {/* Secondary Disaster Result Card */}
                  <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
                    <p className="text-xs text-slate-400 font-medium">Predicted Secondary Disaster</p>
                    <h3 className="text-xl font-extrabold text-red-400 mt-1 flex items-center gap-2">
                      <ShieldAlert className="w-5 h-5 text-red-500" />
                      <span>{lastPrediction.predicted_secondary_disaster}</span>
                    </h3>
                    <p className="text-[11px] text-slate-400 mt-2">
                      Probability: <strong className="text-white">{(lastPrediction.secondary_disaster_probability * 100).toFixed(1)}%</strong>
                    </p>
                  </div>

                  {/* Severity Result Card */}
                  <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
                    <p className="text-xs text-slate-400 font-medium">Cascade Severity Level</p>
                    <div className="flex items-center justify-between mt-1">
                      <span className={`px-3 py-1 rounded text-sm font-extrabold font-mono uppercase ${
                        lastPrediction.severity === 'Critical' ? 'bg-red-950 text-red-400 border border-red-800' :
                        lastPrediction.severity === 'High' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                        'bg-blue-950 text-blue-400 border border-blue-800'
                      }`}>
                        {lastPrediction.severity}
                      </span>
                      <div className="text-right">
                        <span className="text-xs text-slate-400 block">Risk Score</span>
                        <span className="text-xl font-black text-white font-mono">{lastPrediction.risk_score}/100</span>
                      </div>
                    </div>

                    {/* Risk Bar */}
                    <div className="w-full bg-slate-950 rounded-full h-2 mt-3 overflow-hidden border border-slate-700">
                      <div
                        className={`h-full transition-all duration-500 ${
                          lastPrediction.risk_score >= 80 ? 'bg-red-500' :
                          lastPrediction.risk_score >= 60 ? 'bg-amber-500' : 'bg-blue-500'
                        }`}
                        style={{ width: `${lastPrediction.risk_score}%` }}
                      ></div>
                    </div>
                  </div>

                </div>

                {/* Resource Allocation Shortcut Button */}
                <button
                  onClick={() => setActiveTab('resources')}
                  className="w-full py-2.5 bg-blue-950/80 hover:bg-blue-900 border border-blue-800/60 text-blue-300 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-2"
                >
                  <span>Allocate Emergency Resources for this Incident</span>
                  <ArrowRight className="w-4 h-4" />
                </button>

              </div>

              {/* All Secondary Disaster Class Probabilities Chart */}
              <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-3">
                <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
                  <BarChart className="w-4 h-4 text-blue-400" />
                  <span>Class Probability Breakdown (%)</span>
                </h3>

                <div className="h-44">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={probChartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                      <XAxis dataKey="name" stroke="#94a3b8" fontSize={10} />
                      <YAxis stroke="#64748b" fontSize={10} domain={[0, 100]} />
                      <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', fontSize: '11px' }} />
                      <Bar dataKey="probability" radius={[4, 4, 0, 0]}>
                        {probChartData.map((entry, index) => (
                          <Cell 
                            key={`cell-${index}`} 
                            fill={entry.name === lastPrediction.predicted_secondary_disaster ? '#ef4444' : '#3b82f6'} 
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Transparent Explainability Section */}
              <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-3">
                <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
                  <Info className="w-4 h-4 text-amber-400" />
                  <span>Transparent Feature-Impact Explanation</span>
                </h3>

                <ul className="space-y-2 text-xs text-slate-300">
                  {lastPrediction.explanation.map((exp, idx) => (
                    <li key={idx} className="flex items-start space-x-2 bg-slate-800/40 p-2.5 rounded border border-slate-800">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{exp}</span>
                    </li>
                  ))}
                </ul>

                {/* Top Contributing Factors Table */}
                <div className="pt-2">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 font-mono">Top Contributing Factors</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs text-slate-300">
                      <thead className="bg-slate-800/80 uppercase font-mono text-[10px] text-slate-400">
                        <tr>
                          <th className="px-3 py-1.5">Feature</th>
                          <th className="px-3 py-1.5">Input Value</th>
                          <th className="px-3 py-1.5">Impact Level</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                        {lastPrediction.top_contributing_factors.map((factor, idx) => (
                          <tr key={idx}>
                            <td className="px-3 py-1.5 text-blue-400 font-semibold">{factor.feature}</td>
                            <td className="px-3 py-1.5">{factor.value}</td>
                            <td className="px-3 py-1.5">
                              <span className="px-2 py-0.5 rounded bg-red-950 text-red-300 border border-red-800 text-[10px]">
                                {factor.impact}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

              </div>

            </>
          ) : (
            <div className="bg-slate-900/90 p-12 rounded-xl border border-slate-800 text-center space-y-3 flex flex-col items-center justify-center min-h-[400px]">
              <Cpu className="w-12 h-12 text-slate-600 animate-pulse" />
              <h3 className="text-base font-bold text-slate-300">No Active AI Prediction</h3>
              <p className="text-xs text-slate-400 max-w-md">
                Configure environmental parameters on the left and click <strong>Run AI Secondary Prediction</strong> or select one of the preset scenarios.
              </p>
            </div>
          )}

        </div>

      </div>

    </div>
  );
}
