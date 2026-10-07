import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, showDetails: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Application Render Error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-[#090d16] text-slate-100 flex items-center justify-center p-6 font-mono">
          <div className="max-w-md w-full bg-[#121827] border border-amber-500/40 rounded-lg p-6 shadow-2xl text-center space-y-4">
            <div className="inline-flex items-center justify-center p-3 bg-amber-950/80 text-amber-400 rounded-full border border-amber-800/80">
              <AlertCircle className="w-8 h-8" />
            </div>
            
            <h2 className="text-base font-extrabold text-white uppercase tracking-wider">
              Unable to load this assessment
            </h2>
            
            <p className="text-xs text-slate-400 font-sans leading-relaxed">
              An unexpected condition occurred while initializing the location intelligence view. Please try again.
            </p>

            <button
              onClick={() => {
                this.setState({ hasError: false, error: null });
                window.location.reload();
              }}
              className="w-full py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-mono font-bold text-xs uppercase tracking-wider rounded transition-all shadow-md flex items-center justify-center gap-2"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Reload Page & Try Again</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
