"use client";

import { ChangeEvent, FormEvent, useEffect, useMemo, useState } from "react";
import { BookOpen, FileText, Filter, UploadCloud, Users } from "lucide-react";
import { api, publicFileUrl } from "@/lib/api";
import { Analysis, Resource, Statistics, Subject, Topic, User } from "@/lib/types";
import { Badge, Card, Progress } from "./ui";
import { OverviewCharts } from "./charts";

export function AdminOverview({ statistics, resources }: { statistics: Statistics; resources: Resource[] }) {
  const cards = [
    ["Jami fanlar", statistics.subjects],
    ["Jami resurslar", statistics.resources],
    ["Jami foydalanuvchilar", statistics.users],
    ["Mos resurslar", statistics.matched],
    ["Qisman mos", statistics.partial],
    ["Mos emas", statistics.unmatched],
  ];
  return (
    <div className="grid gap-5">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map(([label, value]) => (
          <Card key={label as string}>
            <p className="text-sm text-slate-500">{label as string}</p>
            <p className="mt-3 text-3xl font-semibold">{value as number}</p>
          </Card>
        ))}
      </div>
      <OverviewCharts />
      <ResourceTable title="Oxirgi yuklangan resurslar" resources={resources} />
    </div>
  );
}

export function SubjectManager({
  subjects,
  onCreated,
}: {
  subjects: Subject[];
  onCreated: (subject: Subject) => void;
}) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!name.trim()) return;
    const created = await api.createSubject({ name, description, teacher_id: null });
    onCreated(created);
    setName("");
    setDescription("");
  }

  return (
    <div className="grid gap-5 xl:grid-cols-[0.8fr_1.2fr]">
      <Card>
        <h2 className="text-lg font-semibold">Yangi fan qo'shish</h2>
        <form onSubmit={submit} className="mt-5 grid gap-4">
          <input value={name} onChange={(event) => setName(event.target.value)} placeholder="Fan nomi" className="rounded-2xl border border-slate-200 px-4 py-3" />
          <textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Qisqa tavsif" className="min-h-28 rounded-2xl border border-slate-200 px-4 py-3" />
          <button className="rounded-2xl bg-forest-700 px-4 py-3 font-semibold text-white">Fan qo'shish</button>
        </form>
      </Card>
      <Card>
        <h2 className="text-lg font-semibold">Fanlar ro'yxati</h2>
        <div className="mt-5 grid gap-3">
          {subjects.map((subject) => (
            <div key={subject.id} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="font-semibold">{subject.name}</p>
              <p className="mt-1 text-sm text-slate-500">{subject.description}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

export function TopicManager({
  subjects,
  topics,
  onCreated,
}: {
  subjects: Subject[];
  topics: Topic[];
  onCreated: (topic: Topic) => void;
}) {
  const [subjectId, setSubjectId] = useState(subjects[0]?.id ?? 0);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [keywords, setKeywords] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!subjectId || !title.trim()) return;
    const created = await api.createTopic({ subject_id: subjectId, title, description, keywords });
    onCreated(created);
    setTitle("");
    setDescription("");
    setKeywords("");
  }

  return (
    <div className="grid gap-5 xl:grid-cols-[0.85fr_1.15fr]">
      <Card>
        <h2 className="text-lg font-semibold">Yangi mavzu qo'shish</h2>
        <form onSubmit={submit} className="mt-5 grid gap-4">
          <select value={subjectId} onChange={(event) => setSubjectId(Number(event.target.value))} className="rounded-2xl border border-slate-200 px-4 py-3">
            {subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}
          </select>
          <input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Mavzu nomi" className="rounded-2xl border border-slate-200 px-4 py-3" />
          <textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Mavzu tavsifi" className="min-h-24 rounded-2xl border border-slate-200 px-4 py-3" />
          <input value={keywords} onChange={(event) => setKeywords(event.target.value)} placeholder="Kalit so'zlar" className="rounded-2xl border border-slate-200 px-4 py-3" />
          <button className="rounded-2xl bg-forest-700 px-4 py-3 font-semibold text-white">Mavzu qo'shish</button>
        </form>
      </Card>
      <Card>
        <h2 className="text-lg font-semibold">Mavzular</h2>
        <div className="mt-5 grid gap-3">
          {topics.map((topic) => (
            <div key={topic.id} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="font-semibold">{topic.title}</p>
              <p className="mt-1 text-sm text-slate-500">{subjects.find((subject) => subject.id === topic.subject_id)?.name}</p>
              <p className="mt-2 text-sm text-slate-600">{topic.description}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

export function UserPanel({ users }: { users: User[] }) {
  return (
    <Card>
      <div className="mb-5 flex items-center gap-3">
        <Users className="h-5 w-5 text-forest-700" />
        <h2 className="text-lg font-semibold">Foydalanuvchilar</h2>
      </div>
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {users.map((user) => (
          <div key={user.id} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
            <p className="font-semibold">{user.full_name}</p>
            <p className="mt-1 text-sm text-slate-500">{user.email}</p>
            <p className="mt-3 inline-flex rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold capitalize text-forest-700">{user.role}</p>
          </div>
        ))}
      </div>
    </Card>
  );
}

export function TeacherUpload({
  onAnalyzed,
}: {
  onAnalyzed: (analysis: Analysis) => void;
}) {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function analyze() {
    if (!title.trim()) {
      setMessage("Avval resurs nomini kiriting.");
      return;
    }
    if (!file) {
      setMessage("Avval fayl tanlang.");
      return;
    }
    setLoading(true);
    setMessage("");
    try {
      const form = new FormData();
      form.append("title", title);
      form.append("file", file);
      const resource = await api.uploadResource(form);
      const result = await api.analyze(resource.id);
      setAnalysis(result);
      onAnalyzed(result);
      localStorage.setItem("latestAnalysis", JSON.stringify(result));
      setMessage("Tahlil muvaffaqiyatli yakunlandi.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Tahlil bajarilmadi.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-5 xl:grid-cols-[1.08fr_0.92fr]">
      <Card>
        <h2 className="text-lg font-semibold">Resurs yuklash</h2>
        <div className="mt-5 grid gap-4">
          <label className="grid gap-2 text-sm">
            Resurs nomi
            <input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Masalan: NLP bo'yicha ma'ruza" className="rounded-2xl border border-slate-200 px-4 py-3" />
          </label>
          <label className="grid min-h-48 cursor-pointer place-items-center rounded-3xl border-2 border-dashed border-emerald-200 bg-gradient-to-br from-emerald-50 to-white p-5 text-center">
            <UploadCloud className="h-8 w-8 text-forest-600" />
            <span className="mt-3 font-medium">{file ? file.name : "PDF, DOCX, PPTX yoki TXT faylni tanlang"}</span>
            <span className="mt-1 text-sm text-slate-500">Fayl tanlash uchun bosing</span>
            <input hidden type="file" accept=".pdf,.docx,.pptx,.txt" onChange={(event: ChangeEvent<HTMLInputElement>) => setFile(event.target.files?.[0] ?? null)} />
          </label>
          {message && <p className="text-sm text-forest-700">{message}</p>}
          <button disabled={loading} onClick={analyze} className="rounded-2xl bg-forest-700 px-4 py-3 font-semibold text-white disabled:opacity-60">
            {loading ? "Tahlil qilinmoqda..." : "NLP tahlil qilish"}
          </button>
        </div>
      </Card>
      <AnalysisCard analysis={analysis} />
    </div>
  );
}

export function AnalysisCard({ analysis }: { analysis: Analysis | null }) {
  return (
    <Card>
      <h2 className="text-lg font-semibold">Tahlil natijasi</h2>
      {analysis ? (
        <div className="mt-5 grid gap-4">
          <div className="flex items-center justify-between">
            <span className="text-4xl font-semibold">{analysis.similarity_score}%</span>
            <Badge label={analysis.result_status} />
          </div>
          <Progress value={analysis.similarity_score} />
          <div className="rounded-2xl bg-emerald-50 p-4">
            <p className="text-sm text-slate-500">Eng yaqin fan</p>
            <p className="mt-1 font-semibold text-forest-700">{analysis.detected_subject}</p>
          </div>
          <div>
            <p className="mb-2 text-sm text-slate-500">Fanlar bo'yicha umumiy moslik</p>
            <div className="grid gap-3">
              {analysis.subject_scores.map((subject) => (
                <div key={subject.subject_id}>
                  <div className="mb-1 flex justify-between text-sm">
                    <span>{subject.subject_name}</span>
                    <span>{subject.similarity_score}%</span>
                  </div>
                  <Progress value={subject.similarity_score} />
                </div>
              ))}
            </div>
          </div>
          <div>
            <p className="mb-2 text-sm text-slate-500">Aniqlangan kalit so'zlar</p>
            <div className="flex flex-wrap gap-2">
              {analysis.matched_keywords.map((keyword) => (
                <span key={keyword} className="rounded-full bg-emerald-50 px-3 py-1 text-sm text-forest-700">{keyword}</span>
              ))}
            </div>
          </div>
          <div>
            <p className="mb-2 text-sm text-slate-500">Fayl bo'limlari bo'yicha tahlil</p>
            <div className="grid gap-3">
              {analysis.section_matches.map((section) => (
                <div key={section.section_title} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <p className="font-semibold">{section.section_title}</p>
                    <span className="text-sm font-semibold text-forest-700">{section.similarity_score}%</span>
                  </div>
                  <p className="mt-1 text-sm text-forest-700">{section.subject_name}</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{section.preview}</p>
                </div>
              ))}
            </div>
          </div>
          <p className="rounded-2xl bg-slate-50 p-4 text-sm leading-7">{analysis.recommendation}</p>
        </div>
      ) : (
        <p className="mt-5 text-slate-500">Fayl yuklang va tahlilni ishga tushiring.</p>
      )}
    </Card>
  );
}

export function TeacherDashboard({
  subjects,
  topics,
  resources,
  latestAnalysis,
}: {
  subjects: Subject[];
  topics: Topic[];
  resources: Resource[];
  latestAnalysis: Analysis | null;
}) {
  return (
    <div className="grid gap-5">
      <div className="grid gap-4 md:grid-cols-3">
        <Metric title="Mening fanlarim" value={subjects.length} icon={<BookOpen className="h-5 w-5" />} />
        <Metric title="Kutubxonadagi resurslar" value={resources.length} icon={<FileText className="h-5 w-5" />} />
      </div>
      <div className="grid gap-5 xl:grid-cols-[1.2fr_0.8fr]">
        <ResourceTable title="So'nggi resurslar" resources={resources} />
        <AnalysisCard analysis={latestAnalysis} />
      </div>
    </div>
  );
}

export function StudentCatalog({
  resources,
  subjects,
  topics,
  onlyRecommended = false,
}: {
  resources: Resource[];
  subjects: Subject[];
  topics: Topic[];
  onlyRecommended?: boolean;
}) {
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("Barchasi");
  const filtered = useMemo(
    () =>
      resources.filter(
        (item) =>
          item.title.toLowerCase().includes(query.toLowerCase()) &&
          (status === "Barchasi" || item.status === status) &&
          (!onlyRecommended || item.similarity_score >= 75),
      ),
    [onlyRecommended, query, resources, status],
  );
  return (
    <div className="grid gap-5">
      <Card className="flex flex-col gap-3 md:flex-row">
        <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Resurs qidirish..." className="flex-1 rounded-2xl border border-slate-200 px-4 py-3" />
        <label className="flex items-center gap-2 rounded-2xl border border-slate-200 px-4">
          <Filter className="h-4 w-4" />
          <select value={status} onChange={(event) => setStatus(event.target.value)} className="bg-transparent py-3 outline-none">
            <option>Barchasi</option>
            <option>Mos</option>
            <option>Qisman mos</option>
            <option>Mos emas</option>
          </select>
        </label>
      </Card>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {filtered.map((resource) => (
          <Card key={resource.id}>
            <div className="flex items-start justify-between gap-3">
              <FileText className="h-6 w-6 text-forest-600" />
              <Badge label={resource.status} />
            </div>
            <h3 className="mt-4 text-lg font-semibold">{resource.title}</h3>
            <p className="mt-2 text-sm text-slate-500">{subjects.find((subject) => subject.id === resource.subject_id)?.name}</p>
            <p className="text-sm text-slate-500">{topics.find((topic) => topic.id === resource.topic_id)?.title}</p>
            <div className="mt-4">
              <div className="mb-2 flex justify-between text-sm">
                <span>Moslik</span>
                <span>{resource.similarity_score}%</span>
              </div>
              <Progress value={resource.similarity_score} />
            </div>
            <a href={publicFileUrl(resource.file_url)} className="mt-5 block w-full rounded-2xl bg-forest-700 px-4 py-3 text-center font-semibold text-white">
              Yuklab olish
            </a>
          </Card>
        ))}
      </div>
    </div>
  );
}

export function SubjectCards({ subjects }: { subjects: Subject[] }) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {subjects.map((subject) => (
        <Card key={subject.id}>
          <BookOpen className="h-6 w-6 text-forest-700" />
          <h3 className="mt-4 text-lg font-semibold">{subject.name}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-500">{subject.description}</p>
        </Card>
      ))}
    </div>
  );
}

export function ResourceTable({ title, resources }: { title: string; resources: Resource[] }) {
  return (
    <Card>
      <h2 className="mb-4 text-lg font-semibold">{title}</h2>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[640px] text-left text-sm">
          <thead className="text-slate-500">
            <tr>
              <th className="pb-3">Resurs</th>
              <th className="pb-3">Fayl turi</th>
              <th className="pb-3">Moslik</th>
              <th className="pb-3">Holat</th>
            </tr>
          </thead>
          <tbody>
            {resources.map((resource) => (
              <tr key={resource.id} className="border-t border-slate-100">
                <td className="py-3">
                  <a href={publicFileUrl(resource.file_url)} className="font-medium text-forest-700 hover:underline">
                    {resource.title}
                  </a>
                </td>
                <td className="py-3">{resource.file_type}</td>
                <td className="py-3">{resource.similarity_score}%</td>
                <td className="py-3"><Badge label={resource.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

function Metric({ title, value, icon }: { title: string; value: number; icon: React.ReactNode }) {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-500">{title}</p>
        <span className="rounded-2xl bg-emerald-50 p-3 text-forest-700">{icon}</span>
      </div>
      <p className="mt-4 text-3xl font-semibold">{value}</p>
    </Card>
  );
}
