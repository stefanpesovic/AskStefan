import { SUGGESTED_PROMPTS } from "../config/prompts";

export default function SuggestedPrompts({ onSelect, disabled }) {
  return (
    <div className="flex flex-wrap gap-2 mt-2">
      {SUGGESTED_PROMPTS.map(({ label, query }) => (
        <button
          key={label}
          onClick={() => onSelect(query)}
          disabled={disabled}
          className="glass glass-hover rounded-full px-4 py-2 text-sm text-gray-300 hover:text-white transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {label}
        </button>
      ))}
    </div>
  );
}
