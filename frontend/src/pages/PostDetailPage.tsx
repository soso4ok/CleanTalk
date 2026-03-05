import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchPost } from "../api/posts";
import { fetchComments } from "../api/comments";
import CommentList from "../components/CommentList";
import CommentForm from "../components/CommentForm";

export default function PostDetailPage() {
  const { id } = useParams<{ id: string }>();

  const postQuery = useQuery({
    queryKey: ["post", id],
    queryFn: () => fetchPost(id!),
    enabled: !!id,
  });

  const commentsQuery = useQuery({
    queryKey: ["comments", id],
    queryFn: () => fetchComments(id!),
    enabled: !!id,
  });

  if (postQuery.isLoading) {
    return <p className="text-center text-gray-500">Ładowanie posta...</p>;
  }

  if (postQuery.isError || !postQuery.data) {
    return (
      <div className="text-center">
        <p className="text-red-500">Nie udało się załadować posta.</p>
        <Link to="/" className="mt-2 text-indigo-600 hover:underline">
          ← Powrót do listy
        </Link>
      </div>
    );
  }

  const post = postQuery.data;

  return (
    <article>
      <Link
        to="/"
        className="mb-4 inline-block text-sm text-indigo-600 hover:underline"
      >
        ← Powrót do listy
      </Link>

      <h1 className="text-3xl font-bold text-gray-900">{post.title}</h1>

      <div className="mt-2 flex gap-4 text-sm text-gray-400">
        <span>Autor: {post.author_name}</span>
        <time>{new Date(post.created_at).toLocaleDateString("pl-PL")}</time>
      </div>

      <div className="prose mt-6 max-w-none whitespace-pre-wrap text-gray-700">
        {post.body}
      </div>

      <hr className="my-8" />

      <section>
        <h2 className="mb-4 text-xl font-semibold">Komentarze</h2>
        {commentsQuery.isLoading ? (
          <p className="text-sm text-gray-400">Ładowanie komentarzy...</p>
        ) : (
          <CommentList comments={commentsQuery.data ?? []} />
        )}
        <CommentForm postId={id!} />
      </section>
    </article>
  );
}
