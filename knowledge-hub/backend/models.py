from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey, Table
from sqlalchemy.sql import func
from database import Base

# 多对多关系表（在database.py中定义，这里导入）
from database import knowledge_tags

# 知识点表
class Knowledge(Base):
    __tablename__ = "knowledge"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, index=True)
    content = Column(Text, nullable=False)  # MDX格式内容
    summary = Column(Text)
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    importance = Column(Integer, default=3)  # 1-5
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    subcategory = Column(String(100))
    code_examples = Column(JSON, default=[])  # 代码示例列表
    video_url = Column(String(500))
    quiz = Column(JSON, default=[])  # 测验题
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    tags = Column(JSON, default=[])  # 标签列表（冗余存储，便于查询）
    source = Column(String(500))  # 数据来源
    related_ids = Column(JSON, default=[])  # 相关知识ID
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# 分类表
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), unique=True, index=True)
    description = Column(Text)
    icon = Column(String(50))  # 图标名称（lucide图标）
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

# 标签表
class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    slug = Column(String(50), unique=True, index=True)
    count = Column(Integer, default=0)  # 使用该标签的知识点数量
    created_at = Column(DateTime, default=func.now())

# 代码示例表（也可以存储在Knowledge的JSON字段中，这里作为独立表提供）
class CodeExample(Base):
    __tablename__ = "code_examples"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge.id"), nullable=False)
    title = Column(String(200), nullable=False)
    language = Column(String(50), nullable=False)  # python, javascript, sql, etc.
    code = Column(Text, nullable=False)
    description = Column(Text)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

# 视频表（也可以存储在Knowledge的字段中，这里作为独立表提供）
class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge.id"), nullable=False)
    title = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
    duration = Column(Integer)  # 秒
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())

# 测验表（也可以存储在Knowledge的JSON字段中，这里作为独立表提供）
class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge.id"), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # 选项列表
    answer = Column(Integer, nullable=False)  # 正确答案索引
    explanation = Column(Text)  # 解析
    created_at = Column(DateTime, default=func.now())

# 反馈表
class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge.id"), nullable=False)
    type = Column(String(50), nullable=False)  # correction, suggestion, question
    content = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    contact = Column(String(200))  # 联系方式（可选）
    created_at = Column(DateTime, default=func.now())
