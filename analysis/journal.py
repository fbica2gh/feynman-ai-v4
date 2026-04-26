"""
研究日志 (ResearchJournal)
完整记录研究过程
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime


@dataclass
class JournalEntry:
    """日志条目"""
    timestamp: str
    step: str
    content: Dict
    notes: str = ""


class ResearchJournal:
    """研究日志"""

    def __init__(self, study_title: str = ""):
        self.study_title = study_title
        self.entries: List[JournalEntry] = []
        self.start_time = datetime.now().isoformat()

    def log_step(self, step: str, content: Dict, notes: str = "") -> None:
        """记录研究步骤"""
        entry = JournalEntry(
            timestamp=datetime.now().isoformat(),
            step=step,
            content=content,
            notes=notes,
        )
        self.entries.append(entry)

    def generate_journal(self) -> str:
        """生成研究日志"""
        lines = [
            f"# 研究日志: {self.study_title}",
            f"开始时间：{self.start_time}",
            f"总步骤数：{len(self.entries)}",
            "",
            "---",
            "",
        ]

        for i, entry in enumerate(self.entries, 1):
            lines.append(f"## 步骤 {i}: {entry.step}")
            lines.append(f"时间：{entry.timestamp}")
            if entry.notes:
                lines.append(f"备注：{entry.notes}")
            lines.append("")
            for key, value in entry.content.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")

        return "\n".join(lines)

    def get_summary(self) -> Dict:
        """获取日志摘要"""
        return {
            "study_title": self.study_title,
            "start_time": self.start_time,
            "total_steps": len(self.entries),
            "steps": [e.step for e in self.entries],
        }
