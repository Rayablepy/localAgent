
import "./components.css";

export default function UserBubble({ message }) {
  return (
    <div className="w-full flex justify-end">
      <div className="bubble user-bubble">
        {message}
      </div>
    </div>
  );
}