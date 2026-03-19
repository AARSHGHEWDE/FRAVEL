import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="border-b border-surface-100 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link to="/" className="text-xl font-bold">FRAVEL</Link>
        <div className="flex gap-6">
          <Link to="/plan">Plan Trip</Link>
          <Link to="/history">History</Link>
          <Link to="/auth">Sign In</Link>
        </div>
      </div>
    </nav>
  );
}
