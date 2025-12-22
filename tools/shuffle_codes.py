#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打亂JSON文件中倉頡碼列表的順序
"""

import json
import random
import sys
import os

def main():
    """主函數"""
    # 檢查命令行參數
    if len(sys.argv) < 2:
        print("使用方法: python shuffle_codes.py <JSON文件> [輸出文件]")
        print("示例: python shuffle_codes.py five_char_codes.json five_char_codes_shuffled.json")
        print("       python shuffle_codes.py five_char_codes.json  # 默認覆蓋原文件")
        sys.exit(1)
    
    # 獲取輸入文件路徑
    input_file = sys.argv[1]
    
    # 確定輸出文件路徑
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # 如果沒有指定輸出文件，覆蓋原文件
        output_file = input_file
    
    # 檢查輸入文件是否存在
    if not os.path.exists(input_file):
        print(f"錯誤: 輸入文件 '{input_file}' 不存在")
        sys.exit(1)
    
    # 檢查是否爲JSON文件
    if not input_file.lower().endswith('.json'):
        print(f"警告: 輸入文件 '{input_file}' 可能不是JSON文件")
    
    # 讀取JSON文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            codes = json.load(f)
    except json.JSONDecodeError:
        print(f"錯誤: 文件 '{input_file}' 不是有效的JSON格式")
        sys.exit(1)
    except Exception as e:
        print(f"讀取文件時出錯: {e}")
        sys.exit(1)
    
    # 檢查數據是否爲列表
    if not isinstance(codes, list):
        print(f"錯誤: JSON文件應包含列表，但獲取到 {type(codes).__name__}")
        sys.exit(1)
    
    # 創建列表的副本，避免修改原始數據（如果同一個文件既輸入又輸出）
    shuffled_codes = codes.copy()
    
    # 打亂順序
    random.shuffle(shuffled_codes)
    
    # 寫入文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(shuffled_codes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"寫入文件時出錯: {e}")
        sys.exit(1)
    
    print(f'已打亂{len(shuffled_codes)}個倉頡碼的順序')
    
    # 顯示文件信息
    if input_file == output_file:
        print(f'文件已更新: {input_file}')
    else:
        print(f'原始文件: {input_file}')
        print(f'輸出文件: {output_file}')

if __name__ == "__main__":
    main()