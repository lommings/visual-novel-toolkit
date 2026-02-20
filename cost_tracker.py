#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 成本追蹤器
追蹤所有 Gemini API 調用並估算成本
"""

import json
import time
import functools
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Any
from collections import defaultdict


# 價格表（美金）
PRICING = {
    # 圖片生成
    'imagen-4.0-generate-001': {
        'per_image': 0.05,  # 估計值，實際以 Google 官方為準
        'type': 'image'
    },
    'imagen-3.0-generate-002': {
        'per_image': 0.04,
        'type': 'image'
    },
    'gemini-3-pro-image-preview': {
        'per_image': 0.03,  # 包含輸入圖片 + 輸出圖片
        'type': 'image'
    },
    # 文字生成 (per 1M tokens)
    'gemini-3-flash-preview': {
        'input_per_1m': 0.075,
        'output_per_1m': 0.30,
        'type': 'text',
        'avg_tokens_per_call': 2000  # 估計每次調用的平均 token 數
    },
    'gemini-2.0-flash-exp': {
        'input_per_1m': 0.075,
        'output_per_1m': 0.30,
        'type': 'text',
        'avg_tokens_per_call': 2000
    },
}


class CostTracker:
    """API 成本追蹤器"""
    
    LOG_FILE = Path("api_usage_log.json")
    
    def __init__(self):
        self.usage = defaultdict(lambda: {
            'calls': 0,
            'estimated_cost': 0.0,
            'details': []
        })
        self.start_time = datetime.now()
        self._load_existing()
    
    def _load_existing(self):
        """載入現有的使用記錄"""
        if self.LOG_FILE.exists():
            try:
                with open(self.LOG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 只載入今天的記錄
                today = datetime.now().strftime('%Y-%m-%d')
                if data.get('date') == today:
                    for model, stats in data.get('usage', {}).items():
                        self.usage[model] = stats
                    print(f"[CostTracker] 載入今天的使用記錄: {sum(u['calls'] for u in self.usage.values())} 次調用")
            except:
                pass
    
    def save(self):
        """儲存使用記錄"""
        data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'last_updated': datetime.now().isoformat(),
            'usage': dict(self.usage),
            'total_cost': self.get_total_cost()
        }
        
        with open(self.LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def log_call(self, model: str, call_type: str, details: str = ""):
        """記錄一次 API 調用"""
        pricing = PRICING.get(model, {})
        
        if pricing.get('type') == 'image':
            cost = pricing.get('per_image', 0.05)
        elif pricing.get('type') == 'text':
            avg_tokens = pricing.get('avg_tokens_per_call', 2000)
            input_cost = (avg_tokens / 1_000_000) * pricing.get('input_per_1m', 0.075)
            output_cost = (avg_tokens / 1_000_000) * pricing.get('output_per_1m', 0.30)
            cost = input_cost + output_cost
        else:
            cost = 0.01  # 未知模型的預設成本
        
        self.usage[model]['calls'] += 1
        self.usage[model]['estimated_cost'] += cost
        self.usage[model]['details'].append({
            'time': datetime.now().isoformat(),
            'type': call_type,
            'details': details,
            'cost': cost
        })
        
        # 每次調用後自動儲存
        self.save()
        
        return cost
    
    def get_total_cost(self) -> float:
        """取得總成本"""
        return sum(u['estimated_cost'] for u in self.usage.values())
    
    def get_summary(self) -> str:
        """取得摘要報告"""
        lines = [
            "=" * 60,
            "📊 API 使用量報告",
            f"📅 日期: {datetime.now().strftime('%Y-%m-%d')}",
            "=" * 60,
            ""
        ]
        
        total_calls = 0
        total_cost = 0.0
        
        # 按成本排序
        sorted_models = sorted(
            self.usage.items(),
            key=lambda x: x[1]['estimated_cost'],
            reverse=True
        )
        
        for model, stats in sorted_models:
            calls = stats['calls']
            cost = stats['estimated_cost']
            total_calls += calls
            total_cost += cost
            
            pricing = PRICING.get(model, {})
            model_type = pricing.get('type', 'unknown')
            
            # 決定警告等級
            if cost > 10:
                emoji = "🔴"
            elif cost > 1:
                emoji = "🟡"
            else:
                emoji = "🟢"
            
            lines.append(f"{emoji} {model}")
            lines.append(f"   類型: {model_type}")
            lines.append(f"   調用次數: {calls}")
            lines.append(f"   估計成本: ${cost:.4f}")
            lines.append("")
        
        lines.extend([
            "=" * 60,
            f"📈 總計調用: {total_calls} 次",
            f"💰 總計成本: ${total_cost:.2f}",
            f"💸 日均: ${total_cost:.2f}",
            f"📊 月估: ${total_cost * 30:.2f}",
            "=" * 60
        ])
        
        return "\n".join(lines)
    
    def get_breakdown(self) -> dict:
        """取得詳細分類統計"""
        breakdown = {
            'image_generation': {'calls': 0, 'cost': 0.0, 'models': []},
            'text_generation': {'calls': 0, 'cost': 0.0, 'models': []},
            'total': {'calls': 0, 'cost': 0.0}
        }
        
        for model, stats in self.usage.items():
            pricing = PRICING.get(model, {})
            model_type = pricing.get('type', 'unknown')
            
            category = 'image_generation' if model_type == 'image' else 'text_generation'
            
            breakdown[category]['calls'] += stats['calls']
            breakdown[category]['cost'] += stats['estimated_cost']
            breakdown[category]['models'].append({
                'model': model,
                'calls': stats['calls'],
                'cost': stats['estimated_cost']
            })
            
            breakdown['total']['calls'] += stats['calls']
            breakdown['total']['cost'] += stats['estimated_cost']
        
        return breakdown


# 全域追蹤器實例
_tracker = None


def get_tracker() -> CostTracker:
    """取得全域追蹤器"""
    global _tracker
    if _tracker is None:
        _tracker = CostTracker()
    return _tracker


def track_api_call(model: str, call_type: str = "unknown"):
    """裝飾器：追蹤 API 調用"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracker = get_tracker()
            
            # 調用前記錄
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # 調用後記錄成本
                duration = time.time() - start_time
                details = f"duration={duration:.2f}s"
                cost = tracker.log_call(model, call_type, details)
                
                print(f"[CostTracker] {model} - {call_type}: ${cost:.4f}")
                
                return result
            except Exception as e:
                # 即使失敗也記錄（API 可能已計費）
                tracker.log_call(model, f"{call_type}_failed", str(e))
                raise
        
        return wrapper
    return decorator


def print_daily_report():
    """印出今日報告"""
    tracker = get_tracker()
    print(tracker.get_summary())


def get_cost_breakdown():
    """取得成本分類"""
    tracker = get_tracker()
    return tracker.get_breakdown()


# === 命令列工具 ===

def main():
    """主程式 - 顯示使用報告"""
    import argparse
    
    parser = argparse.ArgumentParser(description='API 成本追蹤器')
    parser.add_argument('--summary', '-s', action='store_true', help='顯示摘要')
    parser.add_argument('--breakdown', '-b', action='store_true', help='顯示詳細分類')
    parser.add_argument('--reset', action='store_true', help='重設今日記錄')
    
    args = parser.parse_args()
    
    tracker = get_tracker()
    
    if args.reset:
        if CostTracker.LOG_FILE.exists():
            CostTracker.LOG_FILE.unlink()
            print("✅ 已重設使用記錄")
        return
    
    if args.breakdown:
        breakdown = tracker.get_breakdown()
        
        print("\n📊 成本分類分析")
        print("=" * 60)
        
        print("\n🖼️ 圖片生成:")
        img = breakdown['image_generation']
        print(f"   調用次數: {img['calls']}")
        print(f"   成本: ${img['cost']:.2f}")
        for m in img['models']:
            print(f"   - {m['model']}: {m['calls']} 次, ${m['cost']:.4f}")
        
        print("\n📝 文字生成:")
        txt = breakdown['text_generation']
        print(f"   調用次數: {txt['calls']}")
        print(f"   成本: ${txt['cost']:.2f}")
        for m in txt['models']:
            print(f"   - {m['model']}: {m['calls']} 次, ${m['cost']:.4f}")
        
        print("\n" + "=" * 60)
        total = breakdown['total']
        print(f"💰 總計: {total['calls']} 次, ${total['cost']:.2f}")
        
        # 成本佔比
        if total['cost'] > 0:
            img_pct = (img['cost'] / total['cost']) * 100
            txt_pct = (txt['cost'] / total['cost']) * 100
            print(f"\n📈 成本佔比:")
            print(f"   圖片: {img_pct:.1f}%")
            print(f"   文字: {txt_pct:.1f}%")
        
        return
    
    # 預設顯示摘要
    print(tracker.get_summary())


if __name__ == '__main__':
    main()
