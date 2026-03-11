"""
专门测试企业套餐支付重试机制的脚本
用于验证修复后的企业套餐重试逻辑
"""

import yaml
import time
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.purchase_page import PurchasePage
from utils.logger import Logger


def main():
    """测试企业套餐支付重试机制"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 专门测试企业套餐支付重试机制")
        logger.info("💡 模拟从个人套餐成功后继续企业套餐的场景")
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
        
        # === 第一阶段：登录 ===
        logger.info("🔐 第一阶段：执行登录流程...")
        login_page.open_homepage(base_url)
        login_success = login_page.login(username, password)
        if not login_success:
            logger.error("❌ 登录流程失败")
            return False
        logger.info("✅ 登录成功")
        
        # === 第二阶段：快速完成个人套餐（不关注支付结果）===
        logger.info("💰 第二阶段：快速完成个人套餐购买...")
        if not purchase_page.wait_for_dashboard():
            logger.error("❌ 未能进入个人中心")
            return False
        
        # 点击第一个立即购买按钮
        if not purchase_page.click_first_buy_button():
            logger.error("❌ 第一个购买按钮点击失败")
            return False
        logger.info("✓ 第一个立即购买按钮点击成功")
        
        # 点击第二个立即购买按钮
        if not purchase_page.click_second_buy_button():
            logger.error("❌ 第二个购买按钮点击失败")
            return False
        logger.info("✓ 第二个立即购买按钮点击成功")
        
        # 模拟个人套餐支付完成后的状态（直接进入企业套餐测试）
        logger.info("⏩ 跳过个人套餐支付，直接测试企业套餐...")
        
        # === 第三阶段：重点测试企业套餐 ===
        logger.info("="*50)
        logger.info("🏢 第三阶段：企业套餐支付重试机制测试")
        logger.info("💡 这是重点测试部分，观察重试逻辑")
        logger.info("="*50)
        
        # 执行企业套餐购买流程（这里会触发重试机制）
        result = purchase_page.complete_second_purchase_flow()
        
        if result:
            logger.info("✅ 企业套餐支付重试机制测试成功！")
            logger.info("🎉 修复方案有效，企业套餐重试逻辑正常工作")
            return True
        else:
            logger.warning("⚠️ 企业套餐支付重试机制仍存在问题")
            logger.warning("💡 建议检查重试逻辑中的等待时间和按钮定位")
            return False
            
    except Exception as e:
        logger.error(f"❌ 企业套餐支付重试测试失败: {str(e)}")
        return False
    
    finally:
        # 清理资源
        if driver_manager:
            try:
                should_close = config.get('browser', {}).get('close_after_test', False)  # 测试时不关闭浏览器
            except:
                should_close = False
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 浏览器保持打开状态，便于调试")
                logger.info("💡 可以手动观察页面状态")


if __name__ == "__main__":
    print("🧪 企业套餐支付重试机制专项测试")
    print("="*50)
    print("🎯 测试目标：")
    print("  1. 验证企业套餐重试时能正确点击选项卡")
    print("  2. 验证页面加载等待时间是否足够")  
    print("  3. 验证按钮定位策略是否有效")
    print("  4. 验证整体重试逻辑是否完善")
    print("="*50)
    print("🚀 开始测试...")
    
    result = main()
    
    print("\n" + "="*50)
    if result:
        print("✅ 企业套餐支付重试机制测试通过")
        print("🎉 修复成功，可以继续其他套餐的测试")
    else:
        print("❌ 企业套餐支付重试机制仍需调整")
        print("💡 建议查看详细日志进行进一步调试")
    print("="*50)




