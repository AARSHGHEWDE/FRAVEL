import type { AgentStatus } from "../types";

export function connectToTripStream(
  tripId: string,
  onStatus: (status: AgentStatus) => void,
  onComplete: (result: string) => void,
  onError: (error: string) => void
): () => void {
  const source = new EventSource(`/api/trips/${tripId}/stream`);

  source.addEventListener("agent_status", (e: MessageEvent) => {
    const data: AgentStatus = JSON.parse(e.data);
    onStatus(data);
    if (data.status === "complete" && data.agent === "system") {
      onComplete(data.detail);
      source.close();
    }
  });

  source.onerror = () => { onError("Connection lost. Retrying..."); };
  return () => source.close();
}
