import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import TripForm from "../components/trip/TripForm";
import AgentStatusPanel from "../components/agents/AgentStatusPanel";
import ItineraryView from "../components/itinerary/ItineraryView";
import { useTripStore } from "../store/tripStore";

export default function Plan() {
  const { itinerary, isPlanning, tripResponse } = useTripStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (itinerary && tripResponse) {
      navigate(`/itinerary/${tripResponse.trip_id}`);
    }
  }, [itinerary, tripResponse, navigate]);

  return (
    <div className="mx-auto max-w-4xl px-6 py-12 space-y-8">
      {!isPlanning && !itinerary && <TripForm />}
      {isPlanning && <AgentStatusPanel />}
      {itinerary && <ItineraryView itinerary={itinerary} />}
    </div>
  );
}
