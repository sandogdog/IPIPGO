"""
IPIPGO登录自动化测试
"""

import pytest
import yaml
import os
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from utils.logger import Logger


class TestIPIPGOLogin:
    """IPIPGO登录测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类初始化"""
        cls.driver_manager = DriverManager()
        cls.driver = cls.driver_manager.get_driver('edge')
        cls.login_page = LoginPage(cls.driver)
        cls.logger = Logger(__name__)
        
        # 读取配置
        with open('config/config.yaml', 'r', encoding='utf-8') as file:
            cls.config = yaml.safe_load(file)
    
    @classmethod
    def teardown_class(cls):
        """测试类清理"""
        if cls.driver:
            cls.driver_manager.quit_driver()
    
    def test_login_flow(self):
        """测试登录流程"""
        try:
            # 获取配置信息
            base_url = self.config['environment']['base_url']
            username = self.config['test_data']['login']['username']
            password = self.config['test_data']['login']['password']
            
            self.logger.info(f"开始测试IPIPGO登录流程")
            self.logger.info(f"访问网站: {base_url}")
            
            # 1. 打开网站
            self.login_page.open_homepage(base_url)
            self.logger.info("成功打开IPIPGO网站")
            
            # 2. 点击登录链接
            self.login_page.click_login_link()
            self.logger.info("成功点击登录链接")
            
            # 3. 输入用户名
            self.login_page.enter_username(username)
            self.logger.info(f"成功输入用户名: {username}")
            
            # 4. 输入密码
            self.login_page.enter_password(password)
            self.logger.info("成功输入密码")
            
            # 5. 点击登录按钮
            self.login_page.click_login_button()
            self.logger.info("成功点击登录按钮")
            
            # 6. 验证登录结果
            if self.login_page.is_login_successful():
                self.logger.info("登录成功！")
            else:
                self.logger.warning("登录可能失败，请检查")
            
            # 截图保存结果
            screenshot_path = self.login_page.take_screenshot("login_result.png")
            self.logger.info(f"截图已保存: {screenshot_path}")
            
        except Exception as e:
            self.logger.error(f"登录测试失败: {str(e)}")
            # 失败时截图
            self.login_page.take_screenshot("login_failure.png")
            raise


if __name__ == "__main__":
    # 直接运行测试
    test_instance = TestIPIPGOLogin()
    test_instance.setup_class()
    try:
        test_instance.test_login_flow()
    finally:
        test_instance.teardown_class() 