const STOPWORDS = new Set([
  "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
  "have", "has", "had", "do", "does", "did", "will", "would", "could",
  "should", "may", "might", "shall", "can", "need", "must",
  "and", "or", "but", "nor", "not", "no", "so", "yet",
  "of", "in", "to", "for", "with", "on", "at", "from", "by", "about",
  "as", "into", "through", "during", "before", "after", "above", "below",
  "between", "under", "over",
  "it", "its", "he", "she", "they", "them", "his", "her", "their",
  "this", "that", "these", "those", "what", "which", "who", "whom",
  "how", "when", "where", "why",
  "i", "me", "my", "we", "us", "our", "you", "your",
  "all", "each", "every", "any", "some", "more", "most", "other",
  "than", "then", "also", "just", "very", "too",
  "tell", "know", "like", "get", "make", "go", "see", "come",
]);

/**
 * Highlight words from the query that appear in the text.
 * Returns an array of React elements (strings and <mark> spans).
 */
export function highlightText(text, query) {
  if (!query || !text) return [text];

  const keywords = query
    .toLowerCase()
    .split(/\s+/)
    .filter((w) => w.length > 2 && !STOPWORDS.has(w));

  if (keywords.length === 0) return [text];

  const pattern = new RegExp(
    `(${keywords.map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})`,
    "gi"
  );

  const parts = text.split(pattern);

  return parts.map((part, i) => {
    if (keywords.some((kw) => part.toLowerCase() === kw)) {
      return (
        <mark
          key={i}
          className="bg-blue-500/30 text-blue-200 rounded px-0.5"
        >
          {part}
        </mark>
      );
    }
    return part;
  });
}
