"use client";

import {
  BarChart3,
  Bell,
  BookOpen,
  Brain,
  LayoutDashboard,
  LibraryBig,
  LogOut,
  Search,
  Settings,
  UploadCloud,
  Users,
} from "lucide-react";
import { ReactNode } from "react";
import { useRouter } from "next/navigation";
import { Role, User } from "@/lib/types";

export const menus = {
  admin: [
    { key: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { key: "subjects", label: "Fanlar", icon: BookOpen },
    { key: "users", label: "Foydalanuvchilar", icon: Users },
    { key: "resources", label: "Resurslar", icon: LibraryBig },
    { key: "analysis", label: "NLP tahlillar", icon: Brain },
    { key: "statistics", label: "Statistika", icon: BarChart3 },
    { key: "settings", label: "Sozlamalar", icon: Settings },
  ],
  teacher: [
    { key: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { key: "subjects", label: "Mening fanlarim", icon: BookOpen },
    { key: "upload", label: "Resurs yuklash", icon: UploadCloud },
    { key: "analysis", label: "Tahlil natijalari", icon: Brain },
    { key: "library", label: "Kutubxona", icon: LibraryBig },
    { key: "profile", label: "Profil", icon: Settings },
  ],
} satisfies Record<Role, { key: string; label: string; icon: typeof LayoutDashboard }[]>;

export function DashboardShell({
  role,
  user,
  activeView,
  onViewChange,
  children,
}: {
  role: Role;
  user: User;
  activeView: string;
  onViewChange: (view: string) => void;
  children: ReactNode;
}) {
  const router = useRouter();

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    router.push("/login");
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(219,244,227,0.75),_transparent_32%),#f7fbf8] lg:grid lg:grid-cols-[288px_1fr]">
      <aside className="flex min-h-screen flex-col bg-gradient-to-b from-forest-700 to-forest-800 p-5 text-white">
        <div className="mb-8 flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-2xl bg-white/15">
            <Brain className="h-6 w-6" />
          </div>
          <div>
            <p className="text-lg font-semibold">SmartKutubxona AI</p>
            <p className="text-xs text-emerald-100">Aqlli elektron kutubxona</p>
          </div>
        </div>
        <nav className="grid gap-2">
          {menus[role].map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => onViewChange(key)}
              className={`flex items-center gap-3 rounded-2xl px-4 py-3 text-left text-sm transition ${
                activeView === key ? "bg-white font-semibold text-forest-700 shadow-lg shadow-emerald-950/15" : "text-emerald-50 hover:bg-white/10"
              }`}
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
        </nav>
        <div className="mt-auto rounded-3xl border border-white/10 bg-white/10 p-4">
          <p className="text-sm font-semibold">{user.full_name}</p>
          <p className="mt-1 text-xs capitalize text-emerald-100">{role}</p>
          <button onClick={logout} className="mt-4 flex w-full items-center justify-center gap-2 rounded-2xl bg-white px-4 py-3 text-sm font-semibold text-forest-700">
            <LogOut className="h-4 w-4" />
            Chiqish
          </button>
        </div>
      </aside>
      <main>
        <header className="flex flex-col gap-4 border-b border-emerald-100/80 bg-white/80 px-5 py-4 backdrop-blur md:flex-row md:items-center md:justify-between md:px-8">
          <label className="flex min-w-0 items-center gap-3 rounded-2xl bg-emerald-50 px-4 py-3 text-sm text-slate-500 md:w-96">
            <Search className="h-4 w-4" />
            <input className="w-full bg-transparent outline-none" placeholder="Qidirish..." />
          </label>
          <div className="flex items-center gap-4">
            <button className="rounded-2xl border border-emerald-100 bg-white p-3 text-forest-700 shadow-sm">
              <Bell className="h-4 w-4" />
            </button>
            <div>
              <p className="text-sm font-semibold">{user.full_name}</p>
              <p className="text-xs capitalize text-slate-500">{role}</p>
            </div>
          </div>
        </header>
        <div className="p-5 md:p-8">{children}</div>
      </main>
    </div>
  );
}
