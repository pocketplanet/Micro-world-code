# 自動化灌溉系統程式

這是一個通過串行通訊從感測器中讀取數據並將其上傳到Firebase Firestore中。以下是程式的主要結構和功能：

## 主要功能：

1. 讀取串行數據：程式通過串行通訊從感測器中讀取數據。
2. 解析數據：將從串行端口讀取的原始數據解析為可理解的格式。
3. 上傳到Firebase Firestore：將解析後的數據上傳到Firebase Firestore中的適當文檔中。
4. 非同步處理：使用異步IO庫asyncio來實現非同步處理，以確保系統的效率和穩定性。

## 主要程式碼結構：

- `parse_data(d)`: 解析從串行端口讀取的原始數據。
- `serial_read()`: 從串行端口讀取數據並返回解析後的數據。
- `upload_data_to_firestore(d)`: 將解析後的數據上傳到Firebase Firestore中的適當文檔中。
- `main()`: 主函數，使用異步IO來執行主要的數據讀取和上傳任務。

## 使用方法：

1. 確保已安裝必要的庫和依賴項。
2. 將串行端口和Firebase帳戶設置為正確的值。
3. 執行程式，系統將開始從串行端口讀取數據並上傳到Firebase。

注意：請確保已將Firebase的服務帳戶金鑰文件放置在正確的路徑（`./pocketplanet-AccountKey/serviceAccountKey.json`）下，並已配置串行端口和其他相關參數。

以上是自動化灌溉系統程式的簡要介紹和使用指南。
