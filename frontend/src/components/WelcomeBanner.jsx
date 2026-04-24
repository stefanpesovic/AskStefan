import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, X } from "lucide-react";

const STORAGE_KEY = "welcomeBannerDismissed";

export default function WelcomeBanner() {
  const [visible, setVisible] = useState(
    () => !sessionStorage.getItem(STORAGE_KEY)
  );

  const dismiss = () => {
    sessionStorage.setItem(STORAGE_KEY, "true");
    setVisible(false);
  };

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
          className="bg-violet-500/10 border border-violet-500/20 backdrop-blur-xl rounded-xl px-6 py-3 flex items-start gap-3"
        >
          <Sparkles size={18} className="text-violet-400 mt-0.5 flex-shrink-0" />
          <p className="text-sm text-gray-300 flex-1">
            Welcome! 👋 This chatbot is a portfolio piece showcasing my work — feel free to ask anything about my projects, skills, or experience. Note: This is hosted on a free tier, so the first message may take 30-60 seconds while the server wakes up. Thanks for your patience!
          </p>
          <button
            onClick={dismiss}
            className="text-gray-400 hover:text-white transition-colors flex-shrink-0"
            aria-label="Dismiss welcome banner"
          >
            <X size={18} />
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
