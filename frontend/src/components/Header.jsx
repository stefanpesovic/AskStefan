import SocialLinks from "./SocialLinks";

export default function Header() {
  return (
    <header className="flex items-center justify-between py-2">
      <div>
        <h1 className="text-2xl font-bold text-white">AskStefan</h1>
        <p className="text-sm text-gray-400">
          AI chatbot trained on my CV and projects
        </p>
      </div>
      <SocialLinks />
    </header>
  );
}
