import "./components.css";

export default function Navbar() {
  return (
    <div className="navbar-container w-full flex items-center justify-between px-4 py-3">
      <h1 className="text-lg font-semibold text-white">Chat</h1>
      <div className="text-sm text-white opacity-70">Online</div>
    </div>
  );
}