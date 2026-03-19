import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { History as HistoryIcon } from "lucide-react";
import TripHistory from "../components/trip/TripHistory";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import { supabase } from "../lib/supabase";

export default function History() {
  const [trips, setTrips] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTrips() {
      const { data } = await supabase
        .from("trips")
        .select("*")
        .order("created_at", { ascending: false });
      setTrips(data || []);
      setLoading(false);
    }
    loadTrips();
  }, []);

  return (
    <div className="mx-auto max-w-4xl px-6 py-12">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="space-y-6"
      >
        <div className="flex items-center gap-3">
          <HistoryIcon size={28} className="text-primary-600" />
          <h1 className="text-3xl font-bold font-display">Trip History</h1>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        ) : (
          <TripHistory trips={trips} />
        )}
      </motion.div>
    </div>
  );
}
