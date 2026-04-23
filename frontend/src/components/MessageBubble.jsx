import { motion } from "framer-motion";
import { User, Bot } from "lucide-react";

export default function MessageBubble({ role, content }) {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
    >
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center mt-1">
          <Bot size={16} className="text-blue-400" />
        </div>
      )}

      <div
        className={`rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-violet-500/20 border border-violet-500/30 max-w-[80%]"
            : "glass max-w-[85%]"
        }`}
      >
        <p className="text-sm leading-relaxed text-gray-100 whitespace-pre-wrap">
          {content}
        </p>
      </div>

      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-violet-500/20 border border-violet-500/30 flex items-center justify-center mt-1">
          <User size={16} className="text-violet-400" />
        </div>
      )}
    </motion.div>
  );
}
