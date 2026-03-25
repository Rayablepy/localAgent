import { useState } from "react";
import Navbar from "./components/Navbar";
import UserBubble from "./components/UserBubble";
import IncomingBubble from "./components/IncomingBubble";
import ChatInput from "./components/ChatInput";
import "./components/components.css";
import "./home.css"

export default function Home() {
    //placeholder
  const [messages, setMessages] = useState([
    { type: "incoming", text: "Hello" },
    { type: "user", text: "Hi" }
  ]);

  const handleSend = (msg) => {
    setMessages((prev) => [...prev, { type: "user", text: msg }]);

    //fake reply
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { type: "incoming", text: "some texxt" }
      ]);
    }, 500);
  };

  return (
    <div className="chat-root h-screen flex flex-col">
      <Navbar />

      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-3">
        {messages.map((msg, i) =>
          msg.type === "user" ? (
            <UserBubble key={i} message={msg.text} />
          ) : (
            <IncomingBubble key={i} message={msg.text} />
          )
        )}
      </div>
      <ChatInput onSend={handleSend} />
    </div>
  );
}