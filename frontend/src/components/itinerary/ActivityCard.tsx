import { motion } from "framer-motion";
import { Clock, MapPin, DollarSign } from "lucide-react";
import Badge from "../ui/Badge";
import type { Activity } from "../../types";

const CATEGORY_COLORS: Record<string, "info" | "success" | "warning" | "default" | "error"> = {
  sightseeing: "info",
  food: "warning",
  transport: "default",
  event: "success",
  free: "default",
};

export default function ActivityCard({ activity }: { activity: Activity }) {
  return (
    <motion.div
      whileHover={{ x: 4 }}
      className="flex gap-4 rounded-xl border border-surface-100 bg-white p-4 dark:border-surface-800 dark:bg-surface-900"
    >
      <div className="flex flex-col items-center">
        <span className="text-sm font-bold text-primary-600 dark:text-primary-400">{activity.time}</span>
        <div className="mt-1 h-full w-px bg-surface-200 dark:bg-surface-700" />
      </div>
      <div className="flex-1 space-y-1">
        <div className="flex items-start justify-between">
          <h4 className="font-semibold">{activity.title}</h4>
          <Badge variant={CATEGORY_COLORS[activity.category] || "default"}>
            {activity.category}
          </Badge>
        </div>
        <p className="text-sm text-surface-500">{activity.description}</p>
        <div className="flex gap-4 text-xs text-surface-400">
          <span className="flex items-center gap-1">
            <Clock size={12} /> {activity.duration_minutes}min
          </span>
          {activity.location && (
            <span className="flex items-center gap-1">
              <MapPin size={12} /> {activity.location}
            </span>
          )}
          {activity.cost > 0 && (
            <span className="flex items-center gap-1">
              <DollarSign size={12} /> ${activity.cost}
            </span>
          )}
        </div>
      </div>
    </motion.div>
  );
}
