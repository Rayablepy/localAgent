import { useState } from "react";
import Navbar from "./components/Navbar";
import UserBubble from "./components/UserBubble";
import IncomingBubble from "./components/IncomingBubble";
import ChatInput from "./components/ChatInput";
import "./components/components.css";
import "./home.css";

type Message = {
  type: "user" | "incoming";
  text: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSend = async (msg: string) => {
    setMessages((prev) => [...prev, { type: "user", text: msg }]);

    try {
      if (!window.AgentAPI?.getOllamaResponse) {
        throw new Error("Electron bridge not available");
      }

      const aiReply = await window.AgentAPI.getOllamaResponse(msg);

      setMessages((prev) => [...prev, { type: "incoming", text: aiReply }]);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unknown error occurred";

      setMessages((prev) => [
        ...prev,
        { type: "incoming", text: `Error: ${message}` },
      ]);
    }
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
          ),
        )}
      </div>
      <ChatInput onSend={handleSend} />
    </div>
  );
}
