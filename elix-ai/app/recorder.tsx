"use client";
import { useState } from "react";
import { useReactMediaRecorder } from "react-media-recorder";
import axios from "axios";

export default function Recorder({ setInput }: { setInput: (text: string) => void }) {
  const [recording, setRecording] = useState(false);
  
  const { startRecording, stopRecording } = useReactMediaRecorder({
    audio: true,
    onStop: async (blobUrl, blob) => {
      console.log("Recording stopped, sending file...");
      const formData = new FormData();
      formData.append("file", blob, "audio.wav");
      
      try {
        const res = await axios.post("http://localhost:8000/transcribe", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setInput(res.data.text); 
      } catch (error) {
        console.error("Error transcribing audio:", error);
      }
    }
  });

  const handleStart = () => {
    setRecording(true);
    startRecording();
  };

  const handleStop = () => {
    setRecording(false);
    stopRecording();
  };

  return (
    <div>
      <button
        className={`p-2 rounded-lg ${recording ? "bg-red-500" : "bg-gray-500"} text-white`}
        onMouseDown={handleStart}
        onMouseUp={handleStop}
      >
        🎤
      </button>
    </div>
  );
}
