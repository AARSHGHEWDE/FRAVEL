import { CloudSun, Cloud, CloudRain, Sun, Snowflake } from "lucide-react";
import type { DayWeather } from "../../types";

const WEATHER_ICONS: Record<string, React.ReactNode> = {
  Clear: <Sun size={16} className="text-amber-500" />,
  Clouds: <Cloud size={16} className="text-surface-400" />,
  Rain: <CloudRain size={16} className="text-blue-500" />,
  Snow: <Snowflake size={16} className="text-blue-300" />,
};

export default function WeatherBadge({ weather }: { weather: DayWeather }) {
  return (
    <div className="flex items-center gap-2 rounded-lg bg-surface-50 px-3 py-1.5 text-xs dark:bg-surface-800">
      {WEATHER_ICONS[weather.condition] || <CloudSun size={16} />}
      <span>{weather.temp_low_c}°-{weather.temp_high_c}°C</span>
      <span className="text-surface-400">{weather.precipitation_chance}% rain</span>
    </div>
  );
}
