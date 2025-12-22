# JNDLE字道

***

## 項目簡介

本項目爲[JNDLE字道（倉頡版Wordle）](https://samuello.io/jndle/)的魔改版，加入了私人定製的倉頡五代碼表判定。私人碼表參考了[五代倉頡補完計劃](https://github.com/Jackchows/Cangjie5)、[六代倉頡（蒼頡檢字法）](https://github.com/InSb/Cangjie6-Sharp)和[西夏文倉頡](https://github.com/Hulenkius/rime_tangutcjkk)方案，竝有箇人改進。

***

## 項目結構

```python
jndle_extension/
├── src/              # 存儲頁面的圖畫等資源文件
├── tools/              # 工具類腳本文件夾
│   ├── convert_letters_to_cangjie.py # 字母到倉頡字母轉換腳本（用於編碼爲字母的txt碼表）
│   ├── generate_json.py      # 五字倉頡碼JSON文件生成腳本
│   ├── shuffle_codes.py      # 打亂五字倉頡碼順序腳本
│   └── update_codes.py       # 將五字倉頡碼塡入程序JS中的腳本
├── cj.js                     # 程序JS文件（核心邏輯䖏理）
├── jndle_ex.html             # 程序HTML入口
└── README.md                 # 項目說明文檔
```

***

## 工具類腳本說明

convert_letters_to_cangjie.py用於指定一个編碼TXT碼表竝將其編碼部分轉化爲倉頡字母，輸出到新的TXT文件中。輸入碼表要求格式爲 **`編碼\t候選字`**。

碼表格式例：① *`a	 日`*（字母編碼版）、②*`卜口金口山	說`*（倉頡字母版）



generate_json.py用於提取格式爲 **`編碼\t候選字`**的txt碼表中的編碼竝導入至JSON文件（默認爲five_char_codes.json）中，該JSON文件用於儲存待塡入程序中的豫設答案。可以使用由convert_letters_to_cangjie.py生成的txt文件。



shuffle_codes.py用於打亂generate_json.py生成的JSON文件裏數組的順序。



update_codes.py用於將儲存答案的JSON文件裏的數組塡入程序JS文件中。

***

## 碼表說明

第五代倉頡輸入法按[五代倉頡補完計劃](https://github.com/Jackchows/Cangjie5)碼表，引入了[六代倉頡（蒼頡檢字法）](https://github.com/InSb/Cangjie6-Sharp)的鏡像字根（Z鍵、即「片」），同时引入「𩰲」字去掉左邊弓的部分（同樣是在Z鍵）用於優化「鬻」等字的重碼，則「鬻」取nfdz（弓火木片），但是原有的nnmrb（弓弓一口月）編碼保留。

[西夏文倉頡](https://github.com/Hulenkius/rime_tangutcjkk)大體遵照日本學者河崎啓剛的設想，但是訂正了部分編碼，竝加入原版倉頡的包含省略規則，使融合後的碼表規則更爲準确統一。

***

# 本說明文檔撰於2025年12月23日04:30，如後有更新與本文檔所述相違，則以最新版本爲準。
