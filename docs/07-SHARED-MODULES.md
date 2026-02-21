# 共用模組說明

## 📋 概述

共用模組位於 `shared/` 目錄，提供所有工具共用的功能，避免重複程式碼。

---

## 📁 模組結構

```
shared/
├── __init__.py
├── ai_client.py          # AI API 封裝
├── image_generator.py    # 圖片生成封裝
├── config_manager.py     # 設定管理
├── file_utils.py         # 檔案操作工具
└── models/               # 資料模型
    ├── __init__.py
    ├── story.py          # 故事相關
    ├── character.py      # 角色相關
    └── scene.py          # 場景相關
```

---

## 🤖 ai_client.py

統一的 AI API 介面，支援多個 provider。

```python
class AIClient:
    """AI API 統一介面"""
    
    def __init__(self, config: dict):
        self.provider = config['ai']['provider']
        self.config = config['ai'][self.provider]
    
    def analyze(self, prompt: str) -> dict:
        """發送分析請求，返回 JSON"""
        pass
    
    def generate_text(self, prompt: str) -> str:
        """生成文字"""
        pass

# 使用範例
from shared.ai_client import AIClient

client = AIClient(config)
result = client.analyze("分析這個故事...")
```

### 支援的 Provider

| Provider | 用途 | 設定 |
|----------|------|------|
| gemini | 文字分析、分支生成 | api_key, model |
| openai | 備用選項 | api_key, model |

---

## 🖼️ image_generator.py

統一的圖片生成介面。

```python
class ImageGenerator:
    """圖片生成統一介面"""
    
    def __init__(self, config: dict):
        self.provider = config['image_generation']['provider']
        self.style = config['visual_style']['current']
    
    def generate(self, prompt: str, output_path: str, **kwargs) -> bool:
        """生成圖片"""
        pass
    
    def generate_character(self, character: dict, expression: str, 
                          output_path: str, reference: str = None) -> bool:
        """生成角色立繪"""
        pass
    
    def generate_scene(self, scene: dict, output_path: str) -> bool:
        """生成場景背景"""
        pass

# 使用範例
from shared.image_generator import ImageGenerator

gen = ImageGenerator(config)
gen.generate_character(
    character={'name': '和也', 'description': '年輕工程師'},
    expression='happy',
    output_path='output/kazuya_happy.png'
)
```

### 支援的 Provider

| Provider | 類型 | 特點 |
|----------|------|------|
| stable_diffusion | 本地 | 免費、可客製化 |
| gemini_imagen | 雲端 | 穩定、無需 GPU |

---

## ⚙️ config_manager.py

統一的設定管理。

```python
class ConfigManager:
    """設定管理器"""
    
    _instance = None
    _config = None
    
    @classmethod
    def load(cls, config_path: str = 'config.json') -> dict:
        """載入設定檔"""
        if cls._config is None:
            with open(config_path, 'r', encoding='utf-8') as f:
                cls._config = json.load(f)
        return cls._config
    
    @classmethod
    def get(cls, key: str, default=None):
        """取得設定值，支援點號分隔的路徑"""
        # config.get('ai.gemini.api_key')
        pass
    
    @classmethod
    def save(cls, config_path: str = 'config.json'):
        """儲存設定"""
        pass

# 使用範例
from shared.config_manager import ConfigManager

config = ConfigManager.load()
api_key = ConfigManager.get('ai.gemini.api_key')
```

---

## 📂 file_utils.py

檔案操作工具函式。

```python
def ensure_dir(path: str) -> None:
    """確保目錄存在"""
    Path(path).mkdir(parents=True, exist_ok=True)

def load_json(path: str) -> dict:
    """載入 JSON 檔案"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: dict, path: str, indent: int = 2) -> None:
    """儲存 JSON 檔案"""
    ensure_dir(Path(path).parent)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def copy_directory(src: str, dst: str) -> None:
    """複製整個目錄"""
    if Path(dst).exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def get_timestamp() -> str:
    """取得 ISO 格式時間戳"""
    return datetime.now().isoformat()
```

---

## 📦 models/

資料模型定義，使用 dataclass 或 Pydantic。

### models/character.py

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Character:
    id: str
    name: str
    description: str = ""
    expressions: List[str] = field(default_factory=lambda: ["normal"])
    color: str = "#ffffff"
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'expressions': self.expressions,
            'color': self.color
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Character':
        return cls(**data)
```

### models/scene.py

```python
@dataclass
class Scene:
    id: str
    name: str
    description: str = ""
    time_of_day: str = "日間"
    mood: str = ""
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'time_of_day': self.time_of_day,
            'mood': self.mood
        }
```

### models/story.py

```python
@dataclass
class DialogueLine:
    character: str
    text: str
    expression: str = "normal"

@dataclass  
class NarrationLine:
    text: str

@dataclass
class Choice:
    text: str
    target: str

@dataclass
class Passage:
    name: str
    scene_id: Optional[str] = None
    lines: List[Union[DialogueLine, NarrationLine]] = field(default_factory=list)
    choices: List[Choice] = field(default_factory=list)
```

---

## 🔧 使用方式

### 在各工具中引用

```python
# novel-to-twee/main.py
import sys
sys.path.insert(0, '..')  # 加入父目錄

from shared.ai_client import AIClient
from shared.config_manager import ConfigManager
from shared.file_utils import load_json, save_json
from shared.models.character import Character

# 載入設定
config = ConfigManager.load()

# 使用 AI
client = AIClient(config)
result = client.analyze(prompt)

# 儲存結果
save_json(result, 'output/analysis.json')
```

### 安裝為套件（可選）

```python
# shared/setup.py
from setuptools import setup, find_packages

setup(
    name='vn-toolkit-shared',
    version='1.0.0',
    packages=find_packages()
)
```

```bash
# 安裝
cd shared
pip install -e .

# 使用
from vn_toolkit_shared.ai_client import AIClient
```

---

## 📜 script_processor.py

腳本處理器，自動處理角色顯示、位置、對話等。

### 功能

- 偵測對話行（`角色名：對話內容`）
- 偵測文字中提到的角色
- 自動加入 `show character` 指令
- 自動決定角色位置（left/right/center）
- 結局標註

### 角色名稱對應表

```python
char_name_mapping = {
    '和也': 'kazuya',
    '相葉': 'aiba'
}
```

### 對話偵測

程式會自動偵測以下格式：
```
相葉：你還好嗎？
```
↓ 自動轉換為
```javascript
'show character aiba normal at center with fadeIn',
'aiba 你還好嗎？'
```

### 角色位置決定

```python
def get_position(shown_chars, new_char):
    if len(shown_chars) == 0:
        return 'center'     # 第一個角色置中
    elif len(shown_chars) == 1:
        return 'right'      # 第二個角色在右
    else:
        return 'center'     # 更多角色置中
```

### 結局標註

段落名稱以 `Ending_` 開頭會自動加上結局標題：

```python
def _get_ending_title(self, passage_name: str) -> str:
    ending_titles = {
        'Ending_BreakChains': '破鏈重生',
        'Ending_LostShadow': '消失的幽影',
        'Ending_SilentEnd': '無聲的終結',
    }
    return ending_titles.get(passage_name, passage_name)
```

輸出：
```javascript
'centered ── 結局：破鏈重生 ──',
'end'
```

### 使用範例

```python
from shared.script_processor import create_processor

processor = create_processor({
    '和也': 'kazuya',
    '相葉': 'aiba'
})

processed = processor.process_script(passages, scene_mapping)
```

---

## ✅ 設計原則

| 原則 | 說明 |
|------|------|
| 單一職責 | 每個模組只負責一種功能 |
| 統一介面 | 不同 provider 使用相同的介面 |
| 可測試 | 每個模組可獨立測試 |
| 無狀態 | 避免全域狀態，使用依賴注入 |
| 型別提示 | 使用 Python type hints |
