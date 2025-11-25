#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拆分新北市房型分析檔案
將大型的 room_type_detailed_analysis.md 拆分成多個小檔案
"""

import re
import os

def split_room_type_analysis():
    # 讀取原始檔案
    input_file = r'c:\Users\user\Desktop\house_report\新北市\room_type_detailed_analysis.md'
    output_dir = r'c:\Users\user\Desktop\house_report\新北市\房型分析'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正則表達式找到所有房型章節
    # 匹配 ## 房型名稱 的標題
    pattern = r'^## ([0-9一-十]+房[0-9一-十]*[廳衛]*[0-9一-十]*[廳衛]*)$'
    
    # 分割內容
    sections = re.split(pattern, content, flags=re.MULTILINE)
    
    # sections[0] 是標題之前的內容 (包含目錄等)
    # sections[1], sections[2], sections[3], sections[4]... 交替是標題和內容
    
    print(f"找到 {(len(sections)-1)//2} 個房型章節")
    
    # 房型列表
    room_types = []
    
    # 處理每個房型
    for i in range(1, len(sections), 2):
        if i+1 < len(sections):
            room_type = sections[i].strip()
            room_content = sections[i+1]
            
            room_types.append(room_type)
            
            # 創建檔案內容
            file_content = f"""# {room_type} - 詳細分析

> 新北市房地產市場分析

[← 返回目錄](./README.md)

---

## {room_type}

{room_content.strip()}

---

## 導航

[返回目錄](./README.md)
"""
            
            # 儲存檔案
            output_file = os.path.join(output_dir, f'{room_type}.md')
            
            # 修正圖片路徑 (從 charts/ 改為 ../charts/)
            file_content = file_content.replace('](charts/', '](../charts/')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            print(f"已創建: {room_type}.md")
    
    # 第二次掃描,加入「上一個」和「下一個」連結
    for i, room_type in enumerate(room_types):
        output_file = os.path.join(output_dir, f'{room_type}.md')
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 建立導航連結
        nav_parts = []
        
        if i > 0:
            prev_room = room_types[i - 1]
            nav_parts.append(f"[← 上一個: {prev_room}](./{prev_room}.md)")
        
        nav_parts.append("[返回目錄](./README.md)")
        
        if i < len(room_types) - 1:
            next_room = room_types[i + 1]
            nav_parts.append(f"[下一個: {next_room} →](./{next_room}.md)")
        
        nav = " | ".join(nav_parts)
        
        # 替換導航部分
        content = re.sub(
            r'## 導航\n\n.*?\n',
            f'## 導航\n\n{nav}\n',
            content,
            flags=re.DOTALL
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"\n完成! 已創建 {len(room_types)} 個房型分析檔案")
    print(f"輸出目錄: {output_dir}")

if __name__ == '__main__':
    split_room_type_analysis()
