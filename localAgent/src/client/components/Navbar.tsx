import "./components.css";
import Dropdown from "./Dropdown";

export default function Navbar() {
  return (
    <div className="navbar-container w-full flex items-center justify-between px-4 py-3">
      <h1 className="text-lg font-semibold text-white">Chat</h1>
      <Dropdown />
    </div>
  );
}
