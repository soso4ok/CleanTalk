import { authApi, authHeader } from "./client";
import type { Token, User } from "../types";

export async function register(
  username: string,
  email: string,
  password: string,
): Promise<User> {
  const { data } = await authApi.post<User>("/register", {
    username,
    email,
    password,
  });
  return data;
}

export async function login(
  username: string,
  password: string,
): Promise<Token> {
  const { data } = await authApi.post<Token>("/login", {
    username,
    password,
  });
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await authApi.get<User>("/me", {
    headers: authHeader(),
  });
  return data;
}
