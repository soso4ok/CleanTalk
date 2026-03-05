export default function Footer() {
  return (
    <footer className="mt-16 border-t bg-white py-6 text-center text-sm text-gray-400">
      <p>
        &copy; {new Date().getFullYear()} CleanTalk &mdash; AI-powered blog
        moderation
      </p>
      <p className="mt-1">
        Built with FastAPI, React &amp; Tailwind CSS
      </p>
    </footer>
  );
}
