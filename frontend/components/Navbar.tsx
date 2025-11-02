"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "../lib/store";
import toast from "react-hot-toast";

export default function Navbar() {
  const router = useRouter();
  const clear = useAuth((s) => s.clear);

  const onLogout = () => {
    clear();
    toast.success("Signed out");
    router.replace("/");
  };

  return (
    <header className="h-14 border-b bg-white flex items-center justify-between px-4">
      <div className="font-semibold">RevalytIQ</div>
      <div className="flex items-center gap-3">
        <Link href="/profile" className="text-sm px-3 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200">
          Profile
        </Link>
        <button
          onClick={onLogout}
          className="text-sm px-3 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200"
        >
          Logout
        </button>
      </div>
    </header>
  );
}
