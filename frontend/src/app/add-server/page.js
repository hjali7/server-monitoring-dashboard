"use client";
import AddServerForm from "../../components/AddServerForm";
import Link from "next/link";

export default function AddServerPage() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center pt-8 px-4">
      <div className="w-full max-w-md">
        <div className="mb-6 flex justify-between items-center">
          <h1 className="text-2xl font-bold">افزودن سرور جدید</h1>
          <Link
            href="/"
            className="text-blue-700 hover:underline bg-white px-3 py-1 rounded shadow"
          >
            بازگشت به داشبورد
          </Link>
        </div>
        <AddServerForm />
      </div>
    </div>
  );
}