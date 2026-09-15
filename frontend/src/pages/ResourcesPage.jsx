import React, { useState, useEffect } from 'react';
import { 
  Boxes, AlertCircle, CheckCircle2, ShieldAlert, RefreshCw, Layers, ArrowRight
} from 'lucide-react';
import { allocateResources } from '../services/api';

export default function ResourcesPage({ lastPrediction }) {
  const [params, setParams] = useState({
    predicted_disaster: lastPrediction?.predicted_secondary_disaster || 'Flood',
    severity: lastPrediction?.severity || 'High',
    risk_score: lastPrediction?.risk_score || 85,
    population_density: lastPrediction?.input_conditions?.population_density || 8500
  });

  const [allocation, setAllocation] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAllocationData = async () => {
    setLoading(true);
    try {
      const res = await allocateResources(params);
      setAllocation(res);
    } catch (err) {
      alert('Error calculating resource allocation: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllocationData();
  }, []);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setParams(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-black text-white font-mono flex items-center gap-2">
            <Boxes className="w-5 h-5 text-blue-400" />
            <span>EMERGENCY RESOURCE ALLOCATION ENGINE</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Dynamic inventory demand calculation based on predicted secondary disaster type, severity multiplier, risk score, and population density.
          </p>
        </div>

        <button
          onClick={fetchAllocationData}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-bold font-mono transition-all flex items-center space-x-2 shrink-0"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Recalculate Allocation</span>
        </button>
      </div>

      {/* Inputs Bar */}
      <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-3">
        <h3 className="text-xs font-bold text-slate-400 uppercase font-mono tracking-wider">Incident Scenario Parameters</h3>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          
          <div>
            <label className="block text-slate-300 font-medium mb-1">Predicted Disaster</label>
            <select
              name="predicted_disaster"
              value={params.predicted_disaster}
              onChange={handleChange}
              className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white font-mono"
            >
              <option value="Flood">Flood</option>
              <option value="Landslide">Landslide</option>
              <option value="Infrastructure Failure">Infrastructure Failure</option>
              <option value="Fire">Fire</option>
              <option value="Disease Outbreak">Disease Outbreak</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Severity</label>
            <select
              name="severity"
              value={params.severity}
              onChange={handleChange}
              className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white font-mono"
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Risk Score (1-100)</label>
            <input
              type="number"
              name="risk_score"
              value={params.risk_score}
              onChange={handleChange}
              className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white font-mono"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Population Density</label>
            <input
              type="number"
              name="population_density"
              value={params.population_density}
              onChange={handleChange}
              className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white font-mono"
            />
          </div>

        </div>
      </div>

      {/* Shortage Alert Header */}
      {allocation && allocation.total_shortage_resources > 0 && (
        <div className="bg-red-950/80 border border-red-800 p-4 rounded-xl flex items-center space-x-3 text-red-200 text-xs">
          <ShieldAlert className="w-6 h-6 text-red-400 shrink-0" />
          <div>
            <strong className="text-white text-sm block font-mono font-bold">RESOURCE SHORTAGE DETECTED!</strong>
            <span>
              {allocation.total_shortage_resources} emergency resource category(s) exceed current inventory pool capacities. Inter-district staging dispatch recommended.
            </span>
          </div>
        </div>
      )}

      {/* Main Allocation Table */}
      <div className="bg-slate-900/90 rounded-xl border border-slate-800 overflow-hidden shadow-xl">
        <div className="p-4 bg-slate-800/80 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Layers className="w-4 h-4 text-blue-400" />
            <span>Required vs Available vs Allocated Inventory Pool</span>
          </h3>
          <span className="text-xs text-slate-400 font-mono">7 Essential Categories</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 uppercase font-mono text-[11px] text-slate-400">
              <tr>
                <th className="px-4 py-3">Resource Category</th>
                <th className="px-4 py-3">Required</th>
                <th className="px-4 py-3">Available Pool</th>
                <th className="px-4 py-3">Allocated</th>
                <th className="px-4 py-3">Shortage</th>
                <th className="px-4 py-3">Priority Status</th>
                <th className="px-4 py-3 text-right">Pool Utilization</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {allocation?.allocations.map((item) => (
                <tr key={item.resource} className="hover:bg-slate-800/40 transition-colors">
                  <td className="px-4 py-3.5 font-bold text-white flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                    <span>{item.resource}</span>
                  </td>
                  <td className="px-4 py-3.5 font-extrabold text-blue-400">{item.required}</td>
                  <td className="px-4 py-3.5 text-slate-300">{item.available}</td>
                  <td className="px-4 py-3.5 font-bold text-emerald-400">{item.allocated}</td>
                  <td className="px-4 py-3.5">
                    {item.shortage > 0 ? (
                      <span className="px-2.5 py-0.5 rounded bg-red-950 text-red-400 border border-red-800 font-bold">
                        +{item.shortage} SHORT
                      </span>
                    ) : (
                      <span className="text-slate-500">0</span>
                    )}
                  </td>
                  <td className="px-4 py-3.5">
                    <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                      item.has_shortage ? 'bg-red-950 text-red-400 border border-red-800' :
                      item.priority === 'Critical' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                      'bg-slate-800 text-slate-300'
                    }`}>
                      {item.priority}
                    </span>
                  </td>
                  <td className="px-4 py-3.5 text-right">
                    <div className="flex items-center justify-end space-x-2">
                      <span className="text-[11px]">{item.utilization_percent}%</span>
                      <div className="w-16 bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-700">
                        <div
                          className={`h-full ${item.utilization_percent >= 100 ? 'bg-red-500' : 'bg-emerald-500'}`}
                          style={{ width: `${item.utilization_percent}%` }}
                        ></div>
                      </div>
                    </div>
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
