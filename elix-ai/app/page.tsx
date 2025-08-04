"use client";

import { useState } from "react";
import axios from "axios";
import { FaPaperPlane } from "react-icons/fa";
import dynamic from "next/dynamic";

// Dynamically import Recorder with SSR disabled
const Recorder = dynamic(() => import("./recorder"), { ssr: false });

interface ResponseObject {
  response: string;
}

interface ChatResponse {
  responses: ResponseObject[];
}

export default function Home() {
  const [messages, setMessages] = useState<{ text: string; sender: string }[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    try {
      const res = await axios.post<ChatResponse>("http://127.0.0.1:8000/chat", { message: input });
      res.data.responses.forEach((responseObj: ResponseObject) => {
        const botMessage = { text: responseObj.response, sender: "bot" };
        setMessages(prev => [...prev, botMessage]);
      });
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="flex flex-col items-center h-screen bg-black p-4 text-white">
      <h1 className="text-2xl font-bold mb-4 text-white">Musk AI</h1>

      <div className="w-full max-w-[80%] bg-gray-800 shadow-md rounded-lg p-4 h-[75vh] overflow-y-auto">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-2 rounded-lg my-1 w-fit max-w-[80%] ${msg.sender === "user" ? "bg-green-300 text-black ml-auto" : "bg-blue-300 text-black"}`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="flex w-full max-w-[80%] items-center gap-2 mt-4">
        <input
          className="flex-1 p-2 border rounded-lg bg-gray-800 text-white"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
        />
        <button className="bg-blue-500 text-white p-2 rounded-lg" onClick={sendMessage}>
          <FaPaperPlane />
        </button>
        <Recorder setInput={setInput} />
      </div>
    </div>
  );
}
