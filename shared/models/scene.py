#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""場景資料模型"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Scene:
    """場景資料類別"""
    
    id: str                              # 英文 ID
    name: str                            # 場景名稱
    description: str = ""                # 場景描述
    location: str = ""                   # 地點
    time_of_day: str = "日間"            # 時段：日間/夜間/黃昏/清晨
    mood: str = ""                       # 氛圍
    notes: Optional[str] = None          # 備註
    appears_in: List[str] = field(default_factory=list)  # 使用此場景的段落
    
    def to_dict(self) -> dict:
        """轉換為字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'time_of_day': self.time_of_day,
            'mood': self.mood,
            'notes': self.notes,
            'appears_in': self.appears_in
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Scene':
        """從字典建立"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            location=data.get('location', ''),
            time_of_day=data.get('time_of_day', '日間'),
            mood=data.get('mood', ''),
            notes=data.get('notes'),
            appears_in=data.get('appears_in', [])
        )
    
    def get_full_description(self) -> str:
        """取得完整描述（用於生成圖片）"""
        parts = [self.name]
        if self.description:
            parts.append(self.description)
        if self.location:
            parts.append(f"地點：{self.location}")
        if self.time_of_day:
            parts.append(f"時段：{self.time_of_day}")
        if self.mood:
            parts.append(f"氛圍：{self.mood}")
        return "，".join(parts)
    
    def __str__(self) -> str:
        return f"Scene({self.id}: {self.name})"
    
    def __repr__(self) -> str:
        return self.__str__()
