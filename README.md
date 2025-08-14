# SmartMall API Test

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/Pytest-7.0+-green.svg)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.9+-orange.svg)](https://docs.qameta.io/allure/)

## 项目简介

SmartMall API Test 是一个基于Python的REST API自动化测试框架，专门用于测试智能商城系统的各种API接口。该项目采用现代化的测试架构，提供完整的API测试解决方案。

## 功能特性

-  **用户注册与认证** - 支持用户注册、登录功能测试
-  **用户信息管理** - 用户信息的增删改查测试
-  **商店管理** - 商店创建、查询等功能测试
-  **商品管理** - 商品的添加、修改、查询测试
-  **用户余额** - 用户余额管理功能测试
-  **支付功能** - 商品购买、支付流程测试
-  **测试报告** - 基于Allure框架的美观测试报告

## 技术栈

- **Python 3.9+** - 主要编程语言
- **Pytest** - 测试框架
- **Requests** - HTTP请求库
- **Allure Framework** - 测试报告生成
- **Faker** - 测试数据生成
- **Flask** - Mock服务器

## 项目结构

```
smartmall-api-test/
├── common/                 # 公共工具模块
│   ├── __init__.py
│   └── deco.py            # 装饰器
├── fixtures/              # 测试夹具
│   ├── auth/              # 认证相关
│   ├── balance/           # 余额相关
│   ├── magazine/          # 商店相关
│   ├── pay/               # 支付相关
│   ├── register/          # 注册相关
│   ├── store_item/        # 商品相关
│   ├── store_items/       # 商品列表相关
│   └── userInfo/          # 用户信息相关
├── mock_server/           # Mock服务器
│   └── app.py            # Flask应用
├── tests/                 # 测试用例
│   ├── authorization/     # 认证测试
│   ├── pay_item/         # 支付测试
│   ├── register/         # 注册测试
│   ├── store_item/       # 商品测试
│   ├── store_items/      # 商品列表测试
│   ├── store_magazine/   # 商店测试
│   ├── user_balance/     # 用户余额测试
│   └── user_info/        # 用户信息测试
├── allure-results/        # Allure测试结果
├── conftest.py           # Pytest配置
├── pytest.ini           # Pytest设置
└── requirements.txt      # 项目依赖
```

## 安装指南

### 前置要求

- Python 3.9 或更高版本
- Java 8+ (用于Allure报告)
- Git

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd smartmall-api-test
```

### 2. 创建虚拟环境

```bash
python -m venv venv
```

### 3. 激活虚拟环境

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 安装Allure (可选)

**Windows (使用Scoop):**
```bash
scoop install allure
```

**Mac (使用Homebrew):**
```bash
brew install allure
```

**或者下载安装包:** [Allure官方下载](https://docs.qameta.io/allure/)

## 使用说明

### 启动Mock服务器

在运行测试之前，需要先启动Mock服务器：

```bash
cd mock_server
python app.py
```

服务器将在 `http://127.0.0.1:8080` 启动

### 运行测试

**运行所有测试:**
```bash
pytest
```

**运行特定测试模块:**
```bash
pytest tests/register/
pytest tests/store_item/
```

**运行正向测试:**
```bash
pytest -m positive
```

**运行负向测试:**
```bash
pytest -m negative
```

**生成Allure报告:**
```bash
pytest --alluredir=allure-results
```

**查看Allure报告:**
```bash
allure serve allure-results
```

### API测试覆盖

| 模块 | 功能 | 状态 |
|------|------|------|
| 用户注册 | 用户注册、数据验证 | ✅ |
| 用户认证 | 登录、Token验证 | ✅ |
| 用户信息 | 添加、查询、删除用户信息 | ✅ |
| 商店管理 | 创建商店、查询商店 | ✅ |
| 商品管理 | 添加、修改、查询商品 | ✅ |
| 商品列表 | 获取商品列表 | ✅ |
| 用户余额 | 添加、查询用户余额 | ✅ |
| 支付功能 | 商品购买流程 | ✅ |

## 测试报告

项目使用Allure框架生成详细的测试报告，包括：

- 📈 测试执行概览
- 📊 测试结果统计
- 📝 详细的测试步骤
- 🐛 失败用例分析
- 📸 请求响应截图

## 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。

---

⭐ 如果这个项目对您有帮助，请给它一个星标！