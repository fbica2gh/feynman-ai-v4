"""
Feynman Research v5.0 - feynman-init
一键生成项目骨架

功能：
- 创建目录结构
- 初始化配置文件
- 生成模板文件
"""

import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class FeynmanInit:
    """项目骨架生成器"""
    
    def __init__(self, research_topic: str, output_path: Optional[str] = None):
        """初始化
        
        Args:
            research_topic: 研究主题
            output_path: 输出路径（可选，默认为当前目录）
        """
        self.research_topic = research_topic
        self.project_name = self._generate_project_name(research_topic)
        self.output_path = Path(output_path or os.getcwd()) / self.project_name
        
    def _generate_project_name(self, topic: str) -> str:
        """生成项目名称
        
        Args:
            topic: 研究主题
            
        Returns:
            项目名称（如 project_quantum_crypto）
        """
        # 简化主题名称
        words = topic.lower().split()
        if len(words) > 3:
            words = words[:3]
        return "project_" + "_".join(words)
    
    def create_structure(self) -> Dict[str, Path]:
        """创建目录结构
        
        Returns:
            创建的目录路径字典
        """
        # 目录结构定义
        directories = {
            "root": self.output_path,
            "data_raw": self.output_path / "data" / "raw",
            "data_processed": self.output_path / "data" / "processed",
            "data_results": self.output_path / "data" / "results",
            "literature": self.output_path / "literature",
            "experiments": self.output_path / "experiments",
            "output_draft": self.output_path / "output" / "draft",
            "output_final": self.output_path / "output" / "final",
            "reviews": self.output_path / "reviews",
            "logs": self.output_path / "logs"
        }
        
        # 创建目录
        for name, path in directories.items():
            path.mkdir(parents=True, exist_ok=True)
        
        return directories
    
    def generate_readme(self) -> str:
        """生成 README.md"""
        return f"""# {self.research_topic}

## 项目说明
本项目由 Feynman AI v5.0 自动生成

## 研究阶段
- ASK: 接收研究主题
- PLAN: 假设生成 + 任务分解
- REVIEW (P1): 假设审查
- ITERATION 1: 初步分析迭代
- BUILD: 实验设计与执行
- REVIEW (P0): 结果审查
- ITERATION 2: 输出迭代
- OUTPUT: 最终交付

## 目录结构
```
{self.project_name}/
├── README.md               # 项目说明
├── research_goal.md        # 研究目标文档
├── hypothesis.md           # 假设列表
├── plan.md                 # 研究计划表
├── state.yaml             # 状态管理
├── iteration_state.yaml   # 迭代状态
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
├── reviews/               # 审查目录
│   ├── p1_review.md      # P1 审查意见
│   ├── p0_review.md      # P0 审查意见
└── logs/                  # 日志目录
```

## 创建时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Feynman AI v5.0
"If you can't explain it simply, you don't understand it well enough."
"""
    
    def generate_research_goal(self) -> str:
        """生成研究目标文档模板"""
        return f"""# 研究目标文档

## 研究主题
{self.research_topic}

## 研究动机
待用户确认

## 研究范围
待定义

## 关键约束条件
待识别

## 期望输出
待明确

## 创建时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def generate_state_file(self) -> Dict:
        """生成状态文件"""
        return {
            "project_name": self.project_name,
            "research_topic": self.research_topic,
            "stage": "ASK",
            "stage_index": 0,
            "iteration_count": 0,
            "max_iterations": 5,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "reviews": {
                "p1_review": None,
                "p0_review": None
            },
            "outputs": []
        }
    
    def generate_iteration_state(self) -> Dict:
        """生成迭代状态文件"""
        return {
            "current_iteration": 0,
            "max_iterations": 5,
            "review_opinions": [],
            "iteration_history": [],
            "created_at": datetime.now().isoformat()
        }
    
    def generate_config_files(self) -> Dict[str, Dict]:
        """生成配置文件"""
        return {
            "agent_models.yaml": {
                "coordinator": {"model": "qwen/qwen3.5-plus", "level": "advanced"},
                "hypothesis": {"model": "qwen/qwen3.5-plus", "level": "advanced"},
                "search": {"model": "ling-2.6-flash-free", "level": "fast"},
                "analysis": {"model": "qwen/glm-5", "level": "standard"},
                "literature_review": {"model": "qwen/glm-5", "level": "standard"},
                "experiment": {"model": "qwen/qwen3.5-plus", "level": "advanced"},
                "quality": {"model": "qwen/qwen3.5-plus", "level": "advanced"},
                "output": {"model": "qwen/glm-5", "level": "standard"}
            },
            "iteration_config.yaml": {
                "max_iterations": 5,
                "review_threshold": {
                    "p0": 90,
                    "p1": 80
                },
                "token_optimization": True
            },
            "review_standards.yaml": {
                "p1_standards": {
                    "direction_correctness": {"weight": 40, "threshold": 80},
                    "hypothesis_verifiability": {"weight": 30, "threshold": 80},
                    "resource_feasibility": {"weight": 20, "threshold": 80},
                    "boundary_clarity": {"weight": 10, "threshold": 80}
                },
                "p0_standards": {
                    "data_dimension": {"weight": 35, "threshold": 90},
                    "theory_dimension": {"weight": 30, "threshold": 90},
                    "constraint_dimension": {"weight": 20, "threshold": 90},
                    "logic_consistency": {"weight": 15, "threshold": 90}
                }
            }
        }
    
    def initialize(self) -> Dict:
        """初始化项目
        
        Returns:
            初始化结果
        """
        # 创建目录结构
        directories = self.create_structure()
        
        # 生成文件
        readme_path = self.output_path / "README.md"
        with open(readme_path, 'w') as f:
            f.write(self.generate_readme())
        
        goal_path = self.output_path / "research_goal.md"
        with open(goal_path, 'w') as f:
            f.write(self.generate_research_goal())
        
        state_path = self.output_path / "state.yaml"
        with open(state_path, 'w') as f:
            yaml.safe_dump(self.generate_state_file(), f, default_flow_style=False)
        
        iteration_path = self.output_path / "iteration_state.yaml"
        with open(iteration_path, 'w') as f:
            yaml.safe_dump(self.generate_iteration_state(), f, default_flow_style=False)
        
        # 生成配置文件
        config_files = self.generate_config_files()
        config_dir = self.output_path / "config"
        config_dir.mkdir(exist_ok=True)
        
        for filename, content in config_files.items():
            config_file = config_dir / filename
            with open(config_file, 'w') as f:
                yaml.safe_dump(content, f, default_flow_style=False)
        
        # 生成初始审查文件
        p1_review_path = self.output_path / "reviews" / "p1_review.md"
        with open(p1_review_path, 'w') as f:
            f.write("# P1 审查意见清单\n\n待生成\n")
        
        p0_review_path = self.output_path / "reviews" / "p0_review.md"
        with open(p0_review_path, 'w') as f:
            f.write("# P0 审查意见清单\n\n待生成\n")
        
        return {
            "project_path": str(self.output_path),
            "project_name": self.project_name,
            "directories": {k: str(v) for k, v in directories.items()},
            "files_created": [
                "README.md",
                "research_goal.md",
                "state.yaml",
                "iteration_state.yaml",
                "config/agent_models.yaml",
                "config/iteration_config.yaml",
                "config/review_standards.yaml",
                "reviews/p1_review.md",
                "reviews/p0_review.md"
            ],
            "created_at": datetime.now().isoformat()
        }


def feynman_init(research_topic: str, output_path: Optional[str] = None) -> Dict:
    """一键生成项目骨架
    
    Args:
        research_topic: 研究主题
        output_path: 输出路径（可选）
        
    Returns:
        初始化结果
    """
    init_tool = FeynmanInit(research_topic, output_path)
    return init_tool.initialize()


if __name__ == "__main__":
    # 示例用法
    result = feynman_init("量子计算对密码学的影响", "/tmp")
    print(f"项目路径: {result['project_path']}")
    print(f"创建的文件: {result['files_created']}")