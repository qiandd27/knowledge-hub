import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  Search as SearchIcon,
  Star,
  Eye,
} from 'lucide-react';
import type { KnowledgeItem } from '@/services/api';
import { fetchKnowledgeList, DIFFICULTY_LABELS, DIFFICULTY_COLORS } from '@/services/api';

export default function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [results, setResults] = useState<KnowledgeItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const searchParamQ = searchParams.get('q') || '';

  useEffect(() => {
    if (!searchParamQ) return;
    setQuery(searchParamQ);
    setLoading(true);
    fetchKnowledgeList({ search: searchParamQ, page_size: 50 })
      .then((data) => {
        setResults(data.items);
        setTotal(data.total);
        setSearched(true);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [searchParamQ]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) return;
    setSearchParams({ q: trimmed });
  };

  return (
    <div className="space-y-8 p-8">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold tracking-tight">搜索</h2>
        <p className="mt-1 text-sm text-gray-500">全文搜索知识点内容、标题和标签</p>
      </div>

      {/* Search bar */}
      <form onSubmit={handleSearch} className="flex gap-3">
        <div className="relative flex-1">
          <SearchIcon className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="输入关键词搜索知识点..."
            className="w-full rounded-xl border border-gray-700 bg-[#0a0a0a] py-3 pl-10 pr-4 text-sm text-gray-200 placeholder:text-gray-600 focus:border-blue-500 focus:outline-none"
            autoFocus
          />
        </div>
        <button
          type="submit"
          disabled={!query.trim()}
          className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          搜索
        </button>
      </form>

      {/* Results */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
        </div>
      ) : searched ? (
        <>
          <p className="text-sm text-gray-500">
            找到 <span className="text-gray-300 font-medium">{total}</span> 条结果
            {searchParamQ && <span> — 关键词："{searchParamQ}"</span>}
          </p>

          {results.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-gray-600">
              <SearchIcon className="h-12 w-12 mb-3 opacity-30" />
              <p>未找到相关内容</p>
              <p className="mt-1 text-sm">尝试使用其他关键词或浏览分类</p>
              <Link
                to="/categories"
                className="mt-4 rounded-lg border border-gray-700 px-4 py-2 text-sm text-gray-400 hover:border-gray-600"
              >
                浏览分类
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {results.map((item) => (
                <Link
                  key={item.id}
                  to={`/knowledge/${item.id}`}
                  className="block rounded-xl border border-gray-800 bg-[#0a0a0a] p-5 hover:border-gray-700 transition-all group"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="min-w-0">
                      <h3 className="font-semibold group-hover:text-blue-400 transition-colors">
                        {item.title}
                      </h3>
                      <p className="mt-1.5 text-sm text-gray-500 line-clamp-2">
                        {item.summary}
                      </p>
                    </div>
                  </div>

                  <div className="mt-3 flex flex-wrap items-center gap-2">
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
                </Link>
              ))}
            </div>
          )}
        </>
      ) : (
        <div className="flex flex-col items-center justify-center py-20 text-gray-600">
          <SearchIcon className="h-12 w-12 mb-3 opacity-20" />
          <p>输入关键词开始搜索</p>
        </div>
      )}
    </div>
  );
}
