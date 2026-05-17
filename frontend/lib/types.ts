export type Role = "admin" | "teacher";

export type User = {
  id: number;
  full_name: string;
  email: string;
  role: Role;
};

export type Subject = {
  id: number;
  name: string;
  description: string;
};

export type Topic = {
  id: number;
  subject_id: number;
  title: string;
  description: string;
  keywords: string;
};

export type Resource = {
  id: number;
  title: string;
  file_url: string;
  file_type: string;
  subject_id: number;
  topic_id: number;
  keywords: string;
  similarity_score: number;
  status: string;
  is_approved: boolean;
};

export type Statistics = {
  subjects: number;
  topics: number;
  resources: number;
  users: number;
  matched: number;
  partial: number;
  unmatched: number;
};

export type Analysis = {
  resource_id: number;
  similarity_score: number;
  matched_keywords: string[];
  recommendation: string;
  result_status: string;
  detected_subject: string;
  subject_scores: {
    subject_id: number;
    subject_name: string;
    similarity_score: number;
  }[];
  section_matches: {
    section_title: string;
    preview: string;
    subject_name: string;
    similarity_score: number;
  }[];
};
