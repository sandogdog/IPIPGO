"""
IPIPGO完整流程自动化主程序
包含登录和购买流程
"""

import yaml
import time
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.purchase_page import PurchasePage
from utils.logger import Logger


def main():
    """主函数"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🚀 开始IPIPGO完整流程自动化测试")
        logger.info("🔹 包含：登录 → 购买 → 支付 → 关闭")
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
        
        logger.info(f"🌐 网站地址: {base_url}")
        logger.info(f"👤 登录用户: {username}")
        
        # ========== 第一阶段：登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开IPIPGO网站...")
        login_page.open_homepage(base_url)
        logger.info("✓ 网站打开成功")
        
        logger.info("步骤1.2: 开始登录流程...")
        login_success = login_page.login(username, password)
        if not login_success:
            logger.error("❌ 登录流程失败")
            raise Exception("登录流程失败")
        
        # 二次确认登录结果
        if login_page.is_login_successful():
            logger.info("🎉 登录成功确认！")
        else:
            logger.warning("⚠️ 登录状态未确认，但登录流程已完成")
        
        # 登录阶段截图
        login_screenshot = login_page.take_screenshot("stage1_login_completed.png")
        logger.info(f"📸 登录阶段截图: {login_screenshot}")
        
        # ========== 第二阶段：购买流程 ==========
        logger.info("\n" + "="*40)
        logger.info("💰 第二阶段：购买流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 等待进入个人中心...")
        if purchase_page.wait_for_dashboard():
            logger.info("✓ 已进入个人中心页面")
        else:
            logger.warning("⚠️ 未能确认进入个人中心，继续执行")
        
        logger.info("步骤2.2: 点击第一个立即购买按钮...")
        if purchase_page.click_first_buy_button():
            logger.info("✓ 成功点击第一个立即购买按钮")
        else:
            logger.error("❌ 第一个购买按钮点击失败")
            raise Exception("第一个购买按钮点击失败")
        
        logger.info("步骤2.3: 点击第二个立即购买按钮...")
        if purchase_page.click_second_buy_button():
            logger.info("✓ 成功点击第二个立即购买按钮")
        else:
            logger.error("❌ 第二个购买按钮点击失败")
            raise Exception("第二个购买按钮点击失败")
        
        logger.info("步骤2.4: 点击立即支付按钮并完成支付流程...")
        if purchase_page.click_pay_button_and_handle_payment():
            logger.info("✓ 成功完成支付流程")
        else:
            logger.error("❌ 支付流程失败")
            raise Exception("支付流程失败")
        
        # ========== 第三阶段：第二次购买流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🏢 第三阶段：企业套餐购买流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始企业套餐购买流程...")
        if purchase_page.complete_second_purchase_flow():
            logger.info("✓ 成功完成企业套餐购买流程")
        else:
            logger.error("❌ 企业套餐购买流程失败")
            raise Exception("企业套餐购买流程失败")
        
        # 最终截图
        final_screenshot = purchase_page.take_screenshot("stage4_enterprise_purchase_completed.png")
        logger.info(f"📸 企业套餐购买完成截图: {final_screenshot}")
        
        # ========== 第四阶段：独享静态套餐购买流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🌐 第四阶段：独享静态套餐购买流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始独享静态套餐购买流程...")
        if purchase_page.complete_third_purchase_flow():
            logger.info("✓ 成功完成独享静态套餐购买流程")
        else:
            logger.error("❌ 独享静态套餐购买流程失败")
            raise Exception("独享静态套餐购买流程失败")
        
        # 最终截图
        final_screenshot = purchase_page.take_screenshot("stage5_static_purchase_completed.png")
        logger.info(f"📸 独享静态套餐购买完成截图: {final_screenshot}")
        
        # ========== 第五阶段：静态住宅套餐购买流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🏘️ 第五阶段：静态住宅套餐购买流程")
        logger.info("="*40)
        
        logger.info("步骤5.1: 开始静态住宅套餐购买流程...")
        if purchase_page.complete_fourth_purchase_flow():
            logger.info("✓ 成功完成静态住宅套餐购买流程")
        else:
            logger.error("❌ 静态住宅套餐购买流程失败")
            raise Exception("静态住宅套餐购买流程失败")
        
        # 最终截图
        final_screenshot = purchase_page.take_screenshot("stage6_residential_purchase_completed.png")
        logger.info(f"📸 静态住宅套餐购买完成截图: {final_screenshot}")
        
        # ========== 第六阶段：动态住宅（长效ISP）套餐购买流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🏠 第六阶段：动态住宅（长效ISP）套餐购买流程")
        logger.info("="*40)
        
        logger.info("步骤6.1: 开始动态住宅（长效ISP）套餐购买流程...")
        if purchase_page.complete_fifth_purchase_flow():
            logger.info("✓ 成功完成动态住宅（长效ISP）套餐购买流程")
        else:
            logger.error("❌ 动态住宅（长效ISP）套餐购买流程失败")
            raise Exception("动态住宅（长效ISP）套餐购买流程失败")
        
        # 最终截图
        final_screenshot = purchase_page.take_screenshot("stage7_dynamic_isp_purchase_completed.png")
        logger.info(f"📸 动态住宅（长效ISP）套餐购买完成截图: {final_screenshot}")
        
        # ========== 第七阶段：动态不限量套餐购买流程 ==========
        logger.info("\n" + "="*40)
        logger.info("♾️ 第七阶段：动态不限量套餐购买流程")
        logger.info("="*40)
        
        logger.info("步骤7.1: 开始动态不限量套餐购买流程...")
        if purchase_page.complete_sixth_purchase_flow():
            logger.info("✓ 成功完成动态不限量套餐购买流程")
        else:
            logger.error("❌ 动态不限量套餐购买流程失败")
            raise Exception("动态不限量套餐购买流程失败")
        
        # 最终截图
        final_screenshot = purchase_page.take_screenshot("stage8_unlimited_purchase_completed.png")
        logger.info(f"📸 动态不限量套餐购买完成截图: {final_screenshot}")
        
        # ========== 第八阶段：动态数据中心（基础）套餐购买流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🏢 第八阶段：动态数据中心（基础）套餐购买流程")
        logger.info("="*40)
        
        logger.info("步骤8.1: 开始动态数据中心（基础）套餐购买流程...")
        if purchase_page.complete_seventh_purchase_flow():
            logger.info("✓ 成功完成动态数据中心（基础）套餐购买流程")
        else:
            logger.error("❌ 动态数据中心（基础）套餐购买流程失败")
            raise Exception("动态数据中心（基础）套餐购买流程失败")
        
        # 最终截图
        final_screenshot = purchase_page.take_screenshot("stage9_dynamic_datacenter_basic_purchase_completed.png")
        logger.info(f"📸 动态数据中心（基础）套餐购买完成截图: {final_screenshot}")
        
        # ========== 第九阶段：静态数据中心套餐购买流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🏢 第九阶段：静态数据中心套餐购买流程")
        logger.info("="*40)
        
        logger.info("步骤9.1: 开始静态数据中心套餐购买流程...")
        if purchase_page.complete_eighth_purchase_flow():
            logger.info("✓ 成功完成静态数据中心套餐购买流程")
        else:
            logger.error("❌ 静态数据中心套餐购买流程失败")
            raise Exception("静态数据中心套餐购买流程失败")
        
        # 最终截图
        final_screenshot = purchase_page.take_screenshot("stage10_static_datacenter_purchase_completed.png")
        logger.info(f"📸 静态数据中心套餐购买完成截图: {final_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "="*60)
        logger.info("🎉 IPIPGO完整流程自动化测试成功完成！")
        logger.info("📋 执行流程：登录 → 个人套餐购买 → 支付 → 企业套餐购买 → 支付 → 独享静态套餐购买 → 支付 → 静态住宅套餐购买 → 支付 → 动态住宅ISP套餐购买 → 支付 → 动态不限量套餐购买 → 支付 → 动态数据中心（基础）套餐购买 → 支付 → 静态数据中心套餐购买 → 支付")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 完整流程自动化测试失败: {str(e)}")
        if driver:
            # 失败时截图
            try:
                purchase_page = PurchasePage(driver)
                error_screenshot = purchase_page.take_screenshot("error_complete_flow.png")
                logger.info(f"📸 错误截图已保存: {error_screenshot}")
            except:
                pass
        raise
    
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                with open('config/config.yaml', 'r', encoding='utf-8') as file:
                    config = yaml.safe_load(file)
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("⚠️  注意：由于WebDriver特性，程序结束时浏览器仍可能被关闭")
                logger.info("💡 建议：如需保持浏览器，请在测试完成后手动操作")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO完整流程自动化测试结束")
        logger.info("="*60)


if __name__ == "__main__":
    main()
