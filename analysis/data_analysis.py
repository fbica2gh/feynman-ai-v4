"""
数据分析器 (DataAnalyzer)
统计分析验证假设
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import numpy as np
from scipy import stats


@dataclass
class AnalysisResult:
    """分析结果数据结构"""
    hypothesis_id: str
    test_type: str  # t-test/ANOVA/regression/correlation
    statistic: float = 0.0
    p_value: float = 1.0
    significant: bool = False
    effect_size: float = 0.0
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    r_squared: float = 0.0
    model_type: str = ""
    model_params: Dict = field(default_factory=dict)
    conclusion: str = ""
    evidence_strength: str = ""  # 强/中等/弱/不足


class DataAnalyzer:
    """数据分析器"""

    def descriptive_stats(self, data: Dict[str, List[float]]) -> Dict:
        """描述性统计"""
        result = {}
        for group, values in data.items():
            arr = np.array(values)
            result[group] = {
                "mean": float(np.mean(arr)),
                "std": float(np.std(arr)),
                "median": float(np.median(arr)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "n": len(values),
            }
        return result

    def hypothesis_test(self, data: Dict[str, List[float]], hypothesis_id: str) -> AnalysisResult:
        """假设检验"""
        result = AnalysisResult(hypothesis_id=hypothesis_id, test_type="ANOVA")

        groups = list(data.values())
        if len(groups) >= 2:
            f_stat, p_value = stats.f_oneway(*groups)
            result.statistic = float(f_stat)
            result.p_value = float(p_value)
            result.significant = p_value < 0.05

            # 效应量 (eta-squared)
            result.effect_size = self._calculate_eta_squared(groups, f_stat, len(groups[0]))

        return result

    def model_fit(self, x: np.ndarray, y: np.ndarray, model: str = "quadratic") -> AnalysisResult:
        """模型拟合"""
        result = AnalysisResult(hypothesis_id="H1", test_type="regression")
        result.model_type = model

        if model == "quadratic":
            # 二次回归: y = ax² + bx + c
            coeffs = np.polyfit(x, y, 2)
            y_pred = np.polyval(coeffs, x)
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            result.r_squared = float(r_squared)
            result.model_params = {
                "a": float(coeffs[0]),
                "b": float(coeffs[1]),
                "c": float(coeffs[2]),
            }

            # 计算峰值
            if coeffs[0] < 0:  # 倒 U 型
                peak_x = -coeffs[1] / (2 * coeffs[0])
                peak_y = np.polyval(coeffs, peak_x)
                result.model_params["peak_x"] = float(peak_x)
                result.model_params["peak_y"] = float(peak_y)
                result.conclusion = f"支持倒 U 型假设 (R²={r_squared:.3f})，峰值在 x={peak_x:.2f}"
            else:
                result.conclusion = f"不支持倒 U 型假设 (R²={r_squared:.3f})"

        return result

    def confidence_interval(self, data: np.ndarray, confidence: float = 0.95) -> Dict:
        """置信区间"""
        mean = np.mean(data)
        sem = stats.sem(data)
        ci_lower, ci_upper = stats.t.interval(confidence, len(data)-1, loc=mean, scale=sem)

        return {
            "mean": float(mean),
            "ci_lower": float(ci_lower),
            "ci_upper": float(ci_upper),
            "margin_of_error": float((ci_upper - ci_lower) / 2),
            "confidence": confidence,
        }

    def effect_size(self, group1: np.ndarray, group2: np.ndarray) -> Dict:
        """效应量计算 (Cohen's d)"""
        pooled_std = np.sqrt((np.var(group1) + np.var(group2)) / 2)
        cohens_d = (np.mean(group1) - np.mean(group2)) / pooled_std

        return {
            "cohens_d": float(cohens_d),
            "interpretation": self._interpret_cohens_d(cohens_d),
        }

    def _calculate_eta_squared(self, groups: List, f_stat: float, n_per_group: int) -> float:
        """计算 eta-squared 效应量"""
        df_between = len(groups) - 1
        df_within = len(groups) * n_per_group - len(groups)
        ss_between = f_stat * df_within
        ss_total = ss_between + df_within
        return float(ss_between / ss_total) if ss_total > 0 else 0.0

    def _interpret_cohens_d(self, d: float) -> str:
        """解释 Cohen's d"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "可忽略"
        elif abs_d < 0.5:
            return "小效应"
        elif abs_d < 0.8:
            return "中等效应"
        else:
            return "大效应"
