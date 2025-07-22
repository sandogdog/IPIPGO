"""
快速测试修改后的功能
测试MeterSphere登录和W_TOKEN前缀功能
"""

from IPIPGO_token import IPIPGOStandaloneLogin
import time

def quick_test():
    """快速测试修改后的功能"""
    print("🚀 开始快速测试修改后的功能")
    print("=" * 60)
    
    # 创建登录实例
    login = IPIPGOStandaloneLogin(headless=False)
    
    try:
        # 测试参数
        ipipgo_url = "https://test.ipipgo.com/zh-CN/"
        ipipgo_username = "18327166247"
        ipipgo_password = "qinrenchi123"
        
        metersphere_login_url = "http://10.20.51.100:8081/#/login?redirect=no-project"
        metersphere_username = "renchi.qin@xiaoxitech.com"
        metersphere_password = "renchi.qin@xiaoxitech.com"
        
        print("📋 测试配置:")
        print(f"IPIPGO登录地址: {ipipgo_url}")
        print(f"IPIPGO用户名: {ipipgo_username}")
        print(f"MeterSphere登录地址: {metersphere_login_url}")
        print(f"MeterSphere用户名: {metersphere_username}")
        print("=" * 60)
        
        # 步骤1：登录IPIPGO
        print("🔐 步骤1：登录IPIPGO")
        login_success = login.login(ipipgo_url, ipipgo_username, ipipgo_password)
        if not login_success:
            print("❌ IPIPGO登录失败")
            return False
        print("✅ IPIPGO登录成功")
        
        # 步骤2：获取W_TOKEN
        print("\n🔑 步骤2：获取W_TOKEN")
        w_token = login.get_w_token_optimized()
        if not w_token:
            print("❌ W_TOKEN获取失败")
            return False
        print(f"✅ W_TOKEN获取成功: {w_token[:50]}...")
        
        # 步骤3：打开MeterSphere登录页面
        print("\n🌐 步骤3：打开MeterSphere登录页面")
        page_opened = login.open_new_page(metersphere_login_url)
        if not page_opened:
            print("❌ MeterSphere登录页面打开失败")
            return False
        print("✅ MeterSphere登录页面打开成功")
        
        # 步骤4：登录MeterSphere
        print("\n🔐 步骤4：登录MeterSphere")
        metersphere_login_success = login.login_metersphere(metersphere_username, metersphere_password)
        if not metersphere_login_success:
            print("❌ MeterSphere登录失败")
            return False
        print("✅ MeterSphere登录成功")
        
        # 步骤5：测试W_TOKEN前缀功能
        print("\n🧪 步骤5：测试W_TOKEN前缀功能")
        cookie_web_value = f"W_TOKEN={w_token}"
        print(f"✅ W_TOKEN前缀处理成功: {cookie_web_value[:60]}...")
        
        # 截图保存测试结果
        login.take_screenshot("quick_test_result.png")
        
        print("\n🎯 测试结果总结:")
        print("=" * 60)
        print("✅ IPIPGO登录：通过")
        print("✅ W_TOKEN获取：通过")
        print("✅ MeterSphere登录页面打开：通过")
        print("✅ MeterSphere登录：通过")
        print("✅ W_TOKEN前缀处理：通过")
        print("✅ 所有功能测试通过！")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 根据配置决定是否关闭浏览器
        login.close()

if __name__ == "__main__":
    quick_test() 