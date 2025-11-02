import { create } from "zustand";

type AuthState = {
  access: string | null;
  refresh: string | null;
  setTokens: (t: { access: string; refresh: string }) => void;
  clear: () => void;
};

export const useAuth = create<AuthState>((set) => ({
  access: null,
  refresh: null,
  setTokens: ({ access, refresh }) => {
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    set({ access, refresh });
  },
  clear: () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    set({ access: null, refresh: null });
  }
}));

export const hydrateAuthFromStorage = () => {
  if (typeof window === "undefined") return;
  const access = localStorage.getItem("access");
  const refresh = localStorage.getItem("refresh");
  if (access && refresh) useAuth.setState({ access, refresh });
};
