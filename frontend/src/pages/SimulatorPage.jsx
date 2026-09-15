import React, { useState } from 'react';
import { 
  Sliders, Play, TrendingUp, AlertTriangle, ArrowRight, RefreshCw, BarChart2
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { runSimulation } from '../services/api';

export default function SimulatorPage() {
  const [baseline, setBaseline] = useState({
    rainfall_mm: 100.0,
    river_level_m: 4.0,
    soil_moisture: 0.50,
    wind_speed_kmph: 30.0,
    temperature_c: 28.0,
    population_density: 5000.0,
    elevation_m: 100.0,
    infrastructure_vulnerability: 0.40,
    road_accessibility: 0.80,
    distance_to_water_body: 3.0,
    primary_disaster: 'Heavy Rain'
  });

  const [modified, setModified] = useState({
    rainfall_mm: 250.0,
    river_level_m: 8.5,
    soil_moisture: 0.85,
    wind_speed_kmph: 30.0,
    temperature_c: 28.0,
    population_density: 5000.0,
    elevation_m: 100.0,
    infrastructure_vulnerability: 0.75,
    road_accessibility: 0.50,
    distance_to_water_body: 1.0,
    primary_disaster: 'Heavy Rain'
  });

  const [simResult, setSimResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const res = await runSimulation(baseline, modified);
      setSimResult(res);
    } catch (err) {
      alert('Simulation error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSliderChange = (param, val) => {
    setModified(prev => ({
      ...prev,
      [param]: parseFloat(val)
    }));
  };

  const comparisonChartData = simResult ? [
    {
      metric: 'Risk Score',
      ScenarioA: simResult.baseline.risk_score,
      ScenarioB: simResult.modified.risk_score
    },
    {
      metric: 'Disaster Probability (%)',
      ScenarioA: Math.round(simResult.baseline.secondary_disaster_probability * 100),
      ScenarioB: Math.round(simResult.modified.secondary_disaster_probability * 100)
    }
  ] : [];

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-black text-white font-mono flex items-center gap-2">
            <Sliders className="w-5 h-5 text-blue-400" />
            <span>WHAT-IF COUNTERFACTUAL SIMULATOR</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Simulate environmental variable shifts to observe chain reaction cascade transitions and risk score sensitivity.
          </p>
        </div>

        <button
          onClick={handleSimulate}
          disabled={loading}
          className="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-lg text-xs font-extrabold uppercase tracking-wider shadow-lg shadow-blue-950 transition-all flex items-center space-x-2 shrink-0"
        >
          <Play className={`w-4 h-4 fill-white ${loading ? 'animate-spin' : ''}`} />
          <span>Run Simulation</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Interactive Controls (5 cols) */}
        <div className="lg:col-span-5 bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 className="text-sm font-bold text-slate-200">Scenario B Parameters (Modified)</h2>
            <button
              onClick={() => setModified({ ...baseline })}
              className="text-[10px] text-blue-400 hover:underline font-mono"
            >
              Reset to Scenario A
            </button>
          </div>

          <div className="space-y-4 text-xs">
            
            {/* Rainfall Slider */}
            <div>
              <div className="flex justify-between font-mono mb-1">
                <span className="text-slate-300 font-medium">Rainfall:</span>
                <span className="text-blue-400 font-bold">{modified.rainfall_mm} mm</span>
              </div>
              <input
                type="range"
                min="0"
                max="400"
                step="5"
                value={modified.rainfall_mm}
                onChange={(e) => handleSliderChange('rainfall_mm', e.target.value)}
                className="w-full accent-blue-500 bg-slate-950 rounded"
              />
            </div>

            {/* River Level Slider */}
            <div>
              <div className="flex justify-between font-mono mb-1">
                <span className="text-slate-300 font-medium">River Gauge Level:</span>
                <span className="text-blue-400 font-bold">{modified.river_level_m} m</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="14.0"
                step="0.5"
                value={modified.river_level_m}
                onChange={(e) => handleSliderChange('river_level_m', e.target.value)}
                className="w-full accent-blue-500 bg-slate-950 rounded"
              />
            </div>

            {/* Soil Moisture Slider */}
            <div>
              <div className="flex justify-between font-mono mb-1">
                <span className="text-slate-300 font-medium">Soil Moisture Saturation:</span>
                <span className="text-emerald-400 font-bold">{Math.round(modified.soil_moisture * 100)}%</span>
              </div>
              <input
                type="range"
                min="0.10"
                max="1.00"
                step="0.05"
                value={modified.soil_moisture}
                onChange={(e) => handleSliderChange('soil_moisture', e.target.value)}
                className="w-full accent-emerald-500 bg-slate-950 rounded"
              />
            </div>

            {/* Wind Speed Slider */}
            <div>
              <div className="flex justify-between font-mono mb-1">
                <span className="text-slate-300 font-medium">Wind Speed:</span>
                <span className="text-amber-400 font-bold">{modified.wind_speed_kmph} km/h</span>
              </div>
              <input
                type="range"
                min="5"
                max="160"
                step="5"
                value={modified.wind_speed_kmph}
                onChange={(e) => handleSliderChange('wind_speed_kmph', e.target.value)}
                className="w-full accent-amber-500 bg-slate-950 rounded"
              />
            </div>

            {/* Infrastructure Vulnerability */}
            <div>
              <div className="flex justify-between font-mono mb-1">
                <span className="text-slate-300 font-medium">Infrastructure Vulnerability:</span>
                <span className="text-red-400 font-bold">{Math.round(modified.infrastructure_vulnerability * 100)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="1.00"
                step="0.05"
                value={modified.infrastructure_vulnerability}
                onChange={(e) => handleSliderChange('infrastructure_vulnerability', e.target.value)}
                className="w-full accent-red-500 bg-slate-950 rounded"
              />
            </div>

            {/* Road Accessibility */}
            <div>
              <div className="flex justify-between font-mono mb-1">
                <span className="text-slate-300 font-medium">Road Accessibility Index:</span>
                <span className="text-purple-400 font-bold">{Math.round(modified.road_accessibility * 100)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="1.00"
                step="0.05"
                value={modified.road_accessibility}
                onChange={(e) => handleSliderChange('road_accessibility', e.target.value)}
                className="w-full accent-purple-500 bg-slate-950 rounded"
              />
            </div>

          </div>

          <button
            onClick={handleSimulate}
            disabled={loading}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-extrabold text-xs uppercase tracking-wider rounded-lg transition-all"
          >
            {loading ? 'Running Counterfactual AI Inference...' : 'Run Simulation Comparison'}
          </button>
        </div>

        {/* Right Column: Comparison Results & Visual Charts (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          
          {simResult ? (
            <>
              {/* Comparison Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                
                {/* Scenario A Card */}
                <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-2">
                  <span className="text-[10px] text-slate-400 font-mono uppercase tracking-wider block">Scenario A (Baseline)</span>
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-bold text-slate-200">{simResult.baseline.predicted_secondary_disaster}</h3>
                    <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono border border-slate-700">
                      {simResult.baseline.severity}
                    </span>
                  </div>
                  <div className="pt-2 flex items-baseline justify-between border-t border-slate-800">
                    <span className="text-xs text-slate-400">Risk Score</span>
                    <span className="text-xl font-extrabold text-white font-mono">{simResult.baseline.risk_score}</span>
                  </div>
                </div>

                {/* Scenario B Card */}
                <div className="bg-slate-900/90 p-5 rounded-xl border border-blue-600/40 space-y-2 relative overflow-hidden">
                  <div className="absolute right-0 top-0 w-24 h-full bg-blue-500/10 pointer-events-none"></div>
                  <span className="text-[10px] text-blue-400 font-mono uppercase tracking-wider block">Scenario B (Simulated)</span>
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-bold text-red-400">{simResult.modified.predicted_secondary_disaster}</h3>
                    <span className="text-xs px-2 py-0.5 rounded bg-red-950 text-red-400 font-mono border border-red-800">
                      {simResult.modified.severity}
                    </span>
                  </div>
                  <div className="pt-2 flex items-baseline justify-between border-t border-slate-800">
                    <span className="text-xs text-slate-400">Risk Score</span>
                    <span className="text-xl font-extrabold text-red-400 font-mono">{simResult.modified.risk_score}</span>
                  </div>
                </div>

              </div>

              {/* Shift Summary Banner */}
              <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-blue-950 p-4 rounded-xl border border-slate-800 flex items-center space-x-3 text-xs text-slate-200 font-mono">
                <TrendingUp className="w-5 h-5 text-amber-400 shrink-0" />
                <div>
                  <strong className="text-white block font-bold">SIMULATION DELTA RESULT:</strong>
                  <span>{simResult.impact_summary}</span>
                </div>
              </div>

              {/* Comparison Chart */}
              <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-3">
                <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
                  <BarChart2 className="w-4 h-4 text-blue-400" />
                  <span>Baseline (A) vs Simulated (B) Comparison</span>
                </h3>

                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={comparisonChartData} margin={{ top: 20, right: 30, left: 10, bottom: 5 }}>
                      <XAxis dataKey="metric" stroke="#94a3b8" fontSize={11} />
                      <YAxis stroke="#64748b" fontSize={11} />
                      <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', fontSize: '12px' }} />
                      <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                      <Bar dataKey="ScenarioA" name="Scenario A (Baseline)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="ScenarioB" name="Scenario B (Simulated)" fill="#ef4444" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

            </>
          ) : (
            <div className="bg-slate-900/90 p-12 rounded-xl border border-slate-800 text-center space-y-3 flex flex-col items-center justify-center min-h-[350px]">
              <Play className="w-12 h-12 text-slate-600 animate-bounce" />
              <h3 className="text-base font-bold text-slate-300">Run What-If Simulation</h3>
              <p className="text-xs text-slate-400 max-w-md">
                Adjust sliders on the left (e.g. increase rainfall from 100mm to 250mm) and click <strong>Run Simulation</strong> to visualize counterfactual risk transitions.
              </p>
            </div>
          )}

        </div>

      </div>

    </div>
  );
}
