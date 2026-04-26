"""
Quality Agent - Feynman AI v4.0 质量验证模块

职责：
1. P0（关键）：全验证（事实+交叉+逻辑）
2. P1（标准）：交叉验证
3. P2（快速）：快速核查
4. 自动降级机制

合并原 H/I/J Agent 为单一质量验证 Agent
"""

import json
from typing import Dict, List, Any, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class PriorityLevel(Enum):
    """优先级等级"""
    P0 = "critical"    # 关键信息
    P1 = "standard"    # 标准信息
    P2 = "quick"       # 快速信息


class ValidationType(Enum):
    """验证类型"""
    FACTUAL = "factual"          # 事实核查
    CROSS_REFERENCE = "cross"    # 交叉验证
    LOGICAL = "logical"          # 逻辑一致性
    SOURCE = "source"            # 来源可信度


@dataclass
class ValidationResult:
    """验证结果"""
    item: str
    priority: PriorityLevel
    validations: Dict[ValidationType, bool]
    overall_score: float
    issues: List[str]
    sources: List[str]


class QualityAgent:
    """
    质量验证 Agent
    
    核心方法：
    - validate(): 执行验证流程
    - fact_check(): 事实核查
    - cross_validate(): 交叉验证
    - logical_check(): 逻辑一致性检查
    """
    
    def __init__(self, model_config: Dict[str, Any]):
        """
        初始化
        
        Args:
            model_config: 模型配置
        """
        self.model = model_config.get('model', 'quality')
        self.validation_history = []
        self.auto_downgrade_keywords = [
            '股价', '财务', '投资建议', '错误', '警告',
            '关键', '紧急', '重要', '风险'
        ]
    
    def validate(
        self,
        items: List[Dict[str, Any]],
        priority: PriorityLevel = PriorityLevel.P1
    ) -> Dict[str, Any]:
        """
        执行验证流程
        
        根据优先级执行不同验证强度：
        - P0: 全验证（事实+交叉+逻辑+来源）
        - P1: 交叉验证 + 来源检查
        - P2: 快速核查
        
        Args:
            items: 待验证项目列表
                [
                    {
                        'content': '内容',
                        'sources': [来源],
                        'context': 上下文
                    },
                    ...
                ]
            priority: 优先级等级
        
        Returns:
            {
                'total_items': 项目总数,
                'passed_items': 通过验证数,
                'failed_items': 失败数,
                'overall_quality': 整体质量评分,
                'details': [验证详情],
                'issues': [问题列表],
                'recommendations': [改进建议]
            }
        """
        results = []
        
        for item in items:
            # 检查是否需要自动降级
            detected_priority = self._detect_priority(item)
            actual_priority = detected_priority if detected_priority else priority
            
            # 根据优先级执行验证
            if actual_priority == PriorityLevel.P0:
                validation_result = self._validate_p0(item)
            elif actual_priority == PriorityLevel.P1:
                validation_result = self._validate_p1(item)
            else:
                validation_result = self._validate_p2(item)
            
            results.append(validation_result)
        
        # 统计结果
        passed = len([r for r in results if r.overall_score >= 0.7])
        failed = len(results) - passed
        
        # 整体质量评分
        overall_quality = sum(r.overall_score for r in results) / len(results)
        
        # 收集问题
        all_issues = []
        for r in results:
            all_issues.extend(r.issues)
        
        # 生成改进建议
        recommendations = self._generate_recommendations(results)
        
        validation_report = {
            'total_items': len(items),
            'passed_items': passed,
            'failed_items': failed,
            'overall_quality': overall_quality,
            'details': [
                {
                    'item': r.item,
                    'priority': r.priority.value,
                    'validations': {k.value: v for k, v in r.validations.items()},
                    'score': r.overall_score,
                    'issues': r.issues,
                    'sources': r.sources
                }
                for r in results
            ],
            'issues': all_issues,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
        self.validation_history.append(validation_report)
        
        return validation_report
    
    def fact_check(self, content: str, sources: List[str]) -> Tuple[bool, List[str]]:
        """
        事实核查
        
        核查方式：
        - 多源验证（至少2个独立来源）
        - 时效性检查（数据是否过期）
        - 官方来源优先
        
        Args:
            content: 待核查内容
            sources: 数据来源
        
        Returns:
            (是否通过, 问题列表)
        """
        issues = []
        
        # 检查来源数量
        if len(sources) < 2:
            issues.append('来源不足（需要至少2个独立来源）')
            return False, issues
        
        # 检查来源可信度
        trusted_sources = self._evaluate_source_credibility(sources)
        if len(trusted_sources) < 1:
            issues.append('无可信来源')
            return False, issues
        
        # 检查时效性（针对实时数据）
        if self._is_time_sensitive(content):
            freshness = self._check_data_freshness(content)
            if not freshness:
                issues.append('数据可能已过期')
        
        # 多源一致性检查
        consistency = self._check_source_consistency(content, sources)
        if not consistency:
            issues.append('来源间数据不一致')
        
        passed = len(issues) == 0
        
        return passed, issues
    
    def cross_validate(
        self,
        content: str,
        sources: List[str],
        independent_required: int = 2
    ) -> Tuple[bool, float, List[str]]:
        """
        交叉验证
        
        验证方式：
        - 独立来源验证（至少 N 个独立来源）
        - 来源依赖关系检测
        - 数据一致性检查
        
        Args:
            content: 待验证内容
            sources: 数据来源
            independent_required: 独立来源数量要求
        
        Returns:
            (是否通过, 置信度, 问题列表)
        """
        issues = []
        
        # 检测独立来源
        independent_sources = self._identify_independent_sources(sources)
        
        if len(independent_sources) < independent_required:
            issues.append(f'独立来源不足（需要{independent_required}个，当前{len(independent_sources)}个）')
            confidence = 0.5
            return False, confidence, issues
        
        # 计算置信度
        confidence = min(1.0, len(independent_sources) / independent_required)
        
        passed = len(issues) == 0
        
        return passed, confidence, issues
    
    def logical_check(self, content: str, context: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        逻辑一致性检查
        
        检查方式：
        - 内部逻辑一致性（自相矛盾）
        - 外部逻辑一致性（与已知事实矛盾）
        - 因果逻辑检查（因果关系合理性）
        
        Args:
            content: 待检查内容
            context: 上下文信息
        
        Returns:
            (是否通过, 问题列表)
        """
        issues = []
        
        # 内部逻辑检查
        internal_consistency = self._check_internal_logic(content)
        if not internal_consistency:
            issues.append('内容存在内部逻辑矛盾')
        
        # 外部逻辑检查（与已知事实对比）
        external_consistency = self._check_external_logic(content, context)
        if not external_consistency:
            issues.append('内容与已知事实矛盾')
        
        # 因果逻辑检查
        causal_logic = self._check_causal_logic(content)
        if not causal_logic:
            issues.append('因果关系逻辑不合理')
        
        passed = len(issues) == 0
        
        return passed, issues
    
    # ===== 优先级验证 =====
    
    def _validate_p0(self, item: Dict[str, Any]) -> ValidationResult:
        """P0（关键）全验证"""
        content = item.get('content', '')
        sources = item.get('sources', [])
        context = item.get('context', {})
        
        # 执行所有验证
        factual_passed, factual_issues = self.fact_check(content, sources)
        cross_passed, confidence, cross_issues = self.cross_validate(content, sources, 3)
        logical_passed, logical_issues = self.logical_check(content, context)
        
        validations = {
            ValidationType.FACTUAL: factual_passed,
            ValidationType.CROSS_REFERENCE: cross_passed,
            ValidationType.LOGICAL: logical_passed,
            ValidationType.SOURCE: len(self._evaluate_source_credibility(sources)) > 0
        }
        
        all_issues = factual_issues + cross_issues + logical_issues
        
        # 计算综合评分
        score = sum(validations.values()) / len(validations) * confidence
        
        return ValidationResult(
            item=content[:50],  # 截取前50字符
            priority=PriorityLevel.P0,
            validations=validations,
            overall_score=score,
            issues=all_issues,
            sources=sources
        )
    
    def _validate_p1(self, item: Dict[str, Any]) -> ValidationResult:
        """P1（标准）交叉验证"""
        content = item.get('content', '')
        sources = item.get('sources', [])
        
        # 执行交叉验证 + 来源检查
        cross_passed, confidence, cross_issues = self.cross_validate(content, sources, 2)
        source_trusted = len(self._evaluate_source_credibility(sources)) > 0
        
        validations = {
            ValidationType.CROSS_REFERENCE: cross_passed,
            ValidationType.SOURCE: source_trusted
        }
        
        # 计算评分
        score = sum(validations.values()) / len(validations) * confidence
        
        return ValidationResult(
            item=content[:50],
            priority=PriorityLevel.P1,
            validations=validations,
            overall_score=score,
            issues=cross_issues,
            sources=sources
        )
    
    def _validate_p2(self, item: Dict[str, Any]) -> ValidationResult:
        """P2（快速）快速核查"""
        content = item.get('content', '')
        sources = item.get('sources', [])
        
        # 快速核查：单源检查 + 基础可信度
        source_trusted = len(sources) > 0 and len(self._evaluate_source_credibility(sources)) > 0
        
        validations = {
            ValidationType.SOURCE: source_trusted
        }
        
        score = 1.0 if source_trusted else 0.3
        
        issues = [] if source_trusted else ['无可信来源']
        
        return ValidationResult(
            item=content[:50],
            priority=PriorityLevel.P2,
            validations=validations,
            overall_score=score,
            issues=issues,
            sources=sources
        )
    
    # ===== 自动降级 =====
    
    def _detect_priority(self, item: Dict[str, Any]) -> PriorityLevel:
        """
        自动检测优先级
        
        检测关键词：
        - 股价、财务、投资建议 → P0
        - 错误、警告、关键、紧急 → P0
        - 其他 → None（使用默认）
        """
        content = item.get('content', '')
        
        for keyword in self.auto_downgrade_keywords:
            if keyword in content:
                return PriorityLevel.P0
        
        return None
    
    # ===== 辅助方法 =====
    
    def _evaluate_source_credibility(self, sources: List[str]) -> List[str]:
        """评估来源可信度"""
        # 可信来源列表
        trusted_domains = [
            'gov.cn', 'edu.cn', 'org.cn',
            'semanticscholar.org', 'arxiv.org',
            'nature.com', 'science.org',
            'reuters.com', 'bloomberg.com'
        ]
        
        trusted = []
        for source in sources:
            for domain in trusted_domains:
                if domain in source:
                    trusted.append(source)
                    break
        
        return trusted
    
    def _is_time_sensitive(self, content: str) -> bool:
        """检查是否时效敏感"""
        time_keywords = ['股价', '汇率', '利率', '实时', '当前']
        return any(kw in content for kw in time_keywords)
    
    def _check_data_freshness(self, content: str) -> bool:
        """检查数据时效性"""
        # TODO: 实现时效性检查
        return True
    
    def _check_source_consistency(self, content: str, sources: List[str]) -> bool:
        """检查来源一致性"""
        # TODO: 实现一致性检查
        return True
    
    def _identify_independent_sources(self, sources: List[str]) -> List[str]:
        """识别独立来源"""
        # 简化实现：假设所有来源独立
        return sources
    
    def _check_internal_logic(self, content: str) -> bool:
        """检查内部逻辑"""
        # TODO: 实现逻辑检查
        return True
    
    def _check_external_logic(self, content: str, context: Dict) -> bool:
        """检查外部逻辑"""
        # TODO: 实现外部逻辑检查
        return True
    
    def _check_causal_logic(self, content: str) -> bool:
        """检查因果逻辑"""
        # TODO: 实现因果逻辑检查
        return True
    
    def _generate_recommendations(self, results: List[ValidationResult]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 统计常见问题
        failed_count = len([r for r in results if r.overall_score < 0.7])
        if failed_count > len(results) * 0.3:
            recommendations.append('建议增加验证来源数量')
        
        # 逻辑问题
        logic_issues = [r for r in results if not r.validations.get(ValidationType.LOGICAL, True)]
        if logic_issues:
            recommendations.append('建议检查逻辑一致性')
        
        return recommendations


# ===== 使用示例 =====

if __name__ == '__main__':
    config = {'model': 'quality'}
    agent = QualityAgent(config)
    
    # 待验证项目
    items = [
        {
            'content': '腾讯控股股价为 380.5 元',
            'sources': ['http://qt.gtimg.cn', 'finance.tencent.com'],
            'context': {'type': 'stock_price'}
        },
        {
            'content': '量子计算机可破解 RSA 加密',
            'sources': ['arxiv.org', 'nature.com'],
            'context': {'type': 'scientific'}
        }
    ]
    
    # 执行验证（P1 标准）
    result = agent.validate(items, PriorityLevel.P1)
    
    print("验证结果：")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print(f"\n整体质量评分：{result['overall_quality']:.2f}")
    print(f"通过验证：{result['passed_items']}/{result['total_items']}")
    
    if result['issues']:
        print("\n问题列表：")
        for issue in result['issues']:
            print(f"  - {issue}")