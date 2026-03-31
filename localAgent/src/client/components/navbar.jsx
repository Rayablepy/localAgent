import "./components.css";
import Dropdown from "./dropdown.jsx"

export default function Navbar() {
  return (
    <div className="navbar-container w-full flex items-center justify-between px-4 py-3">
        <Dropdown />
    </div>
  );
}