import axios from "axios";
import { useAuth } from "./store";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
});

api.interceptors.request.use((config) => {
  const token = useAuth.getState().access;
  if (token) {
    config.headers = config.headers ?? {};
    (config.headers as any)["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

let isRefreshing = false;
api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      if (isRefreshing) throw error;
      original._retry = true;
      isRefreshing = true;
      try {
        const refresh = useAuth.getState().refresh;
        if (!refresh) throw error;
        const res = await axios.post(
          `${api.defaults.baseURL}/api/auth/token/refresh/`,
          { refresh }
        );
        const access = res.data?.access;
        if (!access) throw error;
        useAuth.getState().setTokens({ access, refresh });
        original.headers["Authorization"] = `Bearer ${access}`;
        return api(original);
      } finally {
        isRefreshing = false;
      }
    }
    throw error;
  }
);
