# Feynman Research v4.0 - 科学研究框架

> 从信息收集器升级为真实研究者

## 概述

Feynman AI v4.0 是一个完整的科学研究框架，遵循 Feynman 方法论：
- **假设生成**：识别现象 → 提出假设 → 设计验证
- **实验验证**：设计实验 → 执行验证 → 分析结果
- **文献综述**：提取引用 → 验证真实性 → 评估质量
- **质量控制**：事实核查 → 交叉验证 → 逻辑一致性

## 架构（8 Agent）

```
Coordinator Agent (协调器)
├── Hypothesis Agent (假设生成)
├── Search Agent (信息搜索)
├── Analysis Agent (深度分析)
├── Literature Review Agent (文献综述)
├── Experiment Agent (实验设计)
├── Quality Agent (质量验证)
└── Output Agent (结果输出)
```

### Agent 职责

**1. Coordinator Agent**
- 任务分解与分配
- Agent 间协调
- 进度跟踪
- Token 预算管理

**2. Hypothesis Agent**（新增）
- 识别关键现象和模式
- 生成科学假设
- 设计初步验证方案
- 假设优先级排序

**3. Search Agent**
- 多源信息检索
- 实时数据获取
- API 优先策略
- 结果去重与归并

**4. Analysis Agent**
- 数据深度分析
- 交叉验证
- 模式识别
- 统计分析

**5. Literature Review Agent**（新增）
- 提取论文引用
- Semantic Scholar 验证
- Levenshtein 匹配（>70%）
- 引用质量评估

**6. Experiment Agent**（新增）
- 实验变量识别
- 对照组设计
- 方法论选择
- 执行验证流程

**7. Quality Agent**（合并 H/I/J）
- P0（关键）：全验证（事实+交叉+逻辑）
- P1（标准）：交叉验证
- P2（快速）：快速核查
- 自动降级机制

**8. Output Agent**
- Feynman 式教学输出
- 多格式生成（Markdown/PDF/HTML）
- 可视化支持
- 用户定制化

## Token 优化策略

### Caveman Ultra 模式整合

```
阶段          模式      节省率    适用场景
─────────────────────────────────────────────
信息收集      Ultra      87%      Search Agent
深度分析      Lite       50-75%   Analysis Agent
用户交互      Normal     0%       Output Agent
安全警告      自动降级   -        错误处理
```

### 实现方式

```python
def optimize_output(phase, content, safety_check=True):
    if safety_check and detect_critical_info(content):
        return caveman_normal(content)  # 自动降级
    
    phase_modes = {
        'collection': caveman_ultra,
        'analysis': caveman_lite,
        'output': caveman_normal
    }
    
    return phase_modes[phase](content)
```

## 工作流

### 标准研究流程

```yaml
1. 初始化
   - Coordinator 接收研究主题
   - 分解任务，分配 Agent
   - 设定 Token 预算

2. 假设生成
   - Hypothesis Agent 识别现象
   - 生成假设列表
   - 设计验证实验

3. 信息收集
   - Search Agent 多源搜索
   - API 优先（腾讯财经等）
   - Token 优化：Ultra 模式

4. 文献综述
   - Literature Review Agent 提取引用
   - Semantic Scholar 验证
   - 引用质量评分

5. 深度分析
   - Analysis Agent 交叉验证
   - Token 优化：Lite 模式
   - 模式识别

6. 实验验证
   - Experiment Agent 设计实验
   - 执行验证流程
   - 结果分析

7. 质量控制
   - Quality Agent 优先级验证
   - P0/P1/P2 分级
   - 自动降级机制

8. 结果输出
   - Output Agent Feynman 式输出
   - 多格式生成
   - 用户定制化
```

## 配置

### Agent 模型配置

参考 `config/agent_models.yaml`：
- 高级模型：Coordinator、Hypothesis、Experiment
- 标准模型：Analysis、Literature Review
- 快速模型：Search、Output
- 质量模型：Quality（独立）

### API 优先策略

参考 `config/api_priority.yaml`：
- 股价：腾讯财经 API（HTTP，无 SSL）
- 实时数据：官方 API > 第三方 > Web Search
- 文献：Semantic Scholar > Google Scholar

## 使用示例

### 基础研究

```bash
# 启动 Feynman v4.0 研究
/feynman_v4 "量子计算对密码学的影响"

# 输出：
# 1. 假设生成：3个假设 + 验证方案
# 2. 文献综述：15篇论文 + 引用验证
# 3. 实验设计：对比实验 + 结果分析
# 4. Feynman 解释：教学式输出
```

### 投资研究

```bash
# 投资主题研究（整合实时行情）
/feynman_v4 "新能源汽车产业链投资机会" --investment

# 增强功能：
# - 实时股价获取（腾讯 API）
# - 行业数据分析
# - 财务指标验证
```

### 文献综述

```bash
# 论文引用验证
/feynman_v4 --literature-review "arxiv:2024.xxxx"

# 输出：
# - 引用提取：50个引用
# - 真实性验证：48/50 真实
# - Levenshtein 匹配：平均 85%
# - 质量评分：A+
```

## 参考资源

- DATAGEN：假设生成与状态管理
- PaperOrchestra：文献验证框架
- Caveman：Token 优化策略

## 文件结构

```
skills/feynman-research-v4/
├── SKILL.md                   # 本文档
├── agents/
│   ├── coordinator_agent.py   # 协调器
│   ├── hypothesis_agent.py    # 假设生成
│   ├── search_agent.py        # 信息搜索
│   ├── analysis_agent.py      # 深度分析
│   ├── literature_review_agent.py  # 文献综述
│   ├── experiment_agent.py    # 实验设计
│   ├── quality_agent.py       # 质量验证
│   └── output_agent.py        # 结果输出
├── core/
│   ├── state.py               # 状态管理（参考 DATAGEN）
│   ├── workflow.py            # 工作流引擎
│   └── token_optimizer.py     # Token 优化（caveman）
├── config/
│   ├── agent_models.yaml      # 模型配置
│   ├── api_priority.yaml      # API 优先级
│   └── quality_levels.yaml    # 质量分级
├── templates/
│   ├── hypothesis_template.md
│   ├── experiment_template.md
│   ├── literature_template.md
└── examples/
    ├── investment_research.md
    ├── academic_research.md
    └── literature_review.md
```

## 质量保证

### P0/P1/P2 分级验证

```
P0（关键信息）：
├── 事实核查（多源验证）
├── 交叉验证（独立来源）
└── 逻辑一致性检查

P1（标准信息）：
├── 交叉验证（至少2源）
└── 来源可信度检查

P2（快速信息）：
├── 单源快速核查
└── 基础可信度检查
```

### 安全降级机制

```python
# 检测到关键信息时自动降级到 Normal 模式
def auto_downgrade(content):
    keywords = ['股价', '财务', '投资建议', '错误', '警告']
    if any(kw in content for kw in keywords):
        return 'normal'  # 禁止 Ultra 模式
    return 'ultra'      # 允许优化
```

## 版本历史

- v4.0：完整重构，新增假设/实验/文献 Agent
- v3.0：基础研究框架
- v2.0：信息收集优化
- v1.0：初始版本

---

_Feynman AI v4.0 - "If you can't explain it simply, you don't understand it well enough."_