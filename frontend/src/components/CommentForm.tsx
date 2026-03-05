import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { submitComment } from "../api/comments";
import { useAuth } from "../context/AuthContext";

interface Props {
  postId: string;
}

export default function CommentForm({ postId }: Props) {
  const { user } = useAuth();
  const [body, setBody] = useState("");
  const [feedback, setFeedback] = useState<{
    type: "ok" | "hide" | "error";
    message: string;
  } | null>(null);
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: () => submitComment(postId, body),
    onSuccess: (result) => {
      setBody("");
      if (result.verdict === "ok") {
        setFeedback({
          type: "ok",
          message: "Komentarz został dodany!",
        });
        queryClient.invalidateQueries({ queryKey: ["comments", postId] });
      } else if (result.verdict === "hide") {
        setFeedback({
          type: "hide",
          message:
            "Twój komentarz został przesłany, ale wymaga przeglądu moderatora.",
        });
      }
    },
    onError: (err: unknown) => {
      const message =
        err instanceof Error ? err.message : "Komentarz odrzucony jako spam.";
      setFeedback({ type: "error", message });
    },
  });

  if (!user) {
    return (
      <p className="text-sm text-gray-500">
        <a href="/login" className="text-indigo-600 hover:underline">
          Zaloguj się
        </a>
        , aby dodać komentarz.
      </p>
    );
  }

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (body.trim()) mutation.mutate();
      }}
      className="mt-4 space-y-3"
    >
      <textarea
        value={body}
        onChange={(e) => setBody(e.target.value)}
        rows={3}
        className="w-full rounded border px-3 py-2 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        placeholder="Napisz komentarz..."
      />
      <div className="flex items-center gap-4">
        <button
          type="submit"
          disabled={mutation.isPending || !body.trim()}
          className="rounded bg-indigo-600 px-4 py-2 text-sm text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {mutation.isPending ? "Wysyłanie..." : "Dodaj komentarz"}
        </button>
        {feedback && (
          <span
            className={`text-sm ${
              feedback.type === "ok"
                ? "text-green-600"
                : feedback.type === "hide"
                  ? "text-yellow-600"
                  : "text-red-600"
            }`}
          >
            {feedback.message}
          </span>
        )}
      </div>
    </form>
  );
}
