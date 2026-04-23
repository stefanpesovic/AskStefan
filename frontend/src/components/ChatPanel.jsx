import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import EmptyState from "./EmptyState";
import TypingIndicator from "./TypingIndicator";
import InputBox from "./InputBox";

export default function ChatPanel({ messages, isLoading, onSend }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="glass rounded-2xl h-full flex flex-col overflow-hidden">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.length === 0 && !isLoading ? (
          <EmptyState />
        ) : (
          <div className="flex flex-col gap-4">
            {messages.map((msg, i) => (
              <MessageBubble key={i} role={msg.role} content={msg.content} />
            ))}
            {isLoading && <TypingIndicator />}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <div className="p-3 border-t border-white/5">
        <InputBox onSend={onSend} disabled={isLoading} />
      </div>
    </div>
  );
}
