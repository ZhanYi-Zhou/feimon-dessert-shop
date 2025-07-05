-- 建立資料庫
CREATE DATABASE IF NOT EXISTS feimon_dessert_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用資料庫
USE feimon_dessert_shop;

-- 建立訂單表格
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    customer_address TEXT NOT NULL,
    customer_email VARCHAR(100) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    order_items JSON NOT NULL,
    order_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 建立產品表格
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    stock INT DEFAULT 20
);

-- 插入產品資料
INSERT IGNORE INTO products (id, name, price, unit, category, stock) VALUES
(1, '原味雪Q餅', 100, '包', 'snowq', 20),
(2, '抹茶雪Q餅', 120, '包', 'snowq', 20),
(3, '巧克力雪Q餅', 120, '包', 'snowq', 20),
(4, '綜合雪Q餅', 120, '包', 'snowq', 20),
(5, '靜謐醇熟韻', 50, '顆', 'brownie', 20),
(6, '柔田小確幸', 50, '顆', 'brownie', 20),
(7, '秘醺蘭姆霧', 50, '顆', 'brownie', 20),
(8, '靜甜輕醺係', 50, '顆', 'brownie', 20),
(9, '靜謐醇熟韻 (6入盒裝)', 280, '盒', 'brownie', 20),
(10, '柔田小確幸 (6入盒裝)', 280, '盒', 'brownie', 20),
(11, '秘醺蘭姆霧 (6入盒裝)', 280, '盒', 'brownie', 20),
(12, '靜甜輕醺係 (6入盒裝)', 280, '盒', 'brownie', 20); 