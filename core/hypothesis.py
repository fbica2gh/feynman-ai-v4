"""
假设生成器 (HypothesisGenerator)
提出可验证的假设
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Hypothesis:
    """假设数据结构"""
    id: str
    statement: str
    null_hypothesis: str = ""
    alternative_hypothesis: str = ""
    predict_direction: str = ""  # positive/negative/inverted-U
    predict_value: Dict = field(default_factory=dict)  # 预测值
    falsifiable: bool = True
    specificity: float = 0.0  # 0-10
    literature_based: bool = False
    references: List[str] = field(default_factory=list)
    quantifiable: bool = True
    quality_score: float = 0.0  # 0-100


class HypothesisGenerator:
    """假设生成器"""

    def generate_hypothesis(self, question: str, literature: List[Dict] = None) -> List[Hypothesis]:
        """
        生成假设

        原则:
        1. 可证伪 (Falsifiable)
        2. 具体 (Specific)
        3. 基于文献 (Literature-based)
        4. 可量化 (Quantifiable)
        """
        if "IMC" in question or "imc" in question.lower():
            return self._generate_imc_hypotheses(literature)

        # 通用假设生成
        return [
            Hypothesis(
                id="H1",
                statement=f"{question} 存在显著影响",
                falsifiable=True,
                specificity=7.0,
                quantifiable=True,
            )
        ]

    def _generate_imc_hypotheses(self, literature: List[Dict] = None) -> List[Hypothesis]:
        """生成 IMC 厚度研究假设"""
        hypotheses = [
            Hypothesis(
                id="H1",
                statement="IMC 层厚度与剪切强度呈倒 U 型关系，峰值在 1.5-2.5 μm",
                null_hypothesis="H0: IMC 厚度与剪切强度无线性或二次关系",
                alternative_hypothesis="H1: IMC 厚度与剪切强度呈显著二次关系 (p < 0.05)",
                predict_direction="inverted-U",
                predict_value={"peak_thickness": "1.5-2.5 μm", "peak_strength": "35-40 MPa"},
                falsifiable=True,
                specificity=9.0,
                literature_based=True,
                references=["Hong & Huh 2009", "Lin 2006"],
                quantifiable=True,
                quality_score=92.0,
            ),
            Hypothesis(
                id="H2",
                statement="IMC 层厚度 > 3.0 μm 时，剪切强度显著下降 (>15%, p < 0.01)",
                null_hypothesis="H0: IMC 厚度 > 3.0 μm 时强度不显著变化",
                alternative_hypothesis="H1: IMC 厚度 > 3.0 μm 时强度显著下降 (p < 0.01)",
                predict_direction="negative",
                predict_value={"threshold": "3.0 μm", "decline": ">15%"},
                falsifiable=True,
                specificity=9.5,
                literature_based=True,
                references=["IPC-A-610", "Lee 2008"],
                quantifiable=True,
                quality_score=95.0,
            ),
            Hypothesis(
                id="H3",
                statement="IMC 层厚度 < 1.0 μm 时，热循环寿命显著降低 (>30%, p < 0.05)",
                null_hypothesis="H0: IMC 厚度 < 1.0 μm 时寿命不显著变化",
                alternative_hypothesis="H1: IMC 厚度 < 1.0 μm 时寿命显著降低 (p < 0.05)",
                predict_direction="positive",
                predict_value={"threshold": "1.0 μm", "decline": ">30%"},
                falsifiable=True,
                specificity=8.5,
                literature_based=True,
                references=["Jesmann 2006", "Kang 2007"],
                quantifiable=True,
                quality_score=88.0,
            ),
            Hypothesis(
                id="H4",
                statement="Cu₃Sn 层厚度占比 > 40% 时，跌落性能显著下降",
                null_hypothesis="H0: Cu₃Sn 占比对跌落性能无显著影响",
                alternative_hypothesis="H1: Cu₃Sn 占比 > 40% 时跌落性能显著下降 (p < 0.05)",
                predict_direction="negative",
                predict_value={"threshold": "40%", "decline": ">25%"},
                falsifiable=True,
                specificity=8.0,
                literature_based=True,
                references=["Yeh 2007", "Huang 2009"],
                quantifiable=True,
                quality_score=85.0,
            ),
        ]
        return hypotheses

    def evaluate_hypothesis(self, h: Hypothesis) -> Dict:
        """评估假设质量"""
        score = 0
        score += 25 if h.falsifiable else 0
        score += 25 * (h.specificity / 10)
        score += 25 if h.literature_based else 0
        score += 25 if h.quantifiable else 0
        h.quality_score = score

        return {
            "hypothesis": h.statement,
            "id": h.id,
            "falsifiable": h.falsifiable,
            "specificity": h.specificity,
            "literature_based": h.literature_based,
            "quantifiable": h.quantifiable,
            "quality_score": score,
            "rating": "强" if score >= 85 else "中等" if score >= 70 else "弱",
        }
