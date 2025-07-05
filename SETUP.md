# 馡夢小食光 - 系統設置指南

## 系統架構

- **前端**: HTML5, CSS3, JavaScript
- **後端**: Python Flask
- **資料庫**: MySQL
- **功能**: 電子商務網站 + 管理後台

## 前置需求

### 1. 安裝 Python
- 下載並安裝 Python 3.8 或更新版本
- 確認安裝成功：`python --version`

### 2. 安裝 MySQL
- 下載並安裝 MySQL 8.0 或更新版本
- 記住 root 密碼

### 3. 安裝 Git (可選)
- 用於版本控制

## 設置步驟

### 1. 克隆專案
```bash
git clone https://github.com/ZhanYi-Zhou/feimon-dessert-shop.git
cd feimon-dessert-shop
```

### 2. 設置 Python 環境
```bash
# 建立虛擬環境 (可選但建議)
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安裝依賴套件
pip install -r requirements.txt
```

### 3. 設置 MySQL 資料庫

#### 方法一：使用 MySQL 命令列
```bash
# 登入 MySQL
mysql -u root -p

# 執行資料庫初始化腳本
source database_setup.sql
```

#### 方法二：使用 MySQL Workbench
1. 開啟 MySQL Workbench
2. 連接到您的 MySQL 伺服器
3. 執行 `database_setup.sql` 檔案中的 SQL 指令

### 4. 配置資料庫連接
編輯 `app.py` 檔案，修改資料庫配置：
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # 修改為您的 MySQL 密碼
    'database': 'feimon_dessert_shop'
}
```

### 5. 啟動後端服務
```bash
python app.py
```
後端服務將在 `http://localhost:5000` 運行

### 6. 開啟前端網站
- 直接開啟 `index.html` 檔案
- 或使用本地伺服器：
  ```bash
  # 使用 Python 內建伺服器
  python -m http.server 8000
  ```
  然後訪問 `http://localhost:8000`

## 功能說明

### 客戶端功能
- **產品瀏覽**: 查看雪Q餅和布朗尼系列
- **購物車**: 添加商品、調整數量
- **結帳**: 填寫客戶資料並提交訂單
- **訂單確認**: 顯示訂單編號和總金額

### 管理後台功能
- **訂單管理**: 查看所有訂單
- **統計資料**: 總訂單數、待處理訂單、總營收
- **狀態更新**: 更新訂單處理狀態
- **訂單詳情**: 查看訂單詳細資訊

## API 端點

### 訂單相關
- `POST /api/orders` - 建立新訂單
- `GET /api/orders` - 獲取所有訂單
- `PUT /api/orders/<id>/status` - 更新訂單狀態

### 產品相關
- `GET /api/products` - 獲取產品列表

## 資料庫結構

### orders 表格
- `id`: 訂單編號 (主鍵)
- `customer_name`: 客戶姓名
- `customer_phone`: 聯絡電話
- `customer_address`: 收件地址
- `customer_email`: 電子郵件
- `payment_method`: 付款方式
- `total_amount`: 總金額
- `order_items`: 訂單項目 (JSON)
- `order_status`: 訂單狀態
- `created_at`: 建立時間
- `updated_at`: 更新時間

### products 表格
- `id`: 產品編號 (主鍵)
- `name`: 產品名稱
- `price`: 價格
- `unit`: 單位
- `category`: 分類
- `stock`: 庫存

## 故障排除

### 常見問題

1. **資料庫連接失敗**
   - 確認 MySQL 服務正在運行
   - 檢查資料庫配置是否正確
   - 確認資料庫和表格已建立

2. **CORS 錯誤**
   - 確認後端服務正在運行
   - 檢查 API 端點是否正確

3. **訂單提交失敗**
   - 檢查網路連接
   - 確認後端服務狀態
   - 查看瀏覽器開發者工具的錯誤訊息

### 日誌查看
後端服務會在控制台顯示詳細的錯誤訊息和操作日誌。

## 部署建議

### 開發環境
- 使用本地 MySQL 資料庫
- 前後端分離開發
- 使用瀏覽器開發者工具除錯

### 生產環境
- 使用雲端資料庫服務
- 設置 HTTPS
- 實作身份驗證
- 添加錯誤監控
- 設置備份策略

## 聯絡支援

如有問題，請聯繫開發團隊或提交 Issue。 