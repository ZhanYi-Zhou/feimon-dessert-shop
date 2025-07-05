from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 資料庫配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # 請修改為您的MySQL密碼
    'database': 'feimon_dessert_shop'
}

# 建立資料庫連接
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"資料庫連接錯誤: {err}")
        return None

# 初始化資料庫表格
def init_database():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        
        # 建立訂單表格
        create_orders_table = """
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
        )
        """
        
        # 建立產品表格
        create_products_table = """
        CREATE TABLE IF NOT EXISTS products (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            unit VARCHAR(20) NOT NULL,
            category VARCHAR(50) NOT NULL,
            stock INT DEFAULT 20
        )
        """
        
        try:
            cursor.execute(create_orders_table)
            cursor.execute(create_products_table)
            
            # 插入產品資料
            products_data = [
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
                (12, '靜甜輕醺係 (6入盒裝)', 280, '盒', 'brownie', 20)
            ]
            
            insert_product = """
            INSERT IGNORE INTO products (id, name, price, unit, category, stock) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.executemany(insert_product, products_data)
            connection.commit()
            print("資料庫初始化完成")
            
        except mysql.connector.Error as err:
            print(f"資料庫初始化錯誤: {err}")
        finally:
            cursor.close()
            connection.close()

# 處理訂單提交
@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        # 驗證必要欄位
        required_fields = ['customer_name', 'customer_phone', 'customer_address', 
                          'customer_email', 'payment_method', 'cart_items']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必要欄位: {field}'}), 400
        
        # 計算總金額
        total_amount = sum(item['price'] * item['quantity'] for item in data['cart_items'])
        
        # 準備訂單資料
        order_data = {
            'customer_name': data['customer_name'],
            'customer_phone': data['customer_phone'],
            'customer_address': data['customer_address'],
            'customer_email': data['customer_email'],
            'payment_method': data['payment_method'],
            'total_amount': total_amount,
            'order_items': json.dumps(data['cart_items'], ensure_ascii=False)
        }
        
        # 儲存到資料庫
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '資料庫連接失敗'}), 500
        
        cursor = connection.cursor()
        
        insert_order = """
        INSERT INTO orders (customer_name, customer_phone, customer_address, 
                           customer_email, payment_method, total_amount, order_items)
        VALUES (%(customer_name)s, %(customer_phone)s, %(customer_address)s,
                %(customer_email)s, %(payment_method)s, %(total_amount)s, %(order_items)s)
        """
        
        cursor.execute(insert_order, order_data)
        order_id = cursor.lastrowid
        
        # 更新產品庫存
        for item in data['cart_items']:
            update_stock = """
            UPDATE products SET stock = stock - %s WHERE id = %s
            """
            cursor.execute(update_stock, (item['quantity'], item['id']))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': '訂單提交成功！',
            'order_id': order_id,
            'total_amount': total_amount
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'訂單提交失敗: {str(e)}'}), 500

# 獲取所有訂單
@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '資料庫連接失敗'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT id, customer_name, customer_phone, customer_address, customer_email,
               payment_method, total_amount, order_items, order_status, created_at
        FROM orders ORDER BY created_at DESC
        """
        
        cursor.execute(query)
        orders = cursor.fetchall()
        
        # 解析JSON格式的訂單項目
        for order in orders:
            order['order_items'] = json.loads(order['order_items'])
            order['created_at'] = order['created_at'].isoformat()
        
        cursor.close()
        connection.close()
        
        return jsonify({'orders': orders}), 200
        
    except Exception as e:
        return jsonify({'error': f'獲取訂單失敗: {str(e)}'}), 500

# 獲取產品列表
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '資料庫連接失敗'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT * FROM products ORDER BY category, id"
        cursor.execute(query)
        products = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({'products': products}), 200
        
    except Exception as e:
        return jsonify({'error': f'獲取產品失敗: {str(e)}'}), 500

# 更新訂單狀態
@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': '缺少訂單狀態'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '資料庫連接失敗'}), 500
        
        cursor = connection.cursor()
        
        update_query = "UPDATE orders SET order_status = %s WHERE id = %s"
        cursor.execute(update_query, (new_status, order_id))
        
        if cursor.rowcount == 0:
            return jsonify({'error': '訂單不存在'}), 404
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'message': '訂單狀態更新成功'}), 200
        
    except Exception as e:
        return jsonify({'error': f'更新訂單狀態失敗: {str(e)}'}), 500

if __name__ == '__main__':
    # 初始化資料庫
    init_database()
    
    # 啟動Flask應用
    app.run(debug=True, host='0.0.0.0', port=5000) 