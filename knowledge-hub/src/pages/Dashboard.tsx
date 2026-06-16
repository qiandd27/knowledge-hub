import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  FolderTree,
  Tag,
  Eye,
} from 'lucide-react';
import type { StatsResponse, Category, Tag as TagType, KnowledgeItem } from '@/services/api';
import { fetchStats, fetchCategories, fetchTags, fetchKnowledgeList } from '@/services/api';

export default function Dashboard() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [tags, setTags] = useState<TagType[]>([]);
  const [recent, setRecent] = useState<KnowledgeItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [s, c, t, r] = await Promise.all([
          fetchStats(),
          fetchCategories(),
          fetchTags(),
          fetchKnowledgeList({ page: 1, page_size: 6, order_by: 'created_at', order: 'desc' }),
        ]);
        setStats(s);
        setCategories(c);
        setTags(t);
        setRecent(r.items);
      } catch (err) {
        console.error('Dashboard load error:', err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    );
  }

  const kpiCards = [
    { icon: BookOpen, label: '知识点', value: stats?.total_knowledge || 0, color: 'text-blue-400', bg: 'bg-blue-500/10' },
    { icon: FolderTree, label: '分类', value: stats?.total_categories || 0, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
    { icon: Tag, label: '标签', value: stats?.total_tags || 0, color: 'text-amber-400', bg: 'bg-amber-500/10' },
    { icon: Eye, label: '总浏览量', value: stats?.total_views || 0, color: 'text-purple-400', bg: 'bg-purple-500/10' },
  ];

  return (
    <div className="space-y-8 p-8">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold tracking-tight">仪表盘</h2>
        <p className="mt-1 text-sm text-gray-500">游戏测试知识系统 · 数据总览</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {kpiCards.map((card) => (
          <div
            key={card.label}
            className="rounded-xl border border-gray-800 bg-[#0a0a0a] p-6 hover:border-gray-700 transition-colors"
          >
            <div className="flex items-center gap-4">
              <div className={`rounded-lg p-2.5 ${card.bg}`}>
                <card.icon className={`h-5 w-5 ${card.color}`} />
              </div>
              <div>
                <p className="text-2xl font-bold">{card.value.toLocaleString()}</p>
                <p className="text-xs text-gray-500">{card.label}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick links section */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Categories */}
        <div className="rounded-xl border border-gray-800 bg-[#0a0a0a]">
          <div className="flex items-center justify-between border-b border-gray-800 px-6 py-4">
            <h3 className="font-semibold">知识分类</h3>
            <Link to="/categories" className="text-xs text-blue-400 hover:text-blue-300">
              查看全部
            </Link>
          </div>
          <div className="grid grid-cols-2 gap-2 p-4">
            {categories.slice(0, 8).map((cat) => (
              <Link
                key={cat.id}
                to={`/knowledge?category_id=${cat.id}`}
                className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-gray-300 hover:bg-gray-800/50 transition-colors"
              >
                <span className="text-base">{cat.icon || '📁'}</span>
                {cat.name}
              </Link>
            ))}
          </div>
        </div>

        {/* Recent knowledge */}
        <div className="rounded-xl border border-gray-800 bg-[#0a0a0a]">
          <div className="flex items-center justify-between border-b border-gray-800 px-6 py-4">
            <h3 className="font-semibold">最新知识点</h3>
            <Link to="/knowledge" className="text-xs text-blue-400 hover:text-blue-300">
              查看全部
            </Link>
          </div>
          <div className="divide-y divide-gray-800">
            {recent.map((item) => (
              <Link
                key={item.id}
                to={`/knowledge/${item.id}`}
                className="flex items-center justify-between px-6 py-3 hover:bg-gray-800/30 transition-colors"
              >
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium">{item.title}</p>
                  <p className="truncate text-xs text-gray-500">{item.summary}</p>
                </div>
                <span className="ml-3 shrink-0 text-xs text-gray-600">
                  {item.view_count} 阅读
                </span>
              </Link>
            ))}
            {recent.length === 0 && (
              <p className="px-6 py-8 text-center text-sm text-gray-600">暂无数据</p>
            )}
          </div>
        </div>
      </div>

      {/* Tags cloud */}
      {tags.length > 0 && (
        <div className="rounded-xl border border-gray-800 bg-[#0a0a0a] p-6">
          <h3 className="mb-4 font-semibold">标签</h3>
          <div className="flex flex-wrap gap-2">
            {tags.map((tag) => (
              <Link
                key={tag.id}
                to={`/knowledge?tags=${encodeURIComponent(tag.name)}`}
                className="rounded-full border border-gray-700 px-3 py-1 text-xs text-gray-400 hover:border-blue-500/50 hover:text-blue-400 transition-colors"
              >
                {tag.name}
                {tag.count > 0 && (
                  <span className="ml-1 text-gray-600">({tag.count})</span>
                )}
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
