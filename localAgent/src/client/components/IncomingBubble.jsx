
import "./components.css";

export default function IncomingBubble({ message }) {
  return (
    <div className="w-full flex justify-start">
      <div className="bubble incoming-bubble">
        {message}
      </div>
    </div>
  );
}