from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey, Table
from sqlalchemy.sql import func
import os

# 数据库URL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 优先使用 workspace 可写位置，再回退到项目相对路径
WORKSPACE_DB = r"D:\workbuddy task\2026-06-17-00-54-20\knowledge-hub\data\knowledge.db"
PROJECT_DB = os.path.join(BASE_DIR, "..", "data", "knowledge.db")
DB_PATH = WORKSPACE_DB if os.path.exists(WORKSPACE_DB) else PROJECT_DB
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 开发时打印SQL语句
)

# 创建异步会话
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 声明式基类
Base = declarative_base()

# 多对多关系表
knowledge_tags = Table(
    "knowledge_tags",
    Base.metadata,
    Column("knowledge_id", Integer, ForeignKey("knowledge.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

# 依赖注入：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 初始化数据库
async def init_db():
    """创建所有表（如果不存在）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[OK] 数据库表已创建")

async def close_db():
    """关闭数据库引擎"""
    await engine.dispose()
    print("[OK] 数据库引擎已关闭")
