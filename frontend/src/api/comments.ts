import { commentApi } from "./client";
import type { Comment, ModerationResult } from "../types";

export async function fetchComments(postId: string): Promise<Comment[]> {
  const { data } = await commentApi.get<Comment[]>("", {
    params: { post_id: postId },
  });
  return data;
}

export async function submitComment(
  postId: string,
  body: string,
): Promise<ModerationResult> {
  const { data } = await commentApi.post<ModerationResult>("", {
    post_id: postId,
    body,
  });
  return data;
}

export async function deleteComment(commentId: string): Promise<void> {
  await commentApi.delete(`/${commentId}`);
}
