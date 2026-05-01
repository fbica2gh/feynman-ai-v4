# Feynman Research v5.0 - 科学研究框架（Fair 整合版）

> 从信息收集器升级为真实研究者 + Fair 框架质量控制

## 概述

Feynman AI v5.0 整合了 Fair 框架的优点，实现：
- **8 阶段明确流程**: ASK → PLAN → REVIEW → ITERATION → BUILD → REVIEW → ITERATION → OUTPUT
- **双级质量关卡**: P1 假设审查（方向正确）+ P0 结果审查（事实准确）
- **三维度交叉验证**: 数据维度（实验结果）+ 理论维度（文献支撑）+ 约束维度（边界条件）
- **工具链闭环**: feynman-init → feynman-check → feynman-citation → feynman-export
- **迭代机制**: 最多 5 轮迭代，每轮生成审查意见清单

## 架构（8 Agent）

保留 Feynman v4.0 的 8 Agent 架构（不改变数量）：

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

### Agent 职责（Fair 整合版）

**1. Coordinator Agent**
- 任务分解与分配
- Agent 间协调
- 进度跟踪
- Token 预算管理
- **Fair 整合**: ASK 阶段主控，迭代轮次管理（最多 5 轮）

**2. Hypothesis Agent**
- 识别关键现象和模式
- 生成科学假设
- 设计初步验证方案
- 假设优先级排序
- **Fair 整合**: PLAN 阶段主控，生成假设 + 验证计划

**3. Search Agent**
- 多源信息检索
- 实时数据获取
- API 优先策略
- 结果去重与归并
- **Fair 整合**: BUILD 阶段支持，数据维度验证

**4. Analysis Agent**
- 数据深度分析
- 交叉验证
- 模式识别
- 统计分析
- **Fair 整合**: ITERATION 阶段主控（第一轮），三维度交叉验证（数据维度）

**5. Literature Review Agent**
- 提取论文引用
- Semantic Scholar 验证
- Levenshtein 匹配（>70%）
- 引用质量评估
- **Fair 整合**: ITERATION 阶段支持（第一轮），三维度交叉验证（理论维度）

**6. Experiment Agent**
- 实验变量识别
- 对照组设计
- 方法论选择
- 执行验证流程
- **Fair 整合**: BUILD 阶段主控，实验设计 + 执行验证

**7. Quality Agent**
- P0（关键）：全验证（事实+交叉+逻辑）
- P1（标准）：交叉验证
- P2（快速）：快速核查
- 自动降级机制
- **Fair 整合**: REVIEW 阶段主控（双关卡），P1 假设审查 + P0 结果审查，三维度交叉验证（约束维度）

**8. Output Agent**
- Feynman 式教学输出
- 多格式生成（Markdown/PDF/HTML）
- 可视化支持
- 用户定制化
- **Fair 整合**: ITERATION 阶段主控（第二轮）+ OUTPUT 阶段主控，输出迭代 + 最终交付

## Fair 框架整合

### 8 阶段明确流程

```
ASK → PLAN → REVIEW → ITERATION → BUILD → REVIEW → ITERATION → OUTPUT
```

#### 阶段映射

| 阶段 | Fair 定义 | Feynman v5.0 实现 | 主控 Agent | 输出物 |
|------|----------|------------------|-----------|--------|
| **ASK** | 明确研究问题 | 接收研究主题，渐进式披露问答 | Coordinator | 研究目标文档 |
| **PLAN** | 制定研究计划 | 假设生成 + 任务分解 + 验证计划 | Hypothesis + Coordinator | 研究计划表 |
| **REVIEW** | P1 假设审查 | 假设合理性审查（方向正确） | Quality | P1 审查意见清单 |
| **ITERATION 1** | 初步分析迭代 | 信息收集 + 文献综述 + 三维度验证（数据/理论） | Analysis + Literature Review | 初步分析报告 |
| **BUILD** | 实验设计与执行 | 实验设计 + 信息收集 + 执行验证 | Experiment + Search | 实验结果报告 |
| **REVIEW 2** | P0 结果审查 | 结果准确性审查（事实准确） | Quality | P0 审查意见清单 |
| **ITERATION 2** | 输出迭代 | Feynman 式输出 + 可视化 + 定制化 | Output | 输出草案 v1-v5 |
| **OUTPUT** | 最终交付 | 多格式输出 + 质量保证 + 用户确认 | Output | 最终研究报告 |

### 双级质量关卡

```
关卡 1 (P1): 假设审查（REVIEW 阶段）
├── 方向正确性检查
├── 假设可验证性检查
├── 资源可行性检查
└── 输出: P1 审查意见清单

关卡 2 (P0): 结果审查（REVIEW 2 阶段）
├── 事实准确性检查
├── 三维度交叉验证（数据/理论/约束）
├── 逻辑一致性检查
└── 输出: P0 审查意见清单
```

#### P1 审查标准

| 维度 | 检查项 | 权重 | 通过标准 |
|------|--------|------|---------|
| **方向正确性** | 研究假设是否符合科学原理 | 40% | 专家评审通过 |
| **假设可验证性** | 是否可设计实验验证 | 30% | 实验设计可行 |
| **资源可行性** | 时间/数据/工具是否充足 | 20% | 资源清单完整 |
| **边界清晰性** | 研究范围是否明确 | 10% | 边界文档清晰 |

#### P0 审查标准

| 维度 | 检查项 | 权重 | 通过标准 |
|------|--------|------|---------|
| **数据维度** | 实验结果是否可重复 | 35% | 数据一致性 >90% |
| **理论维度** | 文献支撑是否充分 | 30% | 引用验证 >85% |
| **约束维度** | 边界条件是否满足 | 20% | 约束清单完整 |
| **逻辑一致性** | 结论是否自洽 | 15% | 无逻辑矛盾 |

### 三维度交叉验证

```
数据维度 (Analysis Agent)
├── 实验结果可重复性
├── 数据一致性检查
├── 统计显著性检验
└── 数据质量评分 (0-100)

理论维度 (Literature Review Agent)
├── 文献引用真实性
├── Levenshtein 匹配度 >70%
├── 引用质量评分 A+/A/B/C/D
└── 理论支撑强度 (强/中/弱)

约束维度 (Quality Agent)
├── 边界条件检查
├── 时间约束验证
├── 资源约束验证
├── 约束清单完整性
└── 约束满足度 (0-100%)
```

### 工具链闭环

```
feynman-init → feynman-check → feynman-citation → feynman-export
```

#### 工具功能

| 工具 | 功能 | 输入 | 输出 | 调用时机 |
|------|------|------|------|---------|
| **feynman-init** | 一键生成项目骨架 | 研究主题 | 项目目录结构 | ASK 阶段 |
| **feynman-check** | 实时质量检查 | 分析内容 | 质量报告 | REVIEW/P0 阶段 |
| **feynman-citation** | 文内引用交叉核对 | 引用列表 | 验证报告 | ITERATION 1 阶段 |
| **feynman-export** | 多格式导出 | 研究报告 | PDF/DOCX/PPTX | OUTPUT 阶段 |

#### feynman-init 命令

```bash
# 一键生成项目骨架
feynman-init "量子计算对密码学的影响"

# 输出目录结构：
project_quantum_crypto/
├── README.md               # 项目说明
├── research_goal.md        # 研究目标文档
├── hypothesis.md           # 假设列表
├── plan.md                 # 研究计划表
├── data/                   # 数据目录
│   ├── raw/               # 原始数据
│   ├── processed/         # 处理后数据
│   └── results/           # 实验结果
├── literature/            # 文献目录
│   ├── references.yaml    # 引用列表
│   ├── validation.yaml    # 验证结果
├── experiments/           # 实验目录
│   ├── design.md         # 实验设计
│   ├── protocol.md       # 实验流程
│   ├── results.md        # 实验结果
├── output/                # 输出目录
│   ├── draft/            # 输出草案
│   ├── final/            # 最终报告
└── reviews/               # 审查目录
    ├── p1_review.md      # P1 审查意见
    ├── p0_review.md      # P0 审查意见
```

#### feynman-check 命令

```bash
# 实时质量检查（结构/引用/编号）
feynman-check output/final/report.md --level p0

# 输出：
✅ 结构完整性: 100% (所有章节完整)
✅ 引用质量: 92% (48/52 引用验证通过)
✅ 编号一致性: 95% (编号无冲突)
⚠️ 数据一致性: 88% (2 处数据需复验)
✅ 逻辑自洽性: 100% (无逻辑矛盾)
```

#### feynman-citation 命令

```bash
# 文内引用交叉核对
feynman-citation literature/references.yaml

# 输出：
引用总数: 52
验证通过: 48 (92%)
Levenshtein 平均匹配度: 85%
质量评分: A+ (48), A (2), B (2)
需要补充引用: 3 个
```

#### feynman-export 命令

```bash
# 多格式导出（pdf/docx/pptx）
feynman-export output/final/report.md --format pdf --template academic

# 输出：
✅ PDF 生成完成: output/final/report.pdf
✅ DOCX 生成完成: output/final/report.docx
✅ PPTX 生成完成: output/final/presentation.pptx
```

### 迭代机制

```
最多 5 轮迭代
├── ITERATION 1: 初步分析迭代（Analysis + Literature Review）
├── ITERATION 2: 输出迭代（Output）
└── 每轮生成审查意见清单
```

#### 迭代流程

```yaml
迭代轮次管理 (Coordinator Agent):
  max_iterations: 5
  current_iteration: 0
  
  ITERATION 1 (初步分析):
    执行者: Analysis Agent + Literature Review Agent
    输入: 假设 + 研究计划
    输出: 初步分析报告
    审查: Quality Agent (生成审查意见清单)
    决策: 是否继续迭代
    
  ITERATION 2-5 (输出迭代):
    执行者: Output Agent
    输入: 审查意见清单
    输出: 输出草案 v1-v5
    审查: Quality Agent (生成审查意见清单)
    决策: 是否继续迭代或交付
    
  终止条件:
    - 审查意见全部解决
    - 达到最大迭代轮次（5 轮）
    - 用户确认满意
```

#### 审查意见清单格式

```markdown
# 审查意见清单 - ITERATION 1

## 审查时间
2026-05-01 14:30

## 审查维度
- 数据维度: 88% ⚠️
- 理论维度: 92% ✅
- 约束维度: 95% ✅

## 审查意见
### 高优先级 (P0)
1. [数据维度] 实验 3 的结果数据需复验（一致性 <90%）
   - 建议: 重新执行实验 3，检查数据采集流程
2. [理论维度] 引用 [15] 的 Levenshtein 匹配度仅 65%
   - 建议: 替换为更权威的文献或补充原始文献验证

### 中优先级 (P1)
3. [约束维度] 时间约束未明确标注
   - 建议: 在研究计划表中补充时间里程碑
4. [数据维度] 数据质量评分偏低（78/100）
   - 建议: 补充数据来源可信度评估

### 低优先级 (P2)
5. [理论维度] 部分引用缺少 DOI
   - 建议: 补充 DOI 信息以便验证

## 决策
继续迭代 (ITERATION 2)，重点解决高优先级意见
```

## Token 优化策略

### Caveman Ultra 模式整合

保留 Feynman v4.0 的 Token 优化策略：

```
阶段          模式      节省率    适用场景
─────────────────────────────────────────────
ASK           Normal     0%       Coordinator Agent
PLAN          Lite       50-75%   Hypothesis Agent
REVIEW        Normal     0%       Quality Agent
ITERATION 1   Ultra      87%      Analysis + Literature Review
BUILD         Ultra      87%      Experiment + Search
REVIEW 2      Normal     0%       Quality Agent
ITERATION 2   Lite       50-75%   Output Agent
OUTPUT        Normal     0%       Output Agent
```

## 完整工作流

### 标准研究流程（Fair 整合版）

```yaml
1. ASK 阶段 (Coordinator Agent)
   - 接收研究主题
   - 渐进式披露问答（Phase 0）
   - 生成研究目标文档
   - 调用 feynman-init 生成项目骨架
   - Token 模式: Normal

2. PLAN 阶段 (Hypothesis Agent + Coordinator)
   - Hypothesis Agent: 识别现象 → 生成假设 → 设计验证方案
   - Coordinator: 任务分解 → 分配 Agent → 设定 Token 预算
   - 生成研究计划表
   - Token 模式: Lite

3. REVIEW 阶段 (Quality Agent) - P1 假设审查
   - 方向正确性检查
   - 假设可验证性检查
   - 资源可行性检查
   - 输出: P1 审查意见清单
   - 决策: 是否进入 ITERATION 1
   - Token 模式: Normal

4. ITERATION 1 阶段 (Analysis + Literature Review Agent)
   - Analysis Agent: 信息收集 + 交叉验证（数据维度）
   - Literature Review Agent: 提取引用 + Semantic Scholar 验证（理论维度）
   - Quality Agent: 约束维度验证
   - 生成初步分析报告
   - 调用 feynman-citation 验证引用
   - Quality Agent: 生成审查意见清单
   - Token 模式: Ultra (Analysis + Literature Review), Normal (Quality)

5. BUILD 阶段 (Experiment + Search Agent)
   - Experiment Agent: 实验变量识别 → 对照组设计 → 方法论选择
   - Search Agent: 多源信息检索 → 实时数据获取
   - 执行验证流程
   - 生成实验结果报告
   - Token 模式: Ultra

6. REVIEW 2 阶段 (Quality Agent) - P0 结果审查
   - 三维度交叉验证（数据/理论/约束）
   - 事实准确性检查
   - 逻辑一致性检查
   - 调用 feynman-check 质量检查
   - 输出: P0 审查意见清单
   - 决策: 是否进入 ITERATION 2
   - Token 模式: Normal

7. ITERATION 2 阶段 (Output Agent)
   - Feynman 式教学输出
   - 可视化支持
   - 用户定制化
   - 生成输出草案 v1-v5
   - 根据审查意见清单迭代
   - 最多 5 轮迭代
   - Token 模式: Lite

8. OUTPUT 阶段 (Output Agent)
   - 多格式生成（Markdown/PDF/HTML）
   - 调用 feynman-export 多格式导出
   - 最终质量保证
   - 用户确认交付
   - Token 模式: Normal
```

## 配置

### Agent 模型配置

参考 `config/agent_models.yaml`：
- 高级模型：Coordinator、Hypothesis、Experiment、Quality
- 标准模型：Analysis、Literature Review、Output
- 快速模型：Search

### API 优先策略

参考 `config/api_priority.yaml`：
- 股价：腾讯财经 API（HTTP，无 SSL）
- 实时数据：官方 API > 第三方 > Web Search
- 文献：Semantic Scholar > Google Scholar

### 迭代配置

参考 `config/iteration_config.yaml`：
- max_iterations: 5
- review_threshold: 
  - p0: 90% (数据/理论/约束维度均 >90%)
  - p1: 80% (假设可验证性 >80%)

## 使用示例

### 基础研究

```bash
# 启动 Feynman v5.0 研究
/feynman_v5 "量子计算对密码学的影响"

# 输出：
# 1. ASK: 渐进式披露问答 → 研究目标文档
# 2. PLAN: 3个假设 + 验证方案 + 研究计划表
# 3. REVIEW (P1): 假设审查意见清单
# 4. ITERATION 1: 15篇论文 + 引用验证 + 初步分析
# 5. BUILD: 实验设计 + 执行验证
# 6. REVIEW (P0): 结果审查意见清单
# 7. ITERATION 2: Feynman 式输出草案 v1-v3
# 8. OUTPUT: 多格式导出 + 用户确认
```

### 投资研究

```bash
# 投资主题研究（整合实时行情）
/feynman_v5 "新能源汽车产业链投资机会" --investment

# 增强功能：
# - 实时股价获取（腾讯 API）
# - 行业数据分析
# - 财务指标验证
# - 三维度交叉验证（数据/理论/约束）
```

### 文献综述

```bash
# 论文引用验证
/feynman_v5 --literature-review "arxiv:2024.xxxx"

# 输出：
# - 引用提取：50个引用
# - 真实性验证：48/50 真实
# - Levenshtein 匹配：平均 85%
# - 三维度验证：数据 92%/理论 88%/约束 95%
# - 质量评分：A+
```

## 工具实现

### feynman-init

参考 `tools/feynman_init.py`：
- 生成项目骨架
- 创建目录结构
- 初始化配置文件

### feynman-check

参考 `tools/feynman_check.py`：
- 实时质量检查
- 结构完整性检查
- 引用质量检查
- 编号一致性检查

### feynman-citation

参考 `tools/feynman_citation.py`：
- 文内引用提取
- Semantic Scholar 验证
- Levenshtein 匹配计算
- 引用质量评分

### feynman-export

参考 `tools/feynman_export.py`：
- Markdown 转 PDF（pandoc）
- Markdown 转 DOCX（pandoc）
- Markdown 转 PPTX（自定义模板）

## 文件结构

```
skills/feynman-research-v5/
├── SKILL.md                   # 本文档
├── agents/
│   ├── coordinator_agent.py   # 协调器（ASK + 迭代管理）
│   ├── hypothesis_agent.py    # 假设生成（PLAN）
│   ├── search_agent.py        # 信息搜索（BUILD 支持）
│   ├── analysis_agent.py      # 深度分析（ITERATION 1 + 数据维度）
│   ├── literature_review_agent.py  # 文献综述（ITERATION 1 + 理论维度）
│   ├── experiment_agent.py    # 实验设计（BUILD）
│   ├── quality_agent.py       # 质量验证（REVIEW P1/P0 + 约束维度）
│   └── output_agent.py        # 结果输出（ITERATION 2 + OUTPUT）
├── core/
│   ├── state.py               # 状态管理
│   ├── workflow.py            # 工作流引擎（8 阶段）
│   ├── iteration_manager.py   # 迭代管理器（最多 5 轮）
│   ├── token_optimizer.py     # Token 优化（caveman）
│   ├── review_manager.py      # 审查管理器（P1/P0）
│   └── validation_manager.py  # 三维度交叉验证管理器
├── config/
│   ├── agent_models.yaml      # 模型配置
│   ├── api_priority.yaml      # API 优先级
│   ├── quality_levels.yaml    # 质量分级
│   ├── iteration_config.yaml  # 迭代配置
│   └── review_standards.yaml  # 审查标准（P1/P0）
├── tools/
│   ├── feynman_init.py        # 项目骨架生成
│   ├── feynman_check.py       # 实时质量检查
│   ├── feynman_citation.py    # 引用交叉核对
│   └ feynman_export.py        # 多格式导出
│   ├── feynman_iterate.py     # 迭代执行器
│   └── feynman_review.py      # 审查意见生成器
├── templates/
│   ├── project_structure.yaml # 项目骨架模板
│   ├── hypothesis_template.md # 假设模板
│   ├── experiment_template.md # 实验模板
│   ├── literature_template.md # 文献模板
│   ├── review_checklist.md    # 审查意见清单模板
│   └── output_template.md     # 输出模板
└── examples/
    ├── investment_research.md  # 投资研究示例
    ├── academic_research.md    # 学术研究示例
    ├── literature_review.md    # 文献综述示例
    └── iteration_example.md    # 迭代流程示例
```

## 质量保证

### P0/P1/P2 分级验证（保留 v4.0）

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

### 双关卡验证（新增）

```
关卡 1 (P1 假设审查):
├── 方向正确性（40%）
├── 假设可验证性（30%）
├── 资源可行性（20%）
└── 边界清晰性（10%）

关卡 2 (P0 结果审查):
├── 数据维度（35%）
├── 理论维度（30%）
├── 约束维度（20%）
└── 逻辑一致性（15%）
```

### 三维度交叉验证（新增）

```
数据维度验证:
├── 实验结果可重复性
├── 数据一致性 >90%
├── 统计显著性检验
└── 数据质量评分 >80

理论维度验证:
├── 引用真实性 >85%
├── Levenshtein 匹配度 >70%
├── 引用质量评分 ≥B
└── 理论支撑强度 ≥中

约束维度验证:
├── 边界条件完整性
├── 时间约束满足度
├── 资源约束满足度
└── 约束清单完整性 >90%
```

## 版本历史

- **v5.0**: Fair 框架整合（8 阶段流程 + 双关卡 + 三维度 + 工具链 + 迭代）
- **v4.0**: 完整重构，新增假设/实验/文献 Agent
- **v3.0**: 基础研究框架
- **v2.0**: 信息收集优化
- **v1.0**: 初始版本

## 与 Fair 框架对比

| 特性 | Fair 框架 | Feynman v5.0 | 改进说明 |
|------|----------|-------------|---------|
| **阶段流程** | 8 阶段明确 | 8 阶段映射到 Agent | ✅ 整合 |
| **质量关卡** | P1/P0 双关卡 | P1 假设审查 + P0 结果审查 | ✅ 整合 |
| **交叉验证** | 三维度 | 数据/理论/约束维度映射到 Agent | ✅ 整合 |
| **工具链** | 4 工具闭环 | feynman-init/check/citation/export | ✅ 整合 |
| **迭代机制** | 最多 5 轮 | Coordinator 管理迭代轮次 | ✅ 整合 |
| **Agent 数量** | 未知 | 8 Agent（保留 v4.0） | ⚠️ 不改变数量 |

## 改进点总结

### 相比 Fair 框架

1. **Agent 映射**: 8 阶段流程明确映射到 8 个 Agent，职责清晰
2. **工具集成**: 4 个工具（init/check/citation/export）无缝集成到工作流
3. **审查机制**: 双关卡（P1/P0）自动化生成审查意见清单
4. **三维度验证**: 数据/理论/约束维度明确分配到 Analysis/Literature Review/Quality Agent

### 相比 Feynman v4.0

1. **流程标准化**: 8 阶段明确流程（ASK → PLAN → REVIEW → ITERATION → BUILD → REVIEW → ITERATION → OUTPUT）
2. **质量关卡**: 双关卡机制（P1 假设审查 + P0 结果审查）
3. **三维度验证**: 数据/理论/约束三维度交叉验证
4. **工具链**: 闭环工具链（init → check → citation → export）
5. **迭代管理**: 最大 5 轮迭代 + 审查意见清单

---

_Feynman AI v5.0 - "If you can't explain it simply, you don't understand it well enough."_  
_Fair Integration - "Quality gates ensure scientific rigor."_