"use client";

import { useEffect, useRef } from "react";
import { useJobStore } from "../store/jobStore";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";

export function useWebSocket(userId: number) {
  const ws = useRef<WebSocket | null>(null);
  const addEvent = useJobStore((state) => state.addEvent);

  useEffect(() => {
    if (!ws.current) {
      ws.current = new WebSocket(`${WS_URL}/${userId}`);

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          addEvent(data);
        } catch (err) {
          console.error("Failed to parse WS msg", event.data);
        }
      };

      ws.current.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    }

    return () => {
      ws.current?.close();
      ws.current = null;
    };
  }, [userId, addEvent]);

  return ws.current;
}
