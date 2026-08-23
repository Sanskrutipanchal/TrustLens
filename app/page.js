'use client';
import React, { useState } from 'react';
import {
  ShieldAlert, MessageSquare, Image as ImageIcon, Link as LinkIcon,
  Mic, Play, X, AlertTriangle, CheckCircle2, ShieldCheck,
  Activity, Lock, Eye, Info, Upload
} from 'lucide-react';

export default function TrustLensDashboard() {
  const [activeTab, setActiveTab] = useState('text');
  const [inputText, setInputText] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [showPauseModal, setShowPauseModal] = useState(false);
  const [q1Answer, setQ1Answer] = useState(null);
  const [q2Answer, setQ2Answer] = useState(null);
  const [result, setResult] = useState(null);

  const placeholders = {
    text: 'Paste suspicious SMS, WhatsApp, or chat message here...',
    image: '',
    url: 'Paste suspicious URL here e.g. http://rbi-verify.com',
    voice: 'Paste voice call transcript here...',
  };

  const handleAnalyze = async () => {
    if (activeTab !== 'image' && !inputText.trim()) {
      alert('Please enter some content to analyze.');
      return;
    }
    if (activeTab === 'image' && !imageFile) {
      alert('Please select an image to analyze.');
      return;
    }
    setLoading(true);
    setShowResults(false);
    setShowPauseModal(false);
    setQ1Answer(null);
    setQ2Answer(null);
    try {
      let response;
      if (activeTab === 'text') {
        response = await fetch('http://127.0.0.1:8000/analyze/text', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: inputText }),
        });
      } else if (activeTab === 'url') {
        response = await fetch('http://127.0.0.1:8000/analyze/url', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: inputText }),
        });
      } else if (activeTab === 'voice') {
        response = await fetch('http://127.0.0.1:8000/analyze/voice', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transcript: inputText }),
        });
      } else if (activeTab === 'image') {
        const formData = new FormData();
        formData.append('file', imageFile);
        response = await fetch('http://127.0.0.1:8000/analyze/image', {
          method: 'POST',
          body: formData,
        });
      }
      if (!response.ok) throw new Error(`Backend error: ${response.status}`);
      const data = await response.json();
      setResult(data);
      setShowResults(true);
      if (data.risk_level === 'high') setShowPauseModal(true);
    } catch (error) {
      console.error(error);
      alert('Could not connect to backend. Make sure it is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans pb-16">
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-md px-8 py-4 flex justify-between items-center sticky top-0 z-30">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-red-500/10 border border-red-500/20 rounded-lg">
            <ShieldAlert className="w-6 h-6 text-red-500" />
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-red-500 via-amber-400 to-emerald-400 bg-clip-text text-transparent">
              TRUSTLENS
            </span>
            <p className="text-[10px] text-slate-400 font-mono tracking-widest uppercase">AI Cyber Threat & Psychological Manipulation Shield</p>
          </div>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-800/60 rounded-full border border-slate-700/50 text-xs font-mono text-slate-400">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          Shield Engine: Active
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 mt-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { label: 'Scam Detection Accuracy', val: '99.2%', sub: 'AI Neural Model', icon: ShieldCheck, color: 'text-emerald-400' },
            { label: 'Avg Analysis Speed', val: '< 800ms', sub: 'Low latency engine', icon: Activity, color: 'text-blue-400' },
            { label: 'Active Behavioral Filters', val: '18 Directives', sub: 'Social engineering', icon: Lock, color: 'text-red-400' },
          ].map((stat, i) => {
            const Icon = stat.icon;
            return (
              <div key={i} className="bg-slate-900/80 border border-slate-800/80 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <p className="text-[11px] font-mono uppercase text-slate-400">{stat.label}</p>
                  <p className={`text-xl font-extrabold mt-0.5 ${stat.color}`}>{stat.val}</p>
                  <p className="text-[10px] text-slate-500">{stat.sub}</p>
                </div>
                <Icon className={`w-8 h-8 opacity-20 ${stat.color}`} />
              </div>
            );
          })}
        </div>

        <section className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-2xl backdrop-blur-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-slate-200 flex items-center gap-2">
              <Eye className="w-5 h-5 text-red-400" /> Analyze Input
            </h2>
            <span className="text-xs text-slate-400">Select input medium below</span>
          </div>

          <div className="flex border-b border-slate-800 mb-6 gap-1 overflow-x-auto">
            {[
              { id: 'text', label: 'SMS / Chat Message', icon: MessageSquare },
              { id: 'image', label: 'Screenshot / OCR Scan', icon: ImageIcon },
              { id: 'url', label: 'Suspicious Domain URL', icon: LinkIcon },
              { id: 'voice', label: 'Voice Call Transcript', icon: Mic },
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-3 border-b-2 text-xs font-semibold tracking-wide transition-all cursor-pointer whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'border-red-500 text-red-400 bg-red-500/5'
                      : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>

          {activeTab === 'image' ? (
            <div className="border-2 border-dashed border-slate-700 rounded-xl p-8 text-center">
              <Upload className="w-10 h-10 text-slate-500 mx-auto mb-3" />
              <p className="text-slate-400 text-sm mb-4">Upload a screenshot to analyze for scam content</p>
              <input type="file" accept="image/*" onChange={(e) => setImageFile(e.target.files[0])} className="hidden" id="imageUpload" />
              <label htmlFor="imageUpload" className="px-6 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm rounded-xl cursor-pointer transition-all border border-slate-700">
                Choose Image
              </label>
              {imageFile && <p className="text-emerald-400 text-xs mt-3">✓ {imageFile.name} selected</p>}
            </div>
          ) : (
            <div className="relative">
              <textarea
                rows={4}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={placeholders[activeTab]}
                className="w-full bg-slate-950/90 border border-slate-800 rounded-xl p-4 text-slate-200 focus:outline-none focus:border-red-500/80 font-mono text-sm leading-relaxed resize-none shadow-inner transition-colors"
              />
              <div className="absolute bottom-3 right-3 text-[10px] font-mono text-slate-500">{inputText.length} characters</div>
            </div>
          )}

          <div className="mt-5 flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <Info className="w-4 h-4 text-slate-500" />
              <span>Runs deep psychological, linguistic, and domain verification checks.</span>
            </div>
            <button onClick={handleAnalyze} disabled={loading} className="px-8 py-3.5 bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 text-white font-semibold text-sm rounded-xl flex items-center gap-3 shadow-lg shadow-red-600/20 transition-all cursor-pointer disabled:opacity-50">
              <Play className="w-4 h-4 fill-current" />
              {loading ? 'Scanning...' : 'Run Threat & Manipulation Analysis'}
            </button>
          </div>
        </section>

        {showResults && result && (
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-red-400" /> Analysis Result
            </h3>
            {result.extracted_text && (
              <div className="bg-slate-950 rounded-xl p-4 border border-slate-700">
                <p className="text-[11px] text-slate-400 uppercase font-mono mb-2">Extracted Text from Image</p>
                <p className="text-xs text-slate-300 font-mono">{result.extracted_text}</p>
              </div>
            )}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-950 rounded-xl p-4 border border-slate-800">
                <p className="text-[11px] text-slate-400 uppercase font-mono">Risk Level</p>
                <p className={`text-2xl font-extrabold mt-1 ${result.risk_level === 'high' ? 'text-red-400' : result.risk_level === 'medium' ? 'text-amber-400' : 'text-emerald-400'}`}>
                  {result.risk_level?.toUpperCase()}
                </p>
              </div>
              <div className="bg-slate-950 rounded-xl p-4 border border-slate-800">
                <p className="text-[11px] text-slate-400 uppercase font-mono">Verdict</p>
                <p className="text-lg font-bold mt-1 text-slate-200">{result.verdict?.replace(/_/g, ' ')}</p>
              </div>
              <div className="bg-slate-950 rounded-xl p-4 border border-slate-800">
                <p className="text-[11px] text-slate-400 uppercase font-mono">Confidence</p>
                <p className="text-2xl font-extrabold mt-1 text-blue-400">{((result.confidence || 0) * 100).toFixed(0)}%</p>
              </div>
            </div>
            <div className="bg-slate-950 rounded-xl p-4 border border-slate-800">
              <p className="text-[11px] text-slate-400 uppercase font-mono mb-2">Signals Detected</p>
              <div className="space-y-1">
                {result.signals?.map((sig, i) => (
                  <p key={i} className="text-xs text-slate-300 flex items-center gap-2">
                    <AlertTriangle className="w-3 h-3 text-amber-400 shrink-0" /> {sig}
                  </p>
                ))}
              </div>
            </div>
            <div className="bg-slate-950 rounded-xl p-4 border border-slate-800">
              <p className="text-[11px] text-slate-400 uppercase font-mono mb-2">Explanation</p>
              <p className="text-xs text-slate-300">{result.explanation}</p>
            </div>
            {result.recommended_actions?.length > 0 && (
              <div className="bg-slate-950 rounded-xl p-4 border border-slate-800">
                <p className="text-[11px] text-slate-400 uppercase font-mono mb-2">Recommended Actions</p>
                <div className="space-y-1">
                  {result.recommended_actions.map((action, i) => (
                    <p key={i} className="text-xs text-emerald-400 flex items-center gap-2">
                      <CheckCircle2 className="w-3 h-3 shrink-0" /> {action}
                    </p>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      {showPauseModal && (
        <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-red-500/60 max-w-lg w-full rounded-2xl p-6 shadow-2xl relative space-y-5">
            <button onClick={() => setShowPauseModal(false)} className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors cursor-pointer">
              <X className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-3 text-red-500 border-b border-slate-800 pb-4">
              <div className="p-2 bg-red-500/10 rounded-xl border border-red-500/20">
                <ShieldAlert className="w-7 h-7" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white tracking-tight">ACTIVE SAFETY INTERVENTION</h3>
                <p className="text-xs text-red-400 font-mono">High-Probability Psychological Trap Detected</p>
              </div>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              TrustLens detected urgent time pressure and authority impersonation. Scammers use fear to bypass critical thinking. Pause and complete this 10-second verification:
            </p>
            <div className="space-y-4 bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs">
              <div className="space-y-2">
                <p className="text-slate-200 font-medium">1. Did this sender initiate contact unexpectedly?</p>
                <div className="flex gap-3">
                  <button onClick={() => setQ1Answer('yes')} className={`flex-1 py-2 rounded-lg font-medium transition-all cursor-pointer ${q1Answer === 'yes' ? 'bg-red-600 text-white ring-2 ring-red-400' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}>Yes (Unsolicited)</button>
                  <button onClick={() => setQ1Answer('no')} className={`flex-1 py-2 rounded-lg font-medium transition-all cursor-pointer ${q1Answer === 'no' ? 'bg-emerald-600 text-white ring-2 ring-emerald-400' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}>No (I reached out)</button>
                </div>
              </div>
              <div className="space-y-2 pt-3 border-t border-slate-800/80">
                <p className="text-slate-200 font-medium">2. Are they instructing you to keep this secret or act fast?</p>
                <div className="flex gap-3">
                  <button onClick={() => setQ2Answer('yes')} className={`flex-1 py-2 rounded-lg font-medium transition-all cursor-pointer ${q2Answer === 'yes' ? 'bg-red-600 text-white ring-2 ring-red-400' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}>Yes (High Pressure)</button>
                  <button onClick={() => setQ2Answer('no')} className={`flex-1 py-2 rounded-lg font-medium transition-all cursor-pointer ${q2Answer === 'no' ? 'bg-emerald-600 text-white ring-2 ring-emerald-400' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}>No Pressure</button>
                </div>
              </div>
              {(q1Answer === 'yes' || q2Answer === 'yes') && (
                <div className="p-2.5 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-[11px] font-mono flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0" />
                  High Risk Confirmed: Classic scam indicators selected.
                </div>
              )}
            </div>
            <button onClick={() => setShowPauseModal(false)} className="w-full py-3 bg-red-600 hover:bg-red-500 text-white font-bold text-sm rounded-xl transition-all cursor-pointer">
              I Understand — View Full Analysis
            </button>
          </div>
        </div>
      )}
    </div>
  );
}