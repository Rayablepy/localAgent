import { useState } from "react";
import Navbar from "./components/Navbar";
import UserBubble from "./components/UserBubble";
import IncomingBubble from "./components/IncomingBubble";
import ChatInput from "./components/ChatInput";
import "./components/components.css";
window.messagelog = {
  role:[],
  content:[]
};
export function Home() {
    //dont touch
  const [messages, setMessages] = useState([
  ]);

    const handleSend = async (msg) => {
      setMessages((prev) => [...prev, { type: "user", text: msg }]
      );
      window.messagelog.role.push("user")
      window.messagelog.content.push(msg)
      try {
        if (!window.AgentAPI?.getOllamaResponse) {
          throw new Error("Electron bridge not available");
        }
        
        const aiReply = await window.AgentAPI.getOllamaResponse(msg); //get ai reply
        window.messagelog.role.push("ai")
        window.messagelog.content.push(aiReply)
        setMessages((prev) => [
          ...prev,
          { type: "incoming", text: aiReply }
        ]);
      } catch (error) {
        setMessages((prev) => [
          ...prev,
          { type: "incoming", text: `Error: ${error.message}` }
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
          )
        )}
      </div>
      <ChatInput onSend={handleSend} />
    </div>
  );
}

