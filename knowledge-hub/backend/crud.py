from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
import models
import schemas

# ========== 分类 CRUD ==========
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Category).order_by(models.Category.order).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_category_by_id(db: AsyncSession, category_id: int):
    result = await db.execute(select(models.Category).where(models.Category.id == category_id))
    return result.scalars().first()

async def get_category_by_slug(db: AsyncSession, slug: str):
    result = await db.execute(select(models.Category).where(models.Category.slug == slug))
    return result.scalars().first()

async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

# ========== 标签 CRUD ==========
async def get_tags(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Tag).order_by(models.Tag.count.desc()).offset(skip).limit(limit))
    return result.scalars().all()

async def get_tag_by_id(db: AsyncSession, tag_id: int):
    result = await db.execute(select(models.Tag).where(models.Tag.id == tag_id))
    return result.scalars().first()

async def create_tag(db: AsyncSession, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.model_dump())
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

async def update_tag(db: AsyncSession, tag_id: int, tag: schemas.TagUpdate):
    result = await db.execute(select(models.Tag).where(models.Tag.id == tag_id))
    db_tag = result.scalars().first()
    if not db_tag:
        return None
    update_data = tag.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tag, field, value)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

async def delete_tag(db: AsyncSession, tag_id: int):
    result = await db.execute(select(models.Tag).where(models.Tag.id == tag_id))
    db_tag = result.scalars().first()
    if not db_tag:
        return None
    await db.delete(db_tag)
    await db.commit()
    return db_tag

async def get_tag_by_slug(db: AsyncSession, slug: str):
    result = await db.execute(select(models.Tag).where(models.Tag.slug == slug))
    return result.scalars().first()

# ========== 知识点 CRUD ==========
async def get_knowledge_list(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    category_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None,
    order_by: str = "importance",
    order: str = "desc"
):
    # 构建查询
    query = select(models.Knowledge)
    
    # 过滤条件
    filters = []
    if category_id:
        filters.append(models.Knowledge.category_id == category_id)
    if difficulty:
        filters.append(models.Knowledge.difficulty == difficulty)
    if tags:
        # 简化：检查tags字段（JSON）是否包含任意指定标签
        for tag in tags:
            filters.append(models.Knowledge.tags.contains([tag]))
    if search:
        search_filter = or_(
            models.Knowledge.title.contains(search),
            models.Knowledge.summary.contains(search),
            models.Knowledge.content.contains(search)
        )
        filters.append(search_filter)
    
    if filters:
        query = query.where(and_(*filters))
    
    # 排序
    if order_by == "importance":
        order_col = models.Knowledge.importance
    elif order_by == "view_count":
        order_col = models.Knowledge.view_count
    elif order_by == "created_at":
        order_col = models.Knowledge.created_at
    else:
        order_col = models.Knowledge.importance
    
    if order == "desc":
        query = query.order_by(order_col.desc())
    else:
        query = query.order_by(order_col.asc())
    
    # 分页
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

async def count_knowledge(
    db: AsyncSession,
    category_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None
):
    """统计知识点总数（用于分页）"""
    query = select(func.count()).select_from(models.Knowledge)
    
    filters = []
    if category_id:
        filters.append(models.Knowledge.category_id == category_id)
    if difficulty:
        filters.append(models.Knowledge.difficulty == difficulty)
    if tags:
        for tag in tags:
            filters.append(models.Knowledge.tags.contains([tag]))
    if search:
        search_filter = or_(
            models.Knowledge.title.contains(search),
            models.Knowledge.summary.contains(search),
            models.Knowledge.content.contains(search)
        )
        filters.append(search_filter)
    
    if filters:
        query = query.where(and_(*filters))
    
    result = await db.execute(query)
    return result.scalar_one()

async def get_knowledge_by_id(db: AsyncSession, knowledge_id: int):
    result = await db.execute(select(models.Knowledge).where(models.Knowledge.id == knowledge_id))
    return result.scalars().first()

async def get_knowledge_by_slug(db: AsyncSession, slug: str):
    result = await db.execute(select(models.Knowledge).where(models.Knowledge.slug == slug))
    return result.scalars().first()

async def create_knowledge(db: AsyncSession, knowledge: schemas.KnowledgeCreate):
    # 转换tags列表为JSON存储
    knowledge_data = knowledge.model_dump()
    tags_list = knowledge_data.pop("tags", [])
    
    db_knowledge = models.Knowledge(**knowledge_data)
    db_knowledge.tags = tags_list  # 直接赋值JSON
    
    db.add(db_knowledge)
    await db.commit()
    await db.refresh(db_knowledge)
    return db_knowledge

async def update_knowledge(db: AsyncSession, knowledge_id: int, knowledge: schemas.KnowledgeUpdate):
    result = await db.execute(select(models.Knowledge).where(models.Knowledge.id == knowledge_id))
    db_knowledge = result.scalars().first()
    
    if not db_knowledge:
        return None
    
    # 更新字段
    update_data = knowledge.model_dump(exclude_unset=True)
    if "tags" in update_data:
        db_knowledge.tags = update_data.pop("tags")
    
    for field, value in update_data.items():
        setattr(db_knowledge, field, value)
    
    await db.commit()
    await db.refresh(db_knowledge)
    return db_knowledge

async def delete_knowledge(db: AsyncSession, knowledge_id: int):
    result = await db.execute(select(models.Knowledge).where(models.Knowledge.id == knowledge_id))
    db_knowledge = result.scalars().first()
    
    if not db_knowledge:
        return None
    
    await db.delete(db_knowledge)
    await db.commit()
    return db_knowledge

async def increment_view_count(db: AsyncSession, knowledge_id: int):
    """增加查看次数"""
    result = await db.execute(select(models.Knowledge).where(models.Knowledge.id == knowledge_id))
    db_knowledge = result.scalars().first()
    
    if db_knowledge:
        db_knowledge.view_count += 1
        await db.commit()
        await db.refresh(db_knowledge)
    
    return db_knowledge

# ========== 反馈 CRUD ==========
async def create_feedback(db: AsyncSession, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.model_dump())
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback

async def get_feedbacks(db: AsyncSession, skip: int = 0, limit: int = 20, status: Optional[str] = None):
    query = select(models.Feedback).order_by(models.Feedback.created_at.desc())
    if status:
        query = query.where(models.Feedback.status == status)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

async def count_feedbacks(db: AsyncSession, status: Optional[str] = None):
    query = select(func.count()).select_from(models.Feedback)
    if status:
        query = query.where(models.Feedback.status == status)
    result = await db.execute(query)
    return result.scalar_one()

async def update_feedback_status(db: AsyncSession, feedback_id: int, status: str):
    result = await db.execute(select(models.Feedback).where(models.Feedback.id == feedback_id))
    db_feedback = result.scalars().first()
    if not db_feedback:
        return None
    db_feedback.status = status
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback
