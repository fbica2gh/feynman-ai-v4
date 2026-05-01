"""
Feynman Research v5.0 - Workflow Engine
8 阶段流程引擎（Fair 整合版）

阶段流程：
ASK → PLAN → REVIEW → ITERATION → BUILD → REVIEW → ITERATION → OUTPUT
"""

import os
import yaml
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class FeynmanWorkflowV5:
    """Feynman v5.0 工作流引擎"""
    
    # 8 阶段定义（Fair 整合）
    STAGES = [
        "ASK",           # 接收研究主题，渐进式披露问答
        "PLAN",          # 假设生成 + 任务分解 + 验证计划
        "REVIEW",        # P1 假设审查（方向正确）
        "ITERATION_1",   # 初步分析迭代（信息收集 + 文献综述 + 三维度验证）
        "BUILD",         # 实验设计与执行
        "REVIEW_2",      # P0 结果审查（事实准确）
        "ITERATION_2",   # 输出迭代（Feynman 式输出 + 可视化）
        "OUTPUT"         # 最终交付（多格式输出 + 质量保证）
    ]
    
    # 阶段到 Agent 映射
    STAGE_AGENT_MAP = {
        "ASK": ["coordinator"],
        "PLAN": ["hypothesis", "coordinator"],
        "REVIEW": ["quality"],  # P1 假设审查
        "ITERATION_1": ["analysis", "literature_review", "quality"],
        "BUILD": ["experiment", "search"],
        "REVIEW_2": ["quality"],  # P0 结果审查
        "ITERATION_2": ["output", "quality"],
        "OUTPUT": ["output"]
    }
    
    # Token 优化模式映射
    TOKEN_MODE_MAP = {
        "ASK": "normal",
        "PLAN": "lite",
        "REVIEW": "normal",
        "ITERATION_1": "ultra",  # analysis + literature_review
        "BUILD": "ultra",
        "REVIEW_2": "normal",
        "ITERATION_2": "lite",
        "OUTPUT": "normal"
    }
    
    def __init__(self, project_path: str, config_path: Optional[str] = None):
        """初始化工作流
        
        Args:
            project_path: 项目目录路径
            config_path: 配置文件路径（可选）
        """
        self.project_path = Path(project_path)
        self.current_stage = 0
        self.iteration_count = 0
        self.max_iterations = 5
        self.state = self._load_state()
        self.config = self._load_config(config_path)
        
    def _load_state(self) -> Dict:
        """加载状态文件"""
        state_file = self.project_path / "state.yaml"
        if state_file.exists():
            with open(state_file, 'r') as f:
                return yaml.safe_load(f)
        return {
            "stage": self.STAGES[0],
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
    
    def _save_state(self):
        """保存状态文件"""
        self.state["updated_at"] = datetime.now().isoformat()
        state_file = self.project_path / "state.yaml"
        with open(state_file, 'w') as f:
            yaml.safe_dump(self.state, f, default_flow_style=False)
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {
            "max_iterations": 5,
            "review_threshold": {
                "p0": 90,  # 数据/理论/约束维度均 >90%
                "p1": 80   # 假设可验证性 >80%
            },
            "token_optimization": True
        }
    
    def get_current_stage(self) -> str:
        """获取当前阶段"""
        return self.STAGES[self.current_stage]
    
    def get_agents_for_stage(self, stage: str) -> List[str]:
        """获取阶段对应的 Agent"""
        return self.STAGE_AGENT_MAP.get(stage, [])
    
    def get_token_mode(self, stage: str) -> str:
        """获取阶段的 Token 优化模式"""
        return self.TOKEN_MODE_MAP.get(stage, "normal")
    
    def advance_stage(self) -> Optional[str]:
        """推进到下一阶段
        
        Returns:
            下一阶段名称，如果已完成则返回 None
        """
        if self.current_stage < len(self.STAGES) - 1:
            self.current_stage += 1
            self.state["stage"] = self.STAGES[self.current_stage]
            self.state["stage_index"] = self.current_stage
            self._save_state()
            return self.STAGES[self.current_stage]
        return None
    
    def execute_stage(self, stage: str, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """执行阶段
        
        Args:
            stage: 阶段名称
            agent_results: Agent 执行结果
            
        Returns:
            阶段执行结果
        """
        stage_result = {
            "stage": stage,
            "agents": self.get_agents_for_stage(stage),
            "token_mode": self.get_token_mode(stage),
            "results": agent_results,
            "timestamp": datetime.now().isoformat()
        }
        
        # 处理特定阶段
        if stage == "REVIEW":
            # P1 假设审查
            stage_result["review_type"] = "P1"
            stage_result["decision"] = self._process_p1_review(agent_results)
        
        elif stage == "REVIEW_2":
            # P0 结果审查
            stage_result["review_type"] = "P0"
            stage_result["decision"] = self._process_p0_review(agent_results)
        
        elif stage == "ITERATION_2":
            # 输出迭代
            self.iteration_count += 1
            self.state["iteration_count"] = self.iteration_count
            stage_result["iteration"] = self.iteration_count
            
            # 检查迭代终止条件
            if self.iteration_count >= self.max_iterations:
                stage_result["max_iterations_reached"] = True
        
        # 保存阶段结果
        output_file = self.project_path / "output" / f"{stage.lower()}_result.yaml"
        with open(output_file, 'w') as f:
            yaml.safe_dump(stage_result, f, default_flow_style=False)
        
        self._save_state()
        return stage_result
    
    def _process_p1_review(self, agent_results: Dict) -> str:
        """处理 P1 假设审查
        
        Returns:
            决策结果: "continue", "modify", "abort"
        """
        quality_result = agent_results.get("quality", {})
        p1_score = quality_result.get("p1_score", 0)
        threshold = self.config["review_threshold"]["p1"]
        
        if p1_score >= threshold:
            return "continue"
        elif p1_score >= threshold * 0.8:
            return "modify"
        else:
            return "abort"
    
    def _process_p0_review(self, agent_results: Dict) -> str:
        """处理 P0 结果审查
        
        Returns:
            决策结果: "deliver", "iterate", "abort"
        """
        quality_result = agent_results.get("quality", {})
        
        # 三维度验证
        data_score = quality_result.get("data_score", 0)
        theory_score = quality_result.get("theory_score", 0)
        constraint_score = quality_result.get("constraint_score", 0)
        
        threshold = self.config["review_threshold"]["p0"]
        
        if data_score >= threshold and theory_score >= threshold and constraint_score >= threshold:
            return "deliver"
        elif self.iteration_count < self.max_iterations:
            return "iterate"
        else:
            return "abort"  # 超过最大迭代轮次
    
    def is_complete(self) -> bool:
        """检查工作流是否完成"""
        return self.current_stage == len(self.STAGES) - 1
    
    def get_progress(self) -> Dict:
        """获取进度信息"""
        return {
            "current_stage": self.STAGES[self.current_stage],
            "stage_index": self.current_stage,
            "total_stages": len(self.STAGES),
            "progress_percent": (self.current_stage + 1) / len(self.STAGES) * 100,
            "iteration_count": self.iteration_count,
            "max_iterations": self.max_iterations
        }


class StageExecutor:
    """阶段执行器"""
    
    def __init__(self, workflow: FeynmanWorkflowV5):
        self.workflow = workflow
    
    def execute_ask_stage(self, research_topic: str) -> Dict:
        """执行 ASK 阶段
        
        Args:
            research_topic: 研究主题
            
        Returns:
            研究目标文档
        """
        # 渐进式披露问答（Phase 0）
        # 生成研究目标文档
        return {
            "research_topic": research_topic,
            "research_goal": "待用户确认",
            "scope": "待定义",
            "constraints": "待识别"
        }
    
    def execute_plan_stage(self, ask_result: Dict) -> Dict:
        """执行 PLAN 阶段
        
        Args:
            ask_result: ASK 阶段结果
            
        Returns:
            研究计划表 + 假设列表
        """
        # Hypothesis Agent: 生成假设
        # Coordinator: 任务分解
        return {
            "hypotheses": [],
            "plan": {},
            "token_budget": {}
        }
    
    def execute_review_stage(self, plan_result: Dict, review_type: str = "P1") -> Dict:
        """执行 REVIEW 阶段
        
        Args:
            plan_result: PLAN 阶段结果
            review_type: P1 或 P0
            
        Returns:
            审查意见清单
        """
        # Quality Agent: 生成审查意见清单
        return {
            "review_type": review_type,
            "p1_score": 0,  # P1 假设审查得分
            "p0_score": 0,  # P0 结果审查得分（三维度）
            "opinions": [],
            "decision": "continue"
        }
    
    def execute_iteration_stage(self, iteration: int, previous_result: Dict) -> Dict:
        """执行 ITERATION 阶段
        
        Args:
            iteration: 迭代轮次（1 或 2）
            previous_result: 前一阶段结果
            
        Returns:
            迭代结果
        """
        if iteration == 1:
            # ITERATION 1: 初步分析（Analysis + Literature Review）
            return {
                "analysis_result": {},
                "literature_result": {},
                "validation_scores": {
                    "data": 0,
                    "theory": 0,
                    "constraint": 0
                }
            }
        else:
            # ITERATION 2: 输出迭代（Output）
            return {
                "draft_version": f"v{iteration}",
                "content": "",
                "visualizations": []
            }
    
    def execute_build_stage(self, iteration_1_result: Dict) -> Dict:
        """执行 BUILD 阶段
        
        Args:
            iteration_1_result: ITERATION 1 结果
            
        Returns:
            实验结果报告
        """
        # Experiment Agent: 实验设计
        # Search Agent: 信息收集
        return {
            "experiment_design": {},
            "experiment_results": {},
            "data_collection": {}
        }
    
    def execute_output_stage(self, iteration_2_result: Dict) -> Dict:
        """执行 OUTPUT 阶段
        
        Args:
            iteration_2_result: ITERATION 2 结果
            
        Returns:
            最终研究报告
        """
        # Output Agent: 多格式输出
        return {
            "formats": ["markdown", "pdf", "docx", "pptx"],
            "final_report": "",
            "quality_assurance": {}
        }


if __name__ == "__main__":
    # 示例用法
    workflow = FeynmanWorkflowV5("/tmp/test_project")
    print(f"当前阶段: {workflow.get_current_stage()}")
    print(f"进度: {workflow.get_progress()}")