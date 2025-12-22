#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import json

def extract_array_from_js_file(file_path):
    """
    從JS文件中提取數組內容
    
    Args:
        file_path: JS文件路徑
        
    Returns:
        list: 數組內容，如果提取失敗返回None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # 方法1：嘗試使用正則表達式提取數組
        # 匹配數組開始和結束的位置
        array_pattern = r'\[(.*)\]'
        match = re.search(array_pattern, content, re.DOTALL)
        
        if match:
            array_content = match.group(0)  # 獲取整個數組，包括方括號
            try:
                # 使用json.loads解析數組（需要確保格式正確）
                array_data = json.loads(array_content)
                return array_data
            except json.JSONDecodeError:
                # 如果JSON解析失敗，嘗試手動解析
                print(f"  警告: JSON解析失敗，嘗試手動解析...")
                # 移除首尾方括號
                array_str = match.group(1).strip()
                # 按逗號分割，但要注意字符串內的逗號
                lines = [line.strip() for line in array_str.split(',\n')]
                # 清理每行的引號
                cleaned_lines = []
                for line in lines:
                    line = line.strip()
                    if line:
                        # 移除首尾的引號
                        if (line.startswith('"') and line.endswith('"')) or \
                           (line.startswith("'") and line.endswith("'")):
                            line = line[1:-1]
                        cleaned_lines.append(line)
                return cleaned_lines
        
        # 方法2：如果正則匹配失敗，嘗試逐行讀取
        lines = content.split('\n')
        array_lines = []
        in_array = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('['):
                in_array = True
                # 處理第一行可能包含數組開始和部分內容的情況
                if ']' in line:
                    # 單行數組
                    array_line = line[line.find('[')+1:line.find(']')]
                    if array_line:
                        array_lines.append(array_line.strip(' "\''))
                    return array_lines
                else:
                    array_line = line[line.find('[')+1:]
                    if array_line:
                        array_lines.append(array_line.strip(' "\''))
            elif line.endswith(']'):
                in_array = False
                array_line = line[:line.find(']')]
                if array_line:
                    array_lines.append(array_line.strip(' "\''))
                return array_lines
            elif in_array and line:
                # 移除引號和逗號
                line = line.rstrip(',')
                array_lines.append(line.strip(' "\''))
        
        return None
        
    except Exception as e:
        print(f"錯誤: 無法從文件 {file_path} 提取數組: {e}")
        return None

def replace_la_array_in_js(file_path, new_array):
    """
    替換JS文件中的La數組
    
    Args:
        file_path: JS文件路徑
        new_array: 新的數組內容
        
    Returns:
        bool: 是否成功
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 將新數組轉換爲JS數組字符串
        # 確保每個元素都用雙引號包裹
        array_items = [f'"{item}"' for item in new_array]
        new_array_str = ',\n\t\t'.join(array_items)
        
        # 構建新的數組定義
        new_array_def = f'["{new_array[0]}",\n\t\t' + ',\n\t\t'.join([f'"{item}"' for item in new_array[1:]]) + ']'
        
        # 正則表達式匹配 La 數組定義
        # 支持 var, let, const 聲明，以及不同的格式
        patterns = [
            r'(var\s+La\s*=\s*)\[[^\]]*\];?',  # var La = [...];
            r'(let\s+La\s*=\s*)\[[^\]]*\];?',   # let La = [...];
            r'(const\s+La\s*=\s*)\[[^\]]*\];?', # const La = [...];
            r'(La\s*=\s*)\[[^\]]*\];?',         # La = [...];
        ]
        
        replacement_made = False
        
        for pattern in patterns:
            # 使用 re.DOTALL 使 . 匹配換行符
            match = re.search(pattern, content, re.DOTALL)
            if match:
                # 構建替換字符串
                replacement = match.group(1) + new_array_def
                # 執行替換
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                replacement_made = True
                print(f"  匹配模式: {pattern}")
                break
        
        if not replacement_made:
            print(f"警告: 未找到 La 數組定義，將在文件末尾添加")
            # 在文件末尾添加新的數組定義
            content = content.rstrip() + '\n\n' + f'var La = {new_array_def}\n'
        
        # 寫回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"錯誤: 無法替換文件 {file_path} 中的數組: {e}")
        return False

def main():
    """主函數"""
    print("JS文件數組替換工具")
    print("=" * 50)
    print("功能：將第二個JS文件（數據文件）中的數組內容塡入第一個JS文件（待塡入）的La數組中")
    print("=" * 50)
    
    # 獲取用戶輸入
    template_file = input("請輸入第一個JS文件路徑（包含La數組定義）: ").strip()
    if not template_file:
        print("錯誤: 文件路徑不能爲空")
        return
    
    data_file = input("請輸入第二個JS文件路徑（包含數組數據）: ").strip()
    if not data_file:
        print("錯誤: 文件路徑不能爲空")
        return
    
    # 檢查文件是否存在
    if not os.path.exists(template_file):
        print(f"錯誤: 文件不存在: {template_file}")
        return
    
    if not os.path.exists(data_file):
        print(f"錯誤: 文件不存在: {data_file}")
        return
    
    print(f"\n處理中...")
    print(f"待塡入文件: {template_file}")
    print(f"數據文件: {data_file}")
    
    # 從數據文件提取數組
    print(f"\n1. 從數據文件提取數組...")
    array_data = extract_array_from_js_file(data_file)
    
    if array_data is None:
        print(f"錯誤: 無法從數據文件提取數組")
        return
    
    print(f"  提取到 {len(array_data)} 個元素")
    print(f"  前5個元素示例:")
    for i, item in enumerate(array_data[:5], 1):
        print(f"    {i}. {item}")
    
    # 備份原文件
    import shutil
    backup_file = template_file + '.bak'
    shutil.copy2(template_file, backup_file)
    print(f"\n2. 已創建備份文件: {backup_file}")
    
    # 替換待塡入文件中的數組
    print(f"\n3. 替換待塡入文件中的La數組...")
    success = replace_la_array_in_js(template_file, array_data)
    
    if success:
        print(f"\n{'='*50}")
        print("替換成功!")
        print(f"  原文件已備份到: {backup_file}")
        print(f"  新文件: {template_file}")
        print(f"  替換了 {len(array_data)} 個數組元素")
        
        # 顯示新文件的前幾行
        print(f"\n新文件內容預覽:")
        with open(template_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:10], 1):
                line = line.rstrip()
                if len(line) > 80:
                    line = line[:77] + '...'
                print(f"  {i:2d}: {line}")
            if len(lines) > 10:
                print(f"  ... 還有 {len(lines) - 10} 行")
    else:
        print(f"\n{'='*50}")
        print("替換失敗!")

def batch_process_directory():
    """批量處理目錄下的文件"""
    print("\n批量處理模式")
    print("-" * 50)
    
    template_dir = input("請輸入包含待塡入JS文件的目錄: ").strip()
    if not template_dir:
        template_dir = os.getcwd()
    
    data_dir = input("請輸入包含數據JS文件的目錄: ").strip()
    if not data_dir:
        data_dir = os.getcwd()
    
    if not os.path.exists(template_dir):
        print(f"錯誤: 目錄不存在: {template_dir}")
        return
    
    if not os.path.exists(data_dir):
        print(f"錯誤: 目錄不存在: {data_dir}")
        return
    
    # 查找待塡入文件和數據文件
    template_files = [f for f in os.listdir(template_dir) if f.endswith('.js') and 'la' in f.lower()]
    data_files = [f for f in os.listdir(data_dir) if f.endswith('.js') and 'array' in f.lower()]
    
    print(f"\n找到 {len(template_files)} 個待塡入文件:")
    for i, f in enumerate(template_files, 1):
        print(f"  {i}. {f}")
    
    print(f"\n找到 {len(data_files)} 個數據文件:")
    for i, f in enumerate(data_files, 1):
        print(f"  {i}. {f}")
    
    if not template_files or not data_files:
        print("錯誤: 沒有找到足夠的文件")
        return
    
    # 讓用戶選擇要處理的文件
    template_choice = input(f"\n選擇待塡入文件 (1-{len(template_files)}): ").strip()
    try:
        template_idx = int(template_choice) - 1
        template_file = os.path.join(template_dir, template_files[template_idx])
    except:
        print("無效選擇")
        return
    
    data_choice = input(f"選擇數據文件 (1-{len(data_files)}): ").strip()
    try:
        data_idx = int(data_choice) - 1
        data_file = os.path.join(data_dir, data_files[data_idx])
    except:
        print("無效選擇")
        return
    
    print(f"\n處理文件:")
    print(f"  待塡入: {template_file}")
    print(f"  數據: {data_file}")
    
    confirm = input("\n確認處理? (y/n): ").strip().lower()
    if confirm == 'y':
        # 調用主處理邏輯
        array_data = extract_array_from_js_file(data_file)
        if array_data:
            import shutil
            backup_file = template_file + '.bak'
            shutil.copy2(template_file, backup_file)
            
            success = replace_la_array_in_js(template_file, array_data)
            if success:
                print("批量處理完成!")
            else:
                print("批量處理失敗!")

if __name__ == "__main__":
    print("請選擇操作:")
    print("1. 單文件處理")
    print("2. 批量處理目錄")
    
    choice = input("\n請輸入選項 (1-2): ").strip()
    
    if choice == '1':
        main()
    elif choice == '2':
        batch_process_directory()
    else:
        print("無效選項")