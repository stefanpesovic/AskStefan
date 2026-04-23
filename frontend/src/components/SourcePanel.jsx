import { BookOpen } from "lucide-react";
import SourceCard from "./SourceCard";

export default function SourcePanel({ sources, query }) {
  return (
    <div className="glass rounded-2xl h-full flex flex-col overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-white/5">
        <BookOpen size={16} className="text-blue-400" />
        <h2 className="text-sm font-semibold text-white">Sources</h2>
        {sources.length > 0 && (
          <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300">
            {sources.length}
          </span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {sources.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <p className="text-sm text-gray-500">
              Ask a question to see sources
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {sources.map((source, i) => (
              <SourceCard
                key={source.chunk_id}
                source={source}
                query={query}
                index={i}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
