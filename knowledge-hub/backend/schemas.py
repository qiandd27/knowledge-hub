from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

# ========== 分类 Schemas ==========
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None
    order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ========== 标签 Schemas ==========
class TagBase(BaseModel):
    name: str
    slug: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None

class TagResponse(TagBase):
    id: int
    count: int = 0
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ========== 知识点 Schemas ==========
class KnowledgeBase(BaseModel):
    title: str
    slug: str
    content: str  # MDX格式
    summary: Optional[str] = None
    difficulty: str = "medium"  # easy, medium, hard
    importance: int = Field(default=3, ge=1, le=5)  # 1-5
    category_id: int
    subcategory: Optional[str] = None
    code_examples: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    video_url: Optional[str] = None
    quiz: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    tags: Optional[List[str]] = Field(default_factory=list)
    source: Optional[str] = None
    related_ids: Optional[List[int]] = Field(default_factory=list)

class KnowledgeCreate(KnowledgeBase):
    pass

class KnowledgeUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    difficulty: Optional[str] = None
    importance: Optional[int] = Field(default=None, ge=1, le=5)
    category_id: Optional[int] = None
    subcategory: Optional[str] = None
    code_examples: Optional[List[Dict[str, Any]]] = None
    video_url: Optional[str] = None
    quiz: Optional[List[Dict[str, Any]]] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    related_ids: Optional[List[int]] = None

class KnowledgeResponse(KnowledgeBase):
    id: int
    view_count: int = 0
    like_count: int = 0
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    tags_list: Optional[List[TagResponse]] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)

class KnowledgeListItem(BaseModel):
    """知识点列表项（简化版，用于列表展示）"""
    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    difficulty: str
    importance: int
    category_id: int
    category_name: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    view_count: int = 0
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ========== 分页通用 Schemas ==========
class PaginatedResponse(BaseModel):
    """通用分页响应"""
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int

# ========== 搜索 Schemas ==========
class KnowledgeSearchParams(BaseModel):
    q: Optional[str] = None  # 搜索关键词
    category_id: Optional[int] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    order_by: str = "importance"  # importance, view_count, created_at
    order: str = "desc"  # asc, desc
    page: int = 1
    page_size: int = 20

class KnowledgeSearchResponse(BaseModel):
    items: List[KnowledgeListItem]
    total: int
    page: int
    page_size: int
    total_pages: int

# ========== 反馈 Schemas ==========
class FeedbackBase(BaseModel):
    knowledge_id: int
    type: str  # correction, suggestion, question
    content: str
    contact: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackListResponse(BaseModel):
    """反馈列表响应"""
    items: List['FeedbackResponse']
    total: int

class FeedbackResponse(FeedbackBase):
    id: int
    status: str = "pending"
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
