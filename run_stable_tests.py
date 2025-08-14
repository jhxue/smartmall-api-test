#!/usr/bin/env python3
"""
稳定的测试运行脚本
解决间歇性测试错误问题
"""

import requests
import subprocess
import time
import sys
import os


def reset_mock_server():
    """重置Mock服务器数据"""
    try:
        response = requests.post("http://127.0.0.1:8080/reset", timeout=5)
        if response.status_code == 200:
            print("✅ Mock服务器数据已重置")
            return True
        else:
            print(f"⚠️ 重置失败，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到Mock服务器: {e}")
        return False


def check_mock_server():
    """检查Mock服务器是否运行"""
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Mock服务器正常运行 - 用户: {data.get('registered_users', 0)}, 商店: {data.get('stores', 0)}")
            return True
        else:
            print(f"⚠️ Mock服务器响应异常，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Mock服务器连接失败: {e}")
        print("请确保Mock服务器正在运行：")
        print("cd mock_server && python app.py")
        return False


def run_tests_with_retry(max_retries=3):
    """带重试机制的测试运行"""
    for attempt in range(1, max_retries + 1):
        print(f"\n🔄 第 {attempt} 次测试运行...")
        
        # 重置Mock服务器数据
        if not reset_mock_server():
            print("❌ 无法重置Mock服务器，跳过此次运行")
            continue
            
        # 等待一小段时间确保重置完成
        time.sleep(1)
        
        # 运行测试
        try:
            cmd = [
                sys.executable, "-m", "pytest", 
                "--alluredir=reports/allure-results",
                "-v", "--tb=short"
            ]
            
            print(f"执行命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ 测试成功！(第 {attempt} 次尝试)")
                print("测试输出:")
                print(result.stdout)
                return True
            else:
                print(f"❌ 测试失败 (第 {attempt} 次尝试)")
                print("错误输出:")
                print(result.stderr)
                print("标准输出:")
                print(result.stdout)
                
        except subprocess.TimeoutExpired:
            print(f"⏰ 测试超时 (第 {attempt} 次尝试)")
        except Exception as e:
            print(f"❌ 运行测试时出错: {e}")
        
        if attempt < max_retries:
            print(f"🔄 等待 3 秒后重试...")
            time.sleep(3)
    
    print(f"❌ 经过 {max_retries} 次尝试后测试仍然失败")
    return False


def main():
    """主函数"""
    print("🚀 SmartMall API 稳定测试运行器")
    print("=" * 50)
    
    # 检查Mock服务器状态
    if not check_mock_server():
        return False
    
    # 运行测试
    success = run_tests_with_retry(max_retries=3)
    
    if success:
        print("\n🎉 所有测试成功完成！")
        print("📊 可以查看Allure报告：")
        print("allure serve reports/allure-results")
    else:
        print("\n💡 故障排除建议：")
        print("1. 重启Mock服务器：cd mock_server && python app.py")
        print("2. 检查端口8080是否被占用：netstat -an | findstr 8080")
        print("3. 手动重置数据：curl -X POST http://127.0.0.1:8080/reset")
        print("4. 运行单个测试模块进行调试")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
