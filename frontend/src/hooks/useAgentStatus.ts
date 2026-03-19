import { useTripStore } from "../store/tripStore";

const AGENT_ICONS: Record<string, string> = {
  "Transport Agent": "plane",
  "Events Agent": "ticket",
  "Restaurant Agent": "utensils",
  "Weather Agent": "cloud-sun",
  "Itinerary Compiler": "map",
  system: "cpu",
};

export function useAgentStatus() {
  const agentStatuses = useTripStore((s) => s.agentStatuses);
  const isPlanning = useTripStore((s) => s.isPlanning);
  const agents = agentStatuses
    .filter((s) => s.agent !== "system")
    .map((s) => ({ ...s, icon: AGENT_ICONS[s.agent] || "bot" }));
  const progress = agents.length ? agents.filter((a) => a.status === "done").length / agents.length : 0;
  return { agents, progress, isPlanning };
}
