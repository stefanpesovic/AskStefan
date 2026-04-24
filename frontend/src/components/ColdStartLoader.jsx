import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

const statusTexts = [
  "Waking up the server...",
  "Loading the AI model...",
  "Almost ready...",
  "Any moment now...",
];

export default function ColdStartLoader() {
  const [textIndex, setTextIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setTextIndex((prev) => (prev + 1) % statusTexts.length);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex gap-3 justify-start">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl px-5 py-4 flex items-center gap-3 animate-pulse shadow-lg shadow-blue-500/50"
      >
        <Loader2 size={18} className="text-blue-400 animate-spin" />
        <span className="text-blue-400 text-sm font-medium">
          {statusTexts[textIndex]}
        </span>
      </motion.div>
    </div>
  );
}
