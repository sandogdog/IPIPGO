"""
示例测试文件
展示如何使用项目框架进行UI自动化测试
"""

import pytest
from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from utils.logger import logger


class TestExample:
    """示例测试类"""
    
    def test_baidu_search(self, driver):
        """百度搜索测试示例"""
        logger.info("开始执行百度搜索测试")
        
        # 创建页面对象
        page = BasePage(driver)
        
        # 打开百度首页
        driver.get("https://www.baidu.com")
        logger.info("已打开百度首页")
        
        # 查找搜索框并输入搜索内容
        search_box = (By.ID, "kw")
        page.send_keys(search_box, "Selenium自动化测试")
        logger.info("已输入搜索内容")
        
        # 点击搜索按钮
        search_button = (By.ID, "su")
        page.click(search_button)
        logger.info("已点击搜索按钮")
        
        # 等待搜索结果加载
        page.wait_for_page_load()
        
        # 验证搜索结果
        assert "Selenium自动化测试" in driver.title
        logger.info("搜索结果验证通过")
        
        # 截图
        screenshot_path = page.take_screenshot("baidu_search_result.png")
        logger.info(f"已保存截图: {screenshot_path}")
    
    def test_title_check(self, driver):
        """页面标题检查测试"""
        logger.info("开始执行页面标题检查测试")
        
        page = BasePage(driver)
        
        # 访问测试页面
        driver.get("https://www.example.com")
        
        # 检查页面标题
        title = page.get_title()
        logger.info(f"页面标题: {title}")
        
        assert "Example" in title
        logger.info("标题检查通过")
    
    @pytest.mark.parametrize("search_term", [
        "Python",
        "Selenium", 
        "自动化测试"
    ])
    def test_multiple_searches(self, driver, search_term):
        """参数化测试示例"""
        logger.info(f"开始执行搜索测试: {search_term}")
        
        page = BasePage(driver)
        
        driver.get("https://www.baidu.com")
        
        search_box = (By.ID, "kw")
        search_button = (By.ID, "su")
        
        page.send_keys(search_box, search_term)
        page.click(search_button)
        page.wait_for_page_load()
        
        assert search_term in driver.title
        logger.info(f"搜索 '{search_term}' 测试通过") 