"""
数据库初始化脚本 - 创建表并导入种子数据
"""
import asyncio
import os
import sys
import json

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select
from database import init_db, AsyncSessionLocal, engine
import models
import schemas

# ========== 分类种子数据 ==========
CATEGORIES_DATA = [
    {
        "name": "灾难恢复测试",
        "slug": "disaster-recovery",
        "description": "故障注入、混沌工程、容灾演练",
        "icon": "ShieldAlert",
        "order": 1
    },
    {
        "name": "性能与压测",
        "slug": "performance",
        "description": "压力测试、负载测试、性能优化",
        "icon": "Zap",
        "order": 2
    },
    {
        "name": "安全测试",
        "slug": "security",
        "description": "渗透测试、漏洞扫描、安全防护",
        "icon": "Lock",
        "order": 3
    },
    {
        "name": "自动化测试",
        "slug": "automation",
        "description": "测试框架、CI/CD、持续集成",
        "icon": "Bot",
        "order": 4
    },
    {
        "name": "数据库测试",
        "slug": "database",
        "description": "SQL、NoSQL、数据一致性",
        "icon": "Database",
        "order": 5
    },
    {
        "name": "网络协议",
        "slug": "network",
        "description": "TCP/UDP/HTTP/WebSocket",
        "icon": "Network",
        "order": 6
    },
    {
        "name": "服务器架构",
        "slug": "architecture",
        "description": "微服务、分布式、消息队列",
        "icon": "Server",
        "order": 7
    },
    {
        "name": "测试理论",
        "slug": "theory",
        "description": "测试方法论、测试设计、测试流程",
        "icon": "BookOpen",
        "order": 8
    },
    {
        "name": "AI与游戏测试",
        "slug": "ai-gaming",
        "description": "AI测试、游戏测试、AIGC内容",
        "icon": "Gamepad2",
        "order": 9
    },
]

# ========== 知识点种子数据 ==========
KNOWLEDGE_DATA = [
    {
        "title": "RTO/RPO/SLA - 容灾核心指标",
        "slug": "rto-rpo-sla",
        "summary": "灾难恢复的关键指标：RTO定义恢复时间，RPO定义数据丢失量，SLA定义服务等级。",
        "content": """# RTO/RPO/SLA 容灾核心指标

## 核心定义

| 指标 | 英文 | 定义 | 业务影响 |
|------|------|------|---------|
| **RTO** | Recovery Time Objective | 故障发生到系统恢复的时间 | 业务中断时长 |
| **RPO** | Recovery Point Objective | 数据可恢复的时间点 | 数据丢失量 |
| **SLA** | Service Level Agreement | 服务等级协议 | 系统可用性承诺 |

## 各等级容灾标准

- **L1（本地容灾）**：RTO分钟级、RPO 0、成本低
- **L2（异地备份）**：RTO小时级、RPO分钟级
- **L3（异地活动）**：RTO分钟级、RPO秒级
- **L4（双活）**：RTO秒级、RPO 0
- **L5（异地双活）**：RTO/RPO近0

## 容灾测试方法

1. **桌面演练（Paper Test）**：流程推演
2. **模拟演练（Simulation）**：小范围测试
3. **全链路演练**：生产级别切换
""",
        "difficulty": "medium",
        "importance": 5,
        "category_slug": "disaster-recovery",
        "subcategory": "容灾指标",
        "tags": ["RTO", "RPO", "SLA", "容灾等级", "容灾测试"],
        "source": "GB/T 22239-2019, ISO 22301"
    },
    {
        "title": "混沌工程与Chaos Mesh",
        "slug": "chaos-engineering",
        "summary": "通过主动注入故障验证系统韧性，腾讯互娱基于Chaos Mesh实现了每周150+次演练。",
        "content": """# 混沌工程 Chaos Engineering

## 五大原则

1. **建立稳定状态假设**：定义系统正常运行的指标
2. **多样化真实事件**：模拟真实故障场景
3. **生产环境实验**：在生产环境验证
4. **自动化持续演练**：嵌入CI/CD流程
5. **控制爆炸半径**：限制故障影响范围

## Chaos Mesh 故障注入能力

- **资源类故障**：CPU/内存/磁盘压力
- **容器类故障**：Pod杀死、节点故障
- **网络类故障**：延迟、丢包、乱序
- **IO类故障**：存储IO异常、磁盘满
- **精细化流量**：针对特定账号注入

## 腾讯互娱实践

- 每周演练：>150次
- 参与人数：>50人
- 提前发现问题：>100个/周
- 演练效率提升：10倍+
""",
        "difficulty": "hard",
        "importance": 5,
        "category_slug": "disaster-recovery",
        "subcategory": "混沌工程",
        "tags": ["Chaos Mesh", "混沌工程", "故障注入", "腾讯", "容灾"],
        "source": "腾讯云社区 https://cloud.tencent.com/developer/article/1826103"
    },
    {
        "title": "TCP三次握手与四次挥手",
        "slug": "tcp-handshake",
        "summary": "TCP连接建立与断开过程，是网络协议面试必考点。",
        "content": """# TCP三次握手与四次挥手

## 三次握手（建立连接）

```
客户端          服务端
  |  SYN=1     |
  |------------>|  seq=x
  |             |
  |<------------|  SYN=1, ACK=1
  |   seq=y, ack=x+1
  |
  |------------>|  ACK=1
  |   seq=x+1, ack=y+1
```

**为什么三次？**
- 防止已失效的连接请求突然到达
- 确认双方的发送/接收能力
- 同步初始序列号

## 四次挥手（断开连接）

```
客户端          服务端
  |  FIN=1     |
  |------------>|
  |             |
  |<------------|  ACK
  |             |
  |<------------|  FIN
  |             |
  |------------>|  ACK
```

**状态流转**：FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED

**为什么TIME_WAIT等待2MSL？**
- 确保最后一个ACK到达
- 让旧连接的数据包在网络中消失
""",
        "difficulty": "medium",
        "importance": 5,
        "category_slug": "network",
        "subcategory": "传输层",
        "tags": ["TCP", "三次握手", "四次挥手", "网络协议"],
        "source": "RFC 793"
    },
    {
        "title": "缓存三大问题：击穿、雪崩、穿透",
        "slug": "cache-problems",
        "summary": "Redis缓存系统中常见的三类故障及解决方案。",
        "content": """# 缓存三大问题

## 1. 缓存击穿 (Hotspot Invalid)

**场景**：热点key过期瞬间，大量请求打到DB

**解决方案**：
- 互斥锁（setnx）：只有一个线程能查DB
- 逻辑过期：value里存过期时间，业务层判断
- 永不过期：定期异步刷新

## 2. 缓存雪崩 (Avalanche)

**场景**：大量key同时过期，DB压力剧增

**解决方案**：
- 过期时间随机化：避免同时过期
- 多级缓存：本地缓存 + Redis
- 熔断降级：限流保护DB
- 预热：定时刷新热点key

## 3. 缓存穿透 (Penetration)

**场景**：查询不存在的数据，每次都打到DB

**解决方案**：
- 布隆过滤器：判断key是否存在
- 空值缓存：缓存null值（短时间）
- 接口校验：参数合法性检查

## 监控指标

- 缓存命中率：>95%
- 缓存响应时间：<5ms
- DB查询QPS：异常告警
""",
        "difficulty": "medium",
        "importance": 5,
        "category_slug": "database",
        "subcategory": "Redis",
        "tags": ["缓存", "Redis", "击穿", "雪崩", "穿透"],
        "source": "Redis官方文档 + 字节跳动技术博客"
    },
    {
        "title": "游戏测试用例设计方法",
        "slug": "game-test-case-design",
        "summary": "游戏测试的用例设计方法论：等价类、边界值、场景法、错误猜测法。",
        "content": """# 游戏测试用例设计方法

## 功能测试

### 等价类划分
- **有效等价类**：合法的输入
- **无效等价类**：非法的输入

例：装备等级（1-100级）
- 有效：1, 50, 100
- 无效：0, -1, 101, "abc"

### 边界值分析
- 上点：100
- 离点：101
- 内点：50
- 下点：1
- 离下点：0

### 场景法
- 基本流：玩家正常游戏流程
- 备选流：异常处理路径
- 异常流：错误情况

## 专项测试

### 数值测试
- 属性计算公式
- 暴击、闪避、伤害浮动
- 经济系统（产出/消耗平衡）

### 兼容性测试
- iOS/Android各版本
- 不同分辨率
- 不同机型性能

### 网络测试
- 弱网环境（2G/3G/4G）
- 断网重连
- 延迟测试（100-500ms）

### 反作弊测试
- 协议重放
- 数据篡改
- 加速外挂检测
- 修改器检测
""",
        "difficulty": "medium",
        "importance": 5,
        "category_slug": "theory",
        "subcategory": "测试方法",
        "tags": ["测试用例", "等价类", "边界值", "场景法", "游戏测试"],
        "source": "ISTQB测试工程师认证 + 西山居内部培训"
    },
]

async def seed_data():
    """导入种子数据"""
    # 先初始化表
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # 检查是否已有数据
        result = await db.execute(select(models.Category))
        existing = result.scalars().first()
        if existing:
            print("⚠️ 数据库已有数据，跳过种子导入")
            return
        
        # 导入分类
        print("📂 导入分类数据...")
        category_map = {}  # slug -> id
        for cat_data in CATEGORIES_DATA:
            category = models.Category(**cat_data)
            db.add(category)
            await db.flush()  # 获取ID
            category_map[cat_data["slug"]] = category.id
        
        # 导入知识点
        print("[INFO] 导入知识点数据...")
        for know_data in KNOWLEDGE_DATA:
            # 转换category_slug为category_id
            category_id = category_map.get(know_data.pop("category_slug"))
            if not category_id:
                print(f"⚠️ 跳过 {know_data.get('title')}：找不到分类")
                continue
            
            # 创建知识点
            knowledge = models.Knowledge(
                category_id=category_id,
                **know_data
            )
            db.add(knowledge)
        
        await db.commit()
        print(f"[OK] 成功导入 {len(CATEGORIES_DATA)} 个分类, {len(KNOWLEDGE_DATA)} 个知识点")

if __name__ == "__main__":
    asyncio.run(seed_data())
