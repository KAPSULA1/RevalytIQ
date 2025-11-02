import axios from "axios";

// axios instance
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000",
  headers: { "Content-Type": "application/json" },
});

// 🔑 Login (JWT Token)
export async function login(username: string, password: string) {
  const { data } = await api.post("/api/auth/token/", { username, password });
  return data as { access: string; refresh: string };
}

// 🧾 Register (optional, for signup)
export async function register(username: string, email: string, password: string) {
  const { data } = await api.post("/api/auth/register/", {
    username,
    email,
    password,
  });
  return data;
}

// 📊 KPI & Orders Fetching for Dashboard
export async function fetchKPIs() {
  const token = localStorage.getItem("access");
  const { data } = await api.get("/api/analytics/kpis/", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return data;
}

export interface Order {
  id: number;
  customer: string;
  amount: number | string;
  status: string;
  created_at: string;
}

export async function fetchOrders() {
  const token = localStorage.getItem("access");
  const { data } = await api.get("/api/analytics/orders/", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return data;
}
