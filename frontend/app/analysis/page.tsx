"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, Progress } from "@/components/ui";
import { Analysis } from "@/lib/types";

export default function AnalysisPage() {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);

  useEffect(() => {
    const raw = localStorage.getItem("latestAnalysis");
    if (raw) setAnalysis(JSON.parse(raw) as Analysis);
  }, []);

  return (
    <main className="min-h-screen bg-[#f7fbf8] p-6">
      <div className="mx-auto grid max-w-5xl gap-5">
        <Card>
          <p className="text-sm text-slate-500">NLP tahlil sahifasi</p>
          <h1 className="mt-2 text-3xl font-semibold">Tahlil natijasi</h1>
        </Card>
        <Card>
          {analysis ? (
            <>
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">Similarity score</h2>
                <span className="text-3xl font-semibold">{analysis.similarity_score}%</span>
              </div>
              <div className="mt-4"><Progress value={analysis.similarity_score} /></div>
              <div className="mt-5 rounded-2xl bg-emerald-50 p-4">
                <p className="text-sm text-slate-500">Eng yaqin fan</p>
                <p className="mt-1 font-semibold text-forest-700">{analysis.detected_subject}</p>
              </div>
              <div className="mt-5 grid gap-3">
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
              <div className="mt-5 flex flex-wrap gap-2">
                {analysis.matched_keywords.map((item) => (
                  <span key={item} className="rounded-full bg-emerald-50 px-3 py-1 text-sm text-forest-700">{item}</span>
                ))}
              </div>
              <div className="mt-5 grid gap-3">
                {analysis.section_matches.map((section) => (
                  <div key={section.section_title} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                    <div className="flex justify-between gap-3">
                      <p className="font-semibold">{section.section_title}</p>
                      <span className="font-semibold text-forest-700">{section.similarity_score}%</span>
                    </div>
                    <p className="mt-1 text-sm text-forest-700">{section.subject_name}</p>
                    <p className="mt-2 text-sm text-slate-600">{section.preview}</p>
                  </div>
                ))}
              </div>
              <p className="mt-5 rounded-2xl bg-slate-50 p-4">{analysis.recommendation}</p>
            </>
          ) : (
            <p className="text-slate-600">Hozircha saqlangan tahlil natijasi yo'q.</p>
          )}
          <Link href="/dashboard/teacher?view=upload" className="mt-5 inline-block rounded-2xl bg-forest-700 px-5 py-3 font-semibold text-white">
            Resurs yuklashga qaytish
          </Link>
        </Card>
      </div>
    </main>
  );
}
