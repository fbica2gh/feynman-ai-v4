"""
局限性分析器 (LimitationAnalyzer)
诚实评估研究局限性
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Limitation:
    """局限性数据结构"""
    category: str  # data/method/generalizability/measurement
    description: str
    impact: str  # 高/中等/低
    impact_score: float = 0.0  # 0-10
    mitigation: str = ""


@dataclass
class LimitationAnalysis:
    """局限性分析结果"""
    limitations: List[Limitation] = field(default_factory=list)
    overall_impact: str = ""
    improvement_suggestions: List[str] = field(default_factory=list)


class LimitationAnalyzer:
    """局限性分析器"""

    def identify_limitations(self, study_type: str = "IMC") -> LimitationAnalysis:
        """
        识别局限性

        类别:
        1. 数据局限 (Data limitations)
        2. 方法局限 (Method limitations)
        3. 推广性局限 (Generalizability limitations)
        4. 测量局限 (Measurement limitations)
        """
        analysis = LimitationAnalysis()

        if study_type == "IMC":
            analysis.limitations = [
                Limitation(
                    category="数据局限",
                    description="仅基于文献数据，无实验验证",
                    impact="高",
                    impact_score=8.0,
                    mitigation="需要实验验证最佳厚度范围",
                ),
                Limitation(
                    category="方法局限",
                    description="未考虑不同焊料合金的差异",
                    impact="中等",
                    impact_score=6.0,
                    mitigation="研究 SAC305/SnPb/lead-free 的差异",
                ),
                Limitation(
                    category="推广性局限",
                    description="仅适用于 SAC305 焊料 + Cu 焊盘",
                    impact="中等",
                    impact_score=5.5,
                    mitigation="扩展到其他合金和焊盘类型",
                ),
                Limitation(
                    category="测量局限",
                    description="IMC 厚度测量方法不一致 (SEM vs 金相)",
                    impact="低",
                    impact_score=3.0,
                    mitigation="统一使用 SEM 截面分析",
                ),
            ]

        # 评估总体影响
        max_impact = max([l.impact_score for l in analysis.limitations]) if analysis.limitations else 0
        if max_impact >= 7:
            analysis.overall_impact = "高 - 可能改变结论"
        elif max_impact >= 4:
            analysis.overall_impact = "中等 - 可能影响结论精度"
        else:
            analysis.overall_impact = "低 - 对结论影响小"

        # 改进建议
        analysis.improvement_suggestions = [
            l.mitigation for l in analysis.limitations if l.mitigation
        ]

        return analysis

    def assess_impact(self, limitation: Limitation) -> Dict:
        """评估影响程度"""
        return {
            "category": limitation.category,
            "description": limitation.description,
            "impact": limitation.impact,
            "impact_score": limitation.impact_score,
            "mitigation": limitation.mitigation,
        }

    def suggest_improvements(self, analysis: LimitationAnalysis) -> List[str]:
        """建议改进方向"""
        return analysis.improvement_suggestions
