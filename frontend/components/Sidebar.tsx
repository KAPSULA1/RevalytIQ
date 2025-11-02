// components/Sidebar.tsx
import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/profile", label: "Profile" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-60 border-r bg-white p-4 space-y-2">
      {links.map((link) => {
        const active = pathname?.startsWith(link.href);
        return (
          <Link
            key={link.href}
            href={link.href}
            className={`block px-3 py-2 rounded-lg transition ${
              active ? "bg-blue-50 text-blue-700" : "hover:bg-gray-100"
            }`}
          >
            {link.label}
          </Link>
        );
      })}
    </aside>
  );
}
