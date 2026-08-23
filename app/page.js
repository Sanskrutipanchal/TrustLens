'use client';
import React, { useState } from 'react';
import { 
  ShieldAlert, MessageSquare, Image as ImageIcon, Link as LinkIcon, 
  Mic, Play, X, AlertTriangle, CheckCircle2, ShieldCheck, 
  Activity, ArrowUpRight, Lock, Eye, Zap, Info
} from 'lucide-react';

export default function TrustLensDashboard() {
  const [activeTab, setActiveTab] = useState('text');
  const [inputText, setInputText] = useState(
    "URGENT: Your bank account will be blocked within 30 minutes due to unverified KYC. To secure your account, transfer funds to the RBI safe account immediately. Do not disclose this to anyone. Click http://rbi-verify.com to verify."
  );
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [showPauseModal, setShowPauseModal] = useState(false);

  // State for Interactive Safety Pause Modal Questions
  const [q1Answer, setQ1Answer] = useState(null); // 'yes' or 'no'
  const [q2Answer, setQ2Answer] = useState(null); // 'yes' or 'no'

  const mockResult = {
    riskScore: 94,
    riskLevel: 'CRITICAL',
    threatCategory: 'Financial Impersonation & Social Engineering',
    journey: [
      { stage: '1. Impersonation', status: 'detected', desc: 'Claims official authority (Bank / RBI)' },
      { stage: '2. Urgency & Fear', status: 'detected', desc: 'Imposes 30-minute artificial deadline' },
      { stage: '3. Isolation', status: 'active', desc: 'Explicitly instructs victim not to inform anyone' },
      { stage: '4. Credential Harvest', status: 'pending', desc: 'Phishing URL designed to capture credentials' },
      { stage: '5. Asset Extraction', status: 'next', desc: 'Direct financial transfer to fraudulent safe account' },
    ],
    signals: [
      { name: 'Authority Spoofing', detail: 'Claims RBI official status', severity: 'High', weight: '25%' },
      { name: 'Artificial Panic', detail: 'Threatens 30-min account suspension', severity: 'Critical', weight: '30%' },
      { name: 'Isolation Directive', detail: '"Do not tell anyone" instruction', severity: 'High', weight: '20%' },
      { name: 'Malicious Domain', detail: 'Unencrypted non-official URL', severity: 'Critical', weight: '25%' }
    ],
    nextSteps: [
      'Attacker will request OTP or NetBanking Password',
      'Prompt to download remote access software (AnyDesk / TeamViewer)',
      'Pressure to transfer money immediately via UPI / RTGS'
    ],
    recommendations: [
      'Do NOT click the provided web link or call given numbers.',
      'Contact official customer support using the number behind your debit/credit card.',
      'Report the phishing number and URL to national cybercrime portals.'
    ]
  };

  const handleAnalyze = async () => {
    setLoading(true);
    // Reset modal answers when new analysis runs
    setQ1Answer(null);
    setQ2Answer(null);

    setTimeout(() => {
      setLoading(false);
      setShowResults(true);
      setShowPauseModal(true);
    }, 900);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans pb-16 selection:bg-red-500/30 selection:text-red-200">
      
      {/* Top Header */}
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-md px-8 py-4 flex justify-between items-center sticky top-0 z-30">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-red-500/10 border border-red-500/20 rounded-lg">
            <ShieldAlert className="w-6 h-6 text-red-500" />
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-red-500 via-amber-400 to-emerald-400 bg-clip-text text-transparent">
              TRUSTLENS
            </span>
            <span className="block text-[10px] text-slate-400 font-mono tracking-widest uppercase">
              AI Cyber Threat & Psychological Manipulation Shield
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs font-mono text-slate-400">
          <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-800/60 rounded-full border border-slate-700/50">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Shield Engine: Active</span>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-6 mt-8 space-y-8">

        {/* Live Metrics Header Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Scam Detection Accuracy', val: '99.2%', sub: 'AI Neural Model', icon: ShieldCheck, color: 'text-emerald-400' },
            { label: 'Threats Blocked Today', val: '1,420+', sub: 'Real-time telemetry', icon: Zap, color: 'text-amber-400' },
            { label: 'Avg Analysis Speed', val: '< 800ms', sub: 'Low latency engine', icon: Activity, color: 'text-blue-400' },
            { label: 'Active Behavioral Filters', val: '18 Directives', sub: 'Social engineering', icon: Lock, color: 'text-red-400' }
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

        {/* Input Interface */}
        <section className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-2xl backdrop-blur-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-slate-200 flex items-center gap-2">
              <Eye className="w-5 h-5 text-red-400" />
              Content & Communication Threat Inspector
            </h2>
            <span className="text-xs text-slate-400">Select input medium below</span>
          </div>
          
          {/* Input Tabs */}
          <div className="flex border-b border-slate-800 mb-6 gap-2">
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
                  className={`flex items-center gap-2 px-5 py-3 border-b-2 text-xs font-semibold tracking-wide transition-all cursor-pointer ${
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

          <div className="relative">
            <textarea
              rows={4}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste suspicious text message, email content, or communication here..."
              className="w-full bg-slate-950/90 border border-slate-800 rounded-xl p-4 text-slate-200 focus:outline-none focus:border-red-500/80 font-mono text-sm leading-relaxed resize-none shadow-inner transition-colors"
            />
            <div className="absolute bottom-3 right-3 text-[10px] font-mono text-slate-500">
              {inputText.length} characters
            </div>
          </div>

          <div className="mt-5 flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <Info className="w-4 h-4 text-slate-500" />
              <span>Runs deep psychological, linguistic, and domain verification checks.</span>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="px-8 py-3.5 bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 text-white font-semibold text-sm rounded-xl flex items-center gap-3 shadow-lg shadow-red-600/20 transition-all cursor-pointer disabled:opacity-50"
            >
              <Play className="w-4 h-4 fill-current" />
              {loading ? "Scanning Psychological Journey..." : "Run Threat & Manipulation Analysis"}
            </button>
          </div>
        </section>

        {/* Results Panel */}
        {showResults && (
          <div className="space-y-6 animate-in fade-in duration-500">
            
            {/* Top Analysis Header */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              {/* Risk Gauge */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col items-center justify-center text-center shadow-lg relative overflow-hidden">
                <div className="absolute top-0 left-0 right-0 h-1 bg-red-500" />
                <span className="text-[11px] font-mono uppercase text-slate-400 tracking-wider">Threat Severity Score</span>
                
                <div className="relative my-4 flex items-center justify-center">
                  <div className="w-32 h-32 rounded-full border-8 border-red-500/20 border-t-red-500 flex items-center justify-center shadow-inner">
                    <div className="text-center">
                      <span className="text-4xl font-black text-red-500 tracking-tighter">{mockResult.riskScore}</span>
                      <span className="text-xs text-slate-400 block font-mono">/ 100</span>
                    </div>
                  </div>
                </div>

                <span className="px-3 py-1 bg-red-500/10 text-red-400 border border-red-500/20 rounded-full text-xs font-bold uppercase tracking-widest">
                  {mockResult.riskLevel} THREAT
                </span>
                <p className="text-[11px] text-slate-400 mt-2">{mockResult.threatCategory}</p>
              </div>

              {/* Manipulation Journey Timeline */}
              <div className="md:col-span-2 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-lg">
                <h3 className="text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider mb-5 flex items-center justify-between">
                  <span>Psychological Manipulation Journey</span>
                  <span className="text-slate-500 text-[11px]">5-Stage Attack Vector Mapping</span>
                </h3>

                <div className="space-y-3.5">
                  {mockResult.journey.map((step, idx) => (
                    <div key={idx} className="flex items-start gap-4 p-2.5 bg-slate-950/50 rounded-xl border border-slate-800/60">
                      <div className={`mt-1 w-3 h-3 rounded-full shrink-0 ${
                        step.status === 'detected' ? 'bg-red-500 shadow-md shadow-red-500/50' :
                        step.status === 'active' ? 'bg-amber-500 animate-pulse' : 'bg-slate-700'
                      }`} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <span className={`text-xs font-bold ${
                            step.status === 'detected' ? 'text-red-400' :
                            step.status === 'active' ? 'text-amber-400' : 'text-slate-500'
                          }`}>
                            {step.stage}
                          </span>
                          <span className="text-[10px] font-mono text-slate-500 uppercase">{step.status}</span>
                        </div>
                        <p className="text-[11px] text-slate-400 mt-0.5">{step.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Bottom Grid: Signals, Predictions, Recommendations */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Detected Signals */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-lg">
                <h3 className="text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-500" />
                  Identified Tactical Indicators
                </h3>

                <div className="space-y-3">
                  {mockResult.signals.map((sig, idx) => (
                    <div key={idx} className="bg-slate-950 p-3.5 rounded-xl border border-slate-800/80 flex justify-between items-start">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-semibold text-slate-200">{sig.name}</span>
                          <span className="text-[10px] font-mono text-red-400 bg-red-500/10 px-2 py-0.5 rounded border border-red-500/20">
                            {sig.severity}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 mt-1">{sig.detail}</p>
                      </div>
                      <span className="text-xs font-mono text-slate-500">{sig.weight}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Predictions & Guidance */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-5 shadow-lg">
                <div>
                  <h3 className="text-xs font-mono font-semibold text-amber-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                    <ArrowUpRight className="w-4 h-4" />
                    Predicted Next Attacker Steps
                  </h3>
                  <ul className="text-xs text-slate-300 space-y-2">
                    {mockResult.nextSteps.map((step, i) => (
                      <li key={i} className="flex items-start gap-2 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/50">
                        <span className="text-amber-500 font-bold">•</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="pt-3 border-t border-slate-800">
                  <h3 className="text-xs font-mono font-semibold text-emerald-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4" />
                    Recommended Shielding Actions
                  </h3>
                  <ul className="text-xs text-slate-300 space-y-2">
                    {mockResult.recommendations.map((rec, i) => (
                      <li key={i} className="flex items-start gap-2 bg-emerald-950/20 p-2.5 rounded-lg border border-emerald-500/10">
                        <span className="text-emerald-400 font-bold">✓</span>
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

            </div>
          </div>
        )}
      </main>

      {/* Safety Pause Interactive Intervention Modal */}
      {showPauseModal && (
        <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 z-50 animate-in fade-in duration-300">
          <div className="bg-slate-900 border border-red-500/60 max-w-lg w-full rounded-2xl p-6 shadow-2xl relative space-y-5">
            
            <button 
              onClick={() => setShowPauseModal(false)} 
              className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors cursor-pointer"
            >
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

            {/* Interactive Questions Section */}
            <div className="space-y-4 bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs">
              
              {/* Question 1 */}
              <div className="space-y-2">
                <p className="text-slate-200 font-medium">1. Did this sender initiate contact unexpectedly?</p>
                <div className="flex gap-3">
                  <button 
                    onClick={() => setQ1Answer('yes')}
                    className={`flex-1 py-2 rounded-lg font-medium transition-all cursor-pointer ${
                      q1Answer === 'yes' 
                        ? 'bg-red-600 text-white ring-2 ring-red-400' 
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    Yes (Unsolicited)
                  </button>
                  <button 
                    onClick={() => setQ1Answer('no')}
                    className={`flex-1 py-2 rounded-lg font-medium transition-all cursor-pointer ${
                      q1Answer === 'no' 
                        ? 'bg-emerald-600 text-white ring-2 ring-emerald-400' 
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    No (I reached out)
                  </button>
                </div>
              </div>

              {/* Question 2 */}
              <div className="space-y-2 pt-3 border-t border-slate-800/80">
                <p className="text-slate-200 font-medium">2. Are they instructing you to keep this secret or act fast?</p>
                <div className="flex gap-3">
                  <button 
                    onClick={() => setQ2Answer('yes')}
                    className={`flex-1 py-2 rounded-lg font-medium transition-all cursor-pointer ${
                      q2Answer === 'yes' 
                        ? 'bg-red-600 text-white ring-2 ring-red-400' 
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    Yes (High Pressure)
                  </button>
                  <button 
                    onClick={() => setQ2Answer('no')}
                    className={`flex-1 py-2 rounded-lg font-medium transition-all cursor-pointer ${
                      q2Answer === 'no' 
                        ? 'bg-emerald-600 text-white ring-2 ring-emerald-400' 
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    No Pressure
                  </button>
                </div>
              </div>

              {/* Dynamic Risk Indicator based on selections */}
              {(q1Answer === 'yes' || q2Answer === 'yes') && (
                <div className="p-2.5 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-[11px] font-mono flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0" />
                  <span>High Risk Confirmed: Classic scam indicators selected.</span>
                </div>
              )}
            </div>

            <button 
              onClick={() => setShowPauseModal(false)}
              className="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-xl text-xs font-bold tracking-wide shadow-lg shadow-emerald-600/20 transition-all cursor-pointer"
            >
              Acknowledge Warning & Review Assessment
            </button>
          </div>
        </div>
      )}
    </div>
  );
}