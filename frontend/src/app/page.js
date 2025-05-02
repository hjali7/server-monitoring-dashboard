"use client";
import { useState } from "react";
import ServerList from "../components/ServerList";

// داده تستی اولیه 
const mockServers = [
  { id: 1, name: "Server A", ip: "192.168.1.1", status: "online" },
  { id: 2, name: "Server B", ip: "192.168.1.2", status: "offline" },
  { id: 3, name: "Server C", ip: "10.0.0.1", status: "online" },
];

export default function HomePage() {
  const [servers, setServers] = useState(mockServers);

  // برای اتصال به بک‌اند بعداً این بخش را کامل می‌کنیم
  // useEffect(() => {
  //   fetch('/api/servers')
  //     .then(res => res.json())
  //     .then(setServers);
  // }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-2xl mx-auto pt-8">
        <ServerList servers={servers} />
      </div>
    </div>
  );
}