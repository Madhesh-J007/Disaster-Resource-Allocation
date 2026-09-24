import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import DashboardPage from './pages/DashboardPage';
import PredictPage from './pages/PredictPage';
import ResourcesPage from './pages/ResourcesPage';
import SimulatorPage from './pages/SimulatorPage';
import ModelPage from './pages/ModelPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  
  const [predictFormData, setPredictFormData] = useState({
    rainfall_mm: 220.0,
    river_level_m: 8.5,
    soil_moisture: 0.85,
    wind_speed_kmph: 25.0,
    temperature_c: 28.0,
    population_density: 8500.0,
    elevation_m: 120.0,
    infrastructure_vulnerability: 0.65,
    road_accessibility: 0.70,
    distance_to_water_body: 0.8,
    primary_disaster: 'Heavy Rain'
  });

  const [lastPrediction, setLastPrediction] = useState(null);

  return (
    <div className="min-h-screen flex flex-col bg-[#090d16] text-slate-100">
      
      {/* Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-5">
        {activeTab === 'dashboard' && (
          <DashboardPage 
            setActiveTab={setActiveTab} 
            setPredictFormData={setPredictFormData} 
            setLastPrediction={setLastPrediction} 
            lastPrediction={lastPrediction}
          />
        )}
        
        {activeTab === 'predict' && (
          <PredictPage 
            formData={predictFormData} 
            setFormData={setPredictFormData} 
            lastPrediction={lastPrediction} 
            setLastPrediction={setLastPrediction}
            setActiveTab={setActiveTab} 
          />
        )}
        
        {activeTab === 'resources' && (
          <ResourcesPage lastPrediction={lastPrediction} />
        )}
        
        {activeTab === 'simulator' && (
          <SimulatorPage />
        )}
        
        {activeTab === 'model' && (
          <ModelPage />
        )}
      </main>

      {/* Footer */}
      <Footer />

    </div>
  );
}
