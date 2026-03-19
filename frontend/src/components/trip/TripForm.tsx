import { useState } from "react";
import { motion } from "framer-motion";
import { MapPin, Users, Sparkles } from "lucide-react";
import Input from "../ui/Input";
import Button from "../ui/Button";
import DateRangePicker from "../ui/DateRangePicker";
import Slider from "../ui/Slider";
import { useTripStore } from "../../store/tripStore";

const INTEREST_OPTIONS = [
  "Museums", "Food", "Nightlife", "Nature", "Shopping",
  "History", "Art", "Music", "Sports", "Adventure",
  "Beach", "Architecture", "Photography", "Local Culture",
];

export default function TripForm() {
  const { setTripRequest, startPlanning, isPlanning } = useTripStore();
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [budget, setBudget] = useState(3000);
  const [travelers, setTravelers] = useState(1);
  const [interests, setInterests] = useState<string[]>([]);

  const toggleInterest = (interest: string) => {
    setInterests((prev) =>
      prev.includes(interest)
        ? prev.filter((i) => i !== interest)
        : [...prev, interest]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const request = {
      origin,
      destination,
      departure_date: startDate,
      return_date: endDate,
      budget,
      interests: interests.map((i) => i.toLowerCase()),
      travelers,
    };
    setTripRequest(request);
    await startPlanning();
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="mx-auto max-w-2xl space-y-6 rounded-3xl border border-surface-200 bg-white p-8 shadow-xl dark:border-surface-800 dark:bg-surface-900"
    >
      <div className="text-center">
        <h2 className="text-2xl font-bold font-display">Plan Your Trip</h2>
        <p className="mt-1 text-surface-500">Our AI agents will craft the perfect itinerary</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="relative">
          <MapPin size={16} className="absolute left-3 top-9 text-surface-400" />
          <Input
            label="From"
            placeholder="New York"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            className="pl-9"
            required
          />
        </div>
        <div className="relative">
          <MapPin size={16} className="absolute left-3 top-9 text-primary-500" />
          <Input
            label="To"
            placeholder="Paris"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            className="pl-9"
            required
          />
        </div>
      </div>

      <DateRangePicker
        startDate={startDate}
        endDate={endDate}
        onStartChange={setStartDate}
        onEndChange={setEndDate}
      />

      <Slider
        label="Budget"
        value={budget}
        min={500}
        max={20000}
        step={100}
        format={(v) => `$${v.toLocaleString()}`}
        onChange={setBudget}
      />

      <div className="flex flex-col gap-1.5">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          <Users size={14} className="mr-1 inline" />
          Travelers: {travelers}
        </label>
        <input
          type="range"
          min={1}
          max={10}
          value={travelers}
          onChange={(e) => setTravelers(Number(e.target.value))}
          className="accent-primary-600"
        />
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">Interests</label>
        <div className="flex flex-wrap gap-2">
          {INTEREST_OPTIONS.map((interest) => (
            <motion.button
              key={interest}
              type="button"
              whileTap={{ scale: 0.95 }}
              onClick={() => toggleInterest(interest)}
              className={`rounded-full px-3 py-1 text-sm font-medium transition-colors ${
                interests.includes(interest)
                  ? "bg-primary-600 text-white"
                  : "bg-surface-100 text-surface-600 hover:bg-surface-200 dark:bg-surface-800 dark:text-surface-400"
              }`}
            >
              {interest}
            </motion.button>
          ))}
        </div>
      </div>

      <Button
        type="submit"
        size="lg"
        className="w-full"
        disabled={isPlanning || !origin || !destination || !startDate || !endDate}
      >
        <Sparkles size={18} />
        {isPlanning ? "Planning..." : "Plan My Trip"}
      </Button>
    </motion.form>
  );
}
