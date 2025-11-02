"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { forgotPassword } from "@/lib/auth";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState("");
  const [token, setToken] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMsg("");
    setLoading(true);
    try {
      const res = await forgotPassword(email.trim());
      setMsg(res.detail);
      setToken(res.token);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={onSubmit} className="bg-white shadow-lg rounded-2xl p-6 w-96 flex flex-col gap-4">
        <h2 className="text-2xl font-semibold text-center">Forgot password</h2>
        <input type="email" placeholder="Email" value={email}
          onChange={(e) => setEmail(e.target.value)} className="border p-2 rounded-lg" />
        <button disabled={loading} className="bg-blue-600 text-white py-2 rounded-lg">
          {loading ? "Sending..." : "Send reset link"}
        </button>
        {msg && <p className="text-sm text-center text-gray-700">{msg}</p>}
        {token && (
          <p className="text-xs text-center text-gray-500">
            Demo token: <span className="font-mono">{token}</span>
          </p>
        )}
        <div className="text-sm text-center text-gray-600 flex items-center justify-center gap-3">
          <Link href="/" className="hover:underline text-blue-600">
            Remembered your password? Sign in
          </Link>
          <span>·</span>
          <Link href="/signup" className="hover:underline text-blue-600">
            Need an account?
          </Link>
        </div>
      </form>
    </div>
  );
}
