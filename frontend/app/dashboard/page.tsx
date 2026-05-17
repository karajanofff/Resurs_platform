"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { User } from "@/lib/types";

export default function DashboardIndexPage() {
  const router = useRouter();

  useEffect(() => {
    const raw = localStorage.getItem("user");
    if (!raw) {
      router.push("/login");
      return;
    }
    const user = JSON.parse(raw) as User;
    router.push(`/dashboard/${user.role}`);
  }, [router]);

  return <div className="p-8">Yo'naltirilmoqda...</div>;
}

