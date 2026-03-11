"""
测试支付重试机制的脚本
专门测试已修复的个人套餐和企业套餐
"""

import yaml
import time
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.purchase_page import PurchasePage
from utils.logger import Logger


def test_personal_package_payment_retry():
    """测试个人套餐的支付重试机制"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 测试个人套餐支付重试机制")
        logger.info("="*60)
        
        # 读取配置文件
        with open('config/config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        login_page = LoginPage(driver)
        purchase_page = PurchasePage(driver)
        
        # 获取配置信息
        base_url = config['environment']['base_url']
        username = config['test_data']['login']['username']
        password = config['test_data']['login']['password']
        
        # 登录流程
        logger.info("步骤1: 执行登录流程...")
        login_page.open_homepage(base_url)
        login_success = login_page.login(username, password)
        if not login_success:
            logger.error("❌ 登录流程失败")
            return False
        
        logger.info("✅ 登录成功")
        
        # 进入购买流程
        logger.info("步骤2: 进入购买流程...")
        if not purchase_page.wait_for_dashboard():
            logger.error("❌ 未能进入个人中心")
            return False
        
        # 点击第一个立即购买按钮
        logger.info("步骤3: 点击第一个立即购买按钮...")
        if not purchase_page.click_first_buy_button():
            logger.error("❌ 第一个购买按钮点击失败")
            return False
        
        # 点击第二个立即购买按钮
        logger.info("步骤4: 点击第二个立即购买按钮...")
        if not purchase_page.click_second_buy_button():
            logger.error("❌ 第二个购买按钮点击失败")
            return False
        
        # 测试支付重试机制
        logger.info("步骤5: 测试支付重试机制...")
        logger.info("💡 注意观察日志中的重试逻辑...")
        
        if purchase_page.click_pay_button_and_handle_payment():
            logger.info("✅ 个人套餐支付重试机制测试成功！")
            return True
        else:
            logger.warning("⚠️ 个人套餐支付重试机制测试未完全成功")
            return False
            
    except Exception as e:
        logger.error(f"❌ 个人套餐支付重试测试失败: {str(e)}")
        return False
    
    finally:
        # 清理资源
        if driver_manager:
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")


def test_enterprise_package_payment_retry():
    """测试企业套餐的支付重试机制"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 测试企业套餐支付重试机制")
        logger.info("="*60)
        
        # 读取配置文件
        with open('config/config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        login_page = LoginPage(driver)
        purchase_page = PurchasePage(driver)
        
        # 获取配置信息
        base_url = config['environment']['base_url']
        username = config['test_data']['login']['username']
        password = config['test_data']['login']['password']
        
        # 登录流程
        logger.info("步骤1: 执行登录流程...")
        login_page.open_homepage(base_url)
        login_success = login_page.login(username, password)
        if not login_success:
            logger.error("❌ 登录流程失败")
            return False
        
        logger.info("✅ 登录成功")
        
        # 执行企业套餐购买流程
        logger.info("步骤2: 测试企业套餐支付重试机制...")
        logger.info("💡 注意观察日志中的重试逻辑...")
        
        if purchase_page.complete_second_purchase_flow():
            logger.info("✅ 企业套餐支付重试机制测试成功！")
            return True
        else:
            logger.warning("⚠️ 企业套餐支付重试机制测试未完全成功")
            return False
            
    except Exception as e:
        logger.error(f"❌ 企业套餐支付重试测试失败: {str(e)}")
        return False
    
    finally:
        # 清理资源
        if driver_manager:
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")


if __name__ == "__main__":
    import sys
    
    print("🧪 支付重试机制测试脚本")
    print("="*50)
    print("选择测试项目：")
    print("1. 测试个人套餐支付重试")
    print("2. 测试企业套餐支付重试")
    print("3. 测试两个套餐（依次执行）")
    print("="*50)
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("请输入选择 (1/2/3): ").strip()
    
    if choice == "1":
        print("🚀 开始测试个人套餐支付重试机制...")
        test_personal_package_payment_retry()
    elif choice == "2":
        print("🚀 开始测试企业套餐支付重试机制...")
        test_enterprise_package_payment_retry()
    elif choice == "3":
        print("🚀 开始依次测试两个套餐的支付重试机制...")
        print("\n" + "="*30 + " 第一轮测试 " + "="*30)
        result1 = test_personal_package_payment_retry()
        
        print("\n" + "="*30 + " 第二轮测试 " + "="*30)
        result2 = test_enterprise_package_payment_retry()
        
        print("\n" + "="*60)
        print("📊 测试结果汇总：")
        print(f"个人套餐：{'✅ 成功' if result1 else '❌ 失败'}")
        print(f"企业套餐：{'✅ 成功' if result2 else '❌ 失败'}")
        print("="*60)
    else:
        print("❌ 无效选择")
        sys.exit(1)
