import { AgentStatusBoard } from "@/components/dashboard/AgentStatusBoard";

export default function Home() {
  return (
    <>
      <header className="fixed top-0 w-full z-50 flex justify-between items-center px-6 h-16 bg-[#0e0e0e]/80 backdrop-blur-xl border-b border-[rgba(66,71,84,0.2)] shadow-[0_40px_80px_rgba(229,226,225,0.04)]">
        <div className="flex items-center gap-8">
          <span className="text-lg font-black tracking-tighter text-on-surface">OBSIDIAN.INTEL</span>
          <nav className="hidden md:flex gap-6">
            <a className="font-headline uppercase tracking-[0.05em] text-[10px] text-primary font-bold border-b border-primary" href="#">SYSTEM_HEALTH</a>
            <a className="font-headline uppercase tracking-[0.05em] text-[10px] text-on-surface/60 hover:bg-surface-bright/10 hover:text-on-surface transition-all" href="#">LATENCY: 24MS</a>
            <a className="font-headline uppercase tracking-[0.05em] text-[10px] text-on-surface/60 hover:bg-surface-bright/10 hover:text-on-surface transition-all" href="#">UPTIME: 99.9%</a>
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <div className="material-symbols-outlined text-primary cursor-pointer hover:bg-surface-bright/10 p-2 rounded transition-all">notifications_active</div>
          <div className="material-symbols-outlined text-on-surface/60 cursor-pointer hover:bg-surface-bright/10 p-2 rounded transition-all">settings</div>
          <div className="w-8 h-8 rounded-full overflow-hidden border border-outline-variant/30">
            <img alt="Sovereign Operator Avatar" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC8Mc6htoQxAEWIRe_UbTyFLtxB0fO8mUqR8mP4P78faGYYWz1uniOqWfoeLIjcTD9QrU_dxOxw9Dy_45Wu_vn9Ls9hOMCAPOI53CFHP7ESxw1DY8mK09GGQesHn8krHs7vLqBhE-wVPAqCK5a-DQDMvqdQ5h3-y-ytuj7B0ZPrwANbisO64Rq-8oNzEoMlh1Wb24ds88r1aOKX1gBbzScpC99Sfqf1Pdns-9FipktJxg2k2IXmKqwk4OChBIRyipjRYUsr5eB8LGXX" />
          </div>
        </div>
      </header>

      <aside className="fixed left-0 top-16 h-[calc(100vh-64px)] w-64 bg-background border-r border-[#424754]/20 flex flex-col py-8 z-40 hidden md:flex">
        <div className="px-6 mb-10">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-tertiary animate-pulse"></div>
            <div>
              <div className="font-headline uppercase tracking-[0.05em] text-[11px] text-on-surface font-bold">NODE_01</div>
              <div className="font-headline uppercase tracking-[0.05em] text-[9px] text-tertiary">AUTONOMOUS_MODE</div>
            </div>
          </div>
        </div>
        <nav className="flex-1 space-y-1">
          <a className="flex items-center gap-4 px-6 py-3 bg-surface-container text-primary border-r-2 border-primary transition-colors duration-300" href="#">
            <span className="material-symbols-outlined text-[20px]">memory</span>
            <span className="font-headline uppercase tracking-[0.05em] text-[11px]">ORCHESTRATOR</span>
          </a>
          <a className="flex items-center gap-4 px-6 py-3 text-on-surface/40 hover:bg-surface-container hover:text-on-surface transition-colors duration-300" href="#">
            <span className="material-symbols-outlined text-[20px]">description</span>
            <span className="font-headline uppercase tracking-[0.05em] text-[11px]">RESUME_LAB</span>
          </a>
          <a className="flex items-center gap-4 px-6 py-3 text-on-surface/40 hover:bg-surface-container hover:text-on-surface transition-colors duration-300" href="#">
            <span className="material-symbols-outlined text-[20px]">analytics</span>
            <span className="font-headline uppercase tracking-[0.05em] text-[11px]">MARKET_SCAN</span>
          </a>
        </nav>
        <div className="px-6 mt-auto space-y-6">
          <button className="w-full py-3 bg-gradient-to-b from-primary to-primary-container text-on-primary font-headline uppercase tracking-[0.1em] text-[10px] font-bold rounded-sm active:scale-95 transition-all shadow-[0_0_15px_rgba(173,198,255,0.3)]">
            INITIALIZE_SCAN
          </button>
          <div className="space-y-2">
            <a className="flex items-center gap-4 text-on-surface/40 hover:text-on-surface transition-colors" href="#">
              <span className="material-symbols-outlined text-[18px]">terminal</span>
              <span className="font-headline uppercase tracking-[0.05em] text-[10px]">LOGS</span>
            </a>
            <a className="flex items-center gap-4 text-on-surface/40 hover:text-on-surface transition-colors" href="#">
              <span className="material-symbols-outlined text-[18px]">tune</span>
              <span className="font-headline uppercase tracking-[0.05em] text-[10px]">SETTINGS</span>
            </a>
          </div>
        </div>
      </aside>

      <main className="md:ml-64 pt-24 pb-12 px-8 min-h-screen">
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="glass-panel p-5 flex flex-col justify-between min-h-[120px]">
            <div className="flex justify-between items-start">
              <span className="font-label uppercase text-[10px] tracking-wider text-on-surface-variant">JOBS_SCANNED</span>
              <span className="material-symbols-outlined text-primary text-lg">radar</span>
            </div>
            <div className="mt-4">
              <div className="font-label text-3xl font-bold text-on-surface tracking-tighter">12,842</div>
              <div className="text-[10px] text-tertiary font-label flex items-center gap-1 mt-1">
                <span className="material-symbols-outlined text-[12px]">trending_up</span> +14.2% SINCE_LAST_BOOT
              </div>
            </div>
          </div>
          <div className="glass-panel p-5 flex flex-col justify-between min-h-[120px]">
            <div className="flex justify-between items-start">
              <span className="font-label uppercase text-[10px] tracking-wider text-on-surface-variant">RESUME_VERSIONS</span>
              <span className="material-symbols-outlined text-primary text-lg">layers</span>
            </div>
            <div className="mt-4">
              <div className="font-label text-3xl font-bold text-on-surface tracking-tighter">48</div>
              <div className="text-[10px] text-on-surface-variant font-label mt-1">LATEST: SR_ENGINEER_V4</div>
            </div>
          </div>
          <div className="glass-panel p-5 flex flex-col justify-between min-h-[120px]">
            <div className="flex justify-between items-start">
              <span className="font-label uppercase text-[10px] tracking-wider text-on-surface-variant">ATS_OPTIMIZATION</span>
              <span className="material-symbols-outlined text-tertiary text-lg">verified</span>
            </div>
            <div className="mt-4">
              <div className="font-label text-3xl font-bold text-on-surface tracking-tighter">98.4%</div>
              <div className="text-[10px] text-on-surface-variant font-label mt-1">AGGREGATE_CONFIDENCE</div>
            </div>
          </div>
          <div className="glass-panel p-5 flex flex-col justify-between min-h-[120px]">
            <div className="flex justify-between items-start">
              <span className="font-label uppercase text-[10px] tracking-wider text-on-surface-variant">MARKET_SIGNAL</span>
              <span className="material-symbols-outlined text-error text-lg">sensors</span>
            </div>
            <div className="mt-4">
              <div className="font-label text-3xl font-bold text-on-surface tracking-tighter">HIGH</div>
              <div className="text-[10px] text-primary font-label mt-1">32 NEW ALIGNMENTS FOUND</div>
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2 bg-surface-container-low p-6 border border-outline-variant/10">
            <div className="flex justify-between items-center mb-6">
              <h2 className="font-headline text-lg font-extrabold tracking-tight uppercase">RESUME CORE MATERIAL</h2>
              <div className="flex gap-2">
                <button className="px-3 py-1 bg-surface-container text-on-surface text-[10px] font-label uppercase hover:bg-surface-container-highest transition-colors">EDIT_SOURCE</button>
                <button className="px-3 py-1 bg-primary/10 text-primary text-[10px] font-label uppercase hover:bg-primary/20 transition-colors">FORK_VERSION</button>
              </div>
            </div>
            <div className="space-y-4 font-label text-[13px] text-on-surface/80">
              <div className="p-4 bg-surface-container-lowest border-l-2 border-primary">
                <div className="text-[10px] text-primary-fixed-dim uppercase mb-1">PRO_SUMMARY</div>
                Highly technical AI orchestrator with expertise in obsidian-grade system architectures. Capable of deploying autonomous agents at scale...
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-surface-container-lowest">
                  <div className="text-[10px] text-primary-fixed-dim uppercase mb-1">SKILL_VECTOR_01</div>
                  NEURAL_NET_DESIGN
                </div>
                <div className="p-4 bg-surface-container-lowest">
                  <div className="text-[10px] text-primary-fixed-dim uppercase mb-1">SKILL_VECTOR_02</div>
                  LOW_LATENCY_UI
                </div>
              </div>
            </div>
          </div>

          <div className="bg-surface-container p-6 border border-outline-variant/10 flex flex-col items-center justify-center text-center">
            <h2 className="font-headline text-xs font-bold tracking-[0.2em] uppercase text-on-surface-variant mb-8">ATS OPTIMIZATION ENGINE</h2>
            <div className="relative w-48 h-48 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90 text-surface-container-highest">
                <circle cx="96" cy="96" fill="transparent" r="88" strokeWidth="4" stroke="currentColor"></circle>
                <circle cx="96" cy="96" fill="transparent" r="88" strokeWidth="8" strokeDasharray="552.92" strokeDashoffset="44.23" className="text-tertiary" style={{ filter: "drop-shadow(0 0 8px rgba(78, 222, 163, 0.4))" }} stroke="currentColor"></circle>
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-5xl font-black font-headline tracking-tighter text-on-surface">92</span>
                <span className="text-[10px] font-label text-tertiary uppercase tracking-widest">MATCH_INDEX</span>
              </div>
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex justify-between items-center mb-2">
              <h2 className="font-headline text-sm font-black uppercase tracking-tight">MARKET OPPORTUNITIES</h2>
              <span className="text-[10px] font-label text-primary uppercase">LIVE_STREAM_ACTIVE</span>
            </div>
            
            <AgentStatusBoard />
            
          </div>

          <div className="bg-surface-container-low border border-outline-variant/10 flex flex-col">
            <div className="p-4 border-b border-outline-variant/10 flex justify-between items-center bg-surface-container-lowest">
              <h2 className="font-headline text-sm font-black uppercase tracking-tight">DEPLOYMENT STATUS</h2>
              <span className="material-symbols-outlined text-on-surface-variant text-sm">filter_list</span>
            </div>
            <div className="flex-1 overflow-auto">
              <table className="w-full text-left font-label text-[11px]">
                <thead>
                  <tr className="text-on-surface-variant uppercase tracking-wider border-b border-outline-variant/5">
                    <th className="px-4 py-3 font-medium">TARGET_ID</th>
                    <th className="px-4 py-3 font-medium">STATUS</th>
                    <th className="px-4 py-3 font-medium">SENT_VIA</th>
                    <th className="px-4 py-3 font-medium text-right">TIMESTAMP</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-outline-variant/5">
                  <tr className="hover:bg-surface-container transition-colors">
                    <td className="px-4 py-3 text-on-surface">APPLE_GLOBAL_021</td>
                    <td className="px-4 py-3">
                      <span className="text-tertiary flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-tertiary"></span> INTERVIEW_SCHEDULED
                      </span>
                    </td>
                    <td className="px-4 py-3 text-on-surface-variant">AUTO_AGENT_B</td>
                    <td className="px-4 py-3 text-right text-on-surface-variant">2H_AGO</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <footer className="mt-8 bg-surface-container-lowest border border-outline-variant/40 p-4 font-label">
          <div className="flex justify-between items-center mb-3">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-sm text-tertiary">terminal</span>
              <span className="text-[10px] uppercase font-bold tracking-widest text-on-surface-variant">SYSTEM_ORCHESTRATOR_LOGS</span>
            </div>
            <div className="flex gap-4 text-[9px] text-on-surface-variant/40">
              <span>CPU: 12%</span>
              <span>MEM: 4.2GB</span>
              <span>NET: STABLE</span>
            </div>
          </div>
          <div className="h-32 overflow-y-auto space-y-1 text-[11px] text-on-surface/60 font-mono">
            <div className="flex gap-4">
              <span className="text-tertiary-fixed-dim">[14:02:24]</span>
              <span>INFO: CRON_JOB_342 COMPLETED. 42 NEW JOBS SCANNED.</span>
            </div>
          </div>
        </footer>
      </main>
    </>
  );
}
