"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import {
  AdminOverview,
  ResourceTable,
  SubjectCards,
  SubjectManager,
  TeacherDashboard,
  TeacherUpload,
  UserPanel,
} from "@/components/dashboard-content";
import { OverviewCharts } from "@/components/charts";
import { DashboardShell, menus } from "@/components/shell";
import { Card } from "@/components/ui";
import { api } from "@/lib/api";
import { Analysis, Resource, Role, Statistics, Subject, Topic, User } from "@/lib/types";

export default function RoleDashboardPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const params = useParams<{ role: Role }>();
  const role = params.role;
  const allowedViews = menus[role]?.map((item) => item.key) ?? [];
  const requestedView = searchParams.get("view");
  const activeView = requestedView && allowedViews.includes(requestedView) ? requestedView : "dashboard";
  const [user, setUser] = useState<User | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [resources, setResources] = useState<Resource[]>([]);
  const [latestAnalysis, setLatestAnalysis] = useState<Analysis | null>(null);

  useEffect(() => {
    const raw = localStorage.getItem("user");
    if (!raw) {
      router.push("/login");
      return;
    }
    const stored = JSON.parse(raw) as User;
    if (stored.role !== role) {
      router.push(`/dashboard/${stored.role}`);
      return;
    }
    setUser(stored);
    Promise.all([api.statistics(), api.subjects(), api.topics(), api.resources(), api.me()]).then(([stats, subjectList, topicList, resourceList]) => {
      setStatistics(stats);
      setSubjects(subjectList);
      setTopics(topicList);
      setResources(resourceList);
    });
    if (role === "admin") {
      fetchUsers();
    }
  }, [role, router]);

  async function fetchUsers() {
    const token = localStorage.getItem("token");
    if (!token) return;
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/users`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.ok) setUsers(await response.json());
  }

  function changeView(view: string) {
    router.push(`/dashboard/${role}?view=${view}`);
  }

  if (!user || !statistics) return <div className="p-8">Yuklanmoqda...</div>;

  return (
    <DashboardShell role={role} user={user} activeView={activeView} onViewChange={changeView}>
      {role === "admin" && activeView === "dashboard" && <AdminOverview statistics={statistics} resources={resources} />}
      {role === "admin" && activeView === "subjects" && <SubjectManager subjects={subjects} onCreated={(subject) => setSubjects((current) => [...current, subject])} />}
      {role === "admin" && activeView === "users" && <UserPanel users={users} />}
      {role === "admin" && activeView === "resources" && <ResourceTable title="Barcha resurslar" resources={resources} />}
      {role === "admin" && activeView === "analysis" && <ResourceTable title="NLP tahlil natijalari" resources={resources} />}
      {role === "admin" && activeView === "statistics" && <OverviewCharts />}
      {role === "admin" && activeView === "settings" && <InfoCard title="Sozlamalar" text="Environment, JWT va deploy sozlamalari README orqali boshqariladi." />}

      {role === "teacher" && activeView === "dashboard" && <TeacherDashboard subjects={subjects} topics={topics} resources={resources} latestAnalysis={latestAnalysis} />}
      {role === "teacher" && activeView === "subjects" && <SubjectCards subjects={subjects} />}
      {role === "teacher" && activeView === "upload" && <TeacherUpload onAnalyzed={setLatestAnalysis} />}
      {role === "teacher" && activeView === "analysis" && <InfoCard title="Tahlil natijalari" text={latestAnalysis ? `${latestAnalysis.similarity_score}% - ${latestAnalysis.result_status}` : "Hozircha yangi tahlil bajarilmadi."} />}
      {role === "teacher" && activeView === "library" && <ResourceTable title="Elektron kutubxona" resources={resources} />}
      {role === "teacher" && activeView === "profile" && <InfoCard title="Profil" text={`${user.full_name} - ${user.email}`} />}

    </DashboardShell>
  );
}

function InfoCard({ title, text }: { title: string; text: string }) {
  return (
    <Card>
      <h2 className="text-lg font-semibold">{title}</h2>
      <p className="mt-3 text-slate-600">{text}</p>
    </Card>
  );
}
