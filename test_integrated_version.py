"""
测试整合版本功能的脚本
用于验证standalone_login.py的完整工作流程
"""

from IPIPGO_token import IPIPGOStandaloneLogin
import time

def test_integrated_version():
    """测试整合版本的功能"""
    print("🧪 开始测试整合版本功能")
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
        
        target_url = "http://10.20.51.100:8081/#/project-management/environmentManagement?orgId=100001&pId=49912330342924288"
        
        print("🔧 测试参数:")
        print(f"IPIPGO登录URL: {ipipgo_url}")
        print(f"IPIPGO用户名: {ipipgo_username}")
        print(f"MeterSphere登录URL: {metersphere_login_url}")
        print(f"MeterSphere用户名: {metersphere_username}")
        print(f"目标URL: {target_url}")
        print("=" * 60)
        
        # 测试1：IPIPGO登录功能
        print("🧪 测试1：IPIPGO登录功能")
        login_success = login.login(ipipgo_url, ipipgo_username, ipipgo_password)
        print(f"IPIPGO登录结果: {'✅ 成功' if login_success else '❌ 失败'}")
        
        if not login_success:
            print("❌ IPIPGO登录失败，无法继续测试")
            return False
        
        # 测试2：W_TOKEN获取
        print("\n🧪 测试2：W_TOKEN获取")
        w_token = login.get_w_token_optimized()
        print(f"W_TOKEN获取结果: {'✅ 成功' if w_token else '❌ 失败'}")
        if w_token:
            print(f"W_TOKEN: {w_token[:50]}...")
        
        if not w_token:
            print("❌ W_TOKEN获取失败，无法继续测试")
            return False
        
        # 测试3：打开MeterSphere登录页面
        print("\n🧪 测试3：打开MeterSphere登录页面")
        page_opened = login.open_new_page(metersphere_login_url)
        print(f"MeterSphere登录页面打开结果: {'✅ 成功' if page_opened else '❌ 失败'}")
        
        if not page_opened:
            print("❌ MeterSphere登录页面打开失败，无法继续测试")
            return False
        
        # 测试4：MeterSphere登录
        print("\n🧪 测试4：MeterSphere登录")
        metersphere_login_success = login.login_metersphere(metersphere_username, metersphere_password)
        print(f"MeterSphere登录结果: {'✅ 成功' if metersphere_login_success else '❌ 失败'}")
        
        if not metersphere_login_success:
            print("❌ MeterSphere登录失败，无法继续测试")
            return False
        
        # 测试5：打开环境管理页面
        print("\n🧪 测试5：打开环境管理页面")
        env_page_opened = login.open_new_page(target_url)
        print(f"环境管理页面打开结果: {'✅ 成功' if env_page_opened else '❌ 失败'}")
        
        if not env_page_opened:
            print("❌ 环境管理页面打开失败，无法继续测试")
            return False
        
        # 等待页面加载
        time.sleep(5)
        
        # 测试6：查找输入框
        print("\n🧪 测试6：查找cookie_web输入框")
        input_element = login.find_cookie_web_input()
        if not input_element:
            input_element = login.find_cookie_web_input_by_context()
        
        print(f"输入框查找结果: {'✅ 成功' if input_element else '❌ 失败'}")
        
        if not input_element:
            print("❌ 输入框查找失败，无法继续测试")
            return False
        
        # 测试7：填写cookie_web值（带前缀和分号）
        print("\n🧪 测试7：填写cookie_web值（带前缀和分号）")
        cookie_web_value = f"W_TOKEN={w_token};"
        print(f"将要填写的完整值: {cookie_web_value[:60]}...")
        fill_success = login.fill_cookie_web_value(cookie_web_value)
        print(f"填写结果: {'✅ 成功' if fill_success else '❌ 失败'}")
        
        # 截图保存测试结果
        login.take_screenshot("test_result.png")
        
        # 测试总结
        print("\n🎯 测试总结:")
        print("=" * 60)
        print(f"✅ IPIPGO登录: {'通过' if login_success else '失败'}")
        print(f"✅ W_TOKEN获取: {'通过' if w_token else '失败'}")
        print(f"✅ MeterSphere登录页面打开: {'通过' if page_opened else '失败'}")
        print(f"✅ MeterSphere登录: {'通过' if metersphere_login_success else '失败'}")
        print(f"✅ 环境管理页面打开: {'通过' if env_page_opened else '失败'}")
        print(f"✅ 输入框查找: {'通过' if input_element else '失败'}")
        print(f"✅ 填写功能: {'通过' if fill_success else '失败'}")
        print("=" * 60)
        
        all_tests = [login_success, w_token, page_opened, metersphere_login_success, 
                    env_page_opened, input_element, fill_success]
        
        if all(all_tests):
            print("🎉 所有测试通过！整合版本功能正常")
            return True
        else:
            print("❌ 部分测试失败，请检查相关功能")
            return False
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 根据配置决定是否关闭浏览器
        login.close()

if __name__ == "__main__":
    test_integrated_version() 