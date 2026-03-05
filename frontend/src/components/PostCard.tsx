import { Link } from "react-router-dom";
import type { Post } from "../types";

interface Props {
  post: Post;
}

export default function PostCard({ post }: Props) {
  return (
    <article className="rounded-lg border bg-white p-6 shadow-sm transition hover:shadow-md">
      <Link to={`/posts/${post.id}`}>
        <h2 className="text-xl font-semibold text-gray-900 hover:text-indigo-600">
          {post.title}
        </h2>
      </Link>
      <p className="mt-2 line-clamp-3 text-gray-600">{post.body}</p>
      <div className="mt-4 flex items-center justify-between text-sm text-gray-400">
        <span>Autor: {post.author_name}</span>
        <time>{new Date(post.created_at).toLocaleDateString("pl-PL")}</time>
      </div>
    </article>
  );
}
