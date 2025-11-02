"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useSearchParams } from "next/navigation";
import { resetPassword } from "@/lib/auth";

export default function ResetPasswordPage() {
  const params = useSearchParams();
  const [email, setEmail] = useState(params.get("email") ?? "");
  const [token, setToken] = useState(params.get("token") ?? "");
  const [p1, setP1] = useState("");
  const [p2, setP2] = useState("");
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMsg("");
    if (!email || !token || !p1 || !p2) {
      setMsg("Please fill all fields.");
      return;
    }
    setLoading(true);
    try {
      const res = await resetPassword({
        email,
        token,
        new_password: p1,
        new_password2: p2,
      });
      setMsg(res.detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={onSubmit} className="bg-white shadow-lg rounded-2xl p-6 w-96 flex flex-col gap-4">
        <h2 className="text-2xl font-semibold text-center">Reset password</h2>
        <input type="email" placeholder="Email" value={email}
          onChange={(e) => setEmail(e.target.value)} className="border p-2 rounded-lg" />
        <input type="text" placeholder="Token" value={token}
          onChange={(e) => setToken(e.target.value)} className="border p-2 rounded-lg" />
        <input type="password" placeholder="New password" value={p1}
          onChange={(e) => setP1(e.target.value)} className="border p-2 rounded-lg" />
        <input type="password" placeholder="Confirm password" value={p2}
          onChange={(e) => setP2(e.target.value)} className="border p-2 rounded-lg" />
        <button disabled={loading} className="bg-blue-600 text-white py-2 rounded-lg">
          {loading ? "Resetting..." : "Reset password"}
        </button>
        {msg && <p className="text-sm text-center text-gray-700">{msg}</p>}
        <div className="text-sm text-center text-gray-600 flex items-center justify-center gap-3">
          <Link href="/" className="hover:underline text-blue-600">
            Back to login
          </Link>
          <span>·</span>
          <Link href="/forgot-password" className="hover:underline text-blue-600">
            Need a new token?
          </Link>
        </div>
      </form>
    </div>
  );
}
