from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
import math
import traceback
import os
import uvicorn

# 导入本地模块
from database import get_db, init_db, engine
import crud
import schemas
import models

# 定义 lifespan event handler（替换已弃用的 on_event）
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    await init_db()
    print("[OK] 数据库已初始化")
    # 导入种子数据（幂等：已有数据则跳过）
    try:
        from seed_data import seed_data as seed_fn
        await seed_fn()
    except Exception as e:
        print(f"[WARN] 种子数据导入失败: {e}")
    yield
    # 关闭时执行（可选）
    await engine.dispose()
    print("[OK] 数据库引擎已释放")

# 创建FastAPI应用
app = FastAPI(
    title="测试知识系统API",
    description="专业的测试知识管理系统后端API",
    version="1.0.0",
    docs_url="/api/docs",  # Swagger UI文档
    redoc_url="/api/redoc",  # ReDoc文档
    openapi_url="/api/openapi.json",
    lifespan=lifespan  # 使用新的lifespan事件处理器
)

# CORS 中间件（允许前端访问）- 从环境变量读取，支持灵活配置
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误", "type": type(exc).__name__}
    )

# ========== 分类 API ==========
@app.get("/api/categories", response_model=List[schemas.CategoryResponse], tags=["分类"])
async def read_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """获取分类列表"""
    return await crud.get_categories(db, skip=skip, limit=limit)

@app.get("/api/categories/{category_id}", response_model=schemas.CategoryResponse, tags=["分类"])
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """获取分类详情"""
    db_category = await crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="分类不存在")
    return db_category

@app.post("/api/categories", response_model=schemas.CategoryResponse, tags=["分类"])
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    """创建分类"""
    return await crud.create_category(db, category=category)

# ========== 标签 API ==========
@app.get("/api/tags", response_model=List[schemas.TagResponse], tags=["标签"])
async def read_tags(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """获取标签列表"""
    return await crud.get_tags(db, skip=skip, limit=limit)

@app.post("/api/tags", response_model=schemas.TagResponse, tags=["标签"])
async def create_tag(tag: schemas.TagCreate, db: AsyncSession = Depends(get_db)):
    """创建标签"""
    existing = await crud.get_tag_by_slug(db, slug=tag.slug)
    if existing:
        raise HTTPException(status_code=400, detail="标签slug已存在")
    return await crud.create_tag(db, tag=tag)

@app.put("/api/tags/{tag_id}", response_model=schemas.TagResponse, tags=["标签"])
async def update_tag(tag_id: int, tag: schemas.TagUpdate, db: AsyncSession = Depends(get_db)):
    """更新标签"""
    db_tag = await crud.update_tag(db, tag_id=tag_id, tag=tag)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="标签不存在")
    return db_tag

@app.delete("/api/tags/{tag_id}", tags=["标签"])
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    """删除标签"""
    db_tag = await crud.delete_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="标签不存在")
    return {"message": "标签删除成功"}

# ========== 知识点 API ==========
@app.get("/api/knowledge", response_model=schemas.KnowledgeSearchResponse, tags=["知识点"])
async def read_knowledge_list(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    category_id: Optional[int] = Query(default=None, description="分类ID"),
    difficulty: Optional[str] = Query(default=None, description="难度（easy/medium/hard）"),
    tags: Optional[List[str]] = Query(default=None, description="标签列表"),
    search: Optional[str] = Query(default=None, description="搜索关键词"),
    order_by: str = Query(default="importance", description="排序字段（importance/view_count/created_at）"),
    order: str = Query(default="desc", description="排序方向（asc/desc）")
):
    """获取知识点列表（分页、搜索、过滤）"""
    skip = (page - 1) * page_size
    knowledge_list = await crud.get_knowledge_list(
        db, skip=skip, limit=page_size,
        category_id=category_id, difficulty=difficulty,
        tags=tags, search=search, order_by=order_by, order=order
    )

    total = await crud.count_knowledge(
        db, category_id=category_id, difficulty=difficulty,
        tags=tags, search=search
    )

    items = []
    for knowledge in knowledge_list:
        item = schemas.KnowledgeListItem(
            id=knowledge.id, title=knowledge.title, slug=knowledge.slug,
            summary=knowledge.summary, difficulty=knowledge.difficulty,
            importance=knowledge.importance, category_id=knowledge.category_id,
            tags=knowledge.tags if knowledge.tags else [],
            view_count=knowledge.view_count, created_at=knowledge.created_at
        )
        if knowledge.category_id:
            category = await crud.get_category_by_id(db, category_id=knowledge.category_id)
            if category:
                item.category_name = category.name
        items.append(item)

    return schemas.KnowledgeSearchResponse(
        items=items, total=total, page=page,
        page_size=page_size,
        total_pages=max(1, math.ceil(total / page_size))
    )

@app.get("/api/knowledge/{knowledge_id}", response_model=schemas.KnowledgeResponse, tags=["知识点"])
async def read_knowledge(knowledge_id: int, db: AsyncSession = Depends(get_db)):
    """获取知识点详情"""
    db_knowledge = await crud.get_knowledge_by_id(db, knowledge_id=knowledge_id)
    if db_knowledge is None:
        raise HTTPException(status_code=404, detail="知识点不存在")
    
    # 增加查看次数
    await crud.increment_view_count(db, knowledge_id=knowledge_id)
    
    # 获取分类信息
    category = await crud.get_category_by_id(db, category_id=db_knowledge.category_id)
    category_response = schemas.CategoryResponse(
        id=category.id,
        name=category.name,
        slug=category.slug,
        description=category.description,
        icon=category.icon,
        order=category.order,
        created_at=category.created_at
    ) if category else None
    
    # 构建响应
    response = schemas.KnowledgeResponse(
        id=db_knowledge.id,
        title=db_knowledge.title,
        slug=db_knowledge.slug,
        content=db_knowledge.content,
        summary=db_knowledge.summary,
        difficulty=db_knowledge.difficulty,
        importance=db_knowledge.importance,
        category_id=db_knowledge.category_id,
        subcategory=db_knowledge.subcategory,
        code_examples=db_knowledge.code_examples if db_knowledge.code_examples else [],
        video_url=db_knowledge.video_url,
        quiz=db_knowledge.quiz if db_knowledge.quiz else [],
        view_count=db_knowledge.view_count,
        like_count=db_knowledge.like_count,
        tags=db_knowledge.tags if db_knowledge.tags else [],
        source=db_knowledge.source,
        related_ids=db_knowledge.related_ids if db_knowledge.related_ids else [],
        created_at=db_knowledge.created_at,
        updated_at=db_knowledge.updated_at,
        category=category_response,
        tags_list=[]  # 简化：不加载完整标签对象
    )
    
    return response

@app.post("/api/knowledge", response_model=schemas.KnowledgeResponse, tags=["知识点"])
async def create_knowledge(knowledge: schemas.KnowledgeCreate, db: AsyncSession = Depends(get_db)):
    """创建知识点"""
    return await crud.create_knowledge(db, knowledge=knowledge)

@app.put("/api/knowledge/{knowledge_id}", response_model=schemas.KnowledgeResponse, tags=["知识点"])
async def update_knowledge(
    knowledge_id: int,
    knowledge: schemas.KnowledgeUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新知识点"""
    db_knowledge = await crud.update_knowledge(db, knowledge_id=knowledge_id, knowledge=knowledge)
    if db_knowledge is None:
        raise HTTPException(status_code=404, detail="知识点不存在")
    return db_knowledge

@app.delete("/api/knowledge/{knowledge_id}", tags=["知识点"])
async def delete_knowledge(knowledge_id: int, db: AsyncSession = Depends(get_db)):
    """删除知识点"""
    db_knowledge = await crud.delete_knowledge(db, knowledge_id=knowledge_id)
    if db_knowledge is None:
        raise HTTPException(status_code=404, detail="知识点不存在")
    return {"message": "删除成功"}

# ========== 统计 API ==========
@app.get("/api/stats", tags=["统计"])
async def read_stats(db: AsyncSession = Depends(get_db)):
    """获取系统统计信息"""
    # 知识点总数
    total_knowledge = await crud.count_knowledge(db)
    
    # 分类总数
    categories = await crud.get_categories(db)
    total_categories = len(categories)
    
    # 标签总数
    tags = await crud.get_tags(db)
    total_tags = len(tags)
    
    # 总查看次数
    result = await db.execute(select(func.sum(models.Knowledge.view_count)))
    total_views = result.scalar() or 0
    
    return {
        "total_knowledge": total_knowledge,
        "total_categories": total_categories,
        "total_tags": total_tags,
        "total_views": total_views
    }

# ========== 反馈 API ==========
@app.post("/api/feedback", response_model=schemas.FeedbackResponse, tags=["反馈"])
async def create_feedback(feedback: schemas.FeedbackCreate, db: AsyncSession = Depends(get_db)):
    """提交反馈（纠错/建议/提问）"""
    return await crud.create_feedback(db, feedback=feedback)

@app.get("/api/feedback", response_model=schemas.FeedbackListResponse, tags=["反馈"])
async def read_feedbacks(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: Optional[str] = Query(default=None, description="状态过滤")
):
    """获取反馈列表"""
    skip = (page - 1) * page_size
    items = await crud.get_feedbacks(db, skip=skip, limit=page_size, status=status)
    total = await crud.count_feedbacks(db, status=status)
    return schemas.FeedbackListResponse(items=items, total=total)

@app.put("/api/feedback/{feedback_id}/status", tags=["反馈"])
async def update_feedback_status(
    feedback_id: int,
    status: str = Query(..., pattern="^(pending|resolved|dismissed)$"),
    db: AsyncSession = Depends(get_db)
):
    """更新反馈状态"""
    result = await crud.update_feedback_status(db, feedback_id=feedback_id, status=status)
    if result is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return {"message": f"反馈状态已更新为 {status}"}

# ========== 根路由 ==========
@app.get("/")
async def root():
    """API根路由"""
    return {
        "message": "测试知识系统API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }

# ========== SPA 静态文件服务（必须放在所有 API 路由之后） ==========
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dist")

if os.path.exists(FRONTEND_BUILD_DIR):
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse

    # SPA fallback：所有非API路由返回 index.html
    @app.get("/{fullpath:path}")
    async def serve_spa(fullpath: str):
        """提供前端 SPA（单页应用）- API已在前面匹配"""
        file_path = os.path.join(FRONTEND_BUILD_DIR, fullpath)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        # SPA fallback：返回 index.html
        return FileResponse(os.path.join(FRONTEND_BUILD_DIR, "index.html"))

    print(f"[OK] SPA 服务已启用：{FRONTEND_BUILD_DIR}")
else:
    print(f"[WARN] 前端构建目录不存在：{FRONTEND_BUILD_DIR}")

# ========== 启动服务器 ==========
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
