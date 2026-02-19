#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""角色資料模型"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Character:
    """角色資料類別"""
    
    id: str                              # 英文 ID，用於程式識別
    name: str                            # 顯示名稱
    description: str = ""                # 角色描述
    expressions: List[str] = field(default_factory=lambda: ["normal"])  # 表情列表
    color: str = "#ffffff"               # 對話框顏色
    notes: Optional[str] = None          # 備註
    appears_in: List[str] = field(default_factory=list)  # 出現的段落
    
    def to_dict(self) -> dict:
        """轉換為字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'expressions': self.expressions,
            'color': self.color,
            'notes': self.notes,
            'appears_in': self.appears_in
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Character':
        """從字典建立"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            expressions=data.get('expressions', ['normal']),
            color=data.get('color', '#ffffff'),
            notes=data.get('notes'),
            appears_in=data.get('appears_in', [])
        )
    
    def add_expression(self, expression: str) -> None:
        """新增表情"""
        if expression not in self.expressions:
            self.expressions.append(expression)
    
    def __str__(self) -> str:
        return f"Character({self.id}: {self.name})"
    
    def __repr__(self) -> str:
        return self.__str__()
