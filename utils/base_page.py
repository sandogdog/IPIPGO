"""
基础页面类
包含常用的页面操作方法，供其他页面类继承使用
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os


class BasePage:
    """基础页面类"""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def find_element(self, locator, timeout=None):
        """查找单个元素"""
        if timeout is None:
            timeout = self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"元素未找到: {locator}")
    
    def find_elements(self, locator, timeout=None):
        """查找多个元素"""
        if timeout is None:
            timeout = self.timeout
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            return []
    
    def click(self, locator, timeout=None):
        """点击元素"""
        element = self.wait_for_clickable(locator, timeout)
        element.click()
    
    def send_keys(self, locator, text, timeout=None, clear=True):
        """输入文本"""
        element = self.find_element(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """获取元素文本"""
        element = self.find_element(locator, timeout)
        return element.text
    
    def get_attribute(self, locator, attribute, timeout=None):
        """获取元素属性"""
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)
    
    def wait_for_visible(self, locator, timeout=None):
        """等待元素可见"""
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_clickable(self, locator, timeout=None):
        """等待元素可点击"""
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def wait_for_text_present(self, locator, text, timeout=None):
        """等待元素包含指定文本"""
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    
    def is_element_present(self, locator):
        """检查元素是否存在"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator):
        """检查元素是否可见"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def scroll_to_element(self, locator):
        """滚动到元素位置"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    
    def hover(self, locator):
        """鼠标悬停"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
    
    def double_click(self, locator):
        """双击"""
        element = self.find_element(locator)
        ActionChains(self.driver).double_click(element).perform()
    
    def right_click(self, locator):
        """右键点击"""
        element = self.find_element(locator)
        ActionChains(self.driver).context_click(element).perform()
    
    def select_dropdown_by_text(self, locator, text):
        """通过文本选择下拉框"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
    
    def select_dropdown_by_value(self, locator, value):
        """通过值选择下拉框"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(value)
    
    def execute_script(self, script, *args):
        """执行JavaScript脚本"""
        return self.driver.execute_script(script, *args)
    
    def switch_to_frame(self, frame_locator):
        """切换到iframe"""
        frame = self.find_element(frame_locator)
        self.driver.switch_to.frame(frame)
    
    def switch_to_default_content(self):
        """切换回主文档"""
        self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_handle):
        """切换窗口"""
        self.driver.switch_to.window(window_handle)
    
    def get_current_url(self):
        """获取当前URL"""
        return self.driver.current_url
    
    def get_title(self):
        """获取页面标题"""
        return self.driver.title
    
    def refresh_page(self):
        """刷新页面"""
        self.driver.refresh()
    
    def go_back(self):
        """后退"""
        self.driver.back()
    
    def go_forward(self):
        """前进"""
        self.driver.forward()
    
    def take_screenshot(self, filename=None):
        """截图"""
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
        
        # 确保截图目录存在
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        filepath = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        return filepath
    
    def wait_for_page_load(self, timeout=30):
        """等待页面加载完成"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        ) 