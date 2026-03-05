import axios from "axios";

const authApi = axios.create({ baseURL: "/api/auth" });
const postApi = axios.create({ baseURL: "/api/posts" });
const commentApi = axios.create({ baseURL: "/api/comments" });

function authHeader(): Record<string, string> {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Interceptor to add auth header automatically
for (const client of [postApi, commentApi]) {
  client.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });
}

export { authApi, postApi, commentApi, authHeader };
