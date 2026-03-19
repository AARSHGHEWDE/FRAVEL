import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import Plan from "./pages/Plan";
import Itinerary from "./pages/Itinerary";
import History from "./pages/History";
import Auth from "./pages/Auth";
import Traces from "./pages/Traces";
import Navbar from "./components/layout/Navbar";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/plan" element={<Plan />} />
            <Route path="/itinerary/:tripId" element={<Itinerary />} />
            <Route path="/history" element={<History />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/traces/:tripId" element={<Traces />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
