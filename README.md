# Taiwan Stock RS Rank Utility

這個專案提供了一個小指令腳本，自動獲取 MoneyDJ 的 RS Rank（相對強度）篩選後的股票名單，並根據內建的對照表自動加上市場前綴（TWSE: 或 TPEX:）。

## 功能特點
- **MoneyDJ API 整合**：直接串接 MoneyDJ 的選股 API，支援設定「幾週內」與「RS Rank 大於多少」。
- **自動標記市場**：內建台灣股市對照表，自動區分上市（TWSE）與上櫃/興櫃（TPEX）。
- **自定義輸出格式**：輸出格式為 `PREFIX:CODE,PREFIX:CODE`（例如 `TWSE:2330,TPEX:3300`），方便快速複製使用。

## 檔案說明
- `rs_filter.py`: 主程式，輸入篩選條件並輸出結果。
- `stock_mapping.json`: 儲存股票代號與市場（TWSE/TPEX）的映射表。
- `requirements.txt`: 專案所需的套件清單。
- `.gitignore`: 忽略虛擬環境與暫存結果。

## 使用步驟

### 1. 安裝環境
建議使用虛擬環境：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 執行選股篩選
執行主程式，並依照提示輸入條件：
```bash
python3 rs_filter.py
```
**範例輸入：**
- Enter number of weeks: `1`
- Enter minimum RS Rank: `80`

### 3. 查看結果
程式執行完畢後會：
1. 在畫面上印出符合條件的股票清單與「逗號隔開字串」。
2. 產生 `filtered_stocks.txt`（純文字 `PREFIX:CODE` 格式）。
3. 產生 `filtered_stocks.json`（詳細資料格式）。

## 輸出格式範例
`TWSE:1471,TWSE:2486,TPEX:6492,TWSE:2431,TWSE:2367...`
