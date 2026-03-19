import { Link } from "react-router-dom";
import { Plane } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 border-b border-surface-100 bg-white/80 backdrop-blur-xl dark:border-surface-800 dark:bg-surface-950/80">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold font-display text-primary-600">
          <Plane size={24} />
          FRAVEL
        </Link>
        <div className="flex items-center gap-6">
          <Link to="/plan" className="text-sm font-medium hover:text-primary-500 transition-colors">
            Plan Trip
          </Link>
          <Link to="/history" className="text-sm font-medium hover:text-primary-500 transition-colors">
            History
          </Link>
          <Link to="/auth" className="text-sm font-medium hover:text-primary-500 transition-colors">
            Sign In
          </Link>
          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
}
