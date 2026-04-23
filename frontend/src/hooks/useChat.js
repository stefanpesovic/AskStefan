import { useState, useCallback } from "react";
import toast from "react-hot-toast";
import api from "../api/client";

export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [currentSources, setCurrentSources] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [lastQuery, setLastQuery] = useState("");

  const sendMessage = useCallback(
    async (text) => {
      if (!text.trim() || isLoading) return;

      const userMessage = { role: "user", content: text };
      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setLastQuery(text);

      try {
        const { data } = await api.post("/chat", { question: text });

        const assistantMessage = { role: "assistant", content: data.answer };
        setMessages((prev) => [...prev, assistantMessage]);
        setCurrentSources(data.sources);
      } catch (err) {
        const status = err.response?.status;

        if (status === 429) {
          toast.error("I'm getting a lot of questions — please wait a moment");
        } else if (status === 503) {
          toast.error("Indexing documents... please try again in a moment.");
          try {
            await api.post("/ingest");
            toast.success("Documents indexed! Try your question again.");
          } catch {
            toast.error("Failed to index documents.");
          }
        } else if (err.code === "ERR_NETWORK" || !err.response) {
          toast.error("Connection issue. Please try again.");
        } else {
          toast.error("Something went wrong. Please try again.");
        }

        setMessages((prev) => prev.slice(0, -1));
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading]
  );

  return { messages, currentSources, isLoading, lastQuery, sendMessage };
}
