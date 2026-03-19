import { motion } from "framer-motion";
import { MapPin, Calendar, DollarSign, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Badge from "../ui/Badge";

interface TripCardProps {
  tripId: string;
  origin: string;
  destination: string;
  departureDate: string;
  returnDate: string;
  budget: number;
  status: string;
}

export default function TripCard({
  tripId, origin, destination, departureDate, returnDate, budget, status,
}: TripCardProps) {
  const navigate = useNavigate();

  return (
    <motion.div
      whileHover={{ y: -2 }}
      onClick={() => navigate(`/itinerary/${tripId}`)}
      className="cursor-pointer rounded-2xl border border-surface-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md dark:border-surface-800 dark:bg-surface-900"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-lg font-semibold font-display">
          <MapPin size={18} className="text-primary-500" />
          {origin} <ArrowRight size={16} /> {destination}
        </div>
        <Badge variant={status === "complete" ? "success" : status === "error" ? "error" : "info"}>
          {status}
        </Badge>
      </div>
      <div className="mt-3 flex gap-4 text-sm text-surface-500">
        <span className="flex items-center gap-1">
          <Calendar size={14} /> {departureDate} - {returnDate}
        </span>
        <span className="flex items-center gap-1">
          <DollarSign size={14} /> ${budget.toLocaleString()}
        </span>
      </div>
    </motion.div>
  );
}
