"use client";

import { FormEvent, useEffect, useState } from "react";
import { logout, updateProfile } from "@/lib/auth";
import { useAuth } from "@/lib/store";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

export default function ProfilePage() {
  const router = useRouter();
  const user = useAuth((s) => s.user);
  const initialized = useAuth((s) => s.initialized);
  const clear = useAuth((s) => s.clear);
  const setUser = useAuth((s) => s.setUser);

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!initialized) return;
    if (!user) {
      router.replace("/");
      return;
    }
    setUsername(user.username);
    setEmail(user.email ?? "");
    setLoading(false);
  }, [initialized, user, router]);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const updated = await updateProfile({ username, email });
      setUser(updated);
      toast.success("Profile updated");
    } catch (e) {
      toast.error("Update failed");
    } finally {
      setSaving(false);
    }
  };

  const onLogout = async () => {
    try {
      await logout();
    } catch {
      // ignore errors during logout
    } finally {
      clear();
      router.replace("/");
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading…</div>;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={onSubmit} className="bg-white shadow-lg rounded-2xl p-6 w-96 flex flex-col gap-4">
        <h2 className="text-2xl font-semibold text-center">Profile</h2>
        <input className="border p-2 rounded-lg" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input className="border p-2 rounded-lg" value={email} onChange={(e) => setEmail(e.target.value)} />
        <button disabled={saving} className="bg-blue-600 text-white py-2 rounded-lg">
          {saving ? "Saving..." : "Save"}
        </button>
        <button type="button" onClick={onLogout} className="mt-1 bg-gray-100 py-2 rounded-lg">
          Logout
        </button>
      </form>
    </div>
  );
}
