import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ItineraryView from "../components/itinerary/ItineraryView";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import { useTripStore } from "../store/tripStore";
import { getTrip } from "../lib/api";
import type { Itinerary as ItineraryType } from "../types";

export default function Itinerary() {
  const { tripId } = useParams<{ tripId: string }>();
  const storeItinerary = useTripStore((s) => s.itinerary);
  const [fetchedItinerary, _setFetchedItinerary] = useState<ItineraryType | null>(null);
  const [error, setError] = useState<string | null>(null);

  const itinerary = storeItinerary || fetchedItinerary;

  useEffect(() => {
    if (!storeItinerary && tripId) {
      getTrip(tripId)
        .then((trip) => {
          if (trip.status === "complete") {
            // Itinerary data would be stored in Supabase; fetch it
            // For now, show a message to re-plan
            setError("Itinerary data not in memory. Please re-plan your trip.");
          }
        })
        .catch(() => setError("Trip not found"));
    }
  }, [storeItinerary, tripId]);

  if (error) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <p className="text-surface-500">{error}</p>
      </div>
    );
  }

  if (!itinerary) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="text-center space-y-4">
          <LoadingSpinner size="lg" />
          <p className="text-surface-500">Loading itinerary...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-6 py-12">
      <ItineraryView itinerary={itinerary} />
    </div>
  );
}
