"""Enrich knowledge database with research findings"""
import json
import urllib.request

API = 'http://localhost:8002/api'

def post_knowledge(data):
    req = urllib.request.Request(
        f'{API}/knowledge',
        data=json.dumps(data).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    return json.loads(urllib.request.urlopen(req).read())

ITEMS = [
    {
        "title": "腾讯互娱混沌工程实践：Chaos Mesh落地",
        "slug": "chaos-mesh-tencent-ieg-practice",
        "content": "## 腾讯互娱混沌工程实践\n\n### 核心数据\n- 运营活动日访问量超 **100亿次**，高峰 QPS 超 **100万**\n- 日发布超 **500次**，数据量超 200TB\n- 基于 Chaos Mesh 构建云原生混沌工程平台\n- 落地半年后，平均每周混沌演练超 **150次**\n- 提前发现问题超 **100个**，效率提升 **10倍以上**\n\n### 关键技术\n1. 网关层流量劫持：针对特定账号/大区实现精细化故障注入\n2. DevOps流水线集成：每次版本发布自动执行混沌套餐\n3. 红蓝对抗机制：驱动团队主动做混沌实验\n4. 三层环境分级：演习环境 -> 预发布环境/体验服 -> 生产环境\n\n### 面试重点\n> 腾讯游戏CPU > 60%即出现卡顿投诉，因此资源压力混沌测试是游戏特有的关键场景\n\n来源：https://developer.cloud.tencent.com/article/1826103",
        "summary": "腾讯互娱基于Chaos Mesh构建的混沌工程体系：每周150+次演练、提前发现100+问题、效率提升10倍。含三层环境分级和DevOps集成方案。",
        "difficulty": "hard",
        "importance": 5,
        "category_id": 1,
        "tags": ["混沌工程", "Chaos Mesh", "腾讯互娱", "故障注入", "容灾"],
        "source": "https://developer.cloud.tencent.com/article/1826103",
        "code_examples": [
            {
                "language": "yaml",
                "code": "apiVersion: chaos-mesh.org/v1alpha1\nkind: PodChaos\nmetadata:\n  name: game-server-kill\nspec:\n  action: pod-kill\n  mode: one\n  selector:\n    namespaces: [game-prod]\n    labelSelectors:\n      app: game-server\n  duration: 30m",
                "description": "随机Kill游戏服务器Pod，验证故障自愈能力"
            }
        ],
        "quiz": [
            {"question": "腾讯互娱基于哪个工具构建混沌工程平台？", "options": ["A. ChaosBlade", "B. Chaos Mesh", "C. Litmus", "D. Gremlin"], "answer": 1, "explanation": "腾讯互娱基于Chaos Mesh构建云原生混沌工程平台（CRD驱动）"},
            {"question": "腾讯游戏CPU使用率超过多少会引发玩家卡顿投诉？", "options": ["A. 30%", "B. 50%", "C. 60%", "D. 80%"], "answer": 2, "explanation": "在Gdevops峰会上，腾讯工程师明确指出游戏CPU > 60%即出现卡顿投诉"}
        ]
    },
    {
        "title": "PerfDog性能测试完整指标体系",
        "slug": "perfdog-performance-metrics",
        "content": "## PerfDog 性能测试完整指标体系\n\n### 三大核心指标\n\n1. **Jank（卡顿指标）**\n   - 基于帧时间检测：当前帧 > 前3帧均值x2 且 > 84ms -> 记为一次Jank\n   - 120Hz+设备另有 SmallJank：>125ms 为严重卡顿\n\n2. **Smooth Index（流畅度指数）**\n   - 加权计算卡顿持续时间和严重程度\n   - AAA手游目标 > 95\n\n3. **FPower（帧功耗）**\n   - FPower = 总功耗 / 帧率\n   - 案例：某RPG优化后 FPower 65->48mW/帧(-26%)，月收入增加45万美元\n\n### 测试时长标准\n| 游戏类型 | 建议时长 |\n|---|---|\n| 超休闲 | >3分钟 |\n| 中度 | >10分钟 |\n| AAA/MMO | 20-30分钟 |\n\n> 热降频在10-15分钟后才发生，必须测试足够长时间\n\n来源：https://www.wetest.net/blog/mobile-game-performance-testing-2026-perfdog-guide-1189.html",
        "summary": "腾讯WeTest PerfDog三大核心指标：Jank卡顿检测、Smooth流畅度指数、FPower帧功耗优化。含测试时长标准和真实优化案例。",
        "difficulty": "medium",
        "importance": 5,
        "category_id": 2,
        "tags": ["PerfDog", "WeTest", "性能测试", "腾讯"],
        "source": "https://www.wetest.net/blog/mobile-game-performance-testing-2026-perfdog-guide-1189.html",
        "code_examples": [
            {
                "language": "python",
                "code": "# PerfDog API 自动采集性能数据\ndef start_perfdog_test(device_id, package_name):\n    api = \"https://perfdog.qq.com/api/v1/test/start\"\n    payload = {\n        \"device_id\": device_id,\n        \"package\": package_name,\n        \"duration\": 1800,\n        \"metrics\": [\"fps\", \"jank\", \"cpu\", \"gpu\", \"memory\", \"temperature\"]\n    }\n    return payload",
                "description": "PerfDog API 性能测试采集示例"
            }
        ],
        "quiz": [
            {"question": "PerfDog中Jank的定义是？", "options": ["A. FPS低于30", "B. 当前帧时间 > 前3帧均值x2 且 > 84ms", "C. 内存超过阈值", "D. CPU占用超过80%"], "answer": 1, "explanation": "Jank：当前帧时间 > 前3帧平均x2 且 > 84ms时记为一次卡顿"},
            {"question": "AAA手游建议的PerfDog测试时长？", "options": ["A. 1-3分钟", "B. 5-10分钟", "C. 20-30分钟", "D. 1小时以上"], "answer": 2, "explanation": "AAA/MMO建议20-30分钟，因为热降频在10-15分钟后才发生"}
        ]
    },
    {
        "title": "游戏协议安全测试：五大经典漏洞",
        "slug": "game-protocol-security-testing",
        "content": "## 游戏协议安全测试\n\n### 定义\n通过第三方工具篡改客户端发给服务器的协议，测试服务器逻辑漏洞。\n\n### 五大经典漏洞案例\n\n| 漏洞类型 | 攻击方式 | 后果 |\n|---|---|---|\n| 道具盗刷 | 修改数量字段为负数 | 获得无限道具 |\n| 强制加好友 | 修改目标ID | 强制加他人为好友 |\n| 整数溢出 | 数量改为2147483647 | 钻石变21亿 |\n| 无限合成 | 3个材料ID改成同一个 | 一个道具无限合成 |\n| 重复上阵 | 5个角色ID全改成同一个 | 阵容全变同一个人 |\n\n### 必备工具能力\n- 录制协议 + 展示字段值\n- 修改字段值 / 发送 / 拦截\n- 储存用例（回归复用）\n- 并发发送（10/100次暴力测试）\n\n### 时间规划\n- 全量协议测试约3周\n- 小版本更新约1周\n\n> 面试金句：协议测试最重要的不是工具，而是挖掘漏洞的测试经验\n\n来源：https://testerhome.com/topics/29053",
        "summary": "游戏协议安全测试方法：五大经典漏洞案例（道具盗刷、整数溢出、无限合成等）、工具能力要求、时间规划。TesterHome腾讯系实战经验。",
        "difficulty": "hard",
        "importance": 4,
        "category_id": 3,
        "tags": ["协议安全", "安全测试", "漏洞挖掘"],
        "source": "https://testerhome.com/topics/29053",
        "code_examples": [
            {
                "language": "python",
                "code": "# 协议安全测试：模拟篡改请求\n# 测试用例：负数、超大数、零\ntest_cases = [\n    (\"正常购买\", 1001, 1),\n    (\"负数购买\", 1001, -1),\n    (\"溢出购买\", 1001, 2**31-1),\n    (\"零购买\", 1001, 0),\n]\nfor name, item_id, qty in test_cases:\n    print(f\"Test {name}: item={item_id} qty={qty}\")",
                "description": "协议安全测试：验证服务器是否正确校验数量字段"
            }
        ],
        "quiz": [
            {"question": "全量协议安全测试大约需要多久？", "options": ["A. 1天", "B. 1周", "C. 3周", "D. 3个月"], "answer": 2, "explanation": "全量协议测试约3周，小版本更新约1周"},
            {"question": "以下哪个不属于协议安全测试的关注点？", "options": ["A. 整数溢出攻击", "B. 协议字段篡改", "C. UI视觉还原", "D. 重复发送攻击"], "answer": 2, "explanation": "UI视觉还原属于客户端测试，协议安全关注网络通信层面"}
        ]
    },
    {
        "title": "鸣潮500万PCU服务器集群架构",
        "slug": "wuthering-waves-5m-pcu",
        "content": "## 库洛《鸣潮》500万PCU服务器集群实战\n\n### 架构亮点\n- 立项即定下 **500万PCU** 目标\n- 压测首次达成耗时近一年\n- MongoDB全库表使用分片集群\n- 全集群无单点，所有业务可横向扩容\n\n### 真实压测方法\n不是按比例构造协议，而是：\n1. 录制真实游戏过程\n2. 录包回放\n3. 结合CBT线上真实场景占比\n4. 按比例混合录包模拟开服状态\n\n**实践证明此方法比较接近上线情况**\n\n### 踩坑经验\n- MongoDB BSON增量更新不如全量覆盖\n- 入库需要流速控制保护DB\n- 托管内存语言GC问题多，需大量对象复用优化\n\n来源：https://www.163.com/dy/article/JBE41F8B052688NB.html",
        "summary": "库洛《鸣潮》CTO分享：500万PCU目标、MongoDB全库分片、录包回放压测法、三大踩坑经验。业界顶级游戏服务器架构案例。",
        "difficulty": "medium",
        "importance": 5,
        "category_id": 7,
        "tags": ["鸣潮", "PCU/CCU", "压测", "MongoDB", "服务器架构"],
        "source": "https://www.163.com/dy/article/JBE41F8B052688NB.html",
        "code_examples": [
            {
                "language": "python",
                "code": "# 录包回放压测框架示例\nclass PacketReplay:\n    def __init__(self, capture_file):\n        self.packets = self.load(capture_file)\n    \n    def load(self, filepath):\n        \"\"\"加载录制的游戏协议包\"\"\"\n        # 按时间戳排序，保持原始发送间隔\n        return sorted(json.load(open(filepath)), key=lambda p: p['timestamp'])\n    \n    def replay(self, target_host, speed_factor=1.0):\n        \"\"\"按加速比回放\"\"\"\n        for pkt in self.packets:\n            time.sleep(pkt['interval'] / speed_factor)\n            self.send(target_host, pkt['data'])",
                "description": "录包回放压测框架：模拟真实玩家行为"
            }
        ],
        "quiz": [
            {"question": "鸣潮立项时的PCU目标是多少？", "options": ["A. 100万", "B. 300万", "C. 500万", "D. 1000万"], "answer": 2, "explanation": "库洛CTO演讲：鸣潮立项即定下500万PCU目标"},
            {"question": "鸣潮使用的压测方法是什么？", "options": ["A. JMeter协议构造", "B. 录包回放+按比例混合", "C. Locust纯HTTP压测", "D. 随机流量生成"], "answer": 1, "explanation": "录制真实游戏 + 录包回放 + 结合CBT场景占比混合，此方法较接近上线情况"}
        ]
    },
    {
        "title": "游戏反作弊系统全景对比",
        "slug": "game-anti-cheat-comparison",
        "content": "## 10款主流反作弊系统对比\n\n### 核心方案\n\n| 方案 | 覆盖游戏 | 技术特点 |\n|---|---|---|\n| **腾讯ACE** | 王者荣耀/和平精英/英雄联盟/无畏契约 | 一站式：加固+反外挂+内容安全+经济安全 |\n| BattlEye | PUBG/彩虹六号/方舟 | 内核级驱动，全权控制 |\n| EasyAntiCheat | 堡垒之夜/Apex | Epic旗下，内核级 |\n| Riot Vanguard | Valorant专用 | 随系统启动加载的内核驱动 |\n\n### ACE核心优势\n- 每日监控设备数十亿，检测准确率 **99.99%**\n- 支持2-3个接口快速接入\n- 可部署预启动模式（随Windows启动前运行）\n\n### 纵深防御架构\n客户端加壳 -> 内核级反作弊 -> 服务端权威校验 -> 行为分析 -> ML检测\n\n### 反作弊测试要点\n1. Verify memory protection (value encryption, honeypot variables)\n2. Test anti-debugging layers (IsDebuggerPresent + timing check + CRC32)\n3. Behavior analysis: ML models detect abnormal patterns\n\n来源：https://zhuanlan.zhihu.com/p/1934280699009021005",
        "summary": "10款主流游戏反作弊系统对比（腾讯ACE/BattlEye/EAC/Vanguard），含ACE核心数据（99.99%准确率、数十亿设备监控）和纵深防御架构。",
        "difficulty": "easy",
        "importance": 4,
        "category_id": 3,
        "tags": ["反外挂", "腾讯ACE", "安全测试"],
        "source": "https://zhuanlan.zhihu.com/p/1934280699009021005",
        "quiz": [
            {"question": "腾讯反作弊系统叫什么？", "options": ["A. BattlEye", "B. ACE", "C. EAC", "D. Vanguard"], "answer": 1, "explanation": "腾讯ACE (Anti-Cheat Expert) 覆盖王者荣耀/和平精英等主流游戏"},
            {"question": "ACE检测准确率是多少？", "options": ["A. 90%", "B. 95%", "C. 99%", "D. 99.99%"], "answer": 3, "explanation": "ACE每日监控设备数十亿，检测准确率99.99%"}
        ]
    },
    {
        "title": "AI在游戏测试中的应用全景",
        "slug": "ai-game-testing-landscape",
        "content": "## AI游戏自动化测试：四阶段演进\n\n### 技术演进路径\n\n| 阶段 | 技术 | 特点 | 代表工具 |\n|---|---|---|---|\n| 1. 脚本自动化 | 坐标点击+图像识别 | 脆弱，维护成本高 | Airtest |\n| 2. 探索式 | Monkey/行为树/NavMesh | 引入随机性，成熟 | GameAISDK |\n| 3. 强化学习 | PPO/SAC算法 | 自进化，发现边缘案例 | 绝悟/伏羲RL |\n| 4. 生成式智能体 | GPT-4V/SIMA 2 | 多模态感知+推理 | Acorn AI |\n\n### 行业基准\n- 网易伏羲RL测试：逆水寒500+任务从数周 -> 数小时\n- 腾讯绝悟：MOBA数值平衡测试准确率95%\n- Acorn AI：自然语言指令到游戏内任务执行闭环\n\n### RL vs VLM对比\n| 维度 | RL强化学习 | VLM多模态 |\n|---|---|---|\n| 依赖 | 底层状态数据(需SDK) | 纯视觉感知(黑盒) |\n| 优势 | 发现人类难覆盖的边缘案例 | 通用性强，无需接入 |\n| 劣势 | 奖励函数设计难 | 推理延迟高，有幻觉风险 |\n\n来源：https://www.wetest.net/blog/game-ai-automated-testing-technology-evolution-market-analysis-1171.html",
        "summary": "AI游戏测试四阶段演进（脚本->探索->RL->生成式AI），含腾讯绝悟/网易伏羲/GameAISDK实战数据，RL vs VLM技术对比。",
        "difficulty": "medium",
        "importance": 3,
        "category_id": 9,
        "tags": ["AI测试", "WeTest", "GameAISDK", "腾讯"],
        "source": "https://www.wetest.net/blog/game-ai-automated-testing-technology-evolution-market-analysis-1171.html",
        "quiz": [
            {"question": "腾讯开源的游戏AI自动化框架是？", "options": ["A. Airtest", "B. GameAISDK", "C. ML-Agents", "D. Acorn"], "answer": 1, "explanation": "GameAISDK是腾讯开源的基于纯图像输入的游戏AI自动化框架"},
            {"question": "RL测试相比VLM的核心优势是什么？", "options": ["A. 更便宜", "B. 能发现人类难覆盖的边缘案例", "C. 不需要任何接入", "D. 速度更快"], "answer": 1, "explanation": "RL依赖底层状态数据，能自进化发现人类思维难以覆盖的边缘案例"}
        ]
    },
    {
        "title": "Tick Rate与游戏服务器性能权衡",
        "slug": "tick-rate-performance-tradeoff",
        "content": "## Tick Rate：游戏精度 vs 基础设施成本\n\n### 本质\nTick率翻倍约等于CPU负载和带宽消耗大致翻倍。\n\n### 行业对比\n| 游戏 | Tick Rate | 说明 |\n|---|---|---|\n| VALORANT | 128Hz | Riot几乎重构引擎所有系统 |\n| CS2 | 64Hz (Subtick) | 子tick系统优化 |\n| Marathon | 60Hz | Bungie新作 |\n| Apex Legends | 20Hz | Respawn: 以3倍成本省2帧延迟不值 |\n| Escape from Tarkov | 12-16Hz | 硬核射击 |\n\n### Respawn官方论述\n> 20Hz服务器约5帧延迟，60Hz约3帧延迟。以3倍带宽和CPU成本，最多节省2帧延迟。这就是Apex维持20Hz的理由。\n\n### VALORANT 128Hz的代价\n- 重构引擎所有系统\n- 动画处理开销削减75%\n- 自定义RPC替换UE默认网络层（性能提升100-10,000x）\n- 更换服务器硬件（额外30%提升）\n\n### 面试要点\n> 合适的tick rate不是最高值，而是同时满足精度需求和基础设施可持续性的值\n\n来源：https://edgegap.com/zh/blog/game-server-tick-rate-explained-gameplay-precision-vs-infrastructure-cost",
        "summary": "Tick Rate深入分析：行业对比（VALORANT 128Hz vs Apex 20Hz）、成本公式、VALORANT重构案例。游戏服务器性能测试核心考点。",
        "difficulty": "medium",
        "importance": 4,
        "category_id": 4,
        "tags": ["网络协议", "性能测试", "服务器架构", "UDP"],
        "source": "https://edgegap.com/zh/blog/game-server-tick-rate-explained-gameplay-precision-vs-infrastructure-cost",
        "quiz": [
            {"question": "Apex Legends的Tick Rate是多少？", "options": ["A. 128Hz", "B. 64Hz", "C. 20Hz", "D. 12Hz"], "answer": 2, "explanation": "Apex维持20Hz，Respawn官方论述：以3倍带宽和CPU成本最多节省2帧延迟"},
            {"question": "Tick Rate翻倍大致会导致怎样的成本变化？", "options": ["A. 成本不变", "B. CPU负载和带宽翻倍", "C. 成本增加10%", "D. 只需更多存储"], "answer": 1, "explanation": "翻倍Tick率约等于CPU负载和带宽消耗大致翻倍"}
        ]
    },
    {
        "title": "Clumsy弱网测试实战",
        "slug": "clumsy-weak-network-testing",
        "content": "## Clumsy：Windows弱网模拟工具\n\n### 核心功能\n| 参数 | 说明 | 典型值 |\n|---|---|---|\n| Lag | 延迟(ms) | 100-300 |\n| Drop | 丢包(%) | 1-10% |\n| Out of order | 乱序(%) | 5-15% |\n| Throttle | 限速(KB/s) | 50-256 |\n| Duplicate | 重复(%) | 1-3% |\n\n### 游戏测试案例\n延迟200ms + 丢包5% + 乱序10% -> 模拟真实网络波动\n\n### Filter过滤规则\n指定目标IP/端口，仅对特定流量生效\n\n### 脚本化\n支持命令行参数，适合CI/CD自动化弱网测试\n\n### 底层原理\n利用WinDivert库捕获和修改网络数据包\n\n### 注意事项\n- 需管理员权限\n- 测试完成后务必禁用参数\n\n来源：https://cloud.tencent.com/developer/article/2602551",
        "summary": "Clumsy弱网模拟工具完整指南：核心功能、游戏测试案例（延迟+丢包+乱序组合）、Filter规则、CI/CD脚本化。弱网测试必会工具。",
        "difficulty": "easy",
        "importance": 3,
        "category_id": 6,
        "tags": ["弱网测试", "网络协议", "性能测试"],
        "source": "https://cloud.tencent.com/developer/article/2602551",
        "code_examples": [
            {
                "language": "bash",
                "code": "# Clumsy 命令行模式：模拟弱网\n# 延迟200ms + 丢包5% + 乱序10%\nclumsy.exe --lag on --lag-time 200 \\\n           --drop on --drop-chance 5.0 \\\n           --outoforder on --outoforder-chance 10.0 \\\n           --filter \"ip.DstAddr == 192.168.1.100 && tcp.DstPort == 8080\"",
                "description": "Clumsy命令行：模拟游戏弱网环境"
            }
        ],
        "quiz": [
            {"question": "Clumsy的底层原理是什么？", "options": ["A. 修改系统路由表", "B. WinDivert捕获和修改网络数据包", "C. 代理服务器转发", "D. 修改网卡驱动"], "answer": 1, "explanation": "Clumsy利用WinDivert库(Windows Packet Divert)捕获和修改网络数据包"},
            {"question": "Clumsy不能模拟以下哪种网络异常？", "options": ["A. 延迟", "B. 丢包", "C. 乱序", "D. DNS劫持"], "answer": 3, "explanation": "Clumsy不支持DNS层操作，主要覆盖传输层（延迟/丢包/乱序/限速/重复）"}
        ]
    }
]

for i, item in enumerate(ITEMS):
    try:
        result = post_knowledge(item)
        print(f"[OK] #{result['id']} {result['title']}")
    except Exception as e:
        print(f"[FAIL] {item['title']}: {e}")

stats = json.loads(urllib.request.urlopen(f'{API}/stats').read())
print(f"\n=== Total: {stats['total_knowledge']} knowledge items ===")
