import { create } from "zustand";
import type { TripRequest, TripResponse, AgentStatus, Itinerary } from "../types";
import { createTrip } from "../lib/api";
import { connectToTripStream } from "../lib/sse";

interface TripState {
  tripRequest: TripRequest | null;
  setTripRequest: (req: TripRequest) => void;
  tripResponse: TripResponse | null;
  agentStatuses: AgentStatus[];
  isPlanning: boolean;
  error: string | null;
  itinerary: Itinerary | null;
  startPlanning: () => Promise<void>;
  reset: () => void;
}

export const useTripStore = create<TripState>((set, get) => ({
  tripRequest: null,
  tripResponse: null,
  agentStatuses: [],
  isPlanning: false,
  error: null,
  itinerary: null,

  setTripRequest: (req) => set({ tripRequest: req }),

  startPlanning: async () => {
    const { tripRequest } = get();
    if (!tripRequest) return;
    set({ isPlanning: true, error: null, agentStatuses: [], itinerary: null });

    try {
      const response = await createTrip(tripRequest);
      set({ tripResponse: response });

      connectToTripStream(
        response.trip_id,
        (status) => {
          set((state) => {
            const existing = state.agentStatuses.findIndex((s) => s.agent === status.agent);
            const updated = [...state.agentStatuses];
            if (existing >= 0) { updated[existing] = status; } else { updated.push(status); }
            return { agentStatuses: updated };
          });
        },
        (result) => {
          try {
            const itinerary = JSON.parse(result) as Itinerary;
            set({ itinerary, isPlanning: false });
          } catch {
            set({ isPlanning: false, error: "Failed to parse itinerary" });
          }
        },
        (error) => { set({ error, isPlanning: false }); }
      );
    } catch (e) {
      set({ error: (e as Error).message, isPlanning: false });
    }
  },

  reset: () => set({ tripRequest: null, tripResponse: null, agentStatuses: [], isPlanning: false, error: null, itinerary: null }),
}));
