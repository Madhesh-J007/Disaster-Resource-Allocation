import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-[#0b0f19] border-t border-slate-800 py-6 mt-12 text-slate-400 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
        
        <div className="flex items-center space-x-2 text-slate-400">
          <AlertCircle className="w-4 h-4 text-amber-500 shrink-0" />
          <span>
            <strong className="text-slate-300">Academic Prototype Notice:</strong> System trained on 3,500 synthetic disaster records for research & PBL demonstration.
          </span>
        </div>

        <div className="flex items-center space-x-4 font-mono text-[11px] text-slate-400">
          <span>Tech Stack: FastAPI • React • scikit-learn (RandomForest)</span>
          <span>•</span>
          <span>© 2026 AI PBL Project</span>
        </div>

      </div>
    </footer>
  );
}
