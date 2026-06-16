import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';
import type { Category, KnowledgeItem } from '@/services/api';
import { fetchCategories, fetchKnowledgeList, DIFFICULTY_LABELS, DIFFICULTY_COLORS } from '@/services/api';

interface CategoryWithCount extends Category {
  knowledgeCount: number;
  items: KnowledgeItem[];
}

export default function Categories() {
  const [categories, setCategories] = useState<CategoryWithCount[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const cats = await fetchCategories();

        const enriched = await Promise.all(
          cats.map(async (cat) => {
            const data = await fetchKnowledgeList({
              category_id: cat.id,
              page_size: 5,
              order_by: 'importance',
              order: 'desc',
            });
            return {
              ...cat,
              knowledgeCount: data.total,
              items: data.items,
            };
          })
        );

        setCategories(enriched.filter((c) => c.knowledgeCount > 0));
      } catch (err) {
        console.error('Categories error:', err);
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

  return (
    <div className="space-y-8 p-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">知识分类</h2>
        <p className="mt-1 text-sm text-gray-500">
          {categories.length} 个分类，按领域组织知识体系
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {categories.map((cat) => (
          <div
            key={cat.id}
            className="rounded-xl border border-gray-800 bg-[#0a0a0a] overflow-hidden"
          >
            {/* Category header */}
            <Link
              to={`/knowledge?category_id=${cat.id}`}
              className="flex items-center justify-between border-b border-gray-800 p-5 hover:bg-gray-800/30 transition-colors group"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">{cat.icon || '📁'}</span>
                <div>
                  <h3 className="font-semibold group-hover:text-blue-400 transition-colors">
                    {cat.name}
                  </h3>
                  <p className="text-xs text-gray-500">{cat.description}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className="rounded-full bg-gray-800 px-2.5 py-0.5 text-xs text-gray-400">
                  {cat.knowledgeCount}
                </span>
                <ChevronRight className="h-4 w-4 text-gray-600 group-hover:text-gray-400" />
              </div>
            </Link>

            {/* Sample items */}
            {cat.items.length > 0 && (
              <div className="divide-y divide-gray-800/50">
                {cat.items.map((item) => (
                  <Link
                    key={item.id}
                    to={`/knowledge/${item.id}`}
                    className="flex items-center justify-between px-5 py-3 hover:bg-gray-800/20 transition-colors"
                  >
                    <div className="min-w-0">
                      <p className="truncate text-sm font-medium">{item.title}</p>
                      <p className="truncate text-xs text-gray-500">{item.summary}</p>
                    </div>
                    <span className={`ml-3 shrink-0 rounded-md border px-2 py-0.5 text-[10px] font-medium ${DIFFICULTY_COLORS[item.difficulty] || ''}`}>
                      {DIFFICULTY_LABELS[item.difficulty] || item.difficulty}
                    </span>
                  </Link>
                ))}
              </div>
            )}

            {cat.knowledgeCount > 5 && (
              <div className="border-t border-gray-800 px-5 py-2">
                <Link
                  to={`/knowledge?category_id=${cat.id}`}
                  className="text-xs text-blue-400 hover:text-blue-300"
                >
                  查看全部 {cat.knowledgeCount} 条 →
                </Link>
              </div>
            )}
          </div>
        ))}

        {categories.length === 0 && (
          <div className="col-span-2 flex justify-center py-16 text-gray-600">
            暂无分类数据
          </div>
        )}
      </div>
    </div>
  );
}
