"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { api } from "@/lib/api";
import { Role } from "@/lib/types";

export default function LoginPage() {
  const router = useRouter();
  const [role, setRole] = useState<Role>("admin");
  const [mode, setMode] = useState<"login" | "register">("login");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    try {
      setError("");
      setMessage("");
      if (mode === "register") {
        await api.registerTeacher({ full_name: fullName, email, password });
        setMode("login");
        setRole("teacher");
        setPassword("");
        setMessage("Ro'yxatdan o'tish yakunlandi. Endi login va parol bilan kiring.");
        return;
      }
      const result = await api.login(email, password, role);
      localStorage.setItem("token", result.access_token);
      localStorage.setItem("user", JSON.stringify(result.user));
      router.push(`/dashboard/${result.user.role}`);
    } catch {
      setError(mode === "login" ? "Kirish amalga oshmadi. Login yoki parolni tekshiring." : "Ro'yxatdan o'tish amalga oshmadi. Ma'lumotlarni tekshiring.");
    }
  }

  function chooseRole(nextRole: Role) {
    setRole(nextRole);
  }

  return (
    <main className="grid min-h-screen place-items-center bg-gradient-to-br from-forest-800 via-forest-700 to-emerald-500 p-4">
      <form onSubmit={submit} className="w-full max-w-md rounded-3xl bg-white p-6 shadow-soft md:p-8">
        <p className="text-sm font-medium text-forest-600">Xush kelibsiz</p>
        <h1 className="mt-2 text-3xl font-semibold">{mode === "login" ? "Tizimga kirish" : "Ro'yxatdan o'tish"}</h1>
        {mode === "login" && (
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
        )}
        {mode === "register" && (
          <label className="mt-6 block text-sm">
            F.I.Sh.
            <input value={fullName} onChange={(e) => setFullName(e.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3" />
          </label>
        )}
        <label className={mode === "login" ? "mt-6 block text-sm" : "mt-4 block text-sm"}>
          Email
          <input value={email} onChange={(e) => setEmail(e.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3" />
        </label>
        <label className="mt-4 block text-sm">
          Parol
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3" />
        </label>
        {error && <p className="mt-4 text-sm text-rose-600">{error}</p>}
        {message && <p className="mt-4 text-sm text-forest-700">{message}</p>}
        <button className="mt-6 w-full rounded-2xl bg-forest-700 px-4 py-3 font-semibold text-white hover:bg-forest-800">
          {mode === "login" ? "Kirish" : "Ro'yxatdan o'tish"}
        </button>
        <button
          type="button"
          onClick={() => {
            setError("");
            setMessage("");
            setMode(mode === "login" ? "register" : "login");
            if (mode === "login") setRole("teacher");
          }}
          className="mt-3 w-full rounded-2xl border border-slate-200 px-4 py-3 font-medium text-forest-700"
        >
          {mode === "login" ? "O'qituvchi sifatida ro'yxatdan o'tish" : "Login oynasiga qaytish"}
        </button>
        {mode === "login" && (
          <div className="mt-6 rounded-2xl bg-emerald-50 p-4 text-sm text-slate-600">
            <p className="font-semibold text-forest-700">Kirish ma'lumotlari</p>
            <p>Admin: admin@example.com / admin123</p>
            <p>O'qituvchi: teacher@example.com / teacher123</p>
          </div>
        )}
      </form>
    </main>
  );
}
