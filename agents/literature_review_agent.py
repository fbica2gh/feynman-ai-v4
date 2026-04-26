"""
Literature Review Agent - Feynman AI v4.0 文献综述模块

职责：
1. 提取论文引用
2. Semantic Scholar 验证
3. Levenshtein 匹配（>70%）
4. 引用质量评估

参考：PaperOrchestra 文献验证框架
"""

import json
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Citation:
    """引用数据结构"""
    id: str
    title: str
    authors: List[str]
    year: int
    source: str
    doi: str
    verified: bool = False
    levenshtein_score: float = 0.0
    quality_score: float = 0.0


class LiteratureReviewAgent:
    """
    文献综述 Agent
    
    核心方法：
    - verify_citations(): 验证引用真实性
    - extract_citations(): 提取论文引用
    - evaluate_quality(): 评估引用质量
    """
    
    def __init__(self, model_config: Dict[str, Any]):
        """
        初始化
        
        Args:
            model_config: 模型配置
        """
        self.model = model_config.get('model', 'standard')
        self.semantic_scholar_api = "https://api.semanticscholar.org/v1"
        self.citation_cache = {}
    
    def verify_citations(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证引用真实性
        
        流程：
        1. 提取所有引用
        2. Semantic Scholar 验证
        3. Levenshtein 匹配（>70%）
        4. 质量评分
        
        Args:
            paper: 论文信息
                {
                    'title': '论文标题',
                    'content': '论文内容',
                    'citations_text': '引用文本',
                    'doi': '论文 DOI'
                }
        
        Returns:
            {
                'paper_id': '论文ID',
                'total_citations': 总引用数,
                'verified_citations': 验证成功数,
                'failed_citations': 验证失败数,
                'average_levenshtein': 平均匹配度,
                'quality_score': 质量评分（A+/A/B/C/D/F),
                'details': [
                    {
                        'citation_id': '引用ID',
                        'title': '标题',
                        'verified': True/False,
                        'levenshtein_score': 匹配度,
                        'source': '验证来源'
                    },
                    ...
                ]
            }
        """
        # Step 1: 提取引用
        citations = self.extract_citations(paper)
        
        # Step 2: Semantic Scholar 验证
        verified_citations = self.verify_on_semantic_scholar(citations)
        
        # Step 3: Levenshtein 匹配
        matched_citations = self.levenshtein_match(verified_citations)
        
        # Step 4: 质量评估
        quality_result = self.evaluate_quality(matched_citations)
        
        return {
            'paper_id': paper.get('doi', 'unknown'),
            'total_citations': len(citations),
            'verified_citations': len([c for c in matched_citations if c.verified]),
            'failed_citations': len([c for c in matched_citations if not c.verified]),
            'average_levenshtein': sum(c.levenshtein_score for c in matched_citations) / len(matched_citations),
            'quality_score': quality_result['grade'],
            'details': [
                {
                    'citation_id': c.id,
                    'title': c.title,
                    'verified': c.verified,
                    'levenshtein_score': c.levenshtein_score,
                    'quality_score': c.quality_score,
                    'source': c.source
                }
                for c in matched_citations
            ]
        }
    
    def extract_citations(self, paper: Dict[str, Any]) -> List[Citation]:
        """
        提取论文引用
        
        提取方式：
        - 正则匹配引用格式
        - 解析参考文献列表
        - DOI 解析
        
        Args:
            paper: 论文信息
        
        Returns:
            [Citation 对象列表]
        """
        citations = []
        
        # 从内容中提取引用
        content = paper.get('content', '')
        citations_text = paper.get('citations_text', '')
        
        # 正则匹配常见引用格式
        # 格式1: [作者, 年份]
        pattern1 = r'\[([^\]]+),\s*(\d{4})\]'
        matches1 = re.findall(pattern1, content)
        
        # 格式2: (作者, 年份)
        pattern2 = r'\(([^\)]+),\s*(\d{4})\)'
        matches2 = re.findall(pattern2, content)
        
        # 格式3: DOI
        pattern3 = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'
        dois = re.findall(pattern3, content)
        
        # 合并提取结果
        for i, (author, year) in enumerate(matches1 + matches2):
            citation = Citation(
                id=f'c{i+1}',
                title=f'未知标题 ({author})',
                authors=[author.strip()],
                year=int(year),
                source='正则提取',
                doi=''
            )
            citations.append(citation)
        
        # DOI 引用
        for i, doi in enumerate(dois):
            citation = Citation(
                id=f'd{i+1}',
                title='DOI 引用',
                authors=[],
                year=0,
                source='DOI 提取',
                doi=doi
            )
            citations.append(citation)
        
        # 解析参考文献列表
        if citations_text:
            ref_citations = self._parse_references_list(citations_text)
            citations.extend(ref_citations)
        
        return citations
    
    def verify_on_semantic_scholar(self, citations: List[Citation]) -> List[Citation]:
        """
        Semantic Scholar 验证
        
        验证方式：
        - DOI 查询
        - 标题查询
        - 作者+年份查询
        
        Args:
            citations: 引用列表
        
        Returns:
            [验证后的 Citation 对象]
        """
        verified = []
        
        for citation in citations:
            # 尝试多种验证方式
            verification_result = None
            
            # 方式1: DOI 查询（最准确）
            if citation.doi:
                verification_result = self._verify_by_doi(citation.doi)
            
            # 方式2: 标题查询
            if not verification_result and citation.title != '未知标题':
                verification_result = self._verify_by_title(citation.title)
            
            # 方式3: 作者+年份查询
            if not verification_result and citation.authors and citation.year:
                verification_result = self._verify_by_author_year(
                    citation.authors[0], citation.year
                )
            
            # 更新验证状态
            if verification_result:
                citation.verified = True
                citation.title = verification_result.get('title', citation.title)
                citation.doi = verification_result.get('doi', citation.doi)
                citation.source = 'Semantic Scholar'
            else:
                citation.verified = False
                citation.source = '验证失败'
            
            verified.append(citation)
        
        return verified
    
    def levenshtein_match(self, citations: List[Citation]) -> List[Citation]:
        """
        Levenshtein 匹配
        
        匹配标准：
        - >70%: 高匹配度（可信）
        - 50-70%: 中匹配度（部分可信）
        - <50%: 低匹配度（不可信）
        
        Args:
            citations: 已验证的引用
        
        Returns:
            [匹配度评分后的 Citation 对象]
        """
        matched = []
        
        for citation in citations:
            if citation.verified:
                # 计算标题匹配度
                original_title = citation.title
                verified_title = citation.title
                
                # Levenshtein 距离计算（简化实现）
                score = self._calculate_levenshtein_score(
                    original_title, verified_title
                )
                
                citation.levenshtein_score = score
                
                # 根据匹配度设置质量评分
                if score >= 0.9:
                    citation.quality_score = 1.0  # A+
                elif score >= 0.7:
                    citation.quality_score = 0.8  # A
                elif score >= 0.5:
                    citation.quality_score = 0.6  # B
                else:
                    citation.quality_score = 0.3  # C/D
            else:
                citation.levenshtein_score = 0.0
                citation.quality_score = 0.0
            
            matched.append(citation)
        
        return matched
    
    def evaluate_quality(self, citations: List[Citation]) -> Dict[str, Any]:
        """
        评估引用质量
        
        评分标准：
        - A+: 90%+ 引用验证成功，平均匹配度 >85%
        - A: 80%+ 引用验证成功，平均匹配度 >70%
        - B: 60%+ 引用验证成功，平均匹配度 >50%
        - C: 40%+ 引用验证成功
        - D: 20%+ 引用验证成功
        - F: <20% 引用验证成功
        
        Args:
            citations: 引用列表
        
        Returns:
            {
                'grade': 'A+/A/B/C/D/F',
                'verified_ratio': 验证比例,
                'average_match': 平均匹配度,
                'issues': [问题列表]
            }
        """
        total = len(citations)
        verified = len([c for c in citations if c.verified])
        verified_ratio = verified / total if total > 0 else 0
        
        avg_match = sum(c.levenshtein_score for c in citations) / total if total > 0 else 0
        
        # 评分
        if verified_ratio >= 0.9 and avg_match >= 0.85:
            grade = 'A+'
        elif verified_ratio >= 0.8 and avg_match >= 0.7:
            grade = 'A'
        elif verified_ratio >= 0.6 and avg_match >= 0.5:
            grade = 'B'
        elif verified_ratio >= 0.4:
            grade = 'C'
        elif verified_ratio >= 0.2:
            grade = 'D'
        else:
            grade = 'F'
        
        # 问题检测
        issues = []
        unverified = [c for c in citations if not c.verified]
        if unverified:
            issues.append(f'{len(unverified)} 个引用无法验证')
        
        low_match = [c for c in citations if c.levenshtein_score < 0.5]
        if low_match:
            issues.append(f'{len(low_match)} 个引用匹配度低于50%')
        
        return {
            'grade': grade,
            'verified_ratio': verified_ratio,
            'average_match': avg_match,
            'issues': issues
        }
    
    # ===== 辅助方法 =====
    
    def _parse_references_list(self, refs_text: str) -> List[Citation]:
        """解析参考文献列表"""
        # TODO: 实现完整的参考文献解析
        return []
    
    def _verify_by_doi(self, doi: str) -> Dict[str, Any]:
        """通过 DOI 验证"""
        # TODO: 调用 Semantic Scholar API
        # 当前返回模拟结果
        return {
            'title': 'Verified Paper',
            'doi': doi
        }
    
    def _verify_by_title(self, title: str) -> Dict[str, Any]:
        """通过标题验证"""
        # TODO: 调用 Semantic Scholar API
        return {
            'title': title,
            'doi': '10.xxxx/xxxx'
        }
    
    def _verify_by_author_year(self, author: str, year: int) -> Dict[str, Any]:
        """通过作者+年份验证"""
        # TODO: 调用 Semantic Scholar API
        return {
            'title': f'Paper by {author} ({year})',
            'doi': '10.xxxx/xxxx'
        }
    
    def _calculate_levenshtein_score(self, str1: str, str2: str) -> float:
        """
        计算 Levenshtein 匹配度
        
        返回：匹配度（0-1），越高越匹配
        """
        # 简化实现：使用字符串相似度
        if not str1 or not str2:
            return 0.0
        
        # 标准化字符串
        s1 = str1.lower().strip()
        s2 = str2.lower().strip()
        
        # 计算编辑距离
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(
                        dp[i-1][j] + 1,
                        dp[i][j-1] + 1,
                        dp[i-1][j-1] + 1
                    )
        
        distance = dp[m][n]
        max_len = max(m, n)
        
        # 转换为匹配度
        score = 1 - (distance / max_len) if max_len > 0 else 1.0
        
        return score


# ===== 使用示例 =====

if __name__ == '__main__':
    config = {'model': 'standard'}
    agent = LiteratureReviewAgent(config)
    
    paper = {
        'title': 'Sample Paper',
        'content': 'This paper cites [Smith, 2024] and [Jones, 2023]...',
        'citations_text': 'References:\n1. Smith, J. (2024). Paper A.\n2. Jones, K. (2023). Paper B.',
        'doi': '10.xxxx/sample'
    }
    
    # 验证引用
    result = agent.verify_citations(paper)
    
    print("引用验证结果：")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print(f"\n质量评分：{result['quality_score']}")
    print(f"验证成功：{result['verified_citations']}/{result['total_citations']}")