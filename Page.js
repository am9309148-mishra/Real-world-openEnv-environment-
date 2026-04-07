"use client";
import { useEffect, useState } from "react";

export default function Page() {
  const [logs,setLogs] = useState([]);

  useEffect(()=>{
    const ws = new WebSocket("ws://localhost:8000/train");

    ws.onmessage = e=>{
      const d = JSON.parse(e.data);
      setLogs(prev=>[...prev,d]);
    };
  },[]);

  return (
    <div style={{padding:20}}>
      <h1>🚀 OpenEnv AI</h1>

      {logs.slice(-10).map((l,i)=>(
        <div key={i}>
          Ep {l.episode} | Reward {l.reward} | {l.explanation}
        </div>
      ))}
    </div>
  );
    }
