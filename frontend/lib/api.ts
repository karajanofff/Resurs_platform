import { Analysis, Resource, Statistics, Subject, Topic, User } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

function authHeaders(): Record<string, string> {
  if (typeof window === "undefined") return {};
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const headers = new Headers(options?.headers);
  if (!(options?.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  Object.entries(authHeaders()).forEach(([key, value]) => headers.set(key, value));
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

export const api = {
  login: (email: string, password: string, role: string) =>
    request<{ access_token: string; user: User }>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password, role }),
    }),
  me: () => request<User>("/api/me"),
  statistics: () => request<Statistics>("/api/statistics"),
  subjects: () => request<Subject[]>("/api/subjects"),
  createSubject: (payload: { name: string; description: string; teacher_id?: number | null }) =>
    request<Subject>("/api/subjects", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  topics: () => request<Topic[]>("/api/topics"),
  createTopic: (payload: { subject_id: number; title: string; description: string; keywords: string }) =>
    request<Topic>("/api/topics", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  resources: () => request<Resource[]>("/api/resources"),
  uploadResource: (formData: FormData) =>
    request<Resource>("/api/resources/upload", { method: "POST", body: formData }),
  analyze: (resourceId: number) => {
    const form = new FormData();
    form.append("resource_id", String(resourceId));
    return request<Analysis>("/api/analyze", { method: "POST", body: form });
  },
};

export function publicFileUrl(path: string) {
  return `${API_URL}${path}`;
}
