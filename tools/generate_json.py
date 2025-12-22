#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
從倉頡碼轉換文件中篩選5個字符的中文倉頡碼並保存為JSON格式
"""

import json
import sys
import os

def extract_five_char_codes(input_file):
    """從輸入文件中提取5個字符的中文倉頡碼"""
    five_char_codes = set()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # 解析行結構：序號→倉頡碼漢字序列	漢字
            parts = line.split('\t')
            if len(parts) != 2:
                continue  # 跳過格式不正確的行
            
            index_cangjie, _ = parts
            
            # 提取倉頡碼漢字序列
            if '→' in index_cangjie:
                _, cangjie_sequence = index_cangjie.split('→', 1)
                cangjie_sequence = cangjie_sequence.strip()
            else:
                cangjie_sequence = index_cangjie.strip()
                
            # 檢查是否爲5箇中文字符的倉頡碼
            if len(cangjie_sequence) == 5 and all('\u4e00' <= c <= '\u9fff' for c in cangjie_sequence):
                five_char_codes.add(cangjie_sequence)
    
    # 轉換爲列表並排序
    return sorted(list(five_char_codes))

def main():
    """主函數"""
    # 檢查命令行參數
    if len(sys.argv) < 2:
        print("使用方法: python extract_five_char_codes.py <輸入文件> [輸出文件]")
        print("示例: python extract_five_char_codes.py cangjie_converted.txt five_char_codes.json")
        print("       python extract_five_char_codes.py cangjie_converted.txt （默认輸出five_char_codes.json）")
        sys.exit(1)
    
    # 獲取輸入和輸出文件路徑
    input_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # 如果沒有指定輸出文件，使用默認名稱
        base_name = os.path.splitext(input_file)[0]
        output_file = f"five_char_codes.json"
    
    # 檢查輸入文件是否存在
    if not os.path.exists(input_file):
        print(f"錯誤: 輸入文件 '{input_file}' 不存在")
        sys.exit(1)
    
    # 提取5字符倉頡碼
    five_char_codes = extract_five_char_codes(input_file)
    
    # 寫入JSON文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(five_char_codes, outfile, ensure_ascii=False, indent=2)
    
    print(f"已從 {input_file} 生成5字符中文倉頡碼列表，共 {len(five_char_codes)} 個條目")
    print(f"文件已保存爲 {output_file}")

if __name__ == "__main__":
    main()