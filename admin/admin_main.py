"""
IPIPGO管理后台UI自动化主程序
"""

import yaml
import time
import os
import sys

# 添加父目录到路径，以便导入utils模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.driver_manager import DriverManager
from utils.logger import Logger
from admin.pages.admin_login_page import AdminLoginPage
from admin.pages.customer_page import CustomerPage


def main():
    """管理后台主函数 - 完整测试所有套餐类型"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🚀 开始IPIPGO管理后台完整UI自动化测试")
        logger.info("🔹 包含：管理后台登录 + 切换职位 + 客户查询 + 所有9种套餐购买测试")
        logger.info("🔹 套餐顺序：标准 → 企业 → 基础 → 不限量 → 静态代理Hosting → 静态代理ISP → 静态代理双ISP → 独享静态 → 独享静态TikTok解决方案")
        logger.info("="*60)
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        admin_login_page = AdminLoginPage(driver)
        customer_page = CustomerPage(driver)
        
        # 获取管理后台配置信息
        admin_config = config['admin_environment']
        login_url = admin_config['login_url']
        
        admin_login_data = config['test_data']['admin_login']
        username = admin_login_data['username']
        password = admin_login_data['password']
        target_position = admin_login_data.get('target_position', '秦仁驰')  # 从配置读取，默认为秦仁驰
        
        logger.info(f"🌐 管理后台登录地址: {login_url}")
        logger.info(f"👤 管理员用户: {username}")
        logger.info(f"🔄 目标职位: {target_position}")
        
        # ========== 第一阶段：管理后台登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：管理后台登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开管理后台登录页面...")
        if admin_login_page.open_admin_login_page(login_url):
            logger.info("✓ 管理后台登录页面打开成功")
        else:
            logger.error("❌ 管理后台登录页面打开失败")
            raise Exception("管理后台登录页面打开失败")
        
        logger.info("步骤1.2: 开始管理后台登录流程...")
        if admin_login_page.admin_login(username, password):
            logger.info("✓ 管理后台登录成功")
        else:
            logger.error("❌ 管理后台登录失败")
            raise Exception("管理后台登录失败")
        
        # 登录成功截图
        login_screenshot = admin_login_page.take_screenshot("admin_login_completed.png")
        logger.info(f"📸 管理后台登录完成截图: {login_screenshot}")
        
        # ========== 第二阶段：切换职位流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔄 第二阶段：切换职位流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 开始切换职位流程...")
        if admin_login_page.switch_position(target_position):
            logger.info(f"✓ 职位切换成功，已切换到: {target_position}")
        else:
            logger.error("❌ 职位切换失败")
            raise Exception("职位切换失败")
        
        # 切换职位成功截图
        switch_screenshot = admin_login_page.take_screenshot("admin_position_switched.png")
        logger.info(f"�� 职位切换完成截图: {switch_screenshot}")
        
        # ========== 第三阶段：客户查询流程 ==========
        logger.info("\n" + "="*40)
        logger.info("👥 第三阶段：客户查询流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始客户查询流程...")
        target_user_id = "7156"  # 要查询的用户ID
        logger.info(f"🔍 目标用户ID: {target_user_id}")
        
        if customer_page.navigate_to_customer_and_query(target_user_id):
            logger.info(f"✓ 客户查询流程成功完成，用户ID: {target_user_id}")
        else:
            logger.error("❌ 客户查询流程失败")
            raise Exception("客户查询流程失败")
        
        # 客户查询完成截图
        customer_screenshot = customer_page.take_screenshot("customer_query_completed.png")
        logger.info(f"📸 客户查询完成截图: {customer_screenshot}")
        
        # ========== 动态套餐系列 ==========
        logger.info("\n" + "🔥"*60)
        logger.info("🔥 开始动态套餐系列测试（4种套餐）")
        logger.info("🔥"*60)
        
        # ========== 第四阶段：开标准套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("📦 第四阶段：开标准套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始开标准套餐+支付流程...")
        package_remark = "IPIPGO 标准套餐UI自动化测试"
        logger.info(f"📝 标准套餐备注信息: {package_remark}")
        
        if customer_page.open_package_flow(package_remark):
            logger.info("✓ 标准套餐+支付流程成功完成")
        else:
            logger.error("❌ 标准套餐+支付流程失败")
            raise Exception("标准套餐+支付流程失败")
        
        # 标准套餐+支付完成截图
        package_screenshot = customer_page.take_screenshot("stage1_standard_package_payment_completed.png")
        logger.info(f"📸 标准套餐+支付完成截图: {package_screenshot}")
        
        # ========== 第五阶段：开企业套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🏢 第五阶段：开企业套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤5.1: 开始开企业套餐+支付流程...")
        enterprise_remark = "IPIPGO 企业套餐UI自动化测试"
        logger.info(f"📝 企业套餐备注信息: {enterprise_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_enterprise_package_flow(enterprise_remark):
            logger.info("✓ 企业套餐+支付流程成功完成")
        else:
            logger.error("❌ 企业套餐+支付流程失败")
            raise Exception("企业套餐+支付流程失败")
        
        # 企业套餐+支付完成截图
        enterprise_screenshot = customer_page.take_screenshot("stage2_enterprise_package_payment_completed.png")
        logger.info(f"📸 企业套餐+支付完成截图: {enterprise_screenshot}")
        
        # ========== 第六阶段：开基础套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔧 第六阶段：开基础套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤6.1: 开始开基础套餐+支付流程...")
        basic_remark = "IPIPGO 基础套餐UI自动化测试"
        logger.info(f"📝 基础套餐备注信息: {basic_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_basic_package_flow(basic_remark):
            logger.info("✓ 基础套餐+支付流程成功完成")
        else:
            logger.error("❌ 基础套餐+支付流程失败")
            raise Exception("基础套餐+支付流程失败")
        
        # 基础套餐+支付完成截图
        basic_screenshot = customer_page.take_screenshot("stage3_basic_package_payment_completed.png")
        logger.info(f"📸 基础套餐+支付完成截图: {basic_screenshot}")
        
        # ========== 第七阶段：开不限量套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🚀 第七阶段：开不限量套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤7.1: 开始开不限量套餐+支付流程...")
        unlimited_remark = "IPIPGO 不限量套餐UI自动化测试"
        logger.info(f"📝 不限量套餐备注信息: {unlimited_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_unlimited_package_flow(unlimited_remark):
            logger.info("✓ 不限量套餐+支付流程成功完成")
        else:
            logger.error("❌ 不限量套餐+支付流程失败")
            raise Exception("不限量套餐+支付流程失败")
        
        # 不限量套餐+支付完成截图
        unlimited_screenshot = customer_page.take_screenshot("stage4_unlimited_package_payment_completed.png")
        logger.info(f"📸 不限量套餐+支付完成截图: {unlimited_screenshot}")
        
        # ========== 静态代理套餐系列 ==========
        logger.info("\n" + "🌐"*60)
        logger.info("🌐 开始静态代理套餐系列测试（3种套餐）")
        logger.info("🌐"*60)
        
        # ========== 第八阶段：开静态代理Hosting套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🌐 第八阶段：开静态代理Hosting套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤8.1: 开始开静态代理Hosting套餐+支付流程...")
        static_hosting_remark = "IPIPGO 静态代理Hosting套餐UI自动化测试"
        logger.info(f"📝 静态代理Hosting套餐备注信息: {static_hosting_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_static_package_flow(static_hosting_remark):
            logger.info("✓ 静态代理Hosting套餐+支付流程成功完成")
        else:
            logger.error("❌ 静态代理Hosting套餐+支付流程失败")
            raise Exception("静态代理Hosting套餐+支付流程失败")
        
        # 静态代理Hosting套餐+支付完成截图
        static_hosting_screenshot = customer_page.take_screenshot("stage5_static_hosting_package_payment_completed.png")
        logger.info(f"📸 静态代理Hosting套餐+支付完成截图: {static_hosting_screenshot}")
        
        # ========== 第九阶段：开静态代理ISP套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🌐 第九阶段：开静态代理ISP套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤9.1: 开始开静态代理ISP套餐+支付流程...")
        static_isp_remark = "IPIPGO 静态代理ISP套餐UI自动化测试"
        logger.info(f"📝 静态代理ISP套餐备注信息: {static_isp_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_static_isp_package_flow(static_isp_remark):
            logger.info("✓ 静态代理ISP套餐+支付流程成功完成")
        else:
            logger.error("❌ 静态代理ISP套餐+支付流程失败")
            raise Exception("静态代理ISP套餐+支付流程失败")
        
        # 静态代理ISP套餐+支付完成截图
        static_isp_screenshot = customer_page.take_screenshot("stage6_static_isp_package_payment_completed.png")
        logger.info(f"📸 静态代理ISP套餐+支付完成截图: {static_isp_screenshot}")
        
        # ========== 第十阶段：开静态代理双ISP套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🌐 第十阶段：开静态代理双ISP套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤10.1: 开始开静态代理双ISP套餐+支付流程...")
        static_dual_isp_remark = "IPIPGO 静态代理双ISP套餐UI自动化测试"
        logger.info(f"📝 静态代理双ISP套餐备注信息: {static_dual_isp_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_static_dual_isp_package_flow(static_dual_isp_remark):
            logger.info("✓ 静态代理双ISP套餐+支付流程成功完成")
        else:
            logger.error("❌ 静态代理双ISP套餐+支付流程失败")
            raise Exception("静态代理双ISP套餐+支付流程失败")
        
        # 静态代理双ISP套餐+支付完成截图
        static_dual_isp_screenshot = customer_page.take_screenshot("stage7_static_dual_isp_package_payment_completed.png")
        logger.info(f"📸 静态代理双ISP套餐+支付完成截图: {static_dual_isp_screenshot}")
        
        # ========== 独享静态套餐系列 ==========
        logger.info("\n" + "🎯"*60)
        logger.info("🎯 开始独享静态套餐系列测试（2种套餐）")
        logger.info("🎯"*60)
        
        # ========== 第十一阶段：开独享静态套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🎯 第十一阶段：开独享静态套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤11.1: 开始开独享静态套餐+支付流程...")
        exclusive_static_remark = "IPIPGO 独享静态套餐UI自动化测试"
        logger.info(f"📝 独享静态套餐备注信息: {exclusive_static_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_exclusive_static_package_flow(exclusive_static_remark):
            logger.info("✓ 独享静态套餐+支付流程成功完成")
        else:
            logger.error("❌ 独享静态套餐+支付流程失败")
            raise Exception("独享静态套餐+支付流程失败")
        
        # 独享静态套餐+支付完成截图
        exclusive_static_screenshot = customer_page.take_screenshot("stage8_exclusive_static_package_payment_completed.png")
        logger.info(f"📸 独享静态套餐+支付完成截图: {exclusive_static_screenshot}")
        
        # ========== 第十二阶段：开独享静态TikTok解决方案套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🎵 第十二阶段：开独享静态TikTok解决方案套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤12.1: 开始开独享静态TikTok解决方案套餐+支付流程...")
        tiktok_remark = "IPIPGO 独享静态TikTok解决方案套餐UI自动化测试"
        logger.info(f"📝 独享静态TikTok解决方案套餐备注信息: {tiktok_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_exclusive_static_tiktok_package_flow(tiktok_remark):
            logger.info("✓ 独享静态TikTok解决方案套餐+支付流程成功完成")
        else:
            logger.error("❌ 独享静态TikTok解决方案套餐+支付流程失败")
            raise Exception("独享静态TikTok解决方案套餐+支付流程失败")
        
        # 独享静态TikTok解决方案套餐+支付完成截图
        tiktok_screenshot = customer_page.take_screenshot("stage9_exclusive_static_tiktok_package_payment_completed.png")
        logger.info(f"📸 独享静态TikTok解决方案套餐+支付完成截图: {tiktok_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "🎉"*60)
        logger.info("🎉 IPIPGO管理后台完整自动化测试成功完成！")
        logger.info("🎉"*60)
        logger.info("📋 执行流程：打开管理后台 → 用户名密码登录 → 切换职位 → 客户查询 → 9种套餐购买+支付")
        logger.info("📊 套餐测试结果统计：")
        logger.info("   🔥 动态套餐系列（4种）：✅ 标准套餐 → ✅ 企业套餐 → ✅ 基础套餐 → ✅ 不限量套餐")
        logger.info("   🌐 静态代理系列（3种）：✅ Hosting套餐 → ✅ ISP套餐 → ✅ 双ISP套餐") 
        logger.info("   🎯 独享静态系列（2种）：✅ 独享静态套餐 → ✅ 独享静态TikTok解决方案套餐")
        logger.info("🏆 总计：9种套餐全部测试完成，每种套餐均包含完整的选择+支付流程！")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 管理后台自动化测试失败: {str(e)}")
        if driver:
            # 失败时截图
            try:
                admin_login_page = AdminLoginPage(driver)
                error_screenshot = admin_login_page.take_screenshot("admin_error_complete_flow.png")
                logger.info(f"📸 错误截图已保存: {error_screenshot}")
            except:
                pass
        raise
    
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO管理后台完整自动化测试结束")
        logger.info("="*60)


def test_enterprise_package_only():
    """单独测试企业套餐流程"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 开始IPIPGO企业套餐单独测试")
        logger.info("🔹 包含：管理后台登录 + 切换职位 + 客户查询 + 开企业套餐 + 支付")
        logger.info("="*60)
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        admin_login_page = AdminLoginPage(driver)
        customer_page = CustomerPage(driver)
        
        # 获取管理后台配置信息
        admin_config = config['admin_environment']
        login_url = admin_config['login_url']
        
        admin_login_data = config['test_data']['admin_login']
        username = admin_login_data['username']
        password = admin_login_data['password']
        target_position = admin_login_data.get('target_position', '秦仁驰')  # 从配置读取，默认为秦仁驰
        target_user_id = "7156"  # 要查询的用户ID
        
        logger.info(f"🌐 管理后台登录地址: {login_url}")
        logger.info(f"👤 管理员用户: {username}")
        logger.info(f"🔄 目标职位: {target_position}")
        
        # ========== 第一阶段：管理后台登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：管理后台登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开管理后台登录页面...")
        if admin_login_page.open_admin_login_page(login_url):
            logger.info("✓ 管理后台登录页面打开成功")
        else:
            logger.error("❌ 管理后台登录页面打开失败")
            raise Exception("管理后台登录页面打开失败")
        
        logger.info("步骤1.2: 开始管理后台登录流程...")
        if admin_login_page.admin_login(username, password):
            logger.info("✓ 管理后台登录成功")
        else:
            logger.error("❌ 管理后台登录失败")
            raise Exception("管理后台登录失败")
        
        # 登录完成截图
        login_screenshot = admin_login_page.take_screenshot("admin_login_completed.png")
        logger.info(f"📸 管理后台登录完成截图: {login_screenshot}")
        
        # ========== 第二阶段：切换职位流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔄 第二阶段：切换职位流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 开始切换职位流程...")
        if admin_login_page.switch_position(target_position):
            logger.info(f"✓ 职位切换成功，已切换到: {target_position}")
        else:
            logger.error("❌ 职位切换失败")
            raise Exception("职位切换失败")
        
        # 职位切换完成截图
        position_screenshot = admin_login_page.take_screenshot("admin_position_switched.png")
        logger.info(f"📸 职位切换完成截图: {position_screenshot}")
        
        # ========== 第三阶段：客户查询流程 ==========
        logger.info("\n" + "="*40)
        logger.info("👥 第三阶段：客户查询流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始客户查询流程...")
        logger.info(f"🔍 目标用户ID: {target_user_id}")
        
        if customer_page.navigate_to_customer_and_query(target_user_id):
            logger.info(f"✓ 客户查询流程成功完成，用户ID: {target_user_id}")
        else:
            logger.error("❌ 客户查询流程失败")
            raise Exception("客户查询流程失败")
        
        # 客户查询完成截图
        customer_screenshot = customer_page.take_screenshot("customer_query_completed.png")
        logger.info(f"📸 客户查询完成截图: {customer_screenshot}")
        
        # ========== 第四阶段：开企业套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🏢 第四阶段：开企业套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始开企业套餐+支付流程...")
        enterprise_remark = "IPIPGO 企业套餐UI自动化测试"
        logger.info(f"📝 企业套餐备注信息: {enterprise_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_enterprise_package_flow(enterprise_remark):
            logger.info("✓ 企业套餐+支付流程成功完成")
        else:
            logger.error("❌ 企业套餐+支付流程失败")
            raise Exception("企业套餐+支付流程失败")
        
        # 企业套餐+支付完成截图
        enterprise_screenshot = customer_page.take_screenshot("enterprise_package_payment_completed.png")
        logger.info(f"📸 企业套餐+支付完成截图: {enterprise_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "="*60)
        logger.info("🎉 IPIPGO企业套餐单独测试成功完成！")
        logger.info("📋 执行流程：打开管理后台 → 用户名密码登录 → 切换职位 → 客户查询 → 开企业套餐 → 支付")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 企业套餐测试失败: {e}")
        if driver:
            error_screenshot = customer_page.take_screenshot("admin_error_enterprise_test.png")
            logger.info(f"📸 错误截图已保存: {error_screenshot}")
        raise
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO企业套餐单独测试结束")
        logger.info("="*60)


def test_basic_package_only():
    """单独测试基础套餐流程"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 开始IPIPGO基础套餐单独测试")
        logger.info("🔹 包含：管理后台登录 + 切换职位 + 客户查询 + 开基础套餐 + 支付")
        logger.info("="*60)
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        admin_login_page = AdminLoginPage(driver)
        customer_page = CustomerPage(driver)
        
        # 获取管理后台配置信息
        admin_config = config['admin_environment']
        login_url = admin_config['login_url']
        
        admin_login_data = config['test_data']['admin_login']
        username = admin_login_data['username']
        password = admin_login_data['password']
        target_position = admin_login_data.get('target_position', '秦仁驰')  # 从配置读取，默认为秦仁驰
        target_user_id = "7156"  # 要查询的用户ID
        
        logger.info(f"🌐 管理后台登录地址: {login_url}")
        logger.info(f"👤 管理员用户: {username}")
        logger.info(f"🔄 目标职位: {target_position}")
        
        # ========== 第一阶段：管理后台登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：管理后台登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开管理后台登录页面...")
        if admin_login_page.open_admin_login_page(login_url):
            logger.info("✓ 管理后台登录页面打开成功")
        else:
            logger.error("❌ 管理后台登录页面打开失败")
            raise Exception("管理后台登录页面打开失败")
        
        logger.info("步骤1.2: 开始管理后台登录流程...")
        if admin_login_page.admin_login(username, password):
            logger.info("✓ 管理后台登录成功")
        else:
            logger.error("❌ 管理后台登录失败")
            raise Exception("管理后台登录失败")
        
        # 登录完成截图
        login_screenshot = admin_login_page.take_screenshot("admin_login_completed.png")
        logger.info(f"📸 管理后台登录完成截图: {login_screenshot}")
        
        # ========== 第二阶段：切换职位流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔄 第二阶段：切换职位流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 开始切换职位流程...")
        if admin_login_page.switch_position(target_position):
            logger.info(f"✓ 职位切换成功，已切换到: {target_position}")
        else:
            logger.error("❌ 职位切换失败")
            raise Exception("职位切换失败")
        
        # 职位切换完成截图
        position_screenshot = admin_login_page.take_screenshot("admin_position_switched.png")
        logger.info(f"📸 职位切换完成截图: {position_screenshot}")
        
        # ========== 第三阶段：客户查询流程 ==========
        logger.info("\n" + "="*40)
        logger.info("👥 第三阶段：客户查询流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始客户查询流程...")
        logger.info(f"🔍 目标用户ID: {target_user_id}")
        
        if customer_page.navigate_to_customer_and_query(target_user_id):
            logger.info(f"✓ 客户查询流程成功完成，用户ID: {target_user_id}")
        else:
            logger.error("❌ 客户查询流程失败")
            raise Exception("客户查询流程失败")
        
        # 客户查询完成截图
        customer_screenshot = customer_page.take_screenshot("customer_query_completed.png")
        logger.info(f"📸 客户查询完成截图: {customer_screenshot}")
        
        # ========== 第四阶段：开基础套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔧 第四阶段：开基础套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始开基础套餐+支付流程...")
        basic_remark = "IPIPGO 基础套餐UI自动化测试"
        logger.info(f"📝 基础套餐备注信息: {basic_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_basic_package_flow(basic_remark):
            logger.info("✓ 基础套餐+支付流程成功完成")
        else:
            logger.error("❌ 基础套餐+支付流程失败")
            raise Exception("基础套餐+支付流程失败")
        
        # 基础套餐+支付完成截图
        basic_screenshot = customer_page.take_screenshot("basic_package_payment_completed.png")
        logger.info(f"📸 基础套餐+支付完成截图: {basic_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "="*60)
        logger.info("🎉 IPIPGO基础套餐单独测试成功完成！")
        logger.info("📋 执行流程：打开管理后台 → 用户名密码登录 → 切换职位 → 客户查询 → 开基础套餐 → 支付")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 基础套餐测试失败: {e}")
        if driver:
            error_screenshot = customer_page.take_screenshot("admin_error_basic_test.png")
            logger.info(f"📸 错误截图已保存: {error_screenshot}")
        raise
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO基础套餐单独测试结束")
        logger.info("="*60)


def test_unlimited_package_only():
    """单独测试不限量套餐流程"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 开始IPIPGO不限量套餐单独测试")
        logger.info("🔹 包含：管理后台登录 + 切换职位 + 客户查询 + 开不限量套餐 + 支付")
        logger.info("="*60)
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        admin_login_page = AdminLoginPage(driver)
        customer_page = CustomerPage(driver)
        
        # 获取管理后台配置信息
        admin_config = config['admin_environment']
        login_url = admin_config['login_url']
        
        admin_login_data = config['test_data']['admin_login']
        username = admin_login_data['username']
        password = admin_login_data['password']
        target_position = admin_login_data.get('target_position', '秦仁驰')  # 从配置读取，默认为秦仁驰
        target_user_id = "7156"  # 要查询的用户ID
        
        logger.info(f"🌐 管理后台登录地址: {login_url}")
        logger.info(f"👤 管理员用户: {username}")
        logger.info(f"🔄 目标职位: {target_position}")
        
        # ========== 第一阶段：管理后台登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：管理后台登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开管理后台登录页面...")
        if admin_login_page.open_admin_login_page(login_url):
            logger.info("✓ 管理后台登录页面打开成功")
        else:
            logger.error("❌ 管理后台登录页面打开失败")
            raise Exception("管理后台登录页面打开失败")
        
        logger.info("步骤1.2: 开始管理后台登录流程...")
        if admin_login_page.admin_login(username, password):
            logger.info("✓ 管理后台登录成功")
        else:
            logger.error("❌ 管理后台登录失败")
            raise Exception("管理后台登录失败")
        
        # 登录完成截图
        login_screenshot = admin_login_page.take_screenshot("admin_login_completed.png")
        logger.info(f"📸 管理后台登录完成截图: {login_screenshot}")
        
        # ========== 第二阶段：切换职位流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔄 第二阶段：切换职位流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 开始切换职位流程...")
        if admin_login_page.switch_position(target_position):
            logger.info(f"✓ 职位切换成功，已切换到: {target_position}")
        else:
            logger.error("❌ 职位切换失败")
            raise Exception("职位切换失败")
        
        # 职位切换完成截图
        position_screenshot = admin_login_page.take_screenshot("admin_position_switched.png")
        logger.info(f"📸 职位切换完成截图: {position_screenshot}")
        
        # ========== 第三阶段：客户查询流程 ==========
        logger.info("\n" + "="*40)
        logger.info("👥 第三阶段：客户查询流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始客户查询流程...")
        logger.info(f"🔍 目标用户ID: {target_user_id}")
        
        if customer_page.navigate_to_customer_and_query(target_user_id):
            logger.info(f"✓ 客户查询流程成功完成，用户ID: {target_user_id}")
        else:
            logger.error("❌ 客户查询流程失败")
            raise Exception("客户查询流程失败")
        
        # 客户查询完成截图
        customer_screenshot = customer_page.take_screenshot("customer_query_completed.png")
        logger.info(f"📸 客户查询完成截图: {customer_screenshot}")
        
        # ========== 第四阶段：开不限量套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🚀 第四阶段：开不限量套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始开不限量套餐+支付流程...")
        unlimited_remark = "IPIPGO 不限量套餐UI自动化测试"
        logger.info(f"📝 不限量套餐备注信息: {unlimited_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_unlimited_package_flow(unlimited_remark):
            logger.info("✓ 不限量套餐+支付流程成功完成")
        else:
            logger.error("❌ 不限量套餐+支付流程失败")
            raise Exception("不限量套餐+支付流程失败")
        
        # 不限量套餐+支付完成截图
        unlimited_screenshot = customer_page.take_screenshot("unlimited_package_payment_completed.png")
        logger.info(f"📸 不限量套餐+支付完成截图: {unlimited_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "="*60)
        logger.info("🎉 IPIPGO不限量套餐单独测试成功完成！")
        logger.info("📋 执行流程：打开管理后台 → 用户名密码登录 → 切换职位 → 客户查询 → 开不限量套餐 → 支付")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 不限量套餐测试失败: {e}")
        if driver:
            error_screenshot = customer_page.take_screenshot("admin_error_unlimited_test.png")
            logger.info(f"📸 错误截图已保存: {error_screenshot}")
        raise
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO不限量套餐单独测试结束")
        logger.info("="*60)


def test_static_package_only():
    """单独测试静态代理套餐流程"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 开始IPIPGO静态代理套餐单独测试")
        logger.info("🔹 包含：管理后台登录 + 切换职位 + 客户查询 + 开静态代理套餐 + 支付")
        logger.info("="*60)
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        admin_login_page = AdminLoginPage(driver)
        customer_page = CustomerPage(driver)
        
        # 获取管理后台配置信息
        admin_config = config['admin_environment']
        login_url = admin_config['login_url']
        
        admin_login_data = config['test_data']['admin_login']
        username = admin_login_data['username']
        password = admin_login_data['password']
        target_position = admin_login_data.get('target_position', '秦仁驰')  # 从配置读取，默认为秦仁驰
        target_user_id = "7156"  # 要查询的用户ID
        
        logger.info(f"🌐 管理后台登录地址: {login_url}")
        logger.info(f"👤 管理员用户: {username}")
        logger.info(f"🔄 目标职位: {target_position}")
        
        # ========== 第一阶段：管理后台登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：管理后台登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开管理后台登录页面...")
        if admin_login_page.open_admin_login_page(login_url):
            logger.info("✓ 管理后台登录页面打开成功")
        else:
            logger.error("❌ 管理后台登录页面打开失败")
            raise Exception("管理后台登录页面打开失败")
        
        logger.info("步骤1.2: 开始管理后台登录流程...")
        if admin_login_page.admin_login(username, password):
            logger.info("✓ 管理后台登录成功")
        else:
            logger.error("❌ 管理后台登录失败")
            raise Exception("管理后台登录失败")
        
        # 登录完成截图
        login_screenshot = admin_login_page.take_screenshot("admin_login_completed.png")
        logger.info(f"📸 管理后台登录完成截图: {login_screenshot}")
        
        # ========== 第二阶段：切换职位流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔄 第二阶段：切换职位流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 开始切换职位流程...")
        if admin_login_page.switch_position(target_position):
            logger.info(f"✓ 职位切换成功，已切换到: {target_position}")
        else:
            logger.error("❌ 职位切换失败")
            raise Exception("职位切换失败")
        
        # 职位切换完成截图
        position_screenshot = admin_login_page.take_screenshot("admin_position_switched.png")
        logger.info(f"📸 职位切换完成截图: {position_screenshot}")
        
        # ========== 第三阶段：客户查询流程 ==========
        logger.info("\n" + "="*40)
        logger.info("👥 第三阶段：客户查询流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始客户查询流程...")
        logger.info(f"🔍 目标用户ID: {target_user_id}")
        
        if customer_page.navigate_to_customer_and_query(target_user_id):
            logger.info(f"✓ 客户查询流程成功完成，用户ID: {target_user_id}")
        else:
            logger.error("❌ 客户查询流程失败")
            raise Exception("客户查询流程失败")
        
        # 客户查询完成截图
        customer_screenshot = customer_page.take_screenshot("customer_query_completed.png")
        logger.info(f"📸 客户查询完成截图: {customer_screenshot}")
        
        # ========== 第四阶段：开静态代理套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🚀 第四阶段：开静态代理套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始开静态代理套餐+支付流程...")
        static_remark = "IPIPGO 静态代理套餐UI自动化测试"
        logger.info(f"📝 静态代理套餐备注信息: {static_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_static_package_flow(static_remark):
            logger.info("✓ 静态代理套餐+支付流程成功完成")
        else:
            logger.error("❌ 静态代理套餐+支付流程失败")
            raise Exception("静态代理套餐+支付流程失败")
        
        # 静态代理套餐+支付完成截图
        static_screenshot = customer_page.take_screenshot("static_package_payment_completed.png")
        logger.info(f"📸 静态代理套餐+支付完成截图: {static_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "="*60)
        logger.info("🎉 IPIPGO静态代理套餐单独测试成功完成！")
        logger.info("📋 执行流程：打开管理后台 → 用户名密码登录 → 切换职位 → 客户查询 → 开静态代理套餐 → 支付")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 静态代理套餐测试失败: {e}")
        if driver:
            error_screenshot = customer_page.take_screenshot("admin_error_static_test.png")
            logger.info(f"📸 错误截图已保存: {error_screenshot}")
        raise
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO静态代理套餐单独测试结束")
        logger.info("="*60)


def test_static_isp_package_only():
    """单独测试静态代理ISP套餐流程"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 开始IPIPGO静态代理ISP套餐单独测试")
        logger.info("🔹 包含：管理后台登录 + 切换职位 + 客户查询 + 开静态代理ISP套餐 + 支付")
        logger.info("="*60)
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        admin_login_page = AdminLoginPage(driver)
        customer_page = CustomerPage(driver)
        
        # 获取管理后台配置信息
        admin_config = config['admin_environment']
        login_url = admin_config['login_url']
        
        admin_login_data = config['test_data']['admin_login']
        username = admin_login_data['username']
        password = admin_login_data['password']
        target_position = admin_login_data.get('target_position', '秦仁驰')  # 从配置读取，默认为秦仁驰
        target_user_id = "7156"  # 要查询的用户ID
        
        logger.info(f"🌐 管理后台登录地址: {login_url}")
        logger.info(f"👤 管理员用户: {username}")
        logger.info(f"🔄 目标职位: {target_position}")
        
        # ========== 第一阶段：管理后台登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：管理后台登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开管理后台登录页面...")
        if admin_login_page.open_admin_login_page(login_url):
            logger.info("✓ 管理后台登录页面打开成功")
        else:
            logger.error("❌ 管理后台登录页面打开失败")
            raise Exception("管理后台登录页面打开失败")
        
        logger.info("步骤1.2: 开始管理后台登录流程...")
        if admin_login_page.admin_login(username, password):
            logger.info("✓ 管理后台登录成功")
        else:
            logger.error("❌ 管理后台登录失败")
            raise Exception("管理后台登录失败")
        
        # 登录完成截图
        login_screenshot = admin_login_page.take_screenshot("admin_login_completed.png")
        logger.info(f"📸 管理后台登录完成截图: {login_screenshot}")
        
        # ========== 第二阶段：切换职位流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔄 第二阶段：切换职位流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 开始切换职位流程...")
        if admin_login_page.switch_position(target_position):
            logger.info(f"✓ 职位切换成功，已切换到: {target_position}")
        else:
            logger.error("❌ 职位切换失败")
            raise Exception("职位切换失败")
        
        # 职位切换完成截图
        position_screenshot = admin_login_page.take_screenshot("admin_position_switched.png")
        logger.info(f"📸 职位切换完成截图: {position_screenshot}")
        
        # ========== 第三阶段：客户查询流程 ==========
        logger.info("\n" + "="*40)
        logger.info("👥 第三阶段：客户查询流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始客户查询流程...")
        logger.info(f"🔍 目标用户ID: {target_user_id}")
        
        if customer_page.navigate_to_customer_and_query(target_user_id):
            logger.info(f"✓ 客户查询流程成功完成，用户ID: {target_user_id}")
        else:
            logger.error("❌ 客户查询流程失败")
            raise Exception("客户查询流程失败")
        
        # 客户查询完成截图
        customer_screenshot = customer_page.take_screenshot("customer_query_completed.png")
        logger.info(f"📸 客户查询完成截图: {customer_screenshot}")
        
        # ========== 第四阶段：开静态代理ISP套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🚀 第四阶段：开静态代理ISP套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始开静态代理ISP套餐+支付流程...")
        static_isp_remark = "IPIPGO 静态代理ISP套餐UI自动化测试"
        logger.info(f"📝 静态代理ISP套餐备注信息: {static_isp_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_static_isp_package_flow(static_isp_remark):
            logger.info("✓ 静态代理ISP套餐+支付流程成功完成")
        else:
            logger.error("❌ 静态代理ISP套餐+支付流程失败")
            raise Exception("静态代理ISP套餐+支付流程失败")
        
        # 静态代理ISP套餐+支付完成截图
        static_isp_screenshot = customer_page.take_screenshot("static_isp_package_payment_completed.png")
        logger.info(f"📸 静态代理ISP套餐+支付完成截图: {static_isp_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "="*60)
        logger.info("🎉 IPIPGO静态代理ISP套餐单独测试成功完成！")
        logger.info("📋 执行流程：打开管理后台 → 用户名密码登录 → 切换职位 → 客户查询 → 开静态代理ISP套餐 → 支付")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 静态代理ISP套餐测试失败: {e}")
        if driver:
            error_screenshot = customer_page.take_screenshot("admin_error_static_isp_test.png")
            logger.info(f"📸 错误截图已保存: {error_screenshot}")
        raise
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO静态代理ISP套餐单独测试结束")
        logger.info("="*60)


def test_static_dual_isp_package_only():
    """单独测试静态代理双ISP套餐流程"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 开始IPIPGO静态代理双ISP套餐单独测试")
        logger.info("🔹 包含：管理后台登录 + 切换职位 + 客户查询 + 开静态代理双ISP套餐 + 支付")
        logger.info("="*60)
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        admin_login_page = AdminLoginPage(driver)
        customer_page = CustomerPage(driver)
        
        # 获取管理后台配置信息
        admin_config = config['admin_environment']
        login_url = admin_config['login_url']
        
        admin_login_data = config['test_data']['admin_login']
        username = admin_login_data['username']
        password = admin_login_data['password']
        target_position = admin_login_data.get('target_position', '秦仁驰')  # 从配置读取，默认为秦仁驰
        target_user_id = "7156"  # 要查询的用户ID
        
        logger.info(f"🌐 管理后台登录地址: {login_url}")
        logger.info(f"👤 管理员用户: {username}")
        logger.info(f"🔄 目标职位: {target_position}")
        
        # ========== 第一阶段：管理后台登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：管理后台登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开管理后台登录页面...")
        if admin_login_page.open_admin_login_page(login_url):
            logger.info("✓ 管理后台登录页面打开成功")
        else:
            logger.error("❌ 管理后台登录页面打开失败")
            raise Exception("管理后台登录页面打开失败")
        
        logger.info("步骤1.2: 开始管理后台登录流程...")
        if admin_login_page.admin_login(username, password):
            logger.info("✓ 管理后台登录成功")
        else:
            logger.error("❌ 管理后台登录失败")
            raise Exception("管理后台登录失败")
        
        # 登录完成截图
        login_screenshot = admin_login_page.take_screenshot("admin_login_completed.png")
        logger.info(f"📸 管理后台登录完成截图: {login_screenshot}")
        
        # ========== 第二阶段：切换职位流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔄 第二阶段：切换职位流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 开始切换职位流程...")
        if admin_login_page.switch_position(target_position):
            logger.info(f"✓ 职位切换成功，已切换到: {target_position}")
        else:
            logger.error("❌ 职位切换失败")
            raise Exception("职位切换失败")
        
        # 职位切换完成截图
        position_screenshot = admin_login_page.take_screenshot("admin_position_switched.png")
        logger.info(f"📸 职位切换完成截图: {position_screenshot}")
        
        # ========== 第三阶段：客户查询流程 ==========
        logger.info("\n" + "="*40)
        logger.info("👥 第三阶段：客户查询流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始客户查询流程...")
        logger.info(f"🔍 目标用户ID: {target_user_id}")
        
        if customer_page.navigate_to_customer_and_query(target_user_id):
            logger.info(f"✓ 客户查询流程成功完成，用户ID: {target_user_id}")
        else:
            logger.error("❌ 客户查询流程失败")
            raise Exception("客户查询流程失败")
        
        # 客户查询完成截图
        customer_screenshot = customer_page.take_screenshot("customer_query_completed.png")
        logger.info(f"📸 客户查询完成截图: {customer_screenshot}")
        
        # ========== 第四阶段：开静态代理双ISP套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🚀 第四阶段：开静态代理双ISP套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始开静态代理双ISP套餐+支付流程...")
        static_dual_isp_remark = "IPIPGO 静态代理双ISP套餐UI自动化测试"
        logger.info(f"📝 静态代理双ISP套餐备注信息: {static_dual_isp_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_static_dual_isp_package_flow(static_dual_isp_remark):
            logger.info("✓ 静态代理双ISP套餐+支付流程成功完成")
        else:
            logger.error("❌ 静态代理双ISP套餐+支付流程失败")
            raise Exception("静态代理双ISP套餐+支付流程失败")
        
        # 静态代理双ISP套餐+支付完成截图
        static_dual_isp_screenshot = customer_page.take_screenshot("static_dual_isp_package_payment_completed.png")
        logger.info(f"📸 静态代理双ISP套餐+支付完成截图: {static_dual_isp_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "="*60)
        logger.info("🎉 IPIPGO静态代理双ISP套餐单独测试成功完成！")
        logger.info("📋 执行流程：打开管理后台 → 用户名密码登录 → 切换职位 → 客户查询 → 开静态代理双ISP套餐 → 支付")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 静态代理双ISP套餐测试失败: {e}")
        if driver:
            error_screenshot = customer_page.take_screenshot("admin_error_static_dual_isp_test.png")
            logger.info(f"📸 错误截图已保存: {error_screenshot}")
        raise
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO静态代理双ISP套餐单独测试结束")
        logger.info("="*60)


def test_exclusive_static_tiktok_package_only():
    """单独测试独享静态TikTok解决方案套餐流程"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 开始IPIPGO独享静态TikTok解决方案套餐单独测试")
        logger.info("🔹 包含：管理后台登录 + 切换职位 + 客户查询 + 开独享静态TikTok解决方案套餐 + 支付")
        logger.info("="*60)
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        admin_login_page = AdminLoginPage(driver)
        customer_page = CustomerPage(driver)
        
        # 获取管理后台配置信息
        admin_config = config['admin_environment']
        login_url = admin_config['login_url']
        
        admin_login_data = config['test_data']['admin_login']
        username = admin_login_data['username']
        password = admin_login_data['password']
        target_position = admin_login_data.get('target_position', '秦仁驰')  # 从配置读取，默认为秦仁驰
        target_user_id = "7156"  # 要查询的用户ID
        
        logger.info(f"🌐 管理后台登录地址: {login_url}")
        logger.info(f"👤 管理员用户: {username}")
        logger.info(f"🔄 目标职位: {target_position}")
        
        # ========== 第一阶段：管理后台登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：管理后台登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开管理后台登录页面...")
        if admin_login_page.open_admin_login_page(login_url):
            logger.info("✓ 管理后台登录页面打开成功")
        else:
            logger.error("❌ 管理后台登录页面打开失败")
            raise Exception("管理后台登录页面打开失败")
        
        logger.info("步骤1.2: 开始管理后台登录流程...")
        if admin_login_page.admin_login(username, password):
            logger.info("✓ 管理后台登录成功")
        else:
            logger.error("❌ 管理后台登录失败")
            raise Exception("管理后台登录失败")
        
        # 登录完成截图
        login_screenshot = admin_login_page.take_screenshot("admin_login_completed.png")
        logger.info(f"📸 管理后台登录完成截图: {login_screenshot}")
        
        # ========== 第二阶段：切换职位流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔄 第二阶段：切换职位流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 开始切换职位流程...")
        if admin_login_page.switch_position(target_position):
            logger.info(f"✓ 职位切换成功，已切换到: {target_position}")
        else:
            logger.error("❌ 职位切换失败")
            raise Exception("职位切换失败")
        
        # 职位切换完成截图
        position_screenshot = admin_login_page.take_screenshot("admin_position_switched.png")
        logger.info(f"📸 职位切换完成截图: {position_screenshot}")
        
        # ========== 第三阶段：客户查询流程 ==========
        logger.info("\n" + "="*40)
        logger.info("👥 第三阶段：客户查询流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始客户查询流程...")
        logger.info(f"🔍 目标用户ID: {target_user_id}")
        
        if customer_page.navigate_to_customer_and_query(target_user_id):
            logger.info(f"✓ 客户查询流程成功完成，用户ID: {target_user_id}")
        else:
            logger.error("❌ 客户查询流程失败")
            raise Exception("客户查询流程失败")
        
        # 客户查询完成截图
        customer_screenshot = customer_page.take_screenshot("customer_query_completed.png")
        logger.info(f"📸 客户查询完成截图: {customer_screenshot}")
        
        # ========== 第四阶段：开独享静态TikTok解决方案套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🚀 第四阶段：开独享静态TikTok解决方案套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始开独享静态TikTok解决方案套餐+支付流程...")
        tiktok_remark = "IPIPGO 独享静态TikTok解决方案套餐UI自动化测试"
        logger.info(f"📝 独享静态TikTok解决方案套餐备注信息: {tiktok_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_exclusive_static_tiktok_package_flow(tiktok_remark):
            logger.info("✓ 独享静态TikTok解决方案套餐+支付流程成功完成")
        else:
            logger.error("❌ 独享静态TikTok解决方案套餐+支付流程失败")
            raise Exception("独享静态TikTok解决方案套餐+支付流程失败")
        
        # 独享静态TikTok解决方案套餐+支付完成截图
        tiktok_screenshot = customer_page.take_screenshot("exclusive_static_tiktok_package_payment_completed.png")
        logger.info(f"📸 独享静态TikTok解决方案套餐+支付完成截图: {tiktok_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "="*60)
        logger.info("🎉 IPIPGO独享静态TikTok解决方案套餐单独测试成功完成！")
        logger.info("📋 执行流程：打开管理后台 → 用户名密码登录 → 切换职位 → 客户查询 → 开独享静态TikTok解决方案套餐 → 支付")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 独享静态TikTok解决方案套餐测试失败: {e}")
        if driver:
            error_screenshot = customer_page.take_screenshot("admin_error_exclusive_static_tiktok_test.png")
            logger.info(f"📸 错误截图已保存: {error_screenshot}")
        raise
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO独享静态TikTok解决方案套餐单独测试结束")
        logger.info("="*60)


def test_exclusive_static_package_only():
    """单独测试独享静态套餐流程（IP类型为独享静态）"""
    logger = Logger(__name__)
    driver_manager = None
    driver = None
    
    try:
        logger.info("="*60)
        logger.info("🧪 开始IPIPGO独享静态套餐单独测试")
        logger.info("🔹 包含：管理后台登录 + 切换职位 + 客户查询 + 开独享静态套餐 + 支付")
        logger.info("="*60)
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 初始化驱动管理器
        driver_manager = DriverManager()
        driver = driver_manager.get_driver('edge')
        logger.info("✓ 成功启动Edge浏览器")
        
        # 初始化页面对象
        admin_login_page = AdminLoginPage(driver)
        customer_page = CustomerPage(driver)
        
        # 获取管理后台配置信息
        admin_config = config['admin_environment']
        login_url = admin_config['login_url']
        
        admin_login_data = config['test_data']['admin_login']
        username = admin_login_data['username']
        password = admin_login_data['password']
        target_position = admin_login_data.get('target_position', '秦仁驰')  # 从配置读取，默认为秦仁驰
        target_user_id = "7156"  # 要查询的用户ID
        
        logger.info(f"🌐 管理后台登录地址: {login_url}")
        logger.info(f"👤 管理员用户: {username}")
        logger.info(f"🔄 目标职位: {target_position}")
        
        # ========== 第一阶段：管理后台登录流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔐 第一阶段：管理后台登录流程")
        logger.info("="*40)
        
        logger.info("步骤1.1: 打开管理后台登录页面...")
        if admin_login_page.open_admin_login_page(login_url):
            logger.info("✓ 管理后台登录页面打开成功")
        else:
            logger.error("❌ 管理后台登录页面打开失败")
            raise Exception("管理后台登录页面打开失败")
        
        logger.info("步骤1.2: 开始管理后台登录流程...")
        if admin_login_page.admin_login(username, password):
            logger.info("✓ 管理后台登录成功")
        else:
            logger.error("❌ 管理后台登录失败")
            raise Exception("管理后台登录失败")
        
        # 登录完成截图
        login_screenshot = admin_login_page.take_screenshot("admin_login_completed.png")
        logger.info(f"📸 管理后台登录完成截图: {login_screenshot}")
        
        # ========== 第二阶段：切换职位流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🔄 第二阶段：切换职位流程")
        logger.info("="*40)
        
        logger.info("步骤2.1: 开始切换职位流程...")
        if admin_login_page.switch_position(target_position):
            logger.info(f"✓ 职位切换成功，已切换到: {target_position}")
        else:
            logger.error("❌ 职位切换失败")
            raise Exception("职位切换失败")
        
        # 职位切换完成截图
        position_screenshot = admin_login_page.take_screenshot("admin_position_switched.png")
        logger.info(f"📸 职位切换完成截图: {position_screenshot}")
        
        # ========== 第三阶段：客户查询流程 ==========
        logger.info("\n" + "="*40)
        logger.info("👥 第三阶段：客户查询流程")
        logger.info("="*40)
        
        logger.info("步骤3.1: 开始客户查询流程...")
        logger.info(f"🔍 目标用户ID: {target_user_id}")
        
        if customer_page.navigate_to_customer_and_query(target_user_id):
            logger.info(f"✓ 客户查询流程成功完成，用户ID: {target_user_id}")
        else:
            logger.error("❌ 客户查询流程失败")
            raise Exception("客户查询流程失败")
        
        # 客户查询完成截图
        customer_screenshot = customer_page.take_screenshot("customer_query_completed.png")
        logger.info(f"📸 客户查询完成截图: {customer_screenshot}")
        
        # ========== 第四阶段：开独享静态套餐+支付流程 ==========
        logger.info("\n" + "="*40)
        logger.info("🚀 第四阶段：开独享静态套餐+支付流程")
        logger.info("="*40)
        
        logger.info("步骤4.1: 开始开独享静态套餐+支付流程...")
        exclusive_static_remark = "IPIPGO 独享静态套餐UI自动化测试"
        logger.info(f"📝 独享静态套餐备注信息: {exclusive_static_remark}")
        
        # 等待页面状态稳定
        logger.info("等待3秒让页面状态稳定...")
        time.sleep(3)
        
        if customer_page.open_exclusive_static_package_flow(exclusive_static_remark):
            logger.info("✓ 独享静态套餐+支付流程成功完成")
        else:
            logger.error("❌ 独享静态套餐+支付流程失败")
            raise Exception("独享静态套餐+支付流程失败")
        
        # 独享静态套餐+支付完成截图
        exclusive_static_screenshot = customer_page.take_screenshot("exclusive_static_package_payment_completed.png")
        logger.info(f"📸 独享静态套餐+支付完成截图: {exclusive_static_screenshot}")
        
        # 等待一段时间以便观察结果
        logger.info("等待5秒以便观察最终结果...")
        time.sleep(5)
        
        logger.info("\n" + "="*60)
        logger.info("🎉 IPIPGO独享静态套餐单独测试成功完成！")
        logger.info("📋 执行流程：打开管理后台 → 用户名密码登录 → 切换职位 → 客户查询 → 开独享静态套餐 → 支付")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ 独享静态套餐测试失败: {e}")
        if driver:
            error_screenshot = customer_page.take_screenshot("admin_error_exclusive_static_test.png")
            logger.info(f"📸 错误截图已保存: {error_screenshot}")
        raise
    finally:
        # 清理资源
        if driver_manager:
            # 读取配置决定是否关闭浏览器
            try:
                should_close = config.get('browser', {}).get('close_after_test', True)
            except:
                should_close = True  # 默认关闭
            
            if should_close:
                logger.info("正在关闭浏览器...")
                driver_manager.quit_driver()
                logger.info("✓ 浏览器已关闭")
            else:
                logger.info("🌐 根据配置，浏览器将保持打开状态")
                logger.info("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
        
        logger.info("="*60)
        logger.info("🏁 IPIPGO独享静态套餐单独测试结束")
        logger.info("="*60)


if __name__ == "__main__":
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--enterprise-only":
            test_enterprise_package_only()
        elif sys.argv[1] == "--basic-only":
            test_basic_package_only()
        elif sys.argv[1] == "--unlimited-only":
            test_unlimited_package_only()
        elif sys.argv[1] == "--static-only":
            test_static_package_only()
        elif sys.argv[1] == "--static-isp-only":
            test_static_isp_package_only()
        elif sys.argv[1] == "--static-dual-isp-only":
            test_static_dual_isp_package_only()
        elif sys.argv[1] == "--exclusive-static-tiktok-only":
            test_exclusive_static_tiktok_package_only()
        elif sys.argv[1] == "--exclusive-static-only":
            test_exclusive_static_package_only()
        else:
            print("❌ 未知参数，可用参数：")
            print("   --enterprise-only  (企业套餐单独测试)")
            print("   --basic-only       (基础套餐单独测试)")
            print("   --unlimited-only   (不限量套餐单独测试)")
            print("   --static-only      (静态代理套餐单独测试)")
            print("   --static-isp-only  (静态代理ISP套餐单独测试)")
            print("   --static-dual-isp-only (静态代理双ISP套餐单独测试)")
            print("   --exclusive-static-tiktok-only (独享静态TikTok解决方案套餐单独测试)")
            print("   --exclusive-static-only (独享静态套餐单独测试)")
            print("   无参数             (完整流程测试)")
    else:
        main() 