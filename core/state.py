"""
Feynman Research v4.0 - 状态管理
参考 DATAGEN State 设计
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ResearchState:
    """研究状态 - Action Log + Artifact Digest"""
    
    # === 上下文层 ===
    messages: List[Dict] = field(default_factory=list)
    last_active_agent: Optional[str] = None
    step_count: int = 0
    
    # === 工作流控制 ===
    current_instruction: Optional[str] = None
    next_workflow_step: Optional[str] = None
    
    # === 任务追踪 ===
    todo_list: List[str] = field(default_factory=list)
    completed_tasks: List[str] = field(default_factory=list)
    
    # === 研究产物 ===
    # 假设
    hypothesis: Optional[str] = None
    hypothesis_score: float = 0.0
    
    # 实验
    experiment_design: Optional[Dict] = None
    experiment_results: Optional[Dict] = None
    
    # 文献
    literature_review: Dict[str, str] = field(default_factory=dict)
    citations: Dict[str, Dict] = field(default_factory=dict)  # {citation_id: {verified, quality}}
    
    # 分析
    search_artifacts: Dict[str, str] = field(default_factory=dict)
    analysis_artifacts: Dict[str, str] = field(default_factory=dict)
    
    # 输出
    report_sections: Dict[str, str] = field(default_factory=dict)
    
    # === 质量反馈 ===
    quality_feedback: Optional[str] = None
    quality_score: float = 0.0
    
    # === Token 统计 ===
    token_usage: Dict[str, int] = field(default_factory=dict)
    total_tokens: int = 0
    
    # === 时间统计 ===
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    agent_times: Dict[str, float] = field(default_factory=dict)
    
    def add_artifact(self, agent_name: str, artifact_type: str, path: str, summary: str):
        """添加产物"""
        if artifact_type == 'search':
            self.search_artifacts[path] = summary
        elif artifact_type == 'analysis':
            self.analysis_artifacts[path] = summary
        elif artifact_type == 'literature':
            self.literature_review[path] = summary
        elif artifact_type == 'report':
            self.report_sections[agent_name] = summary
    
    def update_tokens(self, agent_name: str, tokens: int):
        """更新 Token 统计"""
        self.token_usage[agent_name] = tokens
        self.total_tokens += tokens
    
    def mark_complete(self, task: str):
        """标记任务完成"""
        if task in self.todo_list:
            self.todo_list.remove(task)
            self.completed_tasks.append(task)
    
    def get_progress(self) -> float:
        """获取进度"""
        total = len(self.todo_list) + len(self.completed_tasks)
        if total == 0:
            return 0.0
        return len(self.completed_tasks) / total * 100


@dataclass
class HypothesisState:
    """假设状态"""
    hypothesis_id: str
    hypothesis_text: str
    confidence: float
    experiments: List[Dict] = field(default_factory=list)
    verified: bool = False
    verification_result: Optional[str] = None


@dataclass
class CitationState:
    """引用状态"""
    citation_id: str
    citation_text: str
    verified: bool = False
    levenshtein_score: float = 0.0
    quality_grade: str = 'P2'  # P0/P1/P2/reject
    semantic_scholar_match: Optional[Dict] = None


@dataclass
class ExperimentState:
    """实验状态"""
    experiment_id: str
    hypothesis_id: str
    design: Dict
    results: Optional[Dict] = None
    status: str = 'pending'  # pending/running/completed/failed
    insights: Optional[List[str]] = None


class StateManager:
    """状态管理器"""
    
    def __init__(self):
        self.state = ResearchState()
        self.hypotheses: Dict[str, HypothesisState] = {}
        self.citations: Dict[str, CitationState] = {}
        self.experiments: Dict[str, ExperimentState] = {}
    
    def create_hypothesis(self, hypothesis_text: str, confidence: float) -> HypothesisState:
        """创建假设"""
        hypothesis_id = f"hyp_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        hypothesis = HypothesisState(
            hypothesis_id=hypothesis_id,
            hypothesis_text=hypothesis_text,
            confidence=confidence
        )
        self.hypotheses[hypothesis_id] = hypothesis
        self.state.hypothesis = hypothesis_text
        self.state.hypothesis_score = confidence
        return hypothesis
    
    def create_citation(self, citation_text: str) -> CitationState:
        """创建引用"""
        citation_id = f"cit_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        citation = CitationState(
            citation_id=citation_id,
            citation_text=citation_text
        )
        self.citations[citation_id] = citation
        return citation
    
    def create_experiment(self, hypothesis_id: str, design: Dict) -> ExperimentState:
        """创建实验"""
        experiment_id = f"exp_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        experiment = ExperimentState(
            experiment_id=experiment_id,
            hypothesis_id=hypothesis_id,
            design=design
        )
        self.experiments[experiment_id] = experiment
        return experiment
    
    def get_summary(self) -> Dict:
        """获取摘要"""
        return {
            'progress': self.state.get_progress(),
            'hypotheses': len(self.hypotheses),
            'verified_hypotheses': sum(1 for h in self.hypotheses.values() if h.verified),
            'citations': len(self.citations),
            'verified_citations': sum(1 for c in self.citations.values() if c.verified),
            'experiments': len(self.experiments),
            'completed_experiments': sum(1 for e in self.experiments.values() if e.status == 'completed'),
            'total_tokens': self.state.total_tokens
        }