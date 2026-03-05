export interface User {
  id: string;
  username: string;
  email: string;
  created_at: string;
}

export interface Post {
  id: string;
  title: string;
  body: string;
  author_id: string;
  author_name: string;
  created_at: string;
  updated_at: string;
}

export interface PostListResponse {
  items: Post[];
  total: number;
  page: number;
  size: number;
}

export interface Comment {
  id: string;
  post_id: string;
  author_id: string;
  author_name: string;
  body: string;
  status: string;
  created_at: string;
}

export interface ModerationResult {
  comment_id: string;
  verdict: string;
  body: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}
