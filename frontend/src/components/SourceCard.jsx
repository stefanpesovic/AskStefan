import { motion } from "framer-motion";
import { FileText, FileCode, BookOpen, User, File } from "lucide-react";
import { highlightText } from "../utils/highlight.jsx";

const typeConfig = {
  resume: { icon: FileText, badge: "Resume", color: "blue" },
  project_description: { icon: FileCode, badge: "Project", color: "violet" },
  blog: { icon: BookOpen, badge: "Blog", color: "emerald" },
  about: { icon: User, badge: "About", color: "amber" },
  other: { icon: File, badge: "Other", color: "gray" },
};

export default function SourceCard({ source, query, index }) {
  const config = typeConfig[source.source_type] || typeConfig.other;
  const Icon = config.icon;
  const score = Math.round(source.similarity_score * 100);

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      className="glass rounded-2xl p-4 glow-blue-hover transition-all duration-200"
    >
      <div className="flex items-center gap-2 mb-2">
        <Icon size={16} className={`text-${config.color}-400`} />
        <span className="text-sm font-medium text-white truncate">
          {source.source_file}
        </span>
        <span
          className={`ml-auto text-xs px-2 py-0.5 rounded-full bg-${config.color}-500/20 text-${config.color}-300 border border-${config.color}-500/30`}
        >
          {config.badge}
        </span>
      </div>

      <p className="text-xs text-gray-400 mb-2">{source.location}</p>

      <div className="flex items-center gap-2 mb-3">
        <div className="flex-1 h-1.5 rounded-full bg-white/5 overflow-hidden">
          <div
            className="h-full rounded-full bg-blue-500 transition-all duration-500"
            style={{ width: `${score}%` }}
          />
        </div>
        <span className="text-xs font-mono text-blue-400 w-10 text-right">
          {score}%
        </span>
      </div>

      <p className="text-xs leading-relaxed text-gray-300 font-mono line-clamp-4">
        {highlightText(source.text, query)}
      </p>
    </motion.div>
  );
}
