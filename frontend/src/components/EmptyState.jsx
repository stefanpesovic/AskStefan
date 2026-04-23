import { MessageSquare } from "lucide-react";

export default function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center px-4">
      <div className="w-16 h-16 rounded-2xl glass flex items-center justify-center mb-4">
        <MessageSquare size={28} className="text-blue-400" />
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">
        Start a conversation
      </h3>
      <p className="text-sm text-gray-400 max-w-xs">
        Click a suggestion above or type your own question about Stefan
      </p>
    </div>
  );
}
