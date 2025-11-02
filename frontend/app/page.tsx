"use client";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { isAxiosError } from "axios";
import { login } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!username.trim() || !password.trim()) {
      setError("Please enter both username and password.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const data = await login(username.trim(), password.trim());

      // ✅ შეინახე ტოკენები
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);

      // ✅ გადადი dashboard-ზე
      router.push("/dashboard");
    } catch (err) {
      if (isAxiosError(err)) {
        if (err.response?.status === 401) {
          setError("Invalid username or password.");
        } else {
          setError("Login failed. Try again later.");
        }
      } else {
        setError("Unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-lg rounded-2xl p-6 w-96 flex flex-col gap-4"
      >
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
      </form>
    </div>
  );
}
