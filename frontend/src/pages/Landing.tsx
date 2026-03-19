import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Plane, MapPin, Sparkles, Utensils, Cloud, Calendar } from "lucide-react";
import Button from "../components/ui/Button";

const features = [
  { icon: <Plane size={24} />, title: "Smart Flights", desc: "AI finds the best routes and prices" },
  { icon: <Calendar size={24} />, title: "Local Events", desc: "Discover festivals, concerts, tours" },
  { icon: <Utensils size={24} />, title: "Top Restaurants", desc: "Curated dining with real reviews" },
  { icon: <Cloud size={24} />, title: "Weather Aware", desc: "Plans adapt to forecasted conditions" },
  { icon: <MapPin size={24} />, title: "Day-by-Day", desc: "Optimized itineraries with maps" },
  { icon: <Sparkles size={24} />, title: "AI Powered", desc: "5 specialized agents work for you" },
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="overflow-hidden">
      {/* Hero */}
      <section className="relative flex min-h-[80vh] items-center justify-center px-6">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-accent-400/10 dark:from-surface-950 dark:via-surface-950 dark:to-primary-950/30" />
        <div className="absolute inset-0 overflow-hidden">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute h-1 w-1 rounded-full bg-primary-400/20"
              style={{ left: `${Math.random() * 100}%`, top: `${Math.random() * 100}%` }}
              animate={{ y: [0, -30, 0], opacity: [0.2, 0.8, 0.2] }}
              transition={{ duration: 3 + Math.random() * 4, repeat: Infinity, delay: Math.random() * 2 }}
            />
          ))}
        </div>
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative z-10 text-center"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", delay: 0.2 }}
            className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-primary-600 text-white shadow-2xl shadow-primary-500/40"
          >
            <Plane size={40} />
          </motion.div>
          <h1 className="text-5xl font-bold font-display tracking-tight sm:text-7xl">
            <span className="text-primary-600">FR</span>AVEL
          </h1>
          <p className="mt-4 text-lg text-surface-500 sm:text-xl max-w-xl mx-auto">
            AI agents research flights, events, restaurants, and weather — then build your perfect itinerary.
          </p>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-8 flex gap-4 justify-center"
          >
            <Button size="lg" onClick={() => navigate("/plan")}>
              <Sparkles size={18} />
              Plan a Trip
            </Button>
            <Button variant="secondary" size="lg" onClick={() => navigate("/auth")}>
              Sign In
            </Button>
          </motion.div>
        </motion.div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-6xl px-6 py-24">
        <h2 className="text-center text-3xl font-bold font-display">How It Works</h2>
        <p className="mt-2 text-center text-surface-500">Five specialized AI agents work together</p>
        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="rounded-2xl border border-surface-200 bg-white p-6 dark:border-surface-800 dark:bg-surface-900"
            >
              <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400">
                {f.icon}
              </div>
              <h3 className="font-semibold">{f.title}</h3>
              <p className="mt-1 text-sm text-surface-500">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}
