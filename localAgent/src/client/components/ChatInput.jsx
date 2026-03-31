
import { useState } from "react";
import "./components.css";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div className="input-container w-full flex items-center gap-2 px-3 py-3">
      <input
        className="chat-input flex-1 px-3 py-2"
        placeholder="Type a message..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button
        className="send-btn px-4 py-2 "
        onClick={handleSend}
      >
        Send
      </button>
    </div>
  );
}