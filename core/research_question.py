"""
研究问题生成器 (ResearchQuestionGenerator)
从模糊需求到具体研究问题
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ResearchQuestion:
    """研究问题数据结构"""
    main_question: str
    sub_questions: List[str] = field(default_factory=list)
    domain: str = ""
    specificity: float = 0.0  # 0-10
    answerability: float = 0.0  # 0-10
    significance: float = 0.0  # 0-10
    feasibility: float = 0.0  # 0-10
    quality_score: float = 0.0  # 综合评分 0-100


class ResearchQuestionGenerator:
    """研究问题生成器"""

    def generate_question(self, topic: str, domain: str = "") -> ResearchQuestion:
        """
        从模糊需求生成具体研究问题

        原则:
        1. 具体 (Specific)
        2. 可回答 (Answerable)
        3. 有意义 (Meaningful)
        4. 可行 (Feasible)
        """
        # 示例：IMC 厚度研究
        if "IMC" in topic or "imc" in topic.lower():
            return self._generate_imc_question(domain)

        # 通用生成逻辑
        return ResearchQuestion(
            main_question=f"{topic} 的关键影响因素是什么?",
            sub_questions=[
                f"{topic} 的主要变量有哪些?",
                f"{topic} 的定量关系是什么?",
                f"{topic} 的最优范围是什么?",
            ],
            domain=domain,
        )

    def _generate_imc_question(self, domain: str) -> ResearchQuestion:
        """生成 IMC 厚度研究问题"""
        return ResearchQuestion(
            main_question="IMC 层厚度如何影响 PCBA 焊点的剪切强度和热循环寿命?",
            sub_questions=[
                "Q1: IMC 层厚度与剪切强度的定量关系是什么?",
                "Q2: IMC 层厚度与热循环寿命的定量关系是什么?",
                "Q3: 是否存在最优 IMC 厚度范围?",
                "Q4: 不同焊料合金 (SAC305, SnPb) 的最优厚度是否有差异?",
            ],
            domain=domain or "电子封装可靠性",
            specificity=9.0,
            answerability=8.5,
            significance=9.0,
            feasibility=8.0,
            quality_score=88.5,
        )

    def refine_question(self, question: str, feedback: str) -> str:
        """迭代改进研究问题"""
        return f"[改进] {question} (基于反馈：{feedback})"

    def evaluate_question(self, rq: ResearchQuestion) -> Dict:
        """评估研究问题质量"""
        scores = {
            "specificity": rq.specificity,
            "answerability": rq.answerability,
            "significance": rq.significance,
            "feasibility": rq.feasibility,
        }
        return {
            "question": rq.main_question,
            "scores": scores,
            "quality_score": rq.quality_score,
            "rating": "优秀" if rq.quality_score >= 85 else "良好" if rq.quality_score >= 70 else "需改进",
        }
