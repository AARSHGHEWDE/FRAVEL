import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Plane, Ticket, UtensilsCrossed, CloudSun, Map,
  Clock, ChevronDown, ChevronUp, CheckCircle2,
} from "lucide-react";
import { getTraces, type TraceEntry } from "../lib/api";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import Badge from "../components/ui/Badge";

const AGENT_META: Record<string, { icon: React.ReactNode; color: string }> = {
  "Transport Agent":    { icon: <Plane size={18} />,           color: "text-blue-400" },
  "Events Agent":       { icon: <Ticket size={18} />,          color: "text-emerald-400" },
  "Restaurant Agent":   { icon: <UtensilsCrossed size={18} />, color: "text-amber-400" },
  "Weather Agent":      { icon: <CloudSun size={18} />,        color: "text-sky-400" },
  "Itinerary Compiler": { icon: <Map size={18} />,             color: "text-purple-400" },
};

function TraceCard({ trace, index }: { trace: TraceEntry; index: number }) {
  const [expanded, setExpanded] = useState(index === 0);
  const meta = AGENT_META[trace.agent] || { icon: <Map size={18} />, color: "text-surface-400" };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08 }}
      className="rounded-2xl border border-surface-800 bg-surface-900 overflow-hidden"
    >
      {/* Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-4 px-6 py-4 hover:bg-surface-800/50 transition-colors text-left"
      >
        <span className={meta.color}>{meta.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3">
            <span className="font-semibold text-surface-50">{trace.agent}</span>
            <Badge variant="success">
              <CheckCircle2 size={10} /> Done
            </Badge>
          </div>
          <p className="text-xs text-surface-500 mt-0.5 truncate">{trace.task}</p>
        </div>
        <div className="flex items-center gap-4 shrink-0">
          <span className="flex items-center gap-1.5 text-xs text-surface-400">
            <Clock size={12} />
            {trace.duration_seconds}s
          </span>
          <span className="text-xs text-surface-500">{trace.completed_at}</span>
          {expanded
            ? <ChevronUp size={16} className="text-surface-400" />
            : <ChevronDown size={16} className="text-surface-400" />
          }
        </div>
      </button>

      {/* Output */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <div className="px-6 pb-6 border-t border-surface-800">
              <p className="text-xs font-semibold text-surface-500 uppercase tracking-widest mt-4 mb-3">
                Agent Output
              </p>
              <pre className="whitespace-pre-wrap text-sm text-surface-300 leading-relaxed font-mono bg-surface-950 rounded-xl p-4 overflow-auto max-h-96">
                {trace.output}
              </pre>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default function Traces() {
  const { tripId } = useParams<{ tripId: string }>();
  const [traces, setTraces] = useState<TraceEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!tripId) return;
    getTraces(tripId)
      .then(setTraces)
      .catch(() => setError("Traces not available. The planning session may have ended."))
      .finally(() => setLoading(false));
  }, [tripId]);

  const totalTime = traces.reduce((acc, t) => acc + t.duration_seconds, 0);

  return (
    <div className="mx-auto max-w-3xl px-6 py-12">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold font-display">Execution Traces</h1>
          <p className="mt-1 text-surface-500">Step-by-step breakdown of what each AI agent did</p>
        </div>

        {loading && (
          <div className="flex justify-center py-16">
            <LoadingSpinner size="lg" />
          </div>
        )}

        {error && (
          <div className="rounded-xl border border-red-900/50 bg-red-900/20 px-6 py-4 text-red-400 text-sm">
            {error}
          </div>
        )}

        {!loading && !error && traces.length > 0 && (
          <>
            <div className="flex items-center gap-6 rounded-xl border border-surface-800 bg-surface-900 px-6 py-4 text-sm">
              <span className="text-surface-400">Agents ran: <span className="font-semibold text-surface-100">{traces.length}</span></span>
              <span className="text-surface-400">Total time: <span className="font-semibold text-surface-100">{totalTime.toFixed(1)}s</span></span>
            </div>
            <div className="space-y-3">
              {traces.map((trace, i) => (
                <TraceCard key={i} trace={trace} index={i} />
              ))}
            </div>
          </>
        )}

        {!loading && !error && traces.length === 0 && (
          <p className="text-center text-surface-500 py-12">No traces recorded for this trip.</p>
        )}
      </motion.div>
    </div>
  );
}
