import { ReactNode } from "react";

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <section className={`rounded-2xl border border-emerald-100 bg-white p-5 shadow-soft ${className}`}>{children}</section>;
}

export function Badge({ label }: { label: string }) {
  const color =
    label === "Mos"
      ? "bg-emerald-100 text-emerald-700"
      : label === "Qisman mos"
        ? "bg-amber-100 text-amber-700"
        : "bg-rose-100 text-rose-700";
  return <span className={`rounded-full px-3 py-1 text-xs font-semibold ${color}`}>{label}</span>;
}

export function Progress({ value }: { value: number }) {
  const color = value >= 75 ? "bg-emerald-500" : value >= 40 ? "bg-amber-500" : "bg-rose-500";
  return (
    <div className="h-3 overflow-hidden rounded-full bg-slate-100">
      <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
    </div>
  );
}
