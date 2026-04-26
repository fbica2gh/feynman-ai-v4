"""
实验设计器 (ExperimentDesigner)
设计实验验证假设
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Variable:
    """变量定义"""
    name: str
    type: str  # independent/dependent/control
    values: List = field(default_factory=list)
    unit: str = ""
    range_min: float = 0.0
    range_max: float = 0.0


@dataclass
class ExperimentDesign:
    """实验设计数据结构"""
    hypothesis_id: str
    title: str
    independent_variables: List[Variable] = field(default_factory=list)
    dependent_variables: List[Variable] = field(default_factory=list)
    control_variables: List[Variable] = field(default_factory=list)
    sample_size_per_group: int = 0
    num_groups: int = 0
    total_samples: int = 0
    randomization: bool = False
    replication: int = 0  # 重复次数
    confounders: List[str] = field(default_factory=list)
    controls_for_confounders: Dict = field(default_factory=dict)


class ExperimentDesigner:
    """实验设计器"""

    def design_experiment(self, hypothesis_id: str, hypothesis: str) -> ExperimentDesign:
        """
        设计实验

        要素:
        1. 自变量 (Independent Variable)
        2. 因变量 (Dependent Variable)
        3. 控制变量 (Control Variables)
        4. 样本量 (Sample Size)
        5. 随机化 (Randomization)
        6. 重复 (Replication)
        """
        if "IMC" in hypothesis or "imc" in hypothesis.lower():
            return self._design_imc_experiment(hypothesis_id, hypothesis)

        return ExperimentDesign(
            hypothesis_id=hypothesis_id,
            title=f"验证假设 {hypothesis_id}",
        )

    def _design_imc_experiment(self, hypothesis_id: str, hypothesis: str) -> ExperimentDesign:
        """设计 IMC 厚度实验"""
        design = ExperimentDesign(
            hypothesis_id=hypothesis_id,
            title=f"IMC 厚度对焊点性能影响实验 - {hypothesis_id}",
            sample_size_per_group=10,
            num_groups=8,
            total_samples=80,
            randomization=True,
            replication=3,
        )

        # 自变量
        design.independent_variables = [
            Variable(name="IMC 层厚度", type="independent", values=[0.7, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0], unit="μm"),
        ]

        # 因变量
        if "剪切" in hypothesis:
            design.dependent_variables = [
                Variable(name="剪切强度", type="dependent", unit="MPa"),
            ]
        elif "热循环" in hypothesis:
            design.dependent_variables = [
                Variable(name="热循环寿命", type="dependent", unit="cycles"),
            ]
        elif "跌落" in hypothesis:
            design.dependent_variables = [
                Variable(name="跌落寿命", type="dependent", unit="drops"),
            ]
        else:
            design.dependent_variables = [
                Variable(name="剪切强度", type="dependent", unit="MPa"),
                Variable(name="热循环寿命", type="dependent", unit="cycles"),
            ]

        # 控制变量
        design.control_variables = [
            Variable(name="焊料类型", type="control", values=["SAC305"]),
            Variable(name="焊盘类型", type="control", values=["Cu"]),
            Variable(name="回流焊峰值温度", type="control", values=[245], unit="°C"),
            Variable(name="保温时间", type="control", values=[60], unit="s"),
            Variable(name="测试速度", type="control", values=[0.5], unit="mm/s"),
            Variable(name="环境温度", type="control", values=[25], unit="°C"),
        ]

        # 混杂因素
        design.confounders = [
            "焊料合金成分变化",
            "温度波动",
            "测试设备校准",
            "IMC 测量方法差异",
        ]

        design.controls_for_confounders = {
            "焊料合金成分变化": "使用同一批次焊料",
            "温度波动": "恒温实验室 (25±1°C)",
            "测试设备校准": "每次测试前校准",
            "IMC 测量方法差异": "统一使用 SEM 截面分析",
        }

        return design

    def identify_confounders(self, design: ExperimentDesign) -> List[str]:
        """识别混杂因素"""
        return design.confounders

    def design_control(self, confounders: List[str]) -> Dict:
        """设计对照组"""
        return {
            c: f"控制措施：{c}" for c in confounders
        }
