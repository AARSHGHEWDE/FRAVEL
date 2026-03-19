import { motion } from "framer-motion";
import { DndContext, closestCenter } from "@dnd-kit/core";
import { SortableContext, verticalListSortingStrategy } from "@dnd-kit/sortable";
import { DollarSign, Calendar } from "lucide-react";
import DayColumn from "./DayColumn";
import ExportPDF from "./ExportPDF";
import type { Itinerary } from "../../types";

interface ItineraryViewProps {
  itinerary: Itinerary;
}

export default function ItineraryView({ itinerary }: ItineraryViewProps) {
  return (
    <div className="mx-auto max-w-4xl space-y-8" id="itinerary-content">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold font-display">{itinerary.title}</h1>
        {itinerary.summary && (
          <p className="mt-2 text-surface-500 max-w-2xl mx-auto">{itinerary.summary}</p>
        )}
        <div className="mt-4 flex items-center justify-center gap-6">
          <span className="flex items-center gap-2 text-sm">
            <Calendar size={16} className="text-primary-500" />
            {itinerary.days.length} days
          </span>
          <span className="flex items-center gap-2 text-sm">
            <DollarSign size={16} className="text-emerald-500" />
            ${itinerary.total_cost.toLocaleString()} {itinerary.currency}
          </span>
          <ExportPDF />
        </div>
      </motion.div>

      <DndContext collisionDetection={closestCenter}>
        <SortableContext items={itinerary.days.map((d) => d.date)} strategy={verticalListSortingStrategy}>
          <div className="space-y-10">
            {itinerary.days.map((day, i) => (
              <DayColumn key={day.date} day={day} index={i} />
            ))}
          </div>
        </SortableContext>
      </DndContext>
    </div>
  );
}
