"""Direct knowledge enrichment - bypasses sandboxed API"""
import sqlite3
import time
import json

DB = r'D:\workbuddy task\2026-06-17-00-54-20\knowledge-hub\data\knowledge.db'

ITEMS = [
    {
        "title": "腾讯互娱混沌工程实践：Chaos Mesh落地",
        "slug": "chaos-mesh-tencent-ieg-practice",
        "content": "## 腾讯互娱混沌工程实践\n\n### 核心数据\n- 日访问量超100亿次，高峰QPS超100万\n- 日发布超500次，数据量超200TB\n- 基于Chaos Mesh构建云原生混沌工程平台\n- 每周混沌演练超150次，提前发现问题超100个\n- 效率提升10倍以上\n\n### 关键技术\n1. 网关层流量劫持\n2. DevOps流水线集成\n3. 红蓝对抗机制\n4. 三层环境分级\n\n> 腾讯游戏CPU>60%即卡顿投诉",
        "summary": "腾讯互娱基于Chaos Mesh构建的混沌工程体系：每周150+次演练、效率提升10倍",
        "difficulty": "hard",
        "importance": 5,
        "category_id": 1,
        "tags": '["混沌工程","Chaos Mesh","腾讯互娱","故障注入","容灾"]',
        "source": "https://developer.cloud.tencent.com/article/1826103",
        "code_examples": '[{"language":"yaml","code":"apiVersion: chaos-mesh.org/v1alpha1\\nkind: PodChaos","description":"Kill游戏服务器Pod"}]',
        "quiz": '[{"question":"腾讯互娱基于哪个工具构建混沌工程平台？","options":["ChaosBlade","Chaos Mesh","Litmus","Gremlin"],"answer":1,"explanation":"腾讯互娱基于Chaos Mesh构建"},{"question":"腾讯游戏CPU超过多少会卡顿投诉？","options":["30%","50%","60%","80%"],"answer":2,"explanation":"CPU>60%即卡顿投诉"}]',
    },
    {
        "title": "PerfDog性能测试完整指标体系",
        "slug": "perfdog-performance-metrics",
        "content": "## PerfDog性能测试指标体系\n\n### 三大核心指标\n1. **Jank（卡顿）**：当前帧>前3帧均值x2且>84ms\n2. **Smooth Index（流畅度）**：AAA手游目标>95\n3. **FPower（帧功耗）**：案例FPower 65->48mW/帧(-26%)，月收入增45万美元\n\n### 测试时长\n超休闲>3分钟 | 中度>10分钟 | AAA/MMO 20-30分钟",
        "summary": "腾讯WeTest PerfDog三大核心指标：Jank卡顿检测、Smooth流畅度指数、FPower帧功耗优化",
        "difficulty": "medium",
        "importance": 5,
        "category_id": 2,
        "tags": '["PerfDog","WeTest","性能测试","腾讯"]',
        "source": "https://www.wetest.net/blog/mobile-game-performance-testing-2026-perfdog-guide-1189.html",
        "code_examples": '[{"language":"python","code":"# PerfDog API 自动采集性能数据","description":"PerfDog API示例"}]',
        "quiz": '[{"question":"PerfDog中Jank的定义？","options":["FPS<30","当前帧时间>前3帧均值x2且>84ms","内存超阈值","CPU>80%"],"answer":1,"explanation":"当前帧时间>前3帧平均x2且>84ms"}]',
    },
    {
        "title": "游戏协议安全测试：五大经典漏洞",
        "slug": "game-protocol-security-testing",
        "content": "## 游戏协议安全测试\n\n### 五大经典漏洞\n| 漏洞 | 攻击方式 | 后果 |\n|---|---|---|\n| 道具盗刷 | 数量字段为负数 | 无限道具 |\n| 强制加好友 | 修改目标ID | 强制加好友 |\n| 整数溢出 | 数量2147483647 | 钻石变21亿 |\n| 无限合成 | 材料ID改同一个 | 无限合成 |\n| 重复上阵 | 角色ID改同一个 | 阵容同一个人 |\n\n### 时间规划\n全量协议测试~3周 | 小版本~1周",
        "summary": "游戏协议安全测试：五大经典漏洞案例（道具盗刷、整数溢出、无限合成等）",
        "difficulty": "hard",
        "importance": 4,
        "category_id": 3,
        "tags": '["协议安全","安全测试","漏洞挖掘"]',
        "source": "https://testerhome.com/topics/29053",
        "code_examples": '[{"language":"python","code":"# 协议安全测试：模拟整数溢出攻击","description":"数量校验测试"}]',
        "quiz": '[{"question":"全量协议安全测试需要多久？","options":["1天","1周","3周","3个月"],"answer":2,"explanation":"全量测试约3周"}]',
    },
    {
        "title": "鸣潮500万PCU服务器集群架构",
        "slug": "wuthering-waves-5m-pcu",
        "content": "## 鸣潮500万PCU服务器集群\n\n### 架构亮点\n- 立项即定下500万PCU目标\n- 压测首次达成耗时近一年\n- MongoDB全库表使用分片集群\n- 全集群无单点，所有业务可横向扩容\n\n### 真实压测方法\n1. 录制真实游戏过程\n2. 录包回放\n3. 结合CBT上线真实场景占比\n4. 按比例混合录包模拟开服\n\n### 踩坑\n- MongoDB BSON增量更新不如全量覆盖\n- 入库需流速控制保护DB\n- GC问题多，需对象复用优化",
        "summary": "库洛《鸣潮》CTO分享：500万PCU、MongoDB全库分片、录包回放压测法",
        "difficulty": "medium",
        "importance": 5,
        "category_id": 7,
        "tags": '["鸣潮","PCU/CCU","压测","MongoDB","服务器架构"]',
        "source": "https://www.163.com/dy/article/JBE41F8B052688NB.html",
        "code_examples": '[{"language":"python","code":"class PacketReplay: pass","description":"录包回放压测框架"}]',
        "quiz": '[{"question":"鸣潮PCU目标？","options":["100万","300万","500万","1000万"],"answer":2,"explanation":"立项即定下500万PCU"}]',
    },
    {
        "title": "游戏反作弊系统全景对比",
        "slug": "game-anti-cheat-comparison",
        "content": "## 10款主流反作弊系统\n\n| 方案 | 游戏 | 特点 |\n|---|---|---|\n| 腾讯ACE | 王者荣耀/和平精英/无畏契约 | 一站式加固+反外挂 |\n| BattlEye | PUBG/彩虹六号 | 内核级驱动 |\n| EAC | 堡垒之夜/Apex | Epic旗下 |\n| Vanguard | Valorant | 启动即加载内核驱动 |\n\n### ACE核心数据\n- 每日监控设备数十亿\n- 检测准确率99.99%\n\n### 纵深防御\n客户端加壳->内核反作弊->服务端校验->行为分析->ML检测",
        "summary": "10款主流反作弊系统对比，ACE核心数据（99.99%准确率）和纵深防御架构",
        "difficulty": "easy",
        "importance": 4,
        "category_id": 3,
        "tags": '["反外挂","腾讯ACE","安全测试"]',
        "source": "https://zhuanlan.zhihu.com/p/1934280699009021005",
        "quiz": '[{"question":"腾讯反作弊系统？","options":["BattlEye","ACE","EAC","Vanguard"],"answer":1,"explanation":"ACE覆盖王者荣耀等"}]',
    },
    {
        "title": "AI在游戏测试中的应用全景",
        "slug": "ai-game-testing-landscape",
        "content": "## AI游戏测试四阶段\n\n| 阶段 | 技术 | 特点 |\n|---|---|---|\n| 1.脚本 | Airtest | 脆弱 |\n| 2.探索式 | GameAISDK | 成熟 |\n| 3.RL | 绝悟/伏羲 | 自进化 |\n| 4.生成式 | Acorn AI | 多模态 |\n\n### 行业基准\n- 网易伏羲RL：逆水寒500+任务数周->数小时\n- 腾讯绝悟：MOBA平衡测试准确率95%\n\n### RL vs VLM\n| 维度 | RL | VLM |\n|---|---|---|\n| 依赖 | 底层状态(需SDK) | 纯视觉(黑盒) |\n| 优势 | 发现边缘案例 | 通用性强 |",
        "summary": "AI游戏测试四阶段演进，含腾讯绝悟/网易伏羲/GameAISDK实战数据",
        "difficulty": "medium",
        "importance": 3,
        "category_id": 9,
        "tags": '["AI测试","WeTest","GameAISDK","腾讯"]',
        "source": "https://www.wetest.net/blog/game-ai-automated-testing-technology-evolution-market-analysis-1171.html",
        "quiz": '[{"question":"腾讯开源的游戏AI框架？","options":["Airtest","GameAISDK","ML-Agents","Acorn"],"answer":1,"explanation":"GameAISDK腾讯开源"}]',
    },
    {
        "title": "Tick Rate与游戏服务器性能权衡",
        "slug": "tick-rate-performance-tradeoff",
        "content": "## Tick Rate深度分析\n\n### 行业对比\n| 游戏 | Tick | 说明 |\n|---|---|---|\n| VALORANT | 128Hz | 重构引擎 |\n| CS2 | 64Hz(Subtick) | 子tick优化 |\n| Apex | 20Hz | 3倍成本省2帧延迟不值 |\n\n### Respawn论述\n20Hz约5帧延迟，60Hz约3帧延迟。3倍成本最多省2帧延迟。\n\n### VALORANT 128Hz代价\n- 重构引擎所有系统\n- 自定义RPC替换UE网络层(100-10000x提升)\n- 换服务器硬件(+30%提升)",
        "summary": "Tick Rate行业对比（VALORANT 128Hz vs Apex 20Hz）、成本公式、VALORANT重构案例",
        "difficulty": "medium",
        "importance": 4,
        "category_id": 4,
        "tags": '["网络协议","性能测试","服务器架构","UDP"]',
        "source": "https://edgegap.com/zh/blog/game-server-tick-rate-explained-gameplay-precision-vs-infrastructure-cost",
        "quiz": '[{"question":"Apex Legends Tick Rate？","options":["128Hz","64Hz","20Hz","12Hz"],"answer":2,"explanation":"Apex维持20Hz"}]',
    },
    {
        "title": "Clumsy弱网测试实战",
        "slug": "clumsy-weak-network-testing",
        "content": "## Clumsy弱网模拟工具\n\n### 核心功能\n| 参数 | 说明 | 典型值 |\n|---|---|---|\n| Lag | 延迟 | 100-300ms |\n| Drop | 丢包 | 1-10% |\n| Out of order | 乱序 | 5-15% |\n| Throttle | 限速 | 50-256 KB/s |\n\n### 游戏测试案例\n延迟200ms + 丢包5% + 乱序10% -> 模拟真实网络\n\n### 原理\n利用WinDivert库捕获和修改网络数据包\n\n### 注意\n需管理员权限，测试完成后禁用参数",
        "summary": "Clumsy弱网模拟工具完整指南：核心功能、游戏测试案例、Filter规则",
        "difficulty": "easy",
        "importance": 3,
        "category_id": 6,
        "tags": '["弱网测试","网络协议","性能测试"]',
        "source": "https://cloud.tencent.com/developer/article/2602551",
        "code_examples": '[{"language":"bash","code":"clumsy.exe --lag on --lag-time 200","description":"模拟弱网环境"}]',
        "quiz": '[{"question":"Clumsy底层原理？","options":["修改路由表","WinDivert抓包","代理转发","修改网卡"],"answer":1,"explanation":"WinDivert捕获修改数据包"}]',
    },
]

conn = sqlite3.connect(DB)
c = conn.cursor()
before = c.execute('SELECT COUNT(*) FROM knowledge').fetchone()[0]
print(f"Before: {before} items")

now = time.strftime('%Y-%m-%d %H:%M:%S')

for item in ITEMS:
    try:
        c.execute(
            """INSERT INTO knowledge 
            (title,slug,content,summary,difficulty,importance,category_id,
             tags,source,code_examples,quiz,view_count,like_count,related_ids,
             created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,0,0,'[]',?,?)""",
            (
                item["title"], item["slug"], item["content"], item["summary"],
                item["difficulty"], item["importance"], item["category_id"],
                item["tags"], item["source"], item.get("code_examples", "[]"),
                item.get("quiz", "[]"), now, now,
            ),
        )
        print(f"  + {item['title'][:40]}")
    except Exception as e:
        print(f"  FAIL {item['title'][:20]}: {e}")

conn.commit()
after = c.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0]
conn.close()
print(f"\nDone: {before} -> {after} items (+{after - before})")
