import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchPosts } from "../api/posts";
import PostCard from "../components/PostCard";
import CreatePostForm from "../components/CreatePostForm";

export default function PostListPage() {
  const [page, setPage] = useState(1);
  const size = 10;

  const { data, isLoading, isError } = useQuery({
    queryKey: ["posts", page],
    queryFn: () => fetchPosts(page, size),
  });

  if (isLoading) {
    return <p className="text-center text-gray-500">Ładowanie postów...</p>;
  }

  if (isError) {
    return (
      <p className="text-center text-red-500">
        Nie udało się załadować postów.
      </p>
    );
  }

  const totalPages = Math.ceil((data?.total ?? 0) / size);

  return (
    <>
      <CreatePostForm />

      {data && data.items.length === 0 ? (
        <p className="text-center text-gray-400">
          Brak postów. Bądź pierwszym autorem!
        </p>
      ) : (
        <div className="space-y-4">
          {data?.items.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      )}

      {totalPages > 1 && (
        <div className="mt-8 flex justify-center gap-2">
          <button
            disabled={page <= 1}
            onClick={() => setPage((p) => p - 1)}
            className="rounded border px-3 py-1 text-sm disabled:opacity-40"
          >
            ← Poprzednia
          </button>
          <span className="px-3 py-1 text-sm text-gray-600">
            {page} / {totalPages}
          </span>
          <button
            disabled={page >= totalPages}
            onClick={() => setPage((p) => p + 1)}
            className="rounded border px-3 py-1 text-sm disabled:opacity-40"
          >
            Następna →
          </button>
        </div>
      )}
    </>
  );
}
