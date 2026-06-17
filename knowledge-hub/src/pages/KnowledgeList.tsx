import { useEffect, useState, useCallback } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  ChevronLeft,
  ChevronRight,
  Star,
  Eye,
  Filter,
  X,
} from 'lucide-react';
import type { KnowledgeItem, Category } from '@/services/api';
import { fetchKnowledgeList, fetchCategories, DIFFICULTY_LABELS, DIFFICULTY_COLORS } from '@/services/api';

export default function KnowledgeList() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);

  const page = parseInt(searchParams.get('page') || '1', 10);
  const categoryId = searchParams.get('category_id');
  const difficulty = searchParams.get('difficulty');
  const search = searchParams.get('search');
  const orderBy = searchParams.get('order_by') || 'importance';
  const order = searchParams.get('order') || 'desc';

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [data, cats] = await Promise.all([
        fetchKnowledgeList({
          page,
          page_size: 20,
          category_id: categoryId ? parseInt(categoryId, 10) : undefined,
          difficulty: difficulty || undefined,
          search: search || undefined,
          order_by: orderBy,
          order,
        }),
        fetchCategories(),
      ]);
      setItems(data.items);
      setTotal(data.total);
      setTotalPages(data.total_pages);
      setCategories(cats);
    } catch (err) {
      console.error('Knowledge list error:', err);
    } finally {
      setLoading(false);
    }
  }, [page, categoryId, difficulty, search, orderBy, order]);

  useEffect(() => {
    load();
  }, [load]);

  const updateParam = (key: string, value: string | null) => {
    const params = new URLSearchParams(searchParams);
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
    if (key !== 'page') params.set('page', '1');
    setSearchParams(params);
  };

  const clearFilters = () => {
    setSearchParams({});
  };

  const currentCategory = categoryId
    ? categories.find((c) => c.id === parseInt(categoryId, 10))
    : null;

  const hasFilters = !!(categoryId || difficulty || search);

  return (
    <div className="space-y-6 p-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">知识库</h2>
          <p className="mt-1 text-sm text-gray-500">
            共 {total} 个知识点
            {currentCategory && ` · ${currentCategory.name}`}
            {difficulty && ` · ${DIFFICULTY_LABELS[difficulty] || difficulty}`}
            {search && ` · 搜索"${search}"`}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center gap-1.5 rounded-lg border px-3 py-2 text-sm transition-colors ${
              showFilters || hasFilters
                ? 'border-blue-500/50 bg-blue-500/10 text-blue-400'
                : 'border-gray-700 text-gray-400 hover:border-gray-600'
            }`}
          >
            <Filter className="h-4 w-4" />
            筛选
          </button>
        </div>
      </div>

      {/* Filters panel */}
      {showFilters && (
        <div className="rounded-xl border border-gray-800 bg-[#0a0a0a] p-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {/* Category filter */}
            <div>
              <label className="mb-1.5 block text-xs font-medium text-gray-500">分类</label>
              <select
                value={categoryId || ''}
                onChange={(e) => updateParam('category_id', e.target.value || null)}
                className="w-full rounded-lg border border-gray-700 bg-black px-3 py-2 text-sm text-gray-200 focus:border-blue-500 focus:outline-none"
              >
                <option value="">全部</option>
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.icon || '📁'} {cat.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Difficulty filter */}
            <div>
              <label className="mb-1.5 block text-xs font-medium text-gray-500">难度</label>
              <select
                value={difficulty || ''}
                onChange={(e) => updateParam('difficulty', e.target.value || null)}
                className="w-full rounded-lg border border-gray-700 bg-black px-3 py-2 text-sm text-gray-200 focus:border-blue-500 focus:outline-none"
              >
                <option value="">全部</option>
                <option value="easy">入门</option>
                <option value="medium">进阶</option>
                <option value="hard">困难</option>
              </select>
            </div>

            {/* Sort */}
            <div>
              <label className="mb-1.5 block text-xs font-medium text-gray-500">排序</label>
              <select
                value={`${orderBy}-${order}`}
                onChange={(e) => {
                  const [ob, od] = e.target.value.split('-');
                  const params = new URLSearchParams(searchParams);
                  params.set('order_by', ob);
                  params.set('order', od);
                  params.set('page', '1');
                  setSearchParams(params);
                }}
                className="w-full rounded-lg border border-gray-700 bg-black px-3 py-2 text-sm text-gray-200 focus:border-blue-500 focus:outline-none"
              >
                <option value="importance-desc">重要性 ↓</option>
                <option value="importance-asc">重要性 ↑</option>
                <option value="view_count-desc">浏览量 ↓</option>
                <option value="created_at-desc">最新 ↓</option>
              </select>
            </div>
          </div>

          {hasFilters && (
            <button
              onClick={clearFilters}
              className="mt-3 flex items-center gap-1 text-xs text-gray-500 hover:text-gray-300"
            >
              <X className="h-3 w-3" />
              清除所有筛选
            </button>
          )}
        </div>
      )}

      {/* Knowledge list */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
        </div>
      ) : items.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-gray-600">
          <p className="text-lg">暂无数据</p>
          {hasFilters && (
            <button onClick={clearFilters} className="mt-2 text-sm text-blue-400 hover:text-blue-300">
              清除筛选条件
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {items.map((item) => (
            <Link
              key={item.id}
              to={`/knowledge/${item.id}`}
              className="group rounded-xl border border-gray-800 bg-[#0a0a0a] p-5 hover:border-gray-700 transition-all duration-200"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <h3 className="font-semibold group-hover:text-blue-400 transition-colors line-clamp-1">
                    {item.title}
                  </h3>
                  <p className="mt-1.5 text-sm text-gray-500 line-clamp-2">{item.summary}</p>
                </div>
              </div>

              <div className="mt-4 flex flex-wrap items-center gap-2">
                <span className={`rounded-md border px-2 py-0.5 text-[11px] font-medium ${DIFFICULTY_COLORS[item.difficulty] || ''}`}>
                  {DIFFICULTY_LABELS[item.difficulty] || item.difficulty}
                </span>

                <span className="flex items-center gap-1 text-[11px] text-gray-600">
                  <Star className="h-3 w-3 fill-amber-500 text-amber-500" />
                  {item.importance}
                </span>

                <span className="flex items-center gap-1 text-[11px] text-gray-600">
                  <Eye className="h-3 w-3" />
                  {item.view_count}
                </span>

                {item.category_name && (
                  <span className="rounded-md border border-gray-700 px-2 py-0.5 text-[11px] text-gray-500">
                    {item.category_name}
                  </span>
                )}
              </div>

              {item.tags.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {item.tags.slice(0, 4).map((tag) => (
                    <span key={tag} className="rounded-sm bg-gray-800/50 px-1.5 py-0.5 text-[10px] text-gray-500">
                      {tag}
                    </span>
                  ))}
                  {item.tags.length > 4 && (
                    <span className="text-[10px] text-gray-600">+{item.tags.length - 4}</span>
                  )}
                </div>
              )}
            </Link>
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 pt-4">
          <button
            onClick={() => updateParam('page', String(page - 1))}
            disabled={page <= 1}
            className="flex items-center gap-1 rounded-lg border border-gray-700 px-3 py-2 text-sm text-gray-400 hover:border-gray-600 disabled:opacity-30 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="h-4 w-4" />
            上一页
          </button>

          <span className="px-4 text-sm text-gray-500">
            {page} / {totalPages}
          </span>

          <button
            onClick={() => updateParam('page', String(page + 1))}
            disabled={page >= totalPages}
            className="flex items-center gap-1 rounded-lg border border-gray-700 px-3 py-2 text-sm text-gray-400 hover:border-gray-600 disabled:opacity-30 disabled:cursor-not-allowed"
          >
            下一页
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      )}
    </div>
  );
}
