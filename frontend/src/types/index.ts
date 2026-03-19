export interface TripRequest {
  origin: string;
  destination: string;
  departure_date: string;
  return_date: string;
  budget: number;
  interests: string[];
  travelers: number;
}

export interface TripResponse {
  trip_id: string;
  status: "pending" | "planning" | "complete" | "error";
  request: TripRequest;
  itinerary_id?: string;
}

export interface FlightOption {
  airline: string;
  flight_number: string;
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  duration_minutes: number;
  price: number;
  currency: string;
  stops: number;
  cabin_class: string;
}

export interface EventOption {
  name: string;
  venue: string;
  date: string;
  category: string;
  price: number | null;
  currency: string;
  description: string;
  url: string;
  image_url: string;
}

export interface RestaurantOption {
  name: string;
  cuisine: string;
  rating: number;
  price_level: number;
  address: string;
  phone: string;
  url: string;
  image_url: string;
  review_count: number;
}

export interface DayWeather {
  date: string;
  temp_high_c: number;
  temp_low_c: number;
  condition: string;
  icon: string;
  humidity: number;
  wind_speed_kmh: number;
  precipitation_chance: number;
}

export interface Activity {
  time: string;
  title: string;
  description: string;
  category: "sightseeing" | "food" | "transport" | "event" | "free";
  cost: number;
  duration_minutes: number;
  location: string;
  latitude?: number;
  longitude?: number;
}

export interface DayPlan {
  date: string;
  title: string;
  activities: Activity[];
  weather?: DayWeather;
}

export interface Itinerary {
  trip_id: string;
  title: string;
  days: DayPlan[];
  total_cost: number;
  currency: string;
  summary: string;
}

export interface AgentStatus {
  agent: string;
  status: "idle" | "working" | "done" | "error" | "started" | "complete";
  detail: string;
}
