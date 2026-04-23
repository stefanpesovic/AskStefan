import { useState } from "react";
import Header from "./components/Header";
import SuggestedPrompts from "./components/SuggestedPrompts";
import ChatPanel from "./components/ChatPanel";
import SourcePanel from "./components/SourcePanel";
import useChat from "./hooks/useChat";

function App() {
  const { messages, currentSources, isLoading, lastQuery, sendMessage } = useChat();
  const [showSources, setShowSources] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900/30 to-slate-900">
      <div className="mx-auto max-w-7xl px-4 py-4 flex flex-col h-screen">
        <Header />

        <SuggestedPrompts onSelect={sendMessage} disabled={isLoading} />

        <div className="flex flex-1 gap-4 mt-4 min-h-0">
          <div className="flex-[3] min-w-0">
            <ChatPanel
              messages={messages}
              isLoading={isLoading}
              onSend={sendMessage}
            />
          </div>

          <div className="hidden lg:block flex-[2] min-w-0">
            <SourcePanel sources={currentSources} query={lastQuery} />
          </div>
        </div>

        {currentSources.length > 0 && (
          <button
            onClick={() => setShowSources(!showSources)}
            className="lg:hidden fixed bottom-20 right-4 z-50 glass rounded-full px-4 py-2 text-sm text-blue-400 font-medium glow-blue"
          >
            Sources ({currentSources.length})
          </button>
        )}

        {showSources && (
          <div className="lg:hidden fixed inset-0 z-40 flex flex-col">
            <div
              className="flex-1 bg-black/50 backdrop-blur-sm"
              onClick={() => setShowSources(false)}
            />
            <div className="glass rounded-t-2xl max-h-[70vh] overflow-y-auto p-4">
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-white font-semibold">
                  Sources ({currentSources.length})
                </h3>
                <button
                  onClick={() => setShowSources(false)}
                  className="text-gray-400 hover:text-white text-sm"
                >
                  Close
                </button>
              </div>
              <SourcePanel sources={currentSources} query={lastQuery} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
