import TripCard from "./TripCard";

interface Trip {
  id: string;
  request: {
    origin: string;
    destination: string;
    departure_date: string;
    return_date: string;
    budget: number;
  };
  status: string;
}

export default function TripHistory({ trips }: { trips: Trip[] }) {
  if (trips.length === 0) {
    return (
      <div className="text-center py-12 text-surface-500">
        No trips yet. Start planning your first adventure!
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {trips.map((trip) => (
        <TripCard
          key={trip.id}
          tripId={trip.id}
          origin={trip.request.origin}
          destination={trip.request.destination}
          departureDate={trip.request.departure_date}
          returnDate={trip.request.return_date}
          budget={trip.request.budget}
          status={trip.status}
        />
      ))}
    </div>
  );
}
