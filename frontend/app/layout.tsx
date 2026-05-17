import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SmartKutubxona AI",
  description: "Ta'lim resurslarini NLP yordamida avtomatik baholovchi platforma",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="uz">
      <body>{children}</body>
    </html>
  );
}

