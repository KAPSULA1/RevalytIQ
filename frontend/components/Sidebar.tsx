// components/Sidebar.tsx
import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-60 border-r bg-white p-4 space-y-2">
      <Link className="block px-2 py-2 rounded hover:bg-gray-100" href="/dashboard">Dashboard</Link>
    </aside>
  );
}

