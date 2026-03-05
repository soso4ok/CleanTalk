import { postApi } from "./client";
import type { Post, PostListResponse } from "../types";

export async function fetchPosts(
  page = 1,
  size = 10,
): Promise<PostListResponse> {
  const { data } = await postApi.get<PostListResponse>("", {
    params: { page, size },
  });
  return data;
}

export async function fetchPost(id: string): Promise<Post> {
  const { data } = await postApi.get<Post>(`/${id}`);
  return data;
}

export async function createPost(
  title: string,
  body: string,
): Promise<Post> {
  const { data } = await postApi.post<Post>("", { title, body });
  return data;
}

export async function updatePost(
  id: string,
  title: string,
  body: string,
): Promise<Post> {
  const { data } = await postApi.put<Post>(`/${id}`, { title, body });
  return data;
}

export async function deletePost(id: string): Promise<void> {
  await postApi.delete(`/${id}`);
}
