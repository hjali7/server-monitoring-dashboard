"use client";	
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();
  return (
    <nav className="bg-blue-700 text-white px-6 py-3 flex gap-8 items-center">
      <Link
        href="/"
        className={`font-bold transition ${pathname === "/" ? "underline" : ""}`}
      >
        داشبورد سرورها
      </Link>
      <Link
        href="/add-server"
        className={`font-bold transition ${pathname === "/add-server" ? "underline" : ""}`}
      >
        افزودن سرور جدید
      </Link>
    </nav>
  );
}