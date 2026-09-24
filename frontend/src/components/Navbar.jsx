import React, { useState, useEffect } from 'react';
import { LayoutDashboard, Activity, Boxes, Sliders, Cpu, ShieldAlert, Radio, Clock } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  const [timeStr, setTimeStr] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toUTCString().replace('GMT', 'UTC'));
    };
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'predict', label: 'Predictor', icon: Activity },
    { id: 'resources', label: 'Resource Allocation', icon: Boxes },
    { id: 'simulator', label: 'What-If Simulator', icon: Sliders },
    { id: 'model', label: 'ML Analytics', icon: Cpu },
  ];

  return (
    <header className="bg-[#0f172a]/95 border-b border-slate-800/80 sticky top-0 z-50 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo / Brand Header */}
          <div 
            className="flex items-center space-x-3 cursor-pointer group" 
            onClick={() => setActiveTab('dashboard')}
          >
            <div className="p-2 bg-gradient-to-br from-red-600 via-red-700 to-amber-600 rounded-lg shadow-md shadow-red-950/40 border border-red-500/30 group-hover:border-red-400/60 transition-all">
              <ShieldAlert className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-base text-slate-100 tracking-wider font-mono">CHAIN-GUARD</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-blue-950/80 text-blue-400 font-mono font-bold border border-blue-800/50 uppercase tracking-wider">
                  EOC COMMAND
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium">Secondary Disaster Chain Reaction Management</p>
            </div>
          </div>

          {/* Center Navigation Tabs */}
          <nav className="hidden md:flex items-center space-x-1 bg-[#161e31]/80 p-1 rounded-lg border border-slate-800/80">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-xs font-semibold tracking-wide transition-all ${
                    isActive
                      ? 'bg-blue-600/20 text-blue-400 border border-blue-500/40 shadow-sm shadow-blue-950/50'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Status Indicators */}
          <div className="hidden lg:flex items-center space-x-3">
            <div className="flex items-center space-x-1.5 text-[11px] text-slate-400 font-mono bg-slate-900/80 px-2.5 py-1 rounded border border-slate-800">
              <Clock className="w-3 h-3 text-slate-400" />
              <span>{timeStr || 'LIVE UTC'}</span>
            </div>
            
            <div className="flex items-center space-x-2 px-2.5 py-1 rounded-full bg-emerald-950/80 border border-emerald-800/60 text-emerald-400 text-[11px] font-mono">
              <Radio className="w-3 h-3 animate-pulse text-emerald-400" />
              <span className="font-bold tracking-wider">EOC OPERATIONAL</span>
            </div>
          </div>

        </div>

        {/* Mobile Navigation Tabs */}
        <div className="md:hidden flex overflow-x-auto py-2 space-x-1 border-t border-slate-800/80">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded text-xs whitespace-nowrap font-medium ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-slate-400 hover:bg-slate-800'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

      </div>
    </header>
  );
}
