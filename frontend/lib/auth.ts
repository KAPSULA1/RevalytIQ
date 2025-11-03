import { api } from "./api";

export async function login(username: string, password: string) {
  const { data } = await api.post<{ detail: string }>("/api/auth/token/", { username, password });
  return data;
}

export interface RegisterResponse {
  id: number;
  username: string;
  email: string;
}

export async function register(
  username: string,
  email: string,
  password: string,
  password2: string,
) {
  const { data } = await api.post<RegisterResponse>("/api/auth/register/", {
    username,
    email,
    password,
    password2,
  });
  return data;
}

export interface ForgotPasswordResponse {
  detail: string;
  token?: string;
}

export async function forgotPassword(email: string) {
  const { data } = await api.post<ForgotPasswordResponse>("/api/auth/password/forgot/", { email });
  return data;
}

export interface ResetPasswordPayload {
  email: string;
  token: string;
  new_password: string;
  new_password2: string;
}

export async function resetPassword(payload: ResetPasswordPayload) {
  const { data } = await api.post<{ detail: string }>("/api/auth/password/reset/", payload);
  return data;
}

export interface CurrentUser {
  id: number;
  username: string;
  email: string;
}

export async function me() {
  const { data } = await api.get<CurrentUser>("/api/auth/me/");
  return data;
}

export interface ProfileUpdatePayload {
  username?: string;
  email?: string;
}

export async function updateProfile(payload: ProfileUpdatePayload) {
  const { data } = await api.patch<CurrentUser>("/api/auth/profile/", payload);
  return data;
}

export async function logout() {
  await api.post("/api/auth/logout/");
}

export interface Order {
  id: number;
  customer: string;
  amount: number | string;
  status: string;
  created_at: string;
}

export async function fetchOrders() {
  const { data } = await api.get<Order[] | { results: Order[] }>("/api/analytics/orders/");
  return data;
}

export interface KPIResponse {
  revenue: number;
  orders: number;
  aov: number;
}

export async function fetchKPIs() {
  const { data } = await api.get<KPIResponse>("/api/analytics/kpis/");
  return data;
}
