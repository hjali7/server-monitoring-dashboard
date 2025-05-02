import ServerRow from "./ServerRow";

export default function ServerList({ servers }) {
  return (
    <div className="bg-white rounded-xl shadow p-6 mt-8">
      <h2 className="text-2xl font-bold mb-4">وضعیت سرورها</h2>
      <table className="w-full text-right">
        <thead>
          <tr className="border-b">
            <th className="py-2 font-semibold">نام</th>
            <th className="py-2 font-semibold">IP</th>
            <th className="py-2 font-semibold">وضعیت</th>
          </tr>
        </thead>
        <tbody>
          {servers.map((server) => (
            <ServerRow key={server.id} server={server} />
          ))}
        </tbody>
      </table>
    </div>
  );
}