#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將碼表中的英文字母形態的倉頡碼轉換爲漢字形態
輸入格式：序號→字母序列	漢字
輸出格式：序號→倉頡碼漢字序列	漢字
"""

import sys
import os

# 字母到倉頡字母的映射表
letter_to_cangjie = {
    'a': '日',
    'b': '月',
    'c': '金',
    'd': '木',
    'e': '水',
    'f': '火',
    'g': '土',
    'h': '竹',
    'i': '戈',
    'j': '十',
    'k': '大',
    'l': '中',
    'm': '一',
    'n': '弓',
    'o': '人',
    'p': '心',
    'q': '手', 
    'r': '口',  
    's': '尸',  
    't': '廿',  
    'u': '山',
    'v': '女',
    'w': '田',
    'x': '難',
    'y': '卜',
    'z': '片', 
}

def convert_line(line):
    """轉換一行文本"""
    line = line.strip()
    if not line:
        return line
    
    # 解析行結構：序號→字母序列	漢字
    parts = line.split('\t')
    if len(parts) != 2:
        return line  # 格式不正確的行，保持原樣
    
    index_letters, original_char = parts
    
    # 解析序號和字母序列：序號→字母序列
    if '→' in index_letters:
        # 分割序號和字母序列
        index_part, letters = index_letters.split('→', 1)
        # 提取序號和字母
        index = index_part.strip()
        letters = letters.strip()
    else:
        # 如果沒有箭頭，直接使用整個部分作爲字母序列
        index = ''
        letters = index_letters.strip()
    
    # 將字母序列轉換爲倉頡碼漢字序列
    cangjie_sequence = ''.join([letter_to_cangjie.get(c.lower(), c) for c in letters])
    
    # 重新組合行：序號→倉頡碼漢字序列	漢字
    if index:
        return f"{index}→{cangjie_sequence}\t{original_char}"
    else:
        return f"{cangjie_sequence}\t{original_char}"

def main():
    """主函數"""
    # 檢查命令行參數
    if len(sys.argv) < 2:
        print("使用方法: python convert_letters_to_cangjie.py <輸入文件> [輸出文件]")
        print("示例: python convert_letters_to_cangjie.py cangjie.txt cangjie_converted.txt")
        print("       python convert_letters_to_cangjie.py cangjie.txt（默認輸出cangjie_converted.txt）")
        sys.exit(1)
    
    # 獲取輸入和輸出文件路徑
    input_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # 如果沒有指定輸出文件，使用默認名稱
        base_name = os.path.splitext(input_file)[0]
        output_file = f"cangjie_converted.txt"
    
    # 檢查輸入文件是否存在
    if not os.path.exists(input_file):
        print(f"錯誤: 輸入文件 '{input_file}' 不存在")
        sys.exit(1)
    
    # 讀取輸入文件
    with open(input_file, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()
    
    # 轉換所有行
    converted_lines = [convert_line(line) for line in lines]
    
    # 寫入輸出文件
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write('\n'.join(converted_lines))
    
    print(f"轉換完成！")
    print(f"輸入文件: {input_file}")
    print(f"輸出文件: {output_file}")
    print(f"轉換行數: {len(converted_lines)}")

if __name__ == "__main__":
    main()