import { Ticket, Calendar, MapPin } from "lucide-react";
import Card from "../ui/Card";
import Badge from "../ui/Badge";
import type { EventOption } from "../../types";

export default function EventCard({ event }: { event: EventOption }) {
  const date = new Date(event.date);

  return (
    <Card hover className="flex gap-4">
      {event.image_url ? (
        <img
          src={event.image_url}
          alt={event.name}
          className="h-24 w-24 rounded-xl object-cover"
        />
      ) : (
        <div className="flex h-24 w-24 items-center justify-center rounded-xl bg-emerald-100 dark:bg-emerald-900/30">
          <Ticket size={32} className="text-emerald-600" />
        </div>
      )}
      <div className="flex-1 space-y-1">
        <h4 className="font-semibold">{event.name}</h4>
        <div className="flex items-center gap-2">
          <Badge variant="success">{event.category}</Badge>
          {event.price != null && (
            <span className="text-sm font-semibold text-primary-600">${event.price}</span>
          )}
        </div>
        <div className="flex gap-3 text-xs text-surface-400">
          <span className="flex items-center gap-1">
            <Calendar size={12} /> {date.toLocaleDateString()}
          </span>
          <span className="flex items-center gap-1">
            <MapPin size={12} /> {event.venue}
          </span>
        </div>
      </div>
    </Card>
  );
}
