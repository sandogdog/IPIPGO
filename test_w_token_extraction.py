"""
测试W_TOKEN提取功能
专门用于测试登录后获取W_TOKEN的功能
"""

from IPIPGO_token import IPIPGOStandaloneLogin
import time

def test_w_token_extraction():
    """测试W_TOKEN提取功能"""
    print("=" * 80)
    print("🧪 开始测试W_TOKEN提取功能")
    print("=" * 80)
    
    # 创建登录实例
    login = IPIPGOStandaloneLogin(headless=False)
    
    try:
        # 登录信息
        url = "https://test.ipipgo.com/zh-CN/"
        username = "18327166247"  # 替换为您的用户名
        password = "qinrenchi123"  # 替换为您的密码
        
        print(f"🌐 网站地址: {url}")
        print(f"👤 用户名: {username}")
        print("=" * 80)
        
        # 执行登录
        print("🔐 开始登录流程...")
        login_success = login.login(url, username, password)
        
        if not login_success:
            print("❌ 登录失败，无法继续测试")
            return
        
        print("✅ 登录成功，开始获取W_TOKEN...")
        
        # 等待页面完全加载
        print("⏳ 等待页面完全加载...")
        time.sleep(5)
        
        # 测试各种W_TOKEN获取方法
        print("\n" + "=" * 80)
        print("🔍 测试各种W_TOKEN获取方法")
        print("=" * 80)
        
        # 方法1: 从cookies获取
        print("\n1️⃣ 测试从cookies获取W_TOKEN")
        token_cookies = login.get_w_token_from_cookies()
        
        # 方法2: 从JavaScript获取
        print("\n2️⃣ 测试从JavaScript获取W_TOKEN")
        token_js = login.get_w_token_from_javascript()
        
        # 优化后的综合测试
        print("\n" + "=" * 80)
        print("🎯 优化后的W_TOKEN获取测试")
        print("=" * 80)
        
        final_token = login.get_w_token_optimized()
        
        # 结果汇总
        print("\n" + "=" * 80)
        print("📊 测试结果汇总")
        print("=" * 80)
        
        results = {
            "Cookies方法": token_cookies,
            "JavaScript方法": token_js,
            "优化后的方法": final_token
        }
        
        found_count = 0
        for method, token in results.items():
            if token:
                print(f"✅ {method}: {token[:50]}...")
                found_count += 1
            else:
                print(f"❌ {method}: 未找到")
        
        print(f"\n📈 总共找到 {found_count} 个有效结果")
        
        # 检查W_TOKEN是否已存储
        stored_token = login.get_stored_w_token()
        if stored_token:
            print(f"\n✅ W_TOKEN已存储到实例变量中: {stored_token[:50]}...")
        else:
            print("\n❌ W_TOKEN未存储到实例变量中")
        
        if final_token:
            print("\n" + "=" * 80)
            print("🎉 最终获取的W_TOKEN:")
            print(f"W_TOKEN={final_token}")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("❌ 未能获取到W_TOKEN")
            print("建议检查：")
            print("1. 网站是否正确设置了W_TOKEN")
            print("2. 登录是否真正成功")
            print("3. 是否需要等待更长时间")
            print("=" * 80)
        
        # 等待用户观察
        print("\n按回车键继续...")
        input()
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 清理
        print("\n🧹 清理资源...")
        login.close()
        print("✅ 测试完成")

if __name__ == "__main__":
    test_w_token_extraction() 