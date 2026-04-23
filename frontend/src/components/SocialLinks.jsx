import { Github, Linkedin, Mail } from "lucide-react";

const links = [
  {
    href: "https://github.com/stefanpesovic",
    icon: Github,
    label: "GitHub",
  },
  {
    href: "https://www.linkedin.com/in/stefan-pesovic-389a893a3",
    icon: Linkedin,
    label: "LinkedIn",
  },
  {
    href: "mailto:stefanpesovic@outlook.com",
    icon: Mail,
    label: "Email",
  },
];

export default function SocialLinks() {
  return (
    <div className="flex items-center gap-2">
      {links.map(({ href, icon: Icon, label }) => (
        <a
          key={label}
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          aria-label={label}
          className="p-2 rounded-lg text-gray-400 hover:text-white hover:scale-110 transition-all duration-200"
        >
          <Icon size={20} />
        </a>
      ))}
    </div>
  );
}
