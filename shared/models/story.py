#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""故事資料模型"""

from dataclasses import dataclass, field
from typing import List, Optional, Union
from .character import Character
from .scene import Scene


@dataclass
class DialogueLine:
    """對話行"""
    character: str          # 角色 ID
    text: str               # 對話內容
    expression: str = "normal"  # 表情
    
    def to_dict(self) -> dict:
        return {
            'type': 'dialogue',
            'character': self.character,
            'text': self.text,
            'expression': self.expression
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DialogueLine':
        return cls(
            character=data.get('character', ''),
            text=data.get('text', ''),
            expression=data.get('expression', 'normal')
        )


@dataclass
class NarrationLine:
    """旁白行"""
    text: str
    
    def to_dict(self) -> dict:
        return {
            'type': 'narration',
            'text': self.text
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'NarrationLine':
        return cls(text=data.get('text', ''))


@dataclass
class ActionLine:
    """動作行（顯示/隱藏角色、切換場景等）"""
    action: str             # show_character, hide_character, change_scene
    character: Optional[str] = None
    expression: Optional[str] = None
    scene_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        result = {
            'type': 'action',
            'action': self.action
        }
        if self.character:
            result['character'] = self.character
        if self.expression:
            result['expression'] = self.expression
        if self.scene_id:
            result['scene_id'] = self.scene_id
        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ActionLine':
        return cls(
            action=data.get('action', ''),
            character=data.get('character'),
            expression=data.get('expression'),
            scene_id=data.get('scene_id')
        )


@dataclass
class Choice:
    """選項"""
    text: str               # 選項文字
    target: str             # 目標段落名稱
    condition: Optional[str] = None  # 條件（可選）
    
    def to_dict(self) -> dict:
        result = {
            'text': self.text,
            'target': self.target
        }
        if self.condition:
            result['condition'] = self.condition
        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Choice':
        return cls(
            text=data.get('text', ''),
            target=data.get('target', ''),
            condition=data.get('condition')
        )


# 行類型聯合
Line = Union[DialogueLine, NarrationLine, ActionLine]


@dataclass
class Passage:
    """段落"""
    name: str               # 段落名稱
    scene_id: Optional[str] = None  # 場景 ID
    lines: List[Line] = field(default_factory=list)
    choices: List[Choice] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'scene_id': self.scene_id,
            'lines': [line.to_dict() for line in self.lines],
            'choices': [choice.to_dict() for choice in self.choices]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Passage':
        lines = []
        for line_data in data.get('lines', []):
            line_type = line_data.get('type', 'narration')
            if line_type == 'dialogue':
                lines.append(DialogueLine.from_dict(line_data))
            elif line_type == 'action':
                lines.append(ActionLine.from_dict(line_data))
            else:
                lines.append(NarrationLine.from_dict(line_data))
        
        choices = [Choice.from_dict(c) for c in data.get('choices', [])]
        
        return cls(
            name=data.get('name', ''),
            scene_id=data.get('scene_id'),
            lines=lines,
            choices=choices
        )
    
    def add_dialogue(self, character: str, text: str, expression: str = "normal"):
        """新增對話"""
        self.lines.append(DialogueLine(character, text, expression))
    
    def add_narration(self, text: str):
        """新增旁白"""
        self.lines.append(NarrationLine(text))
    
    def add_choice(self, text: str, target: str):
        """新增選項"""
        self.choices.append(Choice(text, target))


@dataclass 
class Story:
    """故事"""
    title: str
    version: str = "1.0"
    summary: str = ""
    characters: List[Character] = field(default_factory=list)
    scenes: List[Scene] = field(default_factory=list)
    passages: List[Passage] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'version': self.version,
            'summary': self.summary,
            'characters': [c.to_dict() for c in self.characters],
            'scenes': [s.to_dict() for s in self.scenes],
            'passages': [p.to_dict() for p in self.passages]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Story':
        return cls(
            title=data.get('title', ''),
            version=data.get('version', '1.0'),
            summary=data.get('summary', ''),
            characters=[Character.from_dict(c) for c in data.get('characters', [])],
            scenes=[Scene.from_dict(s) for s in data.get('scenes', [])],
            passages=[Passage.from_dict(p) for p in data.get('passages', [])]
        )
    
    def get_character(self, char_id: str) -> Optional[Character]:
        """取得角色"""
        for char in self.characters:
            if char.id == char_id:
                return char
        return None
    
    def get_scene(self, scene_id: str) -> Optional[Scene]:
        """取得場景"""
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        return None
    
    def get_passage(self, name: str) -> Optional[Passage]:
        """取得段落"""
        for passage in self.passages:
            if passage.name == name:
                return passage
        return None
    
    def add_character(self, character: Character):
        """新增角色"""
        if not self.get_character(character.id):
            self.characters.append(character)
    
    def add_scene(self, scene: Scene):
        """新增場景"""
        if not self.get_scene(scene.id):
            self.scenes.append(scene)
    
    def add_passage(self, passage: Passage):
        """新增段落"""
        if not self.get_passage(passage.name):
            self.passages.append(passage)
