"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import {
  ResourceTable,
  SubjectCards,
  TeacherDashboard,
  TeacherUpload,
} from "@/components/dashboard-content";
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
  const [user, setUser] = useState<User | null>({
    id: 0,
    full_name: "Ochiq foydalanuvchi",
    email: "",
    role: "teacher",
  });
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [resources, setResources] = useState<Resource[]>([]);
  const [latestAnalysis, setLatestAnalysis] = useState<Analysis | null>(null);

  useEffect(() => {
    if (role !== "teacher") {
      router.push("/dashboard/teacher");
      return;
    }
    Promise.all([api.statistics(), api.subjects(), api.topics(), api.resources()]).then(([stats, subjectList, topicList, resourceList]) => {
      setStatistics(stats);
      setSubjects(subjectList);
      setTopics(topicList);
      setResources(resourceList);
    });
  }, [role, router]);

  function changeView(view: string) {
    router.push(`/dashboard/${role}?view=${view}`);
  }

  if (!user || !statistics) return <div className="p-8">Yuklanmoqda...</div>;

  return (
    <DashboardShell role={role} user={user} activeView={activeView} onViewChange={changeView}>
      {role === "teacher" && activeView === "dashboard" && <TeacherDashboard subjects={subjects} topics={topics} resources={resources} latestAnalysis={latestAnalysis} />}
      {role === "teacher" && activeView === "subjects" && <SubjectCards subjects={subjects} />}
      {role === "teacher" && activeView === "upload" && <TeacherUpload onAnalyzed={setLatestAnalysis} />}
      {role === "teacher" && activeView === "analysis" && <InfoCard title="Tahlil natijalari" text={latestAnalysis ? `${latestAnalysis.similarity_score}% - ${latestAnalysis.result_status}` : "Hozircha yangi tahlil bajarilmadi."} />}
      {role === "teacher" && activeView === "library" && <ResourceTable title="Elektron kutubxona" resources={resources} />}
      {role === "teacher" && activeView === "profile" && <InfoCard title="Profil" text="Ochiq foydalanish rejimi" />}

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
