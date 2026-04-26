"""
结论推导器 (ConclusionDeriver)
从数据推导结论
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Conclusion:
    """结论数据结构"""
    hypothesis_id: str
    statement: str = ""
    supported: bool = False
    evidence_strength: str = ""  # 强/中等/弱/不足
    p_value: float = 1.0
    effect_size: float = 0.0
    confidence_interval: str = ""
    causal_chain: List[str] = field(default_factory=list)
    alternative_explanations: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)


class ConclusionDeriver:
    """结论推导器"""

    def derive_conclusion(self, hypothesis_id: str, analysis_result: Dict) -> Conclusion:
        """
        推导结论

        原则:
        1. 基于数据 (Data-driven)
        2. 量化 (Quantified)
        3. 不确定性 (Uncertainty)
        4. 因果链 (Causal chain)
        """
        conclusion = Conclusion(hypothesis_id=hypothesis_id)

        # 判断证据强度
        p_value = analysis_result.get("p_value", 1.0)
        r_squared = analysis_result.get("r_squared", 0.0)
        n = analysis_result.get("sample_size", 0)

        if p_value < 0.001 and r_squared > 0.8 and n > 30:
            conclusion.evidence_strength = "强"
            conclusion.supported = True
        elif p_value < 0.01 and r_squared > 0.6 and n > 15:
            conclusion.evidence_strength = "中等"
            conclusion.supported = True
        elif p_value < 0.05 and r_squared > 0.4 and n > 10:
            conclusion.evidence_strength = "弱"
            conclusion.supported = True
        else:
            conclusion.evidence_strength = "不足"
            conclusion.supported = False

        conclusion.p_value = p_value
        conclusion.effect_size = analysis_result.get("effect_size", 0.0)
        conclusion.confidence_interval = analysis_result.get("confidence_interval", "")

        return conclusion

    def evaluate_evidence(self, conclusion: Conclusion) -> Dict:
        """评估证据强度"""
        return {
            "hypothesis_id": conclusion.hypothesis_id,
            "supported": conclusion.supported,
            "evidence_strength": conclusion.evidence_strength,
            "p_value": conclusion.p_value,
            "effect_size": conclusion.effect_size,
            "rating": conclusion.evidence_strength,
        }

    def check_alternatives(self, conclusion: Conclusion) -> List[str]:
        """检查替代解释"""
        alternatives = [
            "测量误差是否已控制?",
            "混杂因素是否已排除?",
            "样本是否具有代表性?",
        ]
        conclusion.alternative_explanations = alternatives
        return alternatives

    def generate_causal_chain(self, conclusion: Conclusion) -> List[str]:
        """生成因果链"""
        chain = [
            "IMC 厚度变化 → 界面力学性能变化",
            "界面力学性能变化 → 焊点强度变化",
            "焊点强度变化 → 可靠性变化",
        ]
        conclusion.causal_chain = chain
        return chain
