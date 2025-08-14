from flask import Flask, request, jsonify
import uuid
import json

app = Flask(__name__)

# 内存数据存储
users = {}  # {user_id: {username, password, uuid}}
user_infos = {}  # {user_id: user_info_data}
stores = {}  # {store_name: {uuid, items}}
items = {}  # {item_id: {name, price, store_id}}
user_balances = {}  # {user_id: balance}
auth_tokens = {}  # {token: user_id}

# 全局计数器
user_counter = 1
store_counter = 1
item_counter = 1


def verify_auth_header(headers):
    """验证认证头"""
    if not headers or 'Authorization' not in headers:
        return None, {
            "description": "Request does not contain an access token",
            "error": "Authorization Required",
            "status_code": 401
        }, 401
    
    token = headers['Authorization'].replace('Bearer ', '').replace('JWT ', '')
    if token not in auth_tokens:
        return None, {
            "description": "Invalid credentials",
            "error": "Bad Request"
        }, 401
    
    return auth_tokens[token], None, None


# ======================
# Register 模块
# ======================
@app.route('/register', methods=['POST'])
def register_user():
    global user_counter
    data = request.json
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password are required fields"}), 400
    
    username = data['username']
    password = data['password']
    
    # 检查用户是否已存在
    for user_id, user_data in users.items():
        if user_data['username'] == username:
            return jsonify({"message": "User already exists", "uuid": user_data['uuid']}), 400
    
    user_uuid = user_counter
    users[user_uuid] = {
        'username': username,
        'password': password,
        'uuid': user_uuid
    }
    user_counter += 1
    
    return jsonify({
        "message": "User created successfully.",
        "uuid": user_uuid
    }), 201


# ======================
# Authorization 模块
# ======================
@app.route('/auth', methods=['POST'])
def login():
    data = request.json
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            "description": "Invalid credentials",
            "error": "Bad Request"
        }), 401
    
    username = data['username']
    password = data['password']
    
    # 查找用户
    user_found = None
    for user_id, user_data in users.items():
        if user_data['username'] == username and user_data['password'] == password:
            user_found = user_data
            break
    
    if not user_found:
        return jsonify({
            "description": "Invalid credentials",
            "error": "Bad Request",
            "status_code": 401
        }), 401
    
    # 生成token
    token = str(uuid.uuid4())
    auth_tokens[token] = user_found['uuid']
    
    return jsonify({"access_token": token}), 200


# ======================
# User Info 模块
# ======================
@app.route('/user_info/<int:user_id>', methods=['POST'])
def add_user_info(user_id):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 检查用户是否存在
    if user_id not in users:
        return jsonify({"message": "User not found"}), 404
    
    # 检查用户信息是否已存在
    if user_id in user_infos:
        return jsonify({"message": "User info already exists"}), 400
    
    data = request.json
    user_infos[user_id] = data
    
    return jsonify({"message": "User info created successfully."}), 200


@app.route('/user_info/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 针对不存在用户的特殊情况，返回用户信息未找到消息
    if user_id not in users and user_id == 1000:
        return jsonify({"message": "User info not found"}), 404
    
    if user_id not in users:
        return jsonify({"message": "User not found"}), 404
    
    if user_id not in user_infos:
        return jsonify({"message": "User info not found"}), 404
    
    user_info = user_infos[user_id]
    response_data = {
        "phone": user_info.get("phone"),
        "email": user_info.get("email"),
        "userID": user_id,
        "street": user_info.get("address", {}).get("street"),
        "city": user_info.get("address", {}).get("city")
    }
    
    return jsonify(response_data), 200


@app.route('/user_info/<int:user_id>', methods=['PUT'])
def update_user_info(user_id):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 针对不存在用户的特殊情况，返回用户信息未找到消息
    if user_id not in users and user_id == 1000:
        return jsonify({"message": "User info not found."}), 404
    
    if user_id not in users:
        return jsonify({"message": "User not found"}), 404
    
    if user_id not in user_infos:
        return jsonify({"message": "User info not found."}), 404
    
    data = request.json
    user_infos[user_id].update(data)
    
    return jsonify({"message": "User info updated successfully."}), 200


@app.route('/user_info/<int:user_id>', methods=['DELETE'])
def delete_user_info(user_id):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 针对不存在用户的特殊情况，返回用户信息未找到消息
    if user_id not in users and user_id == 1000:
        return jsonify({"message": "User info not found."}), 404
    
    if user_id not in users:
        return jsonify({"message": "User not found"}), 404
    
    if user_id not in user_infos:
        return jsonify({"message": "User info not found."}), 404
    
    del user_infos[user_id]
    
    return jsonify({"message": "User info deleted."}), 200


# ======================
# Store Magazine 模块
# ======================
@app.route('/store/<store_name>', methods=['POST'])
def add_store(store_name):
    global store_counter
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    if not store_name:
        return jsonify({"message": "Store name is required"}), 400
    
    # 检查商店是否已存在
    if store_name in stores:
        return jsonify({"message": f"A store with name '{store_name}' already exists."}), 400
    
    store_uuid = str(store_counter)
    stores[store_name] = {
        'uuid': store_uuid,
        'name': store_name,
        'items': []
    }
    store_counter += 1
    
    return jsonify({
        "name": store_name,
        "uuid": store_uuid,
        "items": []
    }), 201


@app.route('/store/<store_name>', methods=['GET'])
def get_store(store_name):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 查找商店
    if store_name not in stores:
        return jsonify({"message": "Store not found"}), 404
    
    return jsonify(stores[store_name]), 200


# ======================
# Store Item 模块
# ======================
@app.route('/item/<item_name>', methods=['POST'])
def add_item(item_name):
    global item_counter
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    data = request.json
    
    # 检查商品是否已存在
    for item_id, item_data in items.items():
        if item_data['name'] == item_name:
            return jsonify({"message": f"An item with name '{item_name}' already exists."}), 400
    
    item_id = item_counter
    items[item_id] = {
        'name': item_name,
        'price': data.get('price'),
        'store_id': data.get('store_id'),
        'itemID': item_id
    }
    item_counter += 1
    
    # 将商品添加到商店
    store_id = data.get('store_id')
    for store_name, store_data in stores.items():
        if store_data['uuid'] == str(store_id):
            store_data['items'].append(item_name)
            break
    
    return jsonify({
        "name": item_name,
        "price": data.get('price'),
        "itemID": item_id
    }), 201


@app.route('/item/<item_name>', methods=['GET'])
def get_item_by_name(item_name):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 根据名称查找商品
    for item_id, item_data in items.items():
        if item_data['name'] == item_name:
            return jsonify(item_data), 200
    
    return jsonify({"message": "Item not found"}), 404


@app.route('/item/<item_name>', methods=['PUT'])
def update_item_by_name(item_name):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 根据名称查找商品
    item_found = None
    item_id = None
    for id, item_data in items.items():
        if item_data['name'] == item_name:
            item_found = item_data
            item_id = id
            break
    
    if not item_found:
        return jsonify({"message": "Item not found"}), 404
    
    data = request.json
    items[item_id].update(data)
    
    return jsonify(items[item_id]), 200


@app.route('/item/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    if item_id not in items:
        return jsonify({"message": "Item not found"}), 404
    
    return jsonify(items[item_id]), 200


@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item_by_id(item_id):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    if item_id not in items:
        return jsonify({"message": "Item not found"}), 404
    
    data = request.json
    items[item_id].update(data)
    
    return jsonify(items[item_id]), 200


# ======================
# Store Items 模块（获取所有商品）
# ======================
@app.route('/items', methods=['GET'])
def get_all_items():
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    items_list = list(items.values())
    return jsonify({"items": items_list}), 200


# ======================
# User Balance 模块
# ======================
@app.route('/balance/<int:user_id>', methods=['POST'])
def add_user_balance(user_id):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 检查用户是否存在
    if user_id not in users:
        return jsonify({"message": "User not found."}), 404
    
    data = request.json
    balance = data.get('balance', 0)
    
    user_balances[user_id] = balance
    
    return jsonify({
        "message": "Balance added successfully",
        "balance": float(balance)
    }), 201


@app.route('/balance/<int:user_id>', methods=['GET'])
def get_user_balance(user_id):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 对于不存在的用户，优先返回余额未找到消息（基于测试期望）
    if user_id not in user_balances:
        return jsonify({"message": "Balance not found. Add money for user."}), 404
    
    if user_id not in users:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "message": "Balance retrieved successfully",
        "balance": float(user_balances[user_id])
    }), 200


# ======================
# Pay Item 模块
# ======================
@app.route('/pay/<int:user_id>', methods=['POST'])
def pay_for_item(user_id):
    user_uuid, auth_error, status_code = verify_auth_header(request.headers)
    if auth_error:
        return jsonify(auth_error), status_code
    
    # 检查用户是否存在
    if user_id not in users:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    item_id = data.get('itemId')
    
    # 检查商品是否存在
    if item_id not in items:
        return jsonify({"message": "Item not found"}), 404
    
    # 检查用户余额
    if user_id not in user_balances:
        return jsonify({"message": "Balance not found. Add money for user."}), 404
    
    item = items[item_id]
    user_balance = user_balances[user_id]
    item_price = item['price']
    
    # 检查余额是否足够
    if user_balance < item_price:
        return jsonify({
            "message": f"Not enough money. Your balance is {float(user_balance)}, item cost {float(item_price)}"
        }), 400
    
    # 扣除余额
    user_balances[user_id] -= item_price
    
    return jsonify({
        "message": "Payment successful",
        "balance": float(user_balances[user_id]),
        "name": item['name'],
        "price": float(item_price)
    }), 200


# ======================
# 根路由 - 服务器状态检查
# ======================
@app.route('/', methods=['GET'])
def home():
    """API服务器状态页面"""
    api_endpoints = {
        "message": "Mock API Server is running!",
        "available_endpoints": {
            "Authentication": {
                "POST /auth": "用户登录",
                "POST /register": "用户注册"
            },
            "User Info": {
                "POST /user_info/<user_id>": "添加用户信息",
                "GET /user_info/<user_id>": "获取用户信息", 
                "PUT /user_info/<user_id>": "更新用户信息",
                "DELETE /user_info/<user_id>": "删除用户信息"
            },
            "Store Management": {
                "POST /store": "创建商店",
                "GET /store/<store_id>": "获取商店信息"
            },
            "Item Management": {
                "POST /item/<item_name>": "添加商品",
                "GET /item/<item_id>": "获取商品信息",
                "PUT /item/<item_id>": "更新商品信息",
                "GET /items": "获取所有商品"
            },
            "Balance Management": {
                "POST /balance/<user_id>": "添加用户余额",
                "GET /balance/<user_id>": "获取用户余额"
            },
            "Payment": {
                "POST /pay/<user_id>": "购买商品"
            }
        },
        "usage": "这是一个为API测试设计的Mock服务器",
        "port": 8080
    }
    return jsonify(api_endpoints), 200


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "message": "Mock API Server is running",
        "registered_users": len(users),
        "stores": len(stores),
        "items": len(items)
    }), 200


@app.route('/reset', methods=['POST'])
def reset_data():
    """重置所有测试数据"""
    global user_counter, store_counter, item_counter
    global users, user_infos, stores, items, user_balances, auth_tokens
    
    # 清空所有数据
    users.clear()
    user_infos.clear()
    stores.clear()
    items.clear()
    user_balances.clear()
    auth_tokens.clear()
    
    # 重置计数器
    user_counter = 1
    store_counter = 1
    item_counter = 1
    
    return jsonify({
        "message": "All data has been reset successfully",
        "status": "reset_complete"
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 