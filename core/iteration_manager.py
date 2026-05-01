"""
Feynman Research v5.0 - Iteration Manager
迭代管理器（最多 5 轮）

功能：
- 迭代轮次管理
- 审查意见跟踪
- 终止条件检查
"""

import yaml
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class IterationManager:
    """迭代管理器"""
    
    def __init__(self, project_path: str, max_iterations: int = 5):
        """初始化迭代管理器
        
        Args:
            project_path: 项目目录路径
            max_iterations: 最大迭代轮次（默认 5）
        """
        self.project_path = Path(project_path)
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.review_opinions = []
        self.iteration_history = []
        self.state_file = self.project_path / "iteration_state.yaml"
        self._load_state()
    
    def _load_state(self):
        """加载迭代状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = yaml.safe_load(f)
                self.current_iteration = state.get("current_iteration", 0)
                self.review_opinions = state.get("review_opinions", [])
                self.iteration_history = state.get("iteration_history", [])
    
    def _save_state(self):
        """保存迭代状态"""
        state = {
            "current_iteration": self.current_iteration,
            "max_iterations": self.max_iterations,
            "review_opinions": self.review_opinions,
            "iteration_history": self.iteration_history,
            "updated_at": datetime.now().isoformat()
        }
        with open(self.state_file, 'w') as f:
            yaml.safe_dump(state, f, default_flow_style=False)
    
    def start_iteration(self) -> int:
        """开始新一轮迭代
        
        Returns:
            当前迭代轮次
        """
        if self.current_iteration >= self.max_iterations:
            raise ValueError("已达到最大迭代轮次")
        
        self.current_iteration += 1
        self.review_opinions = []  # 清空审查意见
        self._save_state()
        return self.current_iteration
    
    def add_review_opinion(self, opinion: Dict):
        """添加审查意见
        
        Args:
            opinion: 审查意见
                {
                    "priority": "P0/P1/P2",
                    "dimension": "data/theory/constraint",
                    "issue": "问题描述",
                    "suggestion": "改进建议"
                }
        """
        opinion["added_at"] = datetime.now().isoformat()
        opinion["iteration"] = self.current_iteration
        self.review_opinions.append(opinion)
        self._save_state()
    
    def get_review_opinions(self, priority: Optional[str] = None) -> List[Dict]:
        """获取审查意见
        
        Args:
            priority: 优先级过滤（可选）
            
        Returns:
            审查意见列表
        """
        if priority:
            return [op for op in self.review_opinions if op["priority"] == priority]
        return self.review_opinions
    
    def resolve_opinion(self, opinion_index: int):
        """解决审查意见
        
        Args:
            opinion_index: 审查意见索引
        """
        if 0 <= opinion_index < len(self.review_opinions):
            self.review_opinions[opinion_index]["resolved"] = True
            self.review_opinions[opinion_index]["resolved_at"] = datetime.now().isoformat()
            self._save_state()
    
    def get_unresolved_opinions(self) -> List[Dict]:
        """获取未解决的审查意见"""
        return [op for op in self.review_opinions if not op.get("resolved", False)]
    
    def should_continue_iteration(self) -> bool:
        """检查是否应该继续迭代
        
        Returns:
            True 如果应该继续迭代
        """
        # 检查终止条件
        # 1. 未达到最大迭代轮次
        if self.current_iteration >= self.max_iterations:
            return False
        
        # 2. 所有审查意见已解决
        unresolved = self.get_unresolved_opinions()
        if len(unresolved) == 0:
            return False
        
        # 3. 高优先级意见已解决
        unresolved_p0 = [op for op in unresolved if op["priority"] == "P0"]
        if len(unresolved_p0) == 0:
            # 可以选择终止或继续解决低优先级意见
            return False
        
        return True
    
    def complete_iteration(self, result: Dict):
        """完成迭代
        
        Args:
            result: 迭代结果
        """
        iteration_record = {
            "iteration": self.current_iteration,
            "result": result,
            "review_opinions_count": len(self.review_opinions),
            "resolved_count": len([op for op in self.review_opinions if op.get("resolved", False)]),
            "completed_at": datetime.now().isoformat()
        }
        self.iteration_history.append(iteration_record)
        self._save_state()
    
    def get_iteration_summary(self) -> Dict:
        """获取迭代摘要"""
        return {
            "current_iteration": self.current_iteration,
            "max_iterations": self.max_iterations,
            "total_opinions": len(self.review_opinions),
            "resolved_opinions": len([op for op in self.review_opinions if op.get("resolved", False)]),
            "unresolved_opinions": len(self.get_unresolved_opinions()),
            "should_continue": self.should_continue_iteration(),
            "iteration_history": len(self.iteration_history)
        }
    
    def generate_review_checklist(self) -> str:
        """生成审查意见清单（Markdown 格式）"""
        checklist = f"""# 审查意见清单 - ITERATION {self.current_iteration}

## 审查时间
{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 审查维度
- 数据维度: 待评估
- 理论维度: 待评估
- 约束维度: 待评估

## 审查意见
"""
        
        # P0 高优先级意见
        p0_opinions = self.get_review_opinions("P0")
        if p0_opinions:
            checklist += "### 高优先级 (P0)\n"
            for i, op in enumerate(p0_opinions, 1):
                status = "✅" if op.get("resolved", False) else "⚠️"
                checklist += f"{i}. [{op['dimension']}] {op['issue']} {status}\n"
                checklist += f"   - 建议: {op['suggestion']}\n"
        
        # P1 中优先级意见
        p1_opinions = self.get_review_opinions("P1")
        if p1_opinions:
            checklist += "\n### 中优先级 (P1)\n"
            for i, op in enumerate(p1_opinions, 1):
                status = "✅" if op.get("resolved", False) else "⚠️"
                checklist += f"{i}. [{op['dimension']}] {op['issue']} {status}\n"
                checklist += f"   - 建议: {op['suggestion']}\n"
        
        # P2 低优先级意见
        p2_opinions = self.get_review_opinions("P2")
        if p2_opinions:
            checklist += "\n### 低优先级 (P2)\n"
            for i, op in enumerate(p2_opinions, 1):
                status = "✅" if op.get("resolved", False) else "⚠️"
                checklist += f"{i}. [{op['dimension']}] {op['issue']} {status}\n"
                checklist += f"   - 建议: {op['suggestion']}\n"
        
        # 决策
        checklist += f"""
## 决策
"""
        if self.should_continue_iteration():
            checklist += f"继续迭代 (ITERATION {self.current_iteration + 1}), 重点解决高优先级意见\n"
        else:
            checklist += "终止迭代，准备交付\n"
        
        return checklist


if __name__ == "__main__":
    # 示例用法
    manager = IterationManager("/tmp/test_project")
    manager.start_iteration()
    
    # 添加审查意见
    manager.add_review_opinion({
        "priority": "P0",
        "dimension": "data",
        "issue": "实验 3 的结果数据需复验",
        "suggestion": "重新执行实验 3"
    })
    
    manager.add_review_opinion({
        "priority": "P1",
        "dimension": "theory",
        "issue": "引用 [15] 的 Levenshtein 匹配度仅 65%",
        "suggestion": "替换为更权威的文献"
    })
    
    # 生成审查意见清单
    print(manager.generate_review_checklist())