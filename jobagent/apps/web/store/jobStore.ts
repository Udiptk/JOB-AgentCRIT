"use client";

import { useEffect, useState } from "react";
import { create } from "zustand";

interface AgentEvent {
  type: string;
  node: string;
  title: string;
  message: string;
  agent?: string;
  time?: string;
}

interface JobStore {
  events: AgentEvent[];
  addEvent: (event: AgentEvent) => void;
  clearEvents: () => void;
  isRunning: boolean;
  setRunning: (status: boolean) => void;
}

export const useJobStore = create<JobStore>((set) => ({
  events: [],
  addEvent: (event) => set((state) => ({ events: [{ ...event, time: new Date().toLocaleTimeString() }, ...state.events] })),
  clearEvents: () => set({ events: [] }),
  isRunning: false,
  setRunning: (status) => set({ isRunning: status }),
}));
