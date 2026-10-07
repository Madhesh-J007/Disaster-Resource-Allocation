import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, AlertTriangle, Activity, Database, CheckCircle, ArrowRight,
  TrendingUp, BarChart2, Zap, Server, Radio, Cpu, Layers, MapPin, Sliders, ShieldCheck,
  AlertCircle, Users, Truck, Hospital, Building, Mountain, RefreshCw, Play, Info, Eye, FileText
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie
} from 'recharts';
import SearchableDistrictSelector from '../components/SearchableDistrictSelector';
import { 
  fetchDistricts, 
  fetchDistrictInfo, 
  assessLocationImpact, 
  fetchDemoScenarios, 
  runSimulation 
} from '../services/api';

const PRIMARY_DISASTERS = [
  'Heavy Rain', 'Cyclone', 'Earthquake', 'Extreme Heat', 'Landslide Trigger'
];

const CATEGORY_COLORS = {
  'Flood': '#ef4444',
  'Fire': '#f97316',
  'Infrastructure Failure': '#8b5cf6',
  'Landslide': '#f59e0b',
  'Disease Outbreak': '#3b82f6'
};

const SEVERITY_COLORS = {
  'Critical': '#dc2626',
  'High': '#f59e0b',
  'Medium': '#3b82f6',
  'Low': '#10b981'
};

export default function DashboardPage({ setActiveTab, setPredictFormData, setLastPrediction }) {
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState('Chennai');
  const [primaryDisaster, setPrimaryDisaster] = useState('Heavy Rain');
  const [scenarioInputs, setScenarioInputs] = useState(null);

  const [locationImpact, setLocationImpact] = useState(null);
  const [isAssessmentPending, setIsAssessmentPending] = useState(false);
  const [loading, setLoading] = useState(true);
  const [evaluating, setEvaluating] = useState(false);
  const [demos, setDemos] = useState([]);

  // Location-aware simulator states
  const [simModified, setSimModified] = useState(null);
  const [simResult, setSimResult] = useState(null);
  const [simLoading, setSimLoading] = useState(false);

  // Load Tamil Nadu districts list & initial Chennai impact assessment on mount
  useEffect(() => {
    async function initDashboard() {
      try {
        const distData = await fetchDistricts();
        setDistricts(Array.isArray(distData) ? distData : (distData.districts || []));
        
        const demoData = await fetchDemoScenarios();
        setDemos(demoData.scenarios || []);

        // Initial mount: load Chennai baseline ONLY into Tier 1 (no automatic ML prediction)
        const base = await fetchDistrictInfo('Chennai');
        const inputs = { ...base, primary_disaster: 'Heavy Rain' };
        setScenarioInputs(inputs);
        setLocationImpact(null);
        setIsAssessmentPending(true);

        setSimModified({
          ...inputs,
          rainfall_mm: Math.min(400, Math.round(inputs.rainfall_mm * 1.3)),
          river_level_m: Math.min(14, Math.round(inputs.river_level_m * 1.25 * 10) / 10),
          soil_moisture: Math.min(1.0, Math.round((inputs.soil_moisture + 0.10) * 100) / 100)
        });
      } catch (err) {
        console.error('Error initializing location-aware dashboard:', err);
      } finally {
        setLoading(false);
      }
    }
    initDashboard();
  }, []);

  // STEP 1: District selector change -> Loads baseline ONLY into Tier 1, DOES NOT run ML prediction
  const handleDistrictChange = async (dName) => {
    setSelectedDistrict(dName);
    setEvaluating(true);
    try {
      const base = await fetchDistrictInfo(dName);
      const inputs = { ...base, primary_disaster: primaryDisaster };
      setScenarioInputs(inputs);

      // Explicitly mark assessment as pending and clear downstream ML prediction results
      setIsAssessmentPending(true);
      setLocationImpact(null);
    } catch (err) {
      console.error(`Error loading baseline for ${dName}:`, err);
    } finally {
      setEvaluating(false);
    }
  };

  // STEP 1: Primary disaster change -> Updates inputs, DOES NOT run ML prediction
  const handleDisasterChange = (disaster) => {
    setPrimaryDisaster(disaster);
    setScenarioInputs(prev => ({
      ...prev,
      primary_disaster: disaster
    }));
    setIsAssessmentPending(true);
    setLocationImpact(null);
  };

  // STEP 1: Numeric input change -> Updates inputs, DOES NOT run ML prediction
  const handleInputChange = (field, val) => {
    setScenarioInputs(prev => ({
      ...prev,
      [field]: parseFloat(val) || 0
    }));
    setIsAssessmentPending(true);
    setLocationImpact(null);
  };

  // STEP 2: Explicit "ASSESS DISASTER IMPACT" click -> Runs ML models & updates Tier 2+
  const handleRunAssessment = async (e) => {
    if (e) e.preventDefault();
    setEvaluating(true);
    try {
      const impact = await assessLocationImpact({
        location: selectedDistrict,
        primary_disaster: primaryDisaster,
        ...scenarioInputs
      });
      setLocationImpact(impact);
      setLastPrediction(impact);
      setIsAssessmentPending(false);

      // Re-initialize simulator inputs
      setSimModified({
        ...scenarioInputs,
        rainfall_mm: Math.min(400, Math.round(scenarioInputs.rainfall_mm * 1.3)),
        river_level_m: Math.min(14, Math.round(scenarioInputs.river_level_m * 1.25 * 10) / 10),
        soil_moisture: Math.min(1.0, Math.round((scenarioInputs.soil_moisture + 0.10) * 100) / 100)
      });
    } catch (err) {
      alert('Error evaluating location impact: ' + err.message);
    } finally {
      setEvaluating(false);
    }
  };

  const handleRunDemoScenario = async (demo) => {
    const loc = demo.location || 'Chennai';
    setSelectedDistrict(loc);
    setPrimaryDisaster(demo.data.primary_disaster);
    setScenarioInputs(demo.data);
    setPredictFormData(demo.data);

    setEvaluating(true);
    try {
      const impact = await assessLocationImpact({
        location: loc,
        primary_disaster: demo.data.primary_disaster,
        ...demo.data
      });
      setLocationImpact(impact);
      setLastPrediction(impact);
      setIsAssessmentPending(false);
    } catch (err) {
      alert('Error running demo scenario: ' + err.message);
    } finally {
      setEvaluating(false);
    }
  };

  const handleRunSim = async () => {
    if (!scenarioInputs || !simModified) return;
    setSimLoading(true);
    try {
      const res = await runSimulation(scenarioInputs, simModified, selectedDistrict);
      setSimResult(res);
    } catch (err) {
      alert('Simulation error: ' + err.message);
    } finally {
      setSimLoading(false);
    }
  };

  // Probabilities chart data
  const probChartData = locationImpact?.class_probabilities
    ? Object.entries(locationImpact.class_probabilities).map(([name, prob]) => ({
        name,
        probability: Math.round(prob * 100)
      }))
    : [];

  return (
    <div className="space-y-6 text-slate-100">
      
      {/* 1. LOCATION-AWARE EOC COMMAND HEADER */}
      <div className="bg-[#121827] px-5 py-4 rounded-lg border border-slate-800/80 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-3">
            <h1 className="text-xl font-extrabold text-white font-mono tracking-tight flex items-center gap-2">
              <span>LOCATION-AWARE DISASTER IMPACT ASSESSMENT</span>
            </h1>
            <span className="text-[10px] px-2 py-0.5 rounded bg-blue-950 text-blue-400 border border-blue-800/80 font-mono font-bold uppercase tracking-wider flex items-center gap-1">
              <Radio className="w-3 h-3 animate-pulse text-blue-400" />
              TAMIL NADU DECISION SUPPORT
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Answers: <em>"If a disaster occurs in a specific district, what happens next, what is affected, and what resources are required?"</em>
          </p>
        </div>

        {/* Technical Evidence Tier Badges */}
        <div className="flex flex-wrap items-center gap-2 text-[10px] font-mono">
          <span className="px-2.5 py-1 bg-emerald-950/80 text-emerald-400 rounded border border-emerald-800/80 flex items-center gap-1">
            <Database className="w-3 h-3" /> 1. OBSERVED DISTRICT DATA
          </span>
          <span className="px-2.5 py-1 bg-amber-950/80 text-amber-300 rounded border border-amber-800/80 flex items-center gap-1">
            <Cpu className="w-3 h-3" /> 2. ML MODEL PREDICTION
          </span>
          <span className="px-2.5 py-1 bg-purple-950/80 text-purple-300 rounded border border-purple-800/80 flex items-center gap-1">
            <Building className="w-3 h-3" /> 3. DERIVED EXPOSURE
          </span>
        </div>
      </div>

      {/* 2. TOP LOCATION & SCENARIO SELECTION BAR */}
      <div className="bg-[#121827] p-4 sm:p-5 rounded-lg border border-slate-800/80 space-y-4 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
          <h2 className="text-xs font-bold text-slate-200 uppercase font-mono tracking-wider flex items-center gap-2">
            <MapPin className="w-4 h-4 text-blue-400" />
            <span>Select Target Location & Primary Event</span>
          </h2>
          <span className="text-[10px] text-slate-400 font-mono">
            38 Tamil Nadu Districts Available
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          {/* Location / District Searchable Selector */}
          <div>
            <label className="block text-[11px] font-mono font-bold text-slate-300 uppercase mb-1.5">
              Location / District:
            </label>
            <SearchableDistrictSelector
              districts={districts}
              selectedDistrict={selectedDistrict}
              onSelectDistrict={handleDistrictChange}
            />
          </div>

          {/* Primary Disaster Selector */}
          <div>
            <label className="block text-[11px] font-mono font-bold text-slate-300 uppercase mb-1.5">
              Primary Event:
            </label>
            <select
              value={primaryDisaster}
              onChange={(e) => handleDisasterChange(e.target.value)}
              className="w-full bg-[#0b0f19] border border-slate-700 hover:border-slate-500 rounded p-2.5 text-xs font-mono text-white font-bold focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all shadow-inner"
            >
              {PRIMARY_DISASTERS.map(pd => (
                <option key={pd} value={pd}>🌧 {pd}</option>
              ))}
            </select>
          </div>

        </div>

        {/* Assess Button */}
        <div className="pt-1">
          <button
            onClick={handleRunAssessment}
            disabled={evaluating}
            className="w-full py-3 bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-500 hover:to-indigo-500 text-white font-mono font-extrabold text-xs uppercase tracking-wider rounded transition-all shadow-lg shadow-blue-950/60 flex items-center justify-center space-x-2 border border-blue-400/30 cursor-pointer"
          >
            {evaluating ? (
              <span>Evaluating Location Impact...</span>
            ) : (
              <>
                <Zap className="w-4 h-4 text-amber-300 animate-pulse" />
                <span>Assess Disaster Impact</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* 3. SCENARIO INPUT CONDITIONS GRID */}
      {scenarioInputs && (
        <div className="bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-2 text-xs font-mono">
            <span className="font-bold text-slate-300 uppercase flex items-center gap-1.5">
              <Sliders className="w-3.5 h-3.5 text-amber-400" />
              <span>TIER 1: OBSERVED DISTRICT BASELINE ({selectedDistrict}) + SCENARIO INPUTS</span>
            </span>
            <button 
              onClick={() => handleDistrictChange(selectedDistrict)}
              className="text-[10px] text-blue-400 hover:underline flex items-center gap-1"
            >
              <RefreshCw className="w-3 h-3" /> Reset to District Baseline
            </button>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-5 lg:grid-cols-10 gap-2 text-[11px] font-mono">
            <div>
              <span className="text-slate-400 text-[10px] block">Rainfall (mm)</span>
              <input 
                type="number" 
                value={scenarioInputs.rainfall_mm} 
                onChange={(e) => handleInputChange('rainfall_mm', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-blue-400 font-bold" 
              />
            </div>
            <div>
              <span className="text-slate-400 text-[10px] block">River Stage (m)</span>
              <input 
                type="number" 
                value={scenarioInputs.river_level_m} 
                onChange={(e) => handleInputChange('river_level_m', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-blue-400 font-bold" 
              />
            </div>
            <div>
              <span className="text-slate-400 text-[10px] block">Soil Saturation</span>
              <input 
                type="number" 
                step="0.01"
                value={scenarioInputs.soil_moisture} 
                onChange={(e) => handleInputChange('soil_moisture', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-emerald-400 font-bold" 
              />
            </div>
            <div>
              <span className="text-slate-400 text-[10px] block">Wind (km/h)</span>
              <input 
                type="number" 
                value={scenarioInputs.wind_speed_kmph} 
                onChange={(e) => handleInputChange('wind_speed_kmph', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-amber-400 font-bold" 
              />
            </div>
            <div>
              <span className="text-slate-400 text-[10px] block">Temp (°C)</span>
              <input 
                type="number" 
                value={scenarioInputs.temperature_c} 
                onChange={(e) => handleInputChange('temperature_c', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-slate-200 font-bold" 
              />
            </div>
            <div>
              <span className="text-slate-400 text-[10px] block">Pop Density</span>
              <input 
                type="number" 
                value={scenarioInputs.population_density} 
                onChange={(e) => handleInputChange('population_density', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-slate-200 font-bold" 
              />
            </div>
            <div>
              <span className="text-slate-400 text-[10px] block">Elevation (m)</span>
              <input 
                type="number" 
                value={scenarioInputs.elevation_m} 
                onChange={(e) => handleInputChange('elevation_m', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-slate-200 font-bold" 
              />
            </div>
            <div>
              <span className="text-slate-400 text-[10px] block">Infra Vuln</span>
              <input 
                type="number" 
                step="0.01"
                value={scenarioInputs.infrastructure_vulnerability} 
                onChange={(e) => handleInputChange('infrastructure_vulnerability', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-red-400 font-bold" 
              />
            </div>
            <div>
              <span className="text-slate-400 text-[10px] block">Road Access</span>
              <input 
                type="number" 
                step="0.01"
                value={scenarioInputs.road_accessibility} 
                onChange={(e) => handleInputChange('road_accessibility', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-purple-400 font-bold" 
              />
            </div>
            <div>
              <span className="text-slate-400 text-[10px] block">Dist Water (km)</span>
              <input 
                type="number" 
                step="0.1"
                value={scenarioInputs.distance_to_water_body} 
                onChange={(e) => handleInputChange('distance_to_water_body', e.target.value)}
                className="w-full bg-[#0b0f19] border border-slate-700 rounded p-1 text-slate-200 font-bold" 
              />
            </div>
          </div>
        </div>
      )}

      {/* ASSESSMENT PENDING CARD (BEFORE CLICKING ASSESS DISASTER IMPACT) */}
      {(isAssessmentPending || !locationImpact) && (
        <div className="bg-[#121827] p-8 rounded-lg border border-amber-500/40 shadow-2xl text-center space-y-4 my-2">
          <div className="inline-flex items-center justify-center p-3.5 bg-amber-950/70 text-amber-400 rounded-full border border-amber-800/80 mb-1">
            <AlertCircle className="w-8 h-8 animate-pulse text-amber-400" />
          </div>
          <div>
            <span className="text-[10px] font-mono font-bold uppercase tracking-wider px-2.5 py-1 bg-amber-950 text-amber-400 rounded border border-amber-800/80 inline-block mb-2">
              Assessment Pending
            </span>
            <h3 className="text-base font-extrabold text-white font-mono uppercase tracking-wide">
              No assessment has been run for {selectedDistrict}
            </h3>
            <p className="text-xs text-slate-400 max-w-lg mx-auto mt-2 font-sans leading-relaxed">
              Target location baseline features have been loaded into Tier 1. Click <strong className="text-amber-300 font-bold">"ASSESS DISASTER IMPACT"</strong> to run the Random Forest ML models and generate secondary disaster risks, severity metrics, exposure ratings, and resource allocation.
            </p>
          </div>
          <div className="pt-2">
            <button
              onClick={handleRunAssessment}
              disabled={evaluating}
              className="px-6 py-3 bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-500 hover:to-indigo-500 text-white font-mono font-extrabold text-xs uppercase tracking-wider rounded transition-all shadow-lg shadow-blue-950/60 flex items-center justify-center space-x-2 mx-auto border border-blue-400/30 cursor-pointer"
            >
              <Zap className="w-4 h-4 text-amber-300 animate-pulse" />
              <span>Assess Disaster Impact for {selectedDistrict}</span>
            </button>
          </div>
        </div>
      )}

      {/* 4. PREDICTION OUTPUT & IMPACT CARD */}
      {!isAssessmentPending && locationImpact && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          
          {/* Main Assessment Summary Card (7 Cols) */}
          <div className="lg:col-span-7 bg-[#121827] p-5 rounded-lg border border-slate-800/80 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
              <div className="flex items-center space-x-2">
                <ShieldAlert className="w-5 h-5 text-red-400" />
                <h3 className="text-sm font-extrabold text-white font-mono uppercase tracking-wider">
                  TIER 2: ML PREDICTION OUTPUT ({locationImpact.location.toUpperCase()})
                </h3>
              </div>
              <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${
                locationImpact.severity === 'Critical' ? 'bg-red-950 text-red-400 border-red-800' :
                locationImpact.severity === 'High' ? 'bg-amber-950 text-amber-400 border-amber-800' :
                'bg-blue-950 text-blue-400 border-blue-800'
              }`}>
                {locationImpact.severity} SEVERITY
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              
              <div className="bg-[#0b0f19] p-4 rounded border border-slate-800/90 space-y-2">
                <span className="text-[10px] text-slate-400 font-mono uppercase">Predicted Secondary Hazard</span>
                <h4 className="text-xl font-black text-red-400 font-mono flex items-center gap-2">
                  <span>{locationImpact.predicted_secondary_disaster}</span>
                </h4>
                <div className="text-xs font-mono text-slate-300">
                  Model Confidence: <strong className="text-white">{Math.round(locationImpact.probability * 100)}%</strong>
                </div>
              </div>

              <div className="bg-[#0b0f19] p-4 rounded border border-slate-800/90 space-y-2">
                <span className="text-[10px] text-slate-400 font-mono uppercase">Cascade Risk Index</span>
                <div className="text-2xl font-black text-white font-mono">
                  {locationImpact.risk_score}<span className="text-xs text-slate-500 font-normal">/100</span>
                </div>
                <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div 
                    className={`h-full ${locationImpact.risk_score >= 80 ? 'bg-red-500' : 'bg-amber-500'}`}
                    style={{ width: `${locationImpact.risk_score}%` }}
                  ></div>
                </div>
              </div>

            </div>

            {/* Factor Explanations */}
            <div className="space-y-2 pt-1">
              <span className="text-[11px] font-mono font-bold text-slate-300 uppercase block">Transparent Factor-Impact Reasoning</span>
              <ul className="space-y-1.5 text-xs text-slate-300 font-sans">
                {locationImpact.risk_explanation.map((exp, idx) => (
                  <li key={idx} className="flex items-start space-x-2 bg-[#0b0f19] p-2 rounded border border-slate-800/80">
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                    <span>{exp}</span>
                  </li>
                ))}
              </ul>
            </div>

          </div>

          {/* Secondary Class Probabilities Chart (5 Cols) */}
          <div className="lg:col-span-5 bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3 flex flex-col justify-between">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
              <h3 className="text-xs font-bold text-slate-200 font-mono uppercase">Secondary Class Probabilities (%)</h3>
              <span className="text-[10px] text-slate-400 font-mono">5 Target Classes</span>
            </div>

            <div className="h-52">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={probChartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                  <XAxis dataKey="name" stroke="#94a3b8" fontSize={9} />
                  <YAxis stroke="#64748b" fontSize={9} domain={[0, 100]} />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', fontSize: '11px' }} />
                  <Bar dataKey="probability" radius={[3, 3, 0, 0]}>
                    {probChartData.map((entry) => (
                      <Cell 
                        key={`cell-${entry.name}`} 
                        fill={entry.name === locationImpact?.predicted_secondary_disaster ? '#ef4444' : '#3b82f6'} 
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <button
              onClick={() => setActiveTab('resources')}
              className="w-full py-2 bg-blue-950/80 hover:bg-blue-900 text-blue-300 rounded text-xs font-mono font-bold border border-blue-800/60 transition-all flex items-center justify-center gap-1.5"
            >
              <span>View Full Resource Allocation Table</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

        </div>
      )}

      {/* 5. TIER 3: DERIVED EXPOSURE ASSESSMENT ("WHAT COULD BE AFFECTED?") */}
      {locationImpact && (
        <div className="bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
            <div className="flex items-center space-x-2">
              <Building className="w-4 h-4 text-purple-400" />
              <h3 className="text-xs font-bold text-slate-200 font-mono uppercase tracking-wider">
                TIER 3: DERIVED EXPOSURE ASSESSMENT ({selectedDistrict})
              </h3>
            </div>
            <span className="text-[10px] bg-purple-950 text-purple-400 px-2 py-0.5 rounded border border-purple-800 font-mono font-bold">
              CATEGORY-LEVEL VULNERABILITY RATINGS
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
            {locationImpact.potentially_affected_systems.map((sys, idx) => (
              <div key={idx} className="bg-[#0b0f19] p-3 rounded border border-slate-800 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-200 truncate">{sys.category}</span>
                  <span className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded border ${
                    sys.exposure_level.includes('HIGH') ? 'bg-red-950 text-red-400 border-red-800' :
                    sys.exposure_level.includes('ELEVATED') ? 'bg-amber-950 text-amber-400 border-amber-800' :
                    'bg-slate-900 text-slate-300 border-slate-700'
                  }`}>
                    {sys.exposure_level}
                  </span>
                </div>
                
                <p className="text-[11px] text-slate-400 line-clamp-3 leading-snug">{sys.detail}</p>

                <div className="pt-1.5 border-t border-slate-800/80 text-[10px] font-mono text-slate-300">
                  Observed Metric: <span className="text-blue-400 font-bold">{sys.metric}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 6. TIER 4: CONCEPTUAL CASCADE CHAIN REACTION DIAGRAM */}
      {locationImpact && (
        <div className="bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
            <div className="flex items-center space-x-2">
              <Layers className="w-4 h-4 text-amber-400" />
              <h3 className="text-xs font-bold text-slate-200 font-mono uppercase tracking-wider">
                TIER 4: CONCEPTUAL CASCADE PROPAGATION ("WHAT HAPPENS NEXT?")
              </h3>
            </div>
            <span className="text-[10px] bg-amber-950 text-amber-400 font-mono px-2 py-0.5 rounded border border-amber-800 font-bold">
              PROOFS-OF-CONCEPT DECISION SUPPORT STEP
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-6 gap-2 text-center">
            {locationImpact.cascade_chain.map((step, idx) => (
              <div key={idx} className="relative bg-[#0b0f19] p-3 rounded border border-slate-800 flex flex-col justify-between space-y-2">
                <span className="text-[9px] font-mono text-slate-500 font-bold block">STEP 0{idx+1}</span>
                <p className="text-xs font-mono font-bold text-slate-200 leading-tight">{step}</p>
                {idx < locationImpact.cascade_chain.length - 1 && (
                  <div className="hidden md:block absolute -right-2 top-1/2 -translate-y-1/2 z-10 text-slate-600">
                    ➔
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 7. RESOURCE RESPONSE PLAN & LOCATION RESPONSE PRIORITIES */}
      {locationImpact && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          
          {/* Resource Allocation Table (7 Cols) */}
          <div className="lg:col-span-7 bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
              <h3 className="text-xs font-bold text-slate-200 font-mono uppercase">
                Resource Response Plan ({selectedDistrict})
              </h3>
              <span className="text-[10px] text-slate-400 font-mono">
                Shortage Count: <strong className="text-red-400">{locationImpact.total_shortages}</strong>
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono text-slate-300">
                <thead className="bg-[#0b0f19] uppercase text-[10px] text-slate-400">
                  <tr>
                    <th className="px-3 py-2">Resource</th>
                    <th className="px-3 py-2">Required</th>
                    <th className="px-3 py-2">Available</th>
                    <th className="px-3 py-2">Allocated</th>
                    <th className="px-3 py-2">Shortage</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-[11px]">
                  {locationImpact.resource_allocation.map((item) => (
                    <tr key={item.resource} className="hover:bg-slate-800/30">
                      <td className="px-3 py-2 font-bold text-white">{item.resource}</td>
                      <td className="px-3 py-2 text-blue-400 font-extrabold">{item.required}</td>
                      <td className="px-3 py-2 text-slate-400">{item.available}</td>
                      <td className="px-3 py-2 text-emerald-400 font-bold">{item.allocated}</td>
                      <td className="px-3 py-2">
                        {item.shortage > 0 ? (
                          <span className="px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800 font-bold text-[10px]">
                            +{item.shortage} SHORT
                          </span>
                        ) : (
                          <span className="text-slate-500">0</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Response Priorities (5 Cols) */}
          <div className="lg:col-span-5 bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
              <h3 className="text-xs font-bold text-slate-200 font-mono uppercase">
                Location Response Priorities
              </h3>
              <span className="text-[10px] text-slate-400 font-mono">Ranked Decision Support</span>
            </div>

            <div className="space-y-2">
              {locationImpact.response_priorities.map((p) => (
                <div key={p.rank} className="bg-[#0b0f19] p-2.5 rounded border border-slate-800 space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold font-mono text-white flex items-center gap-1.5">
                      <span className="px-1.5 py-0.5 rounded bg-blue-950 text-blue-400 text-[10px]">RANK #{p.rank}</span>
                      <span>{p.resource}</span>
                    </span>
                    <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800 font-bold">
                      {p.priority}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 leading-snug">{p.reason}</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

      {/* 8. LOCATION-AWARE WHAT-IF SIMULATOR */}
      {simModified && (
        <div className="bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
            <div className="flex items-center space-x-2">
              <Sliders className="w-4 h-4 text-blue-400" />
              <h3 className="text-xs font-bold text-slate-200 font-mono uppercase tracking-wider">
                Location What-If Simulator ({selectedDistrict})
              </h3>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">"What if conditions worsen in {selectedDistrict}?"</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
            
            {/* Simulator Controls (5 Cols) */}
            <div className="md:col-span-5 bg-[#0b0f19] p-3.5 rounded border border-slate-800 space-y-3">
              <span className="text-xs font-bold font-mono text-slate-300 block border-b border-slate-800 pb-1">
                Modified Scenario Parameters ({selectedDistrict})
              </span>

              <div className="space-y-3 text-xs font-mono">
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-400">Rainfall:</span>
                    <span className="text-blue-400 font-bold">{simModified.rainfall_mm} mm</span>
                  </div>
                  <input 
                    type="range" min="0" max="400" step="5" 
                    value={simModified.rainfall_mm}
                    onChange={(e) => setSimModified(prev => ({ ...prev, rainfall_mm: parseFloat(e.target.value) }))}
                    className="w-full accent-blue-500 bg-slate-900"
                  />
                </div>

                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-400">River Stage:</span>
                    <span className="text-blue-400 font-bold">{simModified.river_level_m} m</span>
                  </div>
                  <input 
                    type="range" min="0.5" max="14.0" step="0.5" 
                    value={simModified.river_level_m}
                    onChange={(e) => setSimModified(prev => ({ ...prev, river_level_m: parseFloat(e.target.value) }))}
                    className="w-full accent-blue-500 bg-slate-900"
                  />
                </div>

                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-400">Soil Saturation:</span>
                    <span className="text-emerald-400 font-bold">{Math.round(simModified.soil_moisture * 100)}%</span>
                  </div>
                  <input 
                    type="range" min="0.10" max="1.00" step="0.05" 
                    value={simModified.soil_moisture}
                    onChange={(e) => setSimModified(prev => ({ ...prev, soil_moisture: parseFloat(e.target.value) }))}
                    className="w-full accent-emerald-500 bg-slate-900"
                  />
                </div>
              </div>

              <button
                onClick={handleRunSim}
                disabled={simLoading}
                className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white font-mono font-bold text-xs uppercase tracking-wider rounded transition-all flex items-center justify-center gap-1.5"
              >
                <Play className={`w-3.5 h-3.5 ${simLoading ? 'animate-spin' : ''}`} />
                <span>Run Simulation Comparison</span>
              </button>
            </div>

            {/* Simulation Results (7 Cols) */}
            <div className="md:col-span-7 bg-[#0b0f19] p-3.5 rounded border border-slate-800 space-y-3">
              {simResult ? (
                <>
                  <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                    <div className="bg-[#121827] p-3 rounded border border-slate-800">
                      <span className="text-slate-400 text-[10px] block">Baseline Scenario A</span>
                      <h4 className="text-sm font-bold text-white mt-1">{simResult.baseline.predicted_secondary_disaster}</h4>
                      <div className="text-slate-400 mt-1">
                        Risk Score: <strong className="text-white">{simResult.baseline.risk_score}/100</strong>
                      </div>
                    </div>

                    <div className="bg-[#121827] p-3 rounded border border-blue-800/80">
                      <span className="text-blue-400 text-[10px] block font-bold">Modified Scenario B ({selectedDistrict})</span>
                      <h4 className="text-sm font-bold text-red-400 mt-1">{simResult.modified.predicted_secondary_disaster}</h4>
                      <div className="text-slate-400 mt-1">
                        Risk Score: <strong className="text-red-400">{simResult.modified.risk_score}/100</strong>
                      </div>
                    </div>
                  </div>

                  <div className="p-2.5 bg-[#121827] rounded border border-slate-800 text-xs font-mono text-slate-300 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-amber-400 shrink-0" />
                    <span>{simResult.impact_summary}</span>
                  </div>
                </>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-400 space-y-2">
                  <Sliders className="w-8 h-8 text-slate-600 animate-bounce" />
                  <span className="text-xs font-mono">Adjust sliders on the left and click <strong>Run Simulation Comparison</strong></span>
                </div>
              )}
            </div>

          </div>
        </div>
      )}

      {/* 9. SCENARIO INTELLIGENCE (DEMOS) */}
      <div className="bg-[#121827] p-4 rounded-lg border border-slate-800/80 space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
          <div className="flex items-center space-x-2">
            <Zap className="w-4 h-4 text-amber-400" />
            <h3 className="text-xs font-bold text-slate-200 font-mono uppercase tracking-wider">
              Scenario Intelligence (Preconfigured Test Cases)
            </h3>
          </div>
          <span className="text-[10px] text-slate-400 font-mono">3 Regional Scenarios</span>
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
                  <div>Location: <span className="text-slate-200">{demo.location || 'Chennai'}</span></div>
                </div>
              </div>

              <button
                onClick={() => handleRunDemoScenario(demo)}
                className="w-full py-1.5 bg-blue-600/20 hover:bg-blue-600/40 text-blue-400 hover:text-white border border-blue-500/30 rounded text-xs font-mono font-bold transition-all flex items-center justify-center gap-1"
              >
                <span>Run Location Demo Scenario</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
