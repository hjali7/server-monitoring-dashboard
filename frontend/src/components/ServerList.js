import { useEffect, useState } from "react";

export default function ServerList() {
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editId, setEditId] = useState(null);
  const [editData, setEditData] = useState({ name: "", ip: "", status: "online" });

  // دریافت لیست سرورها
  const fetchServers = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/api/servers");
      if (!res.ok) throw new Error("خطا در دریافت سرورها");
      const data = await res.json();
      setServers(data);
    } catch (err) {
      setError(err.message || "خطا در دریافت داده");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchServers();
  }, []);

  // حذف سرور
  const handleDelete = async (id) => {
    if (!window.confirm("آیا مطمئن هستید؟")) return;
    await fetch(`http://localhost:8000/api/servers/${id}`, { method: "DELETE" });
    fetchServers();
  };

  // شروع ویرایش
  const handleEditStart = (server) => {
    setEditId(server.id ?? server._id); // استفاده از id یا _id
    setEditData({ name: server.name, ip: server.ip, status: server.status });
  };

  // لغو ویرایش
  const handleEditCancel = () => {
    setEditId(null);
    setEditData({ name: "", ip: "", status: "online" });
  };

  // ثبت ویرایش
  const handleEditSave = async () => {
    await fetch(`http://localhost:8000/api/servers/${editId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(editData),
    });
    setEditId(null);
    setEditData({ name: "", ip: "", status: "online" });
    fetchServers();
  };

  // هندل تغییرات فرم ویرایش
  const handleEditChange = (e) => {
    setEditData({ ...editData, [e.target.name]: e.target.value });
  };

  if (loading) return <div>در حال دریافت...</div>;
  if (error) return <div className="text-red-600">{error}</div>;

  return (
    <div className="mt-8">
      <table className="w-full border bg-white">
        <thead>
          <tr>
            <th>نام</th>
            <th>IP</th>
            <th>وضعیت</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          {servers.map((s) => {
            const rowId = s.id ?? s._id; // کلید یکتا (id یا _id)
            if (editId === rowId) {
              // حالت ویرایش
              return (
                <tr key={rowId}>
                  <td>
                    <input
                      type="text"
                      name="name"
                      value={editData.name}
                      onChange={handleEditChange}
                      className="border rounded px-2 py-1"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      name="ip"
                      value={editData.ip}
                      onChange={handleEditChange}
                      className="border rounded px-2 py-1"
                    />
                  </td>
                  <td>
                    <select
                      name="status"
                      value={editData.status}
                      onChange={handleEditChange}
                      className="border rounded px-2 py-1"
                    >
                      <option value="online">Online</option>
                      <option value="offline">Offline</option>
                    </select>
                  </td>
                  <td>
                    <button
                      className="bg-green-600 text-white rounded px-2 py-1 ml-1"
                      onClick={handleEditSave}
                    >
                      ذخیره
                    </button>
                    <button
                      className="bg-gray-400 text-white rounded px-2 py-1"
                      onClick={handleEditCancel}
                    >
                      لغو
                    </button>
                  </td>
                </tr>
              );
            }
            // حالت نمایش معمولی
            return (
              <tr key={rowId}>
                <td>{s.name}</td>
                <td>{s.ip}</td>
                <td>{s.status}</td>
                <td>
                  <button
                    className="bg-blue-600 text-white rounded px-2 py-1 ml-1"
                    onClick={() => handleEditStart(s)}
                  >
                    ویرایش
                  </button>
                  <button
                    className="bg-red-600 text-white rounded px-2 py-1"
                    onClick={() => handleDelete(rowId)}
                  >
                    حذف
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}