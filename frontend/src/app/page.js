"use client";
import { useEffect, useState } from "react";
import ServerList from "../components/ServerList";
import Link from "next/link";

export default function HomePage() {
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // دریافت لیست سرورها
  const fetchServers = () => {
    setLoading(true);
    setError(null);
    fetch("http://localhost:8000/api/servers")
      .then((res) => {
        if (!res.ok) throw new Error("دریافت اطلاعات با خطا مواجه شد");
        return res.json();
      })
      .then((data) => {
        setServers(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "خطا در دریافت داده");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchServers();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-2xl mx-auto pt-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-center">داشبورد مانیتورینگ سرور</h1>
          <Link
            href="/add-server"
            className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 transition"
          >
            افزودن سرور جدید
          </Link>
        </div>
        {loading && <div className="mb-8 text-center">در حال دریافت اطلاعات...</div>}
        {error && <div className="mb-8 text-center text-red-600">{error}</div>}
        {!loading && !error && <ServerList servers={servers} />}
      </div>
    </div>
  );
}