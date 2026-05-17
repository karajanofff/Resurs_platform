"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { api } from "@/lib/api";
import { Role } from "@/lib/types";

const demos = {
  admin: ["admin@example.com", "admin123"],
  teacher: ["teacher@example.com", "teacher123"],
};

export default function LoginPage() {
  const router = useRouter();
  const [role, setRole] = useState<Role>("admin");
  const [email, setEmail] = useState(demos.admin[0]);
  const [password, setPassword] = useState(demos.admin[1]);
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    try {
      const result = await api.login(email, password, role);
      localStorage.setItem("token", result.access_token);
      localStorage.setItem("user", JSON.stringify(result.user));
      router.push(`/dashboard/${result.user.role}`);
    } catch {
      setError("Kirish amalga oshmadi. Login ma'lumotlari yoki server ulanishini tekshiring.");
    }
  }

  function chooseRole(nextRole: Role) {
    setRole(nextRole);
    setEmail(demos[nextRole][0]);
    setPassword(demos[nextRole][1]);
  }

  return (
    <main className="grid min-h-screen place-items-center bg-gradient-to-br from-forest-800 via-forest-700 to-emerald-500 p-4">
      <form onSubmit={submit} className="w-full max-w-md rounded-3xl bg-white p-6 shadow-soft md:p-8">
        <p className="text-sm font-medium text-forest-600">Xush kelibsiz</p>
        <h1 className="mt-2 text-3xl font-semibold">Tizimga kirish</h1>
        <div className="mt-6 grid grid-cols-2 rounded-2xl bg-emerald-50 p-1">
          {(["admin", "teacher"] as Role[]).map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => chooseRole(item)}
              className={`rounded-2xl px-3 py-2 text-sm capitalize ${role === item ? "bg-white font-semibold text-forest-700 shadow" : "text-slate-500"}`}
            >
              {item === "admin" ? "Admin" : "O'qituvchi"}
            </button>
          ))}
        </div>
        <label className="mt-6 block text-sm">
          Email
          <input value={email} onChange={(e) => setEmail(e.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3" />
        </label>
        <label className="mt-4 block text-sm">
          Parol
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3" />
        </label>
        {error && <p className="mt-4 text-sm text-rose-600">{error}</p>}
        <button className="mt-6 w-full rounded-2xl bg-forest-700 px-4 py-3 font-semibold text-white hover:bg-forest-800">Kirish</button>
        <div className="mt-6 rounded-2xl bg-emerald-50 p-4 text-sm text-slate-600">
          <p className="font-semibold text-forest-700">Demo loginlar</p>
          <p>Admin: admin@example.com / admin123</p>
          <p>O'qituvchi: teacher@example.com / teacher123</p>
        </div>
      </form>
    </main>
  );
}
