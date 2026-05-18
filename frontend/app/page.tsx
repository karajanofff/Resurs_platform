import { Brain, LibraryBig, Sparkles } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

const cards = [
  ["NLP asosida tahlil", Brain],
  ["Avtomatik moslik baholash", Sparkles],
  ["Aqlli resurs katalogi", LibraryBig],
];

export default function LandingPage() {
  return (
    <main className="bg-white">
      <section className="relative min-h-[88vh] overflow-hidden bg-forest-800 text-white">
        <Image src="/hero-library.png" alt="" fill priority className="object-cover opacity-45" />
        <div className="absolute inset-0 bg-gradient-to-r from-forest-800 via-forest-800/95 to-forest-700/55" />
        <div className="relative mx-auto flex min-h-[88vh] max-w-7xl flex-col justify-between px-6 py-8 lg:px-10">
          <nav className="flex items-center justify-between">
            <div className="text-xl font-semibold">SmartKutubxona AI</div>
            <Link href="/login" className="rounded-2xl border border-white/25 px-4 py-2 text-sm">
              Kirish
            </Link>
          </nav>
          <div className="grid items-center gap-8 py-12 lg:grid-cols-[minmax(0,1fr)_420px]">
            <div>
            <p className="mb-4 text-sm uppercase tracking-[0.25em] text-emerald-100">NLP bilan aqlli kutubxona</p>
            <h1 className="text-4xl font-semibold leading-tight md:text-6xl">SmartKutubxona AI</h1>
            <p className="mt-6 max-w-2xl text-base leading-8 text-emerald-50 md:text-lg">
              Ta'lim resurslarini fan mavzulariga mosligini NLP yordamida avtomatik baholovchi aqlli elektron kutubxona platformasi
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/login" className="rounded-2xl bg-white px-5 py-3 font-semibold text-forest-700">
                Boshlash
              </Link>
            </div>
            </div>
            <div className="glass rounded-3xl border border-white/20 p-5 text-forest-800 shadow-soft">
              <div className="flex items-center justify-between">
                <p className="font-semibold">AI dashboard preview</p>
                <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold">Mos 88%</span>
              </div>
              <div className="mt-5 grid gap-3">
                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">NLP texnologiyalari.pdf</p>
                  <div className="mt-3 h-3 overflow-hidden rounded-full bg-slate-100">
                    <div className="h-full w-[88%] rounded-full bg-emerald-500" />
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-3 text-center">
                  {["Fanlar 5", "Resurslar 128", "Moslik 88%"].map((item) => (
                    <div key={item} className="rounded-2xl bg-white p-3 text-sm font-medium">{item}</div>
                  ))}
                </div>
              </div>
            </div>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            {cards.map(([title, Icon]) => (
              <div key={title as string} className="glass rounded-2xl border border-white/20 p-5 text-forest-800">
                <Icon className="mb-4 h-6 w-6" />
                <p className="font-semibold">{title as string}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
