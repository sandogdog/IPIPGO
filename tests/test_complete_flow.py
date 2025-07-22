"""
IPIPGO完整流程自动化测试
包含登录和购买流程
"""

import pytest
import yaml
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.purchase_page import PurchasePage
from utils.logger import Logger


class TestCompleteFlow:
    """完整流程测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类初始化"""
        cls.driver_manager = DriverManager()
        cls.driver = cls.driver_manager.get_driver('edge')
        cls.login_page = LoginPage(cls.driver)
        cls.purchase_page = PurchasePage(cls.driver)
        cls.logger = Logger(__name__)
        
        # 读取配置
        with open('config/config.yaml', 'r', encoding='utf-8') as file:
            cls.config = yaml.safe_load(file)
    
    @classmethod
    def teardown_class(cls):
        """测试类清理"""
        if cls.driver:
            cls.driver_manager.quit_driver()
    
    def test_complete_login_and_purchase_flow(self):
        """测试完整的登录和购买流程"""
        try:
            # 获取配置信息
            base_url = self.config['environment']['base_url']
            username = self.config['test_data']['login']['username']
            password = self.config['test_data']['login']['password']
            
            self.logger.info("="*60)
            self.logger.info("开始IPIPGO完整流程测试（登录 + 购买）")
            self.logger.info("="*60)
            
            # ========== 第一阶段：登录流程 ==========
            self.logger.info("🔐 第一阶段：执行登录流程")
            
            # 1. 打开网站
            self.login_page.open_homepage(base_url)
            self.logger.info(f"✓ 成功打开IPIPGO网站: {base_url}")
            
            # 2. 点击登录链接
            self.login_page.click_login_link()
            self.logger.info("✓ 成功点击登录链接")
            
            # 3. 输入用户名
            self.login_page.enter_username(username)
            self.logger.info(f"✓ 成功输入用户名: {username}")
            
            # 4. 输入密码
            self.login_page.enter_password(password)
            self.logger.info("✓ 成功输入密码")
            
            # 5. 点击登录按钮
            self.login_page.click_login_button()
            self.logger.info("✓ 成功点击登录按钮")
            
            # 6. 验证登录结果
            if self.login_page.is_login_successful():
                self.logger.info("🎉 登录成功！")
            else:
                self.logger.warning("⚠️ 登录状态未确认")
            
            # 登录完成截图
            login_screenshot = self.login_page.take_screenshot("login_completed.png")
            self.logger.info(f"📸 登录完成截图: {login_screenshot}")
            
            # ========== 第二阶段：购买流程 ==========
            self.logger.info("\n💰 第二阶段：执行购买流程")
            
            # 执行完整购买流程
            if self.purchase_page.complete_purchase_flow():
                self.logger.info("🎉 购买流程执行成功！")
            else:
                self.logger.error("❌ 购买流程执行失败")
            
            # 最终截图
            final_screenshot = self.purchase_page.take_screenshot("complete_flow_final.png")
            self.logger.info(f"📸 最终截图: {final_screenshot}")
            
            self.logger.info("="*60)
            self.logger.info("✅ IPIPGO完整流程测试完成")
            self.logger.info("="*60)
            
        except Exception as e:
            self.logger.error(f"❌ 完整流程测试失败: {str(e)}")
            # 失败时截图
            self.purchase_page.take_screenshot("complete_flow_failure.png")
            raise


if __name__ == "__main__":
    # 直接运行测试
    test_instance = TestCompleteFlow()
    test_instance.setup_class()
    try:
        test_instance.test_complete_login_and_purchase_flow()
    finally:
        test_instance.teardown_class() 