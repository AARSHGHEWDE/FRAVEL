import { motion, AnimatePresence } from "framer-motion";
import { Plane, Ticket, UtensilsCrossed, CloudSun, Map, Loader2, CheckCircle2 } from "lucide-react";
import { useAgentStatus } from "../../hooks/useAgentStatus";
import AgentProgressRing from "./AgentProgressRing";
import type { ReactNode } from "react";

const ICONS: Record<string, ReactNode> = {
  plane: <Plane size={20} />,
  ticket: <Ticket size={20} />,
  utensils: <UtensilsCrossed size={20} />,
  "cloud-sun": <CloudSun size={20} />,
  map: <Map size={20} />,
};

export default function AgentStatusPanel() {
  const { agents, progress, isPlanning } = useAgentStatus();

  if (!isPlanning && agents.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-surface-200 bg-white p-6 shadow-lg dark:border-surface-800 dark:bg-surface-900"
    >
      <div className="flex items-center gap-6">
        <AgentProgressRing progress={progress} />
        <div className="flex-1 space-y-3">
          <h3 className="text-lg font-semibold font-display">AI Agents Working</h3>
          <AnimatePresence mode="popLayout">
            {agents.map((agent) => (
              <motion.div
                key={agent.agent}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-3"
              >
                <span className={agent.status === "done" ? "text-emerald-500" : "text-primary-500"}>
                  {ICONS[agent.icon] || <Map size={20} />}
                </span>
                <span className="flex-1 text-sm font-medium">{agent.agent}</span>
                {agent.status === "working" ? (
                  <Loader2 size={16} className="animate-spin text-primary-500" />
                ) : agent.status === "done" ? (
                  <CheckCircle2 size={16} className="text-emerald-500" />
                ) : null}
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );
}
