import { useState, useRef } from "react";
import { Send, Loader2 } from "lucide-react";

export default function InputBox({ onSend, disabled }) {
  const [text, setText] = useState("");
  const textareaRef = useRef(null);

  const handleSubmit = () => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = (e) => {
    setText(e.target.value);
    const el = e.target;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 120) + "px";
  };

  return (
    <div className="glass rounded-2xl p-2 flex items-end gap-2">
      <textarea
        ref={textareaRef}
        value={text}
        onChange={handleInput}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder="Ask me anything about Stefan..."
        rows={1}
        className="flex-1 bg-transparent border-none outline-none resize-none text-sm text-gray-100 placeholder-gray-500 px-3 py-2 max-h-[120px]"
      />
      <button
        onClick={handleSubmit}
        disabled={!text.trim() || disabled}
        className="flex-shrink-0 w-9 h-9 rounded-xl bg-blue-500 hover:bg-blue-600 disabled:bg-white/5 disabled:text-gray-600 text-white flex items-center justify-center transition-all duration-200"
      >
        {disabled ? (
          <Loader2 size={16} className="animate-spin" />
        ) : (
          <Send size={16} />
        )}
      </button>
    </div>
  );
}
