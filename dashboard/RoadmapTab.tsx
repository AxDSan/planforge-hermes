import React, { useState, useEffect } from 'react';
import { Map, CheckCircle, Circle, Lock, Unlock, AlertTriangle } from 'lucide-react';

interface Phase {
  number: number;
  name: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'blocked';
  progress: number;
}

interface PlanForgeState {
  project: string;
  currentPhase: number | null;
  phases: Phase[];
  locked: boolean;
}

export default function RoadmapTab() {
  const [state, setState] = useState<PlanForgeState>({
    project: 'Loading...',
    currentPhase: null,
    phases: [],
    locked: false
  });

  useEffect(() => {
    // Fetch state from PlanForge API
    fetch('/api/plugins/planforge/status')
      .then(r => r.json())
      .then(data => setState(data))
      .catch(() => setState({
        project: 'No active project',
        currentPhase: null,
        phases: [
          { number: 1, name: 'Research & Context', status: 'not_started', progress: 0 },
          { number: 2, name: 'Planning', status: 'not_started', progress: 0 },
          { number: 3, name: 'Execution', status: 'not_started', progress: 0 },
          { number: 4, name: 'Verification', status: 'not_started', progress: 0 },
          { number: 5, name: 'Shipping', status: 'not_started', progress: 0 }
        ],
        locked: false
      }));
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'in_progress': return <Circle className="w-5 h-5 text-blue-500 animate-pulse" />;
      case 'blocked': return <AlertTriangle className="w-5 h-5 text-red-500" />;
      default: return <Circle className="w-5 h-5 text-gray-400" />;
    }
  };

  const overallProgress = state.phases.length > 0
    ? Math.round(state.phases.reduce((acc, p) => acc + p.progress, 0) / state.phases.length)
    : 0;

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Map className="w-6 h-6 text-primary" />
          <div>
            <h2 className="text-xl font-bold">{state.project}</h2>
            <p className="text-sm text-muted-foreground">
              Phase {state.currentPhase || '—'} {state.locked && '🔒'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {state.locked ? <Lock className="w-4 h-4 text-amber-500" /> : <Unlock className="w-4 h-4 text-green-500" />}
          <span className="text-sm">{state.locked ? 'Locked' : 'Unlocked'}</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span>Overall Progress</span>
          <span className="font-bold">{overallProgress}%</span>
        </div>
        <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-primary transition-all duration-500"
            style={{ width: `${overallProgress}%` }}
          />
        </div>
      </div>

      {/* Phases */}
      <div className="space-y-3">
        {state.phases.map(phase => (
          <div
            key={phase.number}
            className={`flex items-center gap-4 p-4 rounded-lg border ${
              phase.number === state.currentPhase
                ? 'border-primary bg-primary/5'
                : 'border-border bg-card'
            }`}
          >
            {getStatusIcon(phase.status)}
            <div className="flex-1">
              <div className="flex justify-between items-center">
                <span className="font-semibold">Phase {phase.number}: {phase.name}</span>
                <span className="text-sm text-muted-foreground">{phase.progress}%</span>
              </div>
              <div className="w-full h-1.5 bg-gray-200 rounded-full mt-2 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    phase.status === 'completed' ? 'bg-green-500' :
                    phase.status === 'in_progress' ? 'bg-blue-500' :
                    phase.status === 'blocked' ? 'bg-red-500' :
                    'bg-gray-400'
                  }`}
                  style={{ width: `${phase.progress}%` }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="flex gap-3">
        <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:opacity-90">
          /planforge-status
        </button>
        <button className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:opacity-90">
          /planforge-plan
        </button>
        <button className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:opacity-90">
          /planforge-execute
        </button>
      </div>
    </div>
  );
}
