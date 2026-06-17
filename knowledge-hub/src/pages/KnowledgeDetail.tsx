import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Star,
  Eye,
  Heart,
  ExternalLink,
  AlertCircle,
  ChevronRight,
  Code,
  Play,
  HelpCircle,
} from 'lucide-react';
import type { KnowledgeDetail as DetailType } from '@/services/api';
import {
  fetchKnowledgeDetail,
  DIFFICULTY_LABELS,
  DIFFICULTY_COLORS,
} from '@/services/api';

export default function KnowledgeDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [data, setData] = useState<DetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [quizOpen, setQuizOpen] = useState<number | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetchKnowledgeDetail(parseInt(id, 10))
      .then(setData)
      .catch((err) => setError(`加载失败: ${err.message}`))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4 p-8">
        <AlertCircle className="h-12 w-12 text-red-400" />
        <p className="text-gray-400">{error || '知识点不存在'}</p>
        <button
          onClick={() => navigate('/knowledge')}
          className="rounded-lg border border-gray-700 px-4 py-2 text-sm text-gray-300 hover:border-gray-600"
        >
          返回知识库
        </button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl space-y-8 p-8">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-gray-500">
        <Link to="/knowledge" className="hover:text-gray-300">
          <ArrowLeft className="h-4 w-4 inline mr-1" />
          知识库
        </Link>
        {data.category && (
          <>
            <ChevronRight className="h-3 w-3" />
            <Link
              to={`/knowledge?category_id=${data.category.id}`}
              className="hover:text-gray-300"
            >
              {data.category.name}
            </Link>
          </>
        )}
      </div>

      {/* Title */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">{data.title}</h1>
        <p className="mt-3 text-lg text-gray-400">{data.summary}</p>

        <div className="mt-4 flex flex-wrap items-center gap-3">
          <span className={`rounded-md border px-2.5 py-1 text-xs font-medium ${DIFFICULTY_COLORS[data.difficulty] || ''}`}>
            {DIFFICULTY_LABELS[data.difficulty] || data.difficulty}
          </span>

          <span className="flex items-center gap-1 text-sm text-gray-500">
            <Star className="h-4 w-4 fill-amber-500 text-amber-500" />
            {data.importance}/5 重要性
          </span>

          <span className="flex items-center gap-1 text-sm text-gray-500">
            <Eye className="h-4 w-4" />
            {data.view_count} 阅读
          </span>

          <span className="flex items-center gap-1 text-sm text-gray-500">
            <Heart className="h-4 w-4" />
            {data.like_count} 点赞
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="prose prose-invert max-w-none rounded-xl border border-gray-800 bg-[#0a0a0a] p-8">
        <pre className="text-gray-300 leading-relaxed whitespace-pre-wrap font-sans text-sm break-words">
          {data.content}
        </pre>
      </div>

      {/* Code Examples */}
      {data.code_examples && data.code_examples.length > 0 && (
        <section>
          <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold">
            <Code className="h-5 w-5" />
            代码示例
          </h3>
          <div className="space-y-4">
            {data.code_examples.map((ex, i) => (
              <div key={i} className="rounded-xl border border-gray-800 bg-[#0a0a0a] overflow-hidden">
                <div className="flex items-center justify-between border-b border-gray-800 px-4 py-2">
                  <span className="text-xs text-gray-500">{ex.language}</span>
                  <span className="text-xs text-gray-600">{ex.description}</span>
                </div>
                <pre className="p-4 text-sm text-gray-300 overflow-x-auto">
                  <code>{ex.code}</code>
                </pre>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Video */}
      {data.video_url && (
        <section>
          <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold">
            <Play className="h-5 w-5" />
            视频演练
          </h3>
          <div className="rounded-xl border border-gray-800 bg-[#0a0a0a] overflow-hidden">
            <iframe
              src={data.video_url}
              className="w-full aspect-video"
              allowFullScreen
              title="Video tutorial"
            />
          </div>
        </section>
      )}

      {/* Quiz */}
      {data.quiz && data.quiz.length > 0 && (
        <section>
          <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold">
            <HelpCircle className="h-5 w-5" />
            互动测验
          </h3>
          <div className="space-y-3">
            {data.quiz.map((q, i) => (
              <div key={i} className="rounded-xl border border-gray-800 bg-[#0a0a0a] overflow-hidden">
                <button
                  onClick={() => setQuizOpen(quizOpen === i ? null : i)}
                  className="w-full px-5 py-4 text-left hover:bg-gray-800/30 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">
                      Q{i + 1}. {q.question}
                    </span>
                    <ChevronRight
                      className={`h-4 w-4 text-gray-600 transition-transform ${
                        quizOpen === i ? 'rotate-90' : ''
                      }`}
                    />
                  </div>
                </button>
                {quizOpen === i && (
                  <div className="border-t border-gray-800 px-5 py-4 space-y-2">
                    {q.options.map((opt, j) => (
                      <div
                        key={j}
                        className={`rounded-lg border px-3 py-2 text-sm ${
                          j === q.answer
                            ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'
                            : 'border-gray-700 text-gray-500'
                        }`}
                      >
                        {String.fromCharCode(65 + j)}. {opt}
                        {j === q.answer && ' ✓'}
                      </div>
                    ))}
                    <p className="mt-3 text-sm text-gray-500">
                      <span className="text-blue-400">解析：</span>
                      {q.explanation}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Meta */}
      <div className="flex flex-wrap items-center gap-4 text-xs text-gray-600">
        {data.source && (
          <a
            href={data.source}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 hover:text-gray-400"
          >
            <ExternalLink className="h-3 w-3" />
            来源
          </a>
        )}
        <span>创建于 {new Date(data.created_at).toLocaleDateString('zh-CN')}</span>
        <span>更新于 {new Date(data.updated_at).toLocaleDateString('zh-CN')}</span>
      </div>

      {/* Tags */}
      {data.tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {data.tags.map((tag) => (
            <Link
              key={tag}
              to={`/knowledge?tags=${encodeURIComponent(tag)}`}
              className="rounded-full border border-gray-700 px-3 py-1 text-xs text-gray-400 hover:border-blue-500/50 hover:text-blue-400 transition-colors"
            >
              {tag}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
