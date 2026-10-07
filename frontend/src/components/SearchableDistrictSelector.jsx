import React, { useState, useRef, useEffect } from 'react';
import { Search, ChevronDown, MapPin, Check, X } from 'lucide-react';

export default function SearchableDistrictSelector({ districts = [], selectedDistrict = '', onSelectDistrict }) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [highlightedIndex, setHighlightedIndex] = useState(0);

  const containerRef = useRef(null);
  const searchInputRef = useRef(null);
  const listRef = useRef(null);

  // Normalize districts prop to array of district names safely
  const safeDistricts = Array.isArray(districts) ? districts : [];
  const districtNames = safeDistricts.map(d => typeof d === 'string' ? d : (d && d.district) || '').filter(Boolean);

  // Filter district names based on search query
  const filteredDistricts = districtNames.filter(name =>
    name.toLowerCase().includes(searchQuery.toLowerCase().trim())
  );

  // Close dropdown on click outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Focus search input when dropdown opens
  useEffect(() => {
    if (isOpen) {
      setHighlightedIndex(0);
      setTimeout(() => {
        if (searchInputRef.current) {
          searchInputRef.current.focus();
        }
      }, 50);
    } else {
      setSearchQuery('');
    }
  }, [isOpen]);

  // Scroll highlighted item into view during keyboard navigation
  useEffect(() => {
    if (isOpen && listRef.current && filteredDistricts.length > 0) {
      const highlightedEl = listRef.current.children[highlightedIndex];
      if (highlightedEl && typeof highlightedEl.scrollIntoView === 'function') {
        highlightedEl.scrollIntoView({ block: 'nearest' });
      }
    }
  }, [highlightedIndex, isOpen, filteredDistricts.length]);

  const handleSelect = (districtName) => {
    onSelectDistrict(districtName);
    setIsOpen(false);
    setSearchQuery('');
  };

  const handleKeyDown = (e) => {
    if (!isOpen) {
      if (e.key === 'Enter' || e.key === 'ArrowDown' || e.key === ' ') {
        e.preventDefault();
        setIsOpen(true);
      }
      return;
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setHighlightedIndex(prev => (prev + 1) % Math.max(1, filteredDistricts.length));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setHighlightedIndex(prev => (prev - 1 + filteredDistricts.length) % Math.max(1, filteredDistricts.length));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredDistricts.length > 0 && highlightedIndex < filteredDistricts.length) {
        handleSelect(filteredDistricts[highlightedIndex]);
      }
    } else if (e.key === 'Escape') {
      e.preventDefault();
      setIsOpen(false);
    }
  };

  return (
    <div className="relative w-full" ref={containerRef} onKeyDown={handleKeyDown}>
      {/* Selector Trigger Field */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full bg-[#0b0f19] border border-slate-700 hover:border-slate-500 rounded p-2.5 text-xs font-mono text-white font-bold flex items-center justify-between transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/50 shadow-inner"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
      >
        <div className="flex items-center gap-2 truncate">
          <MapPin className="w-4 h-4 text-blue-400 shrink-0" />
          {selectedDistrict ? (
            <span className="truncate text-slate-100 font-extrabold">{selectedDistrict}</span>
          ) : (
            <span className="text-slate-400 font-normal">🔍 Search district...</span>
          )}
        </div>
        <ChevronDown className={`w-4 h-4 text-slate-400 shrink-0 transition-transform duration-200 ${isOpen ? 'rotate-180 text-blue-400' : ''}`} />
      </button>

      {/* Searchable Dropdown Popover */}
      {isOpen && (
        <div className="absolute z-50 top-full left-0 right-0 mt-1.5 bg-[#0b0f19] border border-slate-700 rounded-md shadow-2xl overflow-hidden ring-1 ring-blue-500/30">
          
          {/* Search Input Field */}
          <div className="p-2 border-b border-slate-800 bg-[#121827] sticky top-0 z-10">
            <div className="relative flex items-center">
              <Search className="w-3.5 h-3.5 absolute left-2.5 text-slate-400" />
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setHighlightedIndex(0);
                }}
                placeholder="Search district (e.g. Chennai, Coimbatore)..."
                className="w-full bg-[#0b0f19] border border-slate-700 rounded pl-8 pr-7 py-1.5 text-xs text-white placeholder-slate-500 font-mono focus:outline-none focus:border-blue-500"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery('')}
                  className="absolute right-2 text-slate-400 hover:text-white"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>

          {/* Scrollable Districts List (Max Height ~300px - 320px) */}
          <div
            ref={listRef}
            className="max-h-[300px] overflow-y-auto divide-y divide-slate-800/40 custom-scrollbar"
            role="listbox"
          >
            {filteredDistricts.length > 0 ? (
              filteredDistricts.map((dName, idx) => {
                const isSelected = dName === selectedDistrict;
                const isHighlighted = idx === highlightedIndex;

                return (
                  <div
                    key={dName}
                    role="option"
                    aria-selected={isSelected}
                    onClick={() => handleSelect(dName)}
                    onMouseEnter={() => setHighlightedIndex(idx)}
                    className={`px-3 py-2 text-xs font-mono cursor-pointer flex items-center justify-between transition-colors ${
                      isSelected
                        ? 'bg-blue-900/40 text-blue-200 font-bold border-l-2 border-blue-400'
                        : isHighlighted
                        ? 'bg-slate-800/80 text-white'
                        : 'text-slate-300 hover:bg-slate-800/50'
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate">
                      {isSelected ? (
                        <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      ) : (
                        <div className="w-3.5 h-3.5 shrink-0" />
                      )}
                      <span className="truncate">{dName}</span>
                      {dName === 'Chennai' && (
                        <span className="text-[9px] px-1.5 py-0.5 bg-blue-950 text-blue-400 border border-blue-800 rounded font-bold shrink-0">
                          DEMO CORE
                        </span>
                      )}
                    </div>
                    {isSelected && (
                      <span className="text-[10px] text-emerald-400 font-semibold font-mono shrink-0 ml-2">
                        SELECTED
                      </span>
                    )}
                  </div>
                );
              })
            ) : (
              <div className="p-4 text-center text-xs text-slate-500 font-mono">
                No districts match "{searchQuery}"
              </div>
            )}
          </div>

          {/* Dropdown Footer Status */}
          <div className="px-3 py-1.5 bg-[#090d16] border-t border-slate-800/80 text-[10px] text-slate-400 font-mono flex items-center justify-between">
            <span>Showing {filteredDistricts.length} of {districtNames.length} districts</span>
            <span className="text-slate-500">Press ↑↓ to navigate</span>
          </div>

        </div>
      )}
    </div>
  );
}
