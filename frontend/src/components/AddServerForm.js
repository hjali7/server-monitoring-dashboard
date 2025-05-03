import { useState } from "react";

// تابع بررسی IP معتبر (همه بخش‌ها عدد و بین ۰ تا ۲۵۵)
function isValidIp(ip) {
  const parts = ip.trim().split(".");
  if (parts.length !== 4) return false;
  for (let part of parts) {
    if (!/^\d+$/.test(part)) return false;
    const n = Number(part);
    if (n < 0 || n > 255) return false;
  }
  return true;
}

export default function AddServerForm({ onAdd }) {
  const [name, setName] = useState("");
  const [ip, setIp] = useState("");
  const [status, setStatus] = useState("online");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (!name.trim() || !ip.trim()) {
      setError("نام و IP را وارد کنید.");
      return;
    }
    if (!isValidIp(ip)) {
      setError("فرمت IP معتبر نیست (مثال: 192.168.1.1).");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/servers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, ip, status }),
      });
      if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg || "خطا در افزودن سرور");
      }
      const data = await res.json();
      if (onAdd) onAdd(data);
      setSuccess("سرور با موفقیت افزوده شد!");
      setName("");
      setIp("");
      setStatus("online");
    } catch (err) {
      setError(err.message || "خطا در افزودن سرور");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-xl shadow p-6 flex flex-col gap-4 w-full max-w-md"
    >
      <h2 className="text-xl font-bold mb-2">افزودن سرور جدید</h2>
      {error && <p className="text-red-600">{error}</p>}
      {success && <p className="text-green-600">{success}</p>}
      <div>
        <label className="block mb-1">نام سرور:</label>
        <input
          className="border rounded px-3 py-1 w-full"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={loading}
          required
        />
      </div>
      <div>
        <label className="block mb-1">IP:</label>
        <input
          className="border rounded px-3 py-1 w-full"
          value={ip}
          onChange={(e) => setIp(e.target.value)}
          disabled={loading}
          required
          placeholder="192.168.1.1"
        />
      </div>
      <div>
        <label className="block mb-1">وضعیت:</label>
        <select
          className="border rounded px-3 py-1 w-full"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          disabled={loading}
        >
          <option value="online">Online</option>
          <option value="offline">Offline</option>
        </select>
      </div>
      <button
        type="submit"
        className="bg-blue-600 text-white rounded py-2 mt-2"
        disabled={loading}
      >
        {loading ? "در حال افزودن..." : "افزودن سرور"}
      </button>
    </form>
  );
}