// API 服务层 — 封装所有后端调用
// 开发环境通过 Vite 代理到 localhost:8003
// 生产环境直接使用相对路径（后端提供前端静态文件）

// 根据环境确定 API 基础地址
const getBaseUrl = () => {
  // 开发环境：使用 Vite 代理
  if (import.meta.env.DEV) {
    return '/api';
  }
  // 生产环境：使用相对路径（后端和前端同一域名）
  return '/api';
};

const BASE_URL = getBaseUrl();

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface StatsResponse {
  total_knowledge: number;
  total_categories: number;
  total_tags: number;
  total_views: number;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  icon: string | null;
  order: number;
  created_at: string;
}

export interface Tag {
  id: number;
  name: string;
  slug: string;
  count: number;
  created_at: string;
}

export interface KnowledgeItem {
  id: number;
  title: string;
  slug: string;
  summary: string | null;
  difficulty: string;
  importance: number;
  category_id: number;
  category_name?: string;
  tags: string[];
  view_count: number;
  created_at: string;
}

export interface KnowledgeDetail extends KnowledgeItem {
  content: string;
  subcategory: string | null;
  code_examples: Array<{ language: string; code: string; description: string }>;
  video_url: string | null;
  quiz: Array<{
    question: string;
    options: string[];
    answer: number;
    explanation: string;
  }>;
  like_count: number;
  source: string | null;
  related_ids: number[];
  updated_at: string;
  category: Category | null;
}

export interface Feedback {
  id: number;
  knowledge_id: number;
  type: string;
  content: string;
  contact: string | null;
  status: string;
  created_at: string;
}

export interface KnowledgeListParams {
  page?: number;
  page_size?: number;
  category_id?: number;
  difficulty?: string;
  tags?: string[];
  search?: string;
  order_by?: string;
  order?: string;
}

// ========== 知识点 API ==========
export async function fetchKnowledgeList(
  params: KnowledgeListParams = {}
): Promise<PaginatedResponse<KnowledgeItem>> {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      if (Array.isArray(value)) {
        value.forEach((v) => searchParams.append(key, v));
      } else {
        searchParams.set(key, String(value));
      }
    }
  });
  const res = await fetch(`${BASE_URL}/knowledge?${searchParams.toString()}`);
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

export async function fetchKnowledgeDetail(id: number): Promise<KnowledgeDetail> {
  const res = await fetch(`${BASE_URL}/knowledge/${id}`);
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

export async function deleteKnowledge(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/knowledge/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
}

// ========== 分类 API ==========
export async function fetchCategories(): Promise<Category[]> {
  const res = await fetch(`${BASE_URL}/categories`);
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

// ========== 标签 API ==========
export async function fetchTags(): Promise<Tag[]> {
  const res = await fetch(`${BASE_URL}/tags`);
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

// ========== 统计 API ==========
export async function fetchStats(): Promise<StatsResponse> {
  const res = await fetch(`${BASE_URL}/stats`);
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

// ========== 反馈 API ==========
export async function submitFeedback(data: {
  knowledge_id: number;
  type: string;
  content: string;
  contact?: string;
}): Promise<Feedback> {
  const res = await fetch(`${BASE_URL}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

// ========== 工具函数 ==========
export const DIFFICULTY_LABELS: Record<string, string> = {
  easy: '入门',
  medium: '进阶',
  hard: '困难',
};

export const DIFFICULTY_COLORS: Record<string, string> = {
  easy: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  medium: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
  hard: 'bg-red-500/10 text-red-400 border-red-500/20',
};
