"use client";
import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isAxiosError } from "axios";
import { login, me } from "@/lib/auth";
import { useAuth } from "@/lib/store";
import toast from "react-hot-toast";

export default function LoginPage() {
  const router = useRouter();
  const user = useAuth((s) => s.user);
  const setUser = useAuth((s) => s.setUser);
  const setInitialized = useAuth((s) => s.setInitialized);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) router.replace("/dashboard");
  }, [user, router]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError("Please enter both username and password.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      await login(username.trim(), password.trim());
      const currentUser = await me();
      setUser(currentUser);
      setInitialized(true);
      toast.success("Welcome back!");
      router.push("/dashboard");
    } catch (err) {
      if (isAxiosError(err)) {
        setError(err.response?.status === 401 ? "Invalid credentials." : "Login failed.");
      } else {
        setError("Unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white shadow-lg rounded-2xl p-6 w-96 flex flex-col gap-4">
        <h2 className="text-2xl font-semibold text-center">RevalytIQ Login</h2>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border p-2 rounded-lg"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 rounded-lg"
        />

        {error && <p className="text-red-500 text-sm text-center">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-70"
        >
          {loading ? "Signing in..." : "Sign In"}
        </button>

        <div className="text-sm text-center text-gray-600 flex items-center justify-center gap-3">
          <Link href="/signup" className="hover:underline">Create account</Link>
          <span>·</span>
          <Link href="/forgot-password" className="hover:underline">Forgot password?</Link>
        </div>
      </form>
    </div>
  );
}
