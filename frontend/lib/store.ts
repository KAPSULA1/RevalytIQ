import { create } from "zustand";
import type { CurrentUser } from "./auth";

type AuthState = {
  user: CurrentUser | null;
  initialized: boolean;
  setUser: (user: CurrentUser | null) => void;
  setInitialized: (value: boolean) => void;
  clear: () => void;
};

export const useAuth = create<AuthState>((set) => ({
  user: null,
  initialized: false,
  setUser: (user) => set({ user }),
  setInitialized: (value) => set({ initialized: value }),
  clear: () => set({ user: null, initialized: true }),
}));
