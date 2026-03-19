import { Plane, Clock, ArrowRight } from "lucide-react";
import Card from "../ui/Card";
import Badge from "../ui/Badge";
import type { FlightOption } from "../../types";

export default function FlightCard({ flight }: { flight: FlightOption }) {
  const dep = new Date(flight.departure_time);
  const arr = new Date(flight.arrival_time);

  return (
    <Card hover className="flex items-center gap-4">
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400">
        <Plane size={24} />
      </div>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className="font-semibold">{flight.airline} {flight.flight_number}</span>
          <Badge variant={flight.stops === 0 ? "success" : "warning"}>
            {flight.stops === 0 ? "Direct" : `${flight.stops} stop(s)`}
          </Badge>
        </div>
        <div className="flex items-center gap-2 text-sm text-surface-500">
          <span>{flight.origin} {dep.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
          <ArrowRight size={14} />
          <span>{flight.destination} {arr.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
          <span className="flex items-center gap-1"><Clock size={12} /> {Math.floor(flight.duration_minutes / 60)}h {flight.duration_minutes % 60}m</span>
        </div>
      </div>
      <div className="text-right">
        <div className="text-xl font-bold text-primary-600 dark:text-primary-400">${flight.price}</div>
        <div className="text-xs text-surface-400">{flight.cabin_class}</div>
      </div>
    </Card>
  );
}
