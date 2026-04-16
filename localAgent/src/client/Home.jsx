import { useState } from "react";
import Navbar from "./components/Navbar";
import UserBubble from "./components/UserBubble";
import IncomingBubble from "./components/IncomingBubble";
import ChatInput from "./components/ChatInput";
import { addmessage, voidmessage } from "./chatmemorycache.js";
import "./components/components.css";

export function Home() {
  //dont touch
  const [messages, setMessages] = useState([]);

  const handleSend = async (msg) => {
    setMessages((prev) => [...prev, {type: "user", text: msg}]
    );
    addmessage("user", msg)
    try {
      if (!window.AgentAPI?.getOllamaResponse) {
        throw new Error("Electron bridge not available");
      }

      const aiReply = await window.AgentAPI.getOllamaResponse(msg); //get ai reply
      addmessage("ai", aiReply);
      setMessages((prev) => [
        ...prev,
        {type: "incoming", text: aiReply}
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {type: "incoming", text: `Error: ${error.message}`}
      ]);
    }
  };
  voidmessage()
  return (
      <div className="chat-root h-screen flex flex-col">
        <Navbar/>

        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-3">
          {messages.map((msg, i) =>
              msg.type === "user" ? (
                  <UserBubble key={i} message={msg.text}/>
              ) : (
                  <IncomingBubble key={i} message={msg.text}/>
              )
          )}
        </div>
        <ChatInput onSend={handleSend}/>
      </div>
  );
}

