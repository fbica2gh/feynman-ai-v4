"""
Feynman Research v5.0 - feynman-check
实时质量检查（结构/引用/编号）

功能：
- 结构完整性检查
- 引用质量检查
- 编号一致性检查
- 数据一致性检查
- 逻辑自洽性检查
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class FeynmanCheck:
    """质量检查工具"""
    
    def __init__(self, report_path: str, level: str = "p0"):
        """初始化
        
        Args:
            report_path: 报告文件路径
            level: 检查级别（p0/p1/p2）
        """
        self.report_path = Path(report_path)
        self.level = level
        self.content = self._load_content()
        self.results = {}
    
    def _load_content(self) -> str:
        """加载报告内容"""
        if self.report_path.exists():
            with open(self.report_path, 'r') as f:
                return f.read()
        return ""
    
    def check_structure(self) -> Dict:
        """检查结构完整性
        
        Returns:
            结构检查结果
        """
        # 必要章节定义
        required_sections = [
            "执行摘要",
            "研究背景",
            "核心概念解析",
            "资料收集总结",
            "深度分析",
            "结论与建议",
            "附录"
        ]
        
        # 检查章节
        found_sections = []
        missing_sections = []
        
        for section in required_sections:
            if f"## {section}" in self.content or f"# {section}" in self.content:
                found_sections.append(section)
            else:
                missing_sections.append(section)
        
        completeness = len(found_sections) / len(required_sections) * 100
        
        return {
            "found_sections": found_sections,
            "missing_sections": missing_sections,
            "completeness": completeness,
            "passed": completeness >= 90 if self.level == "p0" else completeness >= 80
        }
    
    def check_references(self) -> Dict:
        """检查引用质量
        
        Returns:
            引用检查结果
        """
        # 提取引用（格式：[1], [2], 等）
        references = re.findall(r'\[\d+\]', self.content)
        total_refs = len(references)
        
        # 检查引用编号连续性
        ref_numbers = [int(re.search(r'\d+', ref).group()) for ref in references]
        max_ref = max(ref_numbers) if ref_numbers else 0
        
        # 检查缺失编号
        expected_refs = set(range(1, max_ref + 1))
        found_refs = set(ref_numbers)
        missing_refs = expected_refs - found_refs
        
        # 检查重复引用
        duplicate_refs = [ref for ref in references if references.count(ref) > 1]
        
        quality_score = 100 - len(missing_refs) * 5 - len(duplicate_refs) * 2
        
        return {
            "total_references": total_refs,
            "max_reference_number": max_ref,
            "missing_references": list(missing_refs),
            "duplicate_references": duplicate_refs,
            "quality_score": max(quality_score, 0),
            "passed": quality_score >= 90 if self.level == "p0" else quality_score >= 80
        }
    
    def check_numbering(self) -> Dict:
        """检查编号一致性
        
        Returns:
            编号检查结果
        """
        # 检查章节编号（1., 2., 等）
        section_numbers = re.findall(r'^\d+\.', self.content)
        
        # 检查子章节编号（1.1, 1.2, 等）
        subsection_numbers = re.findall(r'^\d+\.\d+', self.content)
        
        # 检查编号冲突
        conflicts = []
        
        # 检查章节编号顺序
        section_nums = [int(re.search(r'\d+', num).group()) for num in section_numbers]
        expected_sequence = list(range(1, len(section_nums) + 1))
        
        if section_nums != expected_sequence:
            conflicts.append("章节编号不连续")
        
        consistency_score = 100 - len(conflicts) * 10
        
        return {
            "section_numbers": section_numbers,
            "subsection_numbers": subsection_numbers,
            "conflicts": conflicts,
            "consistency_score": max(consistency_score, 0),
            "passed": consistency_score >= 95 if self.level == "p0" else consistency_score >= 85
        }
    
    def check_data_consistency(self) -> Dict:
        """检查数据一致性
        
        Returns:
            数据检查结果
        """
        # 提取数字数据
        numbers = re.findall(r'\d+(?:\.\d+)?', self.content)
        
        # 检查数据范围合理性
        anomalies = []
        
        # 检查百分比数据（应该在 0-100）
        percentages = re.findall(r'(\d+(?:\.\d+)?)%', self.content)
        for p in percentages:
            p_val = float(p)
            if p_val < 0 or p_val > 100:
                anomalies.append(f"异常百分比: {p}%")
        
        # 检查年份数据（应该合理）
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', self.content)
        
        consistency_score = 100 - len(anomalies) * 5
        
        return {
            "total_numbers": len(numbers),
            "percentages": percentages,
            "years": years,
            "anomalies": anomalies,
            "consistency_score": max(consistency_score, 0),
            "passed": consistency_score >= 90 if self.level == "p0" else consistency_score >= 80
        }
    
    def check_logic_consistency(self) -> Dict:
        """检查逻辑自洽性
        
        Returns:
            逻辑检查结果
        """
        # 简单的逻辑检查
        contradictions = []
        
        # 检查矛盾词汇
        contradiction_patterns = [
            (r'增加', r'减少'),
            (r'上升', r'下降'),
            (r'增长', r'衰退'),
            (r'提高', r'降低'),
            (r'增强', r'减弱')
        ]
        
        for pattern1, pattern2 in contradiction_patterns:
            if re.search(pattern1, self.content) and re.search(pattern2, self.content):
                # 可能存在矛盾，需要人工确认
                contradictions.append(f"可能存在矛盾: {pattern1} vs {pattern2}")
        
        logic_score = 100 - len(contradictions) * 10
        
        return {
            "contradictions": contradictions,
            "logic_score": max(logic_score, 0),
            "passed": logic_score >= 100 if self.level == "p0" else logic_score >= 90
        }
    
    def run_all_checks(self) -> Dict:
        """运行所有检查
        
        Returns:
            检查结果汇总
        """
        self.results = {
            "structure": self.check_structure(),
            "references": self.check_references(),
            "numbering": self.check_numbering(),
            "data": self.check_data_consistency(),
            "logic": self.check_logic_consistency(),
            "level": self.level,
            "timestamp": datetime.now().isoformat()
        }
        
        # 计算总体评分
        scores = [
            self.results["structure"]["completeness"],
            self.results["references"]["quality_score"],
            self.results["numbering"]["consistency_score"],
            self.results["data"]["consistency_score"],
            self.results["logic"]["logic_score"]
        ]
        
        overall_score = sum(scores) / len(scores)
        
        # 检查是否全部通过
        all_passed = all([
            self.results["structure"]["passed"],
            self.results["references"]["passed"],
            self.results["numbering"]["passed"],
            self.results["data"]["passed"],
            self.results["logic"]["passed"]
        ])
        
        self.results["overall_score"] = overall_score
        self.results["all_passed"] = all_passed
        
        return self.results
    
    def generate_report(self) -> str:
        """生成检查报告（Markdown）"""
        report = f"""# Feynman Check 报告

## 检查时间
{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 检查级别
{self.level.upper()}

## 检查结果

### 1. 结构完整性
完整性: {self.results['structure']['completeness']:.1f}% {self._status_icon(self.results['structure']['passed'])}

找到的章节: {', '.join(self.results['structure']['found_sections'])}
缺失的章节: {', '.join(self.results['structure']['missing_sections']) if self.results['structure']['missing_sections'] else '无'}

### 2. 引用质量
质量评分: {self.results['references']['quality_score']:.1f}% {self._status_icon(self.results['references']['passed'])}

总引用数: {self.results['references']['total_references']}
最大编号: {self.results['references']['max_reference_number']}
缺失编号: {', '.join(map(str, self.results['references']['missing_references'])) if self.results['references']['missing_references'] else '无'}
重复引用: {len(self.results['references']['duplicate_references'])}

### 3. 编号一致性
一致性评分: {self.results['numbering']['consistency_score']:.1f}% {self._status_icon(self.results['numbering']['passed'])}

章节编号: {len(self.results['numbering']['section_numbers'])}
子章节编号: {len(self.results['numbering']['subsection_numbers'])}
编号冲突: {', '.join(self.results['numbering']['conflicts']) if self.results['numbering']['conflicts'] else '无'}

### 4. 数据一致性
一致性评分: {self.results['data']['consistency_score']:.1f}% {self._status_icon(self.results['data']['passed'])}

数据总数: {self.results['data']['total_numbers']}
百分比数据: {len(self.results['data']['percentages'])}
年份数据: {len(self.results['data']['years'])}
异常数据: {len(self.results['data']['anomalies'])}

### 5. 逻辑自洽性
逻辑评分: {self.results['logic']['logic_score']:.1f}% {self._status_icon(self.results['logic']['passed'])}

潜在矛盾: {len(self.results['logic']['contradictions'])}

## 总体评分
{self.results['overall_score']:.1f}% {self._status_icon(self.results['all_passed'])}

## 结论
{self._conclusion_text()}
"""
        
        return report
    
    def _status_icon(self, passed: bool) -> str:
        """状态图标"""
        return "✅" if passed else "⚠️"
    
    def _conclusion_text(self) -> str:
        """结论文本"""
        if self.results['all_passed']:
            return "所有检查通过，报告质量良好"
        else:
            issues = []
            if not self.results['structure']['passed']:
                issues.append("结构完整性不足")
            if not self.results['references']['passed']:
                issues.append("引用质量需改进")
            if not self.results['numbering']['passed']:
                issues.append("编号一致性需修正")
            if not self.results['data']['passed']:
                issues.append("数据一致性需复验")
            if not self.results['logic']['passed']:
                issues.append("逻辑矛盾需解决")
            
            return f"存在问题: {', '.join(issues)}，需要改进"


def feynman_check(report_path: str, level: str = "p0") -> Dict:
    """实时质量检查
    
    Args:
        report_path: 报告文件路径
        level: 检查级别（p0/p1/p2）
        
    Returns:
        检查结果
    """
    check_tool = FeynmanCheck(report_path, level)
    results = check_tool.run_all_checks()
    
    # 生成报告
    report = check_tool.generate_report()
    report_path_obj = Path(report_path)
    check_report_path = report_path_obj.parent / f"check_report_{level}.md"
    
    with open(check_report_path, 'w') as f:
        f.write(report)
    
    return results


if __name__ == "__main__":
    # 示例用法
    results = feynman_check("/tmp/test_project/output/final/report.md", "p0")
    print(f"总体评分: {results['overall_score']:.1f}%")
    print(f"是否通过: {results['all_passed']}")