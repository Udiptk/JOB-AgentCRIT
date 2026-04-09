"use client";

import { useJobStore } from "../../store/jobStore";

export function AgentStatusBoard() {
  const events = useJobStore((state) => state.events);
  const isRunning = useJobStore((state) => state.isRunning);

  return (
    <div className="bg-surface-container-low border border-outline-variant/10 flex flex-col h-[350px]">
      <div className="p-4 border-b border-outline-variant/10 flex justify-between items-center bg-surface-container-lowest">
        <h3 className="font-headline text-sm font-black uppercase tracking-tight">Agent Activity Node</h3>
        {isRunning && (
            <span className="text-primary flex items-center gap-2 text-[10px] uppercase font-bold animate-pulse">
                <span className="w-1.5 h-1.5 rounded-full bg-primary"></span> PIPELINE ACTIVE
            </span>
        )}
      </div>

      <div className="flex-1 overflow-auto p-4 space-y-3 font-mono text-[11px]">
        {events.length === 0 ? (
          <div className="text-on-surface-variant/40 text-center mt-20 uppercase font-headline">
            System Standby - Awaiting Directives...
          </div>
        ) : (
          events.map((evt, i) => (
            <div key={i} className="flex space-x-3 border-l-[1.5px] pl-3 border-primary/50 transition-all opacity-100 animate-in fade-in slide-in-from-left-4">
              <span className="text-primary-fixed-dim/60 shrink-0">[{evt.time}]</span>
              <div className="flex-1 text-on-surface/80">
                <span className="font-bold text-primary mr-1">{evt.agent ? `${evt.agent.toUpperCase()}_NODE:` : "SYSTEM:"}</span>
                {evt.message}
              </div>
            </div>
          ))
        )}
      </div>
      <div className="p-3 border-t border-outline-variant/10 bg-surface-container-lowest font-label">
          <div className="flex justify-between items-center text-[9px] uppercase tracking-widest text-on-surface-variant/50">
              <span>{events.length} EVENTS RECORDED</span>
              <span>SYNCHRONIZED</span>
          </div>
      </div>
    </div>
  );
}
