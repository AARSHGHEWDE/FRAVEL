import { motion } from "framer-motion";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { GripVertical } from "lucide-react";
import ActivityCard from "./ActivityCard";
import WeatherBadge from "./WeatherBadge";
import type { DayPlan } from "../../types";

interface DayColumnProps {
  day: DayPlan;
  index: number;
}

export default function DayColumn({ day, index }: DayColumnProps) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({
    id: day.date,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const dateObj = new Date(day.date);

  return (
    <motion.div
      ref={setNodeRef}
      style={style}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="space-y-4"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button
            {...attributes}
            {...listeners}
            className="cursor-grab text-surface-400 hover:text-surface-600 dark:hover:text-surface-300"
          >
            <GripVertical size={20} />
          </button>
          <div>
            <h3 className="text-lg font-bold font-display">{day.title}</h3>
            <p className="text-sm text-surface-500">
              {dateObj.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
            </p>
          </div>
        </div>
        {day.weather && <WeatherBadge weather={day.weather} />}
      </div>
      <div className="space-y-3">
        {day.activities.map((activity, i) => (
          <ActivityCard key={`${day.date}-${i}`} activity={activity} />
        ))}
      </div>
    </motion.div>
  );
}
