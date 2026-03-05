import type { Comment } from "../types";

interface Props {
  comments: Comment[];
}

export default function CommentList({ comments }: Props) {
  if (comments.length === 0) {
    return <p className="text-sm text-gray-400">Brak komentarzy.</p>;
  }

  return (
    <ul className="space-y-4">
      {comments.map((c) => (
        <li key={c.id} className="rounded border bg-gray-50 p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">
              {c.author_name}
            </span>
            <time className="text-xs text-gray-400">
              {new Date(c.created_at).toLocaleString("pl-PL")}
            </time>
          </div>
          <p className="mt-1 text-gray-600">{c.body}</p>
        </li>
      ))}
    </ul>
  );
}
