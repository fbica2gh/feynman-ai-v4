# Feynman AI v4.0

> **从信息收集器升级为真实研究者**

## 🎯 核心改进

### 1. 假设驱动研究

**新增能力**: 从收集信息 → 提出假设 → 设计验证

```
观察现象 → 提出假设 → 设计实验 → 执行验证 → 发现规律 → 创造知识
```

**Hypothesis Agent**:
- 识别关键现象
- 生成创新假设
- 设计验证实验

### 2. 实验验证能力

**Experiment Agent**:
- 定义变量（独立变量/控制变量）
- 设计对照组
- 选择方法论（经验/模拟/理论）
- 执行验证并分析结果

### 3. 文献综述验证

**Literature Review Agent**:
- 提取引用（BibTeX格式）
- 验证引用真实性（Semantic Scholar API）
- Levenshtein匹配（>70%相似度）
- 引用质量分级（P0/P1/P2/reject）

### 4. 质量验证合并

**Quality Agent**（合并H/I/J → 单一Agent）:
- P0（关键）：全验证（事实+交叉+逻辑）
- P1（标准）：交叉验证
- P2（快速）：快速核查

### 5. Token优化整合

**caveman模式**:
- 信息收集阶段：Ultra（87%节省）
- 深度分析阶段：Lite（50-75%节省）
- 用户交互阶段：Normal
- 安全警告：自动降级

---

## 📊 架构对比

| 维度 | v3.0 | v4.0 | 改进 |
|------|------|------|------|
| **Agent数量** | 13 | 8 | -5（简化） |
| **假设生成** | ❌ | ✅ | 新增 |
| **实验验证** | ❌ | ✅ | 新增 |
| **引用质量** | ❌ | ✅ P0/P1/P2 | 新增 |
| **Token优化** | ❌ | ✅ caveman | 87%节省 |

---

## 🏗️ 架构（8 Agent）

```
Coordinator Agent (协调器)
├── Hypothesis Agent (假设生成) ← 新增
├── Search Agent (信息搜索) ← 保留
├── Analysis Agent (深度分析) ← 保留
├── Literature Review Agent (文献综述) ← 新增
├── Experiment Agent (实验设计) ← 新增
├── Quality Agent (质量验证) ← 合并优化
└── Output Agent (结果输出) ← 优化
```

---

## 📁 文件结构

```
feynman-ai-v4/
├── SKILL.md                 # 完整框架文档
├── agents/
│   ├── hypothesis_agent.py  # 假设生成Agent
│   ├── experiment_agent.py  # 实验设计Agent
│   ├── literature_review_agent.py  # 文献综述Agent
│   └── quality_agent.py     # 质量验证Agent
├── core/
│   ├── state.py             # 状态管理（参考DATAGEN）
│   ├── hypothesis.py        # 假设模型
│   ├── experiment.py        # 实验模型
│   └── research_question.py # 研究问题模型
├── config/
│   └── agent_models.yaml    # 模型配置
├── analysis/                # 分析工具
├── examples/                # 使用示例
├── reports/                 # 报告模板
└── templates/               # 模板文件
```

---

## 🚀 使用方式

```bash
# 查看完整框架
cat SKILL.md

# 使用示例（待集成到OpenClaw）
/feynman-research-v4 "研究量子计算对加密的影响"

# 输出：
# 1. 假设：量子计算将破解现有加密算法
# 2. 实验：分析RSA/ECC在量子攻击下的脆弱性
# 3. 文献：引用验证（P0级质量）
# 4. 结论：建议迁移到量子抗性算法
```

---

## 📚 参考项目

| 项目 | Stars | 参考内容 |
|------|-------|---------|
| **DATAGEN** | 1700 | Hypothesis Engine |
| **PaperOrchestra** | 272 | Literature Review + Autoraters |
| **caveman** | 46936 | Token优化（Ultra模式） |

---

## 📖 核心Agent详解

### Hypothesis Agent

```python
class HypothesisAgent:
    def generate_hypotheses(self, observations):
        # 1. 识别关键现象
        patterns = self.identify_patterns(observations)
        
        # 2. 生成假设（创新点）
        hypotheses = self.create_hypotheses(patterns)
        
        # 3. 设计验证实验
        experiments = self.design_experiments(hypotheses)
        
        return {'hypotheses': hypotheses, 'experiments': experiments}
```

### Experiment Agent

```python
class ExperimentAgent:
    def design_experiment(self, hypothesis):
        # 1. 定义变量
        variables = self.identify_variables(hypothesis)
        
        # 2. 设计对照组
        controls = self.design_controls(variables)
        
        # 3. 选择方法
        methods = self.select_methodologies(hypothesis)
        
        # 4. 执行验证
        results = self.execute(methods)
        
        return {'experiment': methods, 'results': results}
```

### Literature Review Agent

```python
class LiteratureReviewAgent:
    def verify_citations(self, paper):
        # 1. 提取引用
        citations = self.extract_citations(paper)
        
        # 2. 验证引用（Semantic Scholar）
        verified = self.verify_on_semantic_scholar(citations)
        
        # 3. Levenshtein匹配（>70%）
        quality = self.evaluate_quality(verified)
        
        return {'citations': verified, 'quality': quality}
```

---

## 🎓 质量验证级别

| 级别 | 验证内容 | 适用场景 |
|------|---------|---------|
| **P0** | 事实核查+交叉验证+逻辑一致性 | 关键决策 |
| **P1** | 交叉验证 | 标准研究 |
| **P2** | 快速核查 | 快速检索 |

---

## 📊 预期效果

- **研究质量**: 从信息汇总 → 创造新知识
- **假设生成**: 自动提出创新观点
- **实验验证**: 科学方法论验证假设
- **引用质量**: P0/P1/P2分级验证
- **Token成本**: 减少 67-87%

---

## 🔗 相关仓库

- **最佳实践**: fbica2gh/openclaw-harness-best-practices
- **投资系统**: fbica2gh/openclaw-investment-system
- **记忆系统**: fbica2gh/ai-agent-memory-framework
- **能力框架**: fbica2gh/openclaw-agent-capability-framework

---

## 📝 更新日志

**v4.0 (2026-04-27)**:
- ✅ 新增 Hypothesis Agent（假设生成）
- ✅ 新增 Experiment Agent（实验验证）
- ✅ 新增 Literature Review Agent（文献综述）
- ✅ 合并 Quality Agent（H/I/J → 单一）
- ✅ 整合 caveman Token优化
- ✅ 参考 DATAGEN State 设计

---

## 👤 作者

- OpenClaw Agent Capability Framework
- 参考项目：DATAGEN, PaperOrchestra, caveman

---

**创建时间**: 2026-04-27  
**状态**: ✅ 完成  
**仓库**: 私有