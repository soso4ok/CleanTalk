import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createPost } from "../api/posts";
import { useAuth } from "../context/AuthContext";

export default function CreatePostForm() {
  const { user } = useAuth();
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [open, setOpen] = useState(false);
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: () => createPost(title, body),
    onSuccess: () => {
      setTitle("");
      setBody("");
      setOpen(false);
      queryClient.invalidateQueries({ queryKey: ["posts"] });
    },
  });

  if (!user) return null;

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="mb-6 rounded bg-indigo-600 px-4 py-2 text-sm text-white hover:bg-indigo-700"
      >
        + Nowy post
      </button>
    );
  }

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (title.trim() && body.trim()) mutation.mutate();
      }}
      className="mb-6 space-y-3 rounded-lg border bg-white p-6 shadow-sm"
    >
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Tytuł posta"
        className="w-full rounded border px-3 py-2 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
      />
      <textarea
        value={body}
        onChange={(e) => setBody(e.target.value)}
        rows={5}
        placeholder="Treść posta..."
        className="w-full rounded border px-3 py-2 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
      />
      <div className="flex gap-2">
        <button
          type="submit"
          disabled={mutation.isPending}
          className="rounded bg-indigo-600 px-4 py-2 text-sm text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {mutation.isPending ? "Publikowanie..." : "Opublikuj"}
        </button>
        <button
          type="button"
          onClick={() => setOpen(false)}
          className="rounded bg-gray-200 px-4 py-2 text-sm hover:bg-gray-300"
        >
          Anuluj
        </button>
      </div>
      {mutation.isError && (
        <p className="text-sm text-red-600">
          Nie udało się opublikować posta. Spróbuj ponownie.
        </p>
      )}
    </form>
  );
}
