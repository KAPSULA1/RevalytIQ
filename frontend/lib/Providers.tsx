"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactNode, useEffect, useState } from "react";
import { me } from "./auth";
import { useAuth } from "./store";

export default function Providers({ children }: { children: ReactNode }) {
  const [client] = useState(() => new QueryClient());
  const setUser = useAuth((s) => s.setUser);
  const setInitialized = useAuth((s) => s.setInitialized);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const current = await me();
        if (!cancelled) setUser(current);
      } catch {
        if (!cancelled) setUser(null);
      } finally {
        if (!cancelled) setInitialized(true);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [setInitialized, setUser]);

  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}
