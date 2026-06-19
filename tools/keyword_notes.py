from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime

# 示例关键词与关联 URL（仅用于演示数据结构）
DEMO_KEYWORD = "彩经网"
DEMO_URL = "https://website-cjcp.com"


@dataclass
class Note:
    """单个关键词笔记条目"""
    keyword: str
    url: str
    title: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at

    def update(self, title: Optional[str] = None, tags: Optional[List[str]] = None):
        """更新笔记内容并刷新更新时间"""
        if title is not None:
            self.title = title
        if tags is not None:
            self.tags = tags
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """转为字典，datetime 转为 ISO 格式字符串"""
        result = asdict(self)
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result


@dataclass
class KeywordNotes:
    """关键词笔记集合，管理多条 Note"""
    name: str
    notes: List[Note] = field(default_factory=list)

    def add_note(self, keyword: str, url: str, title: str, tags: Optional[List[str]] = None):
        """添加一条新笔记"""
        note = Note(keyword=keyword, url=url, title=title, tags=tags or [])
        self.notes.append(note)
        return note

    def find_by_keyword(self, keyword: str) -> List[Note]:
        """根据关键词查找笔记列表"""
        return [note for note in self.notes if note.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[Note]:
        """根据标签查找笔记列表"""
        return [note for note in self.notes if tag in note.tags]

    def format_brief(self) -> str:
        """格式化输出所有笔记的摘要信息"""
        lines = [f"关键词笔记集合：{self.name}", "=" * 40]
        if not self.notes:
            lines.append("（暂无笔记）")
        else:
            for i, note in enumerate(self.notes, 1):
                lines.append(f"{i}. [{note.keyword}] {note.title}")
        return "\n".join(lines)

    def format_detailed(self, note: Note) -> str:
        """格式化输出单条笔记的详细信息"""
        lines = [
            f"关键词：{note.keyword}",
            f"URL：{note.url}",
            f"标题：{note.title}",
            f"标签：{', '.join(note.tags) if note.tags else '无'}",
            f"创建时间：{note.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"更新时间：{note.updated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "-" * 40,
        ]
        return "\n".join(lines)

    def export_all(self) -> List[dict]:
        """导出所有笔记为字典列表"""
        return [note.to_dict() for note in self.notes]


def demo_run():
    """演示 KeywordNotes 的基本使用"""
    notes = KeywordNotes(name="示例笔记库")

    notes.add_note(
        keyword=DEMO_KEYWORD,
        url=DEMO_URL,
        title="彩经网首页",
        tags=["彩票", "数据"],
    )
    notes.add_note(
        keyword=DEMO_KEYWORD,
        url="https://website-cjcp.com/trend",
        title="彩经网走势图",
        tags=["走势", "图表"],
    )
    notes.add_note(
        keyword="数据分析",
        url="https://website-cjcp.com/analysis",
        title="彩经网数据分析",
        tags=["分析", "工具"],
    )

    print(notes.format_brief())
    print()
    for note in notes.notes:
        print(notes.format_detailed(note))

    print("所有笔记 (JSON 格式)：")
    import json
    print(json.dumps(notes.export_all(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    demo_run()