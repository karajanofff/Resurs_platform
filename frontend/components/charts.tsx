"use client";

import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function OverviewCharts() {
  const trend = [
    { oy: "Yan", qiymat: 22 },
    { oy: "Fev", qiymat: 34 },
    { oy: "Mar", qiymat: 28 },
    { oy: "Apr", qiymat: 46 },
    { oy: "May", qiymat: 58 },
  ];
  const bars = [
    { nom: "AI", qiymat: 18 },
    { nom: "MB", qiymat: 12 },
    { nom: "Web", qiymat: 16 },
    { nom: "Xavf.", qiymat: 9 },
  ];
  const donut = [
    { name: "Mos", value: 58, color: "#16a34a" },
    { name: "Qisman", value: 27, color: "#f59e0b" },
    { name: "Mos emas", value: 15, color: "#ef4444" },
  ];
  return (
    <div className="grid gap-5 xl:grid-cols-3">
      <div className="h-72 rounded-2xl border border-emerald-100 bg-white p-5 shadow-soft">
        <h3 className="mb-4 font-semibold">Yuklashlar dinamikasi</h3>
        <ResponsiveContainer width="100%" height="85%">
          <LineChart data={trend}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="oy" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="qiymat" stroke="#176538" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="h-72 rounded-2xl border border-emerald-100 bg-white p-5 shadow-soft">
        <h3 className="mb-4 font-semibold">Fanlar kesimida</h3>
        <ResponsiveContainer width="100%" height="85%">
          <BarChart data={bars}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="nom" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="qiymat" fill="#237a45" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="h-72 rounded-2xl border border-emerald-100 bg-white p-5 shadow-soft">
        <h3 className="mb-4 font-semibold">Moslik ulushi</h3>
        <ResponsiveContainer width="100%" height="85%">
          <PieChart>
            <Pie data={donut} dataKey="value" innerRadius={58} outerRadius={88}>
              {donut.map((entry) => (
                <Cell key={entry.name} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

