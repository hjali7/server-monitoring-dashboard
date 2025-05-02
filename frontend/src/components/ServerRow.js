export default function ServerRow({ server }) {
    return (
      <tr className="border-b">
        <td className="py-2">{server.name}</td>
        <td className="py-2">{server.ip}</td>
        <td className="py-2">
          {server.status === "online" ? (
            <span className="text-green-600 font-semibold">Online</span>
          ) : (
            <span className="text-red-600 font-semibold">Offline</span>
          )}
        </td>
      </tr>
    );
  }