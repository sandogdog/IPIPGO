"""
WebDriver管理器
用于初始化和管理不同类型的浏览器驱动
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import yaml
import os


class DriverManager:
    """WebDriver管理器类"""
    
    def __init__(self, config_path="config/config.yaml"):
        self.config = self._load_config(config_path)
        self.driver = None
    
    def _load_config(self, config_path):
        """加载配置文件"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        return {}
    
    def get_driver(self, browser_name=None):
        """获取WebDriver实例"""
        if browser_name is None:
            browser_name = self.config.get('browser', {}).get('default', 'chrome')
        
        if browser_name.lower() == 'chrome':
            self.driver = self._get_chrome_driver()
        elif browser_name.lower() == 'firefox':
            self.driver = self._get_firefox_driver()
        elif browser_name.lower() == 'edge':
            self.driver = self._get_edge_driver()
        else:
            raise ValueError(f"不支持的浏览器类型: {browser_name}")
        
        self._set_driver_config()
        return self.driver
    
    def _get_chrome_driver(self):
        """获取Chrome驱动"""
        options = ChromeOptions()
        
        # 添加常用选项
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 无头模式
        if self.config.get('browser', {}).get('headless', False):
            options.add_argument('--headless')
        
        # 窗口大小
        window_size = self.config.get('browser', {}).get('window_size', '1920,1080')
        options.add_argument(f'--window-size={window_size}')
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _get_firefox_driver(self):
        """获取Firefox驱动"""
        options = FirefoxOptions()
        
        # 无头模式
        if self.config.get('browser', {}).get('headless', False):
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def _get_edge_driver(self):
        """获取Edge驱动"""
        options = EdgeOptions()
        
        # 无头模式
        if self.config.get('browser', {}).get('headless', False):
            options.add_argument('--headless')
        
        # 窗口大小
        window_size = self.config.get('browser', {}).get('window_size', '1920,1080')
        options.add_argument(f'--window-size={window_size}')
        
        # 尝试使用本地驱动程序，如果不存在则使用自动下载
        local_driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'drivers', 'msedgedriver.exe')
        
        if os.path.exists(local_driver_path):
            # 使用本地驱动程序
            service = EdgeService(local_driver_path)
            print(f"使用本地 Edge 驱动程序: {local_driver_path}")
        else:
            # 如果本地驱动不存在，尝试自动下载（需要网络连接）
            try:
                service = EdgeService(EdgeChromiumDriverManager().install())
                print("使用自动下载的 Edge 驱动程序")
            except Exception as e:
                raise Exception(f"无法获取 Edge 驱动程序。本地驱动程序不存在 ({local_driver_path})，自动下载也失败: {str(e)}")
        
        return webdriver.Edge(service=service, options=options)
    
    def _set_driver_config(self):
        """设置驱动配置"""
        if self.driver:
            timeout_config = self.config.get('timeout', {})
            
            # 设置隐式等待
            implicitly_wait = timeout_config.get('implicitly_wait', 10)
            self.driver.implicitly_wait(implicitly_wait)
            
            # 设置页面加载超时
            page_load_timeout = timeout_config.get('page_load_timeout', 30)
            self.driver.set_page_load_timeout(page_load_timeout)
            
            # 设置脚本超时
            script_timeout = timeout_config.get('script_timeout', 30)
            self.driver.set_script_timeout(script_timeout)
            
            # 最大化窗口
            self.driver.maximize_window()
    
    def quit_driver(self, force_close=False):
        """
        关闭驱动
        
        Args:
            force_close (bool): 强制关闭浏览器，忽略配置文件设置
        """
        if self.driver:
            # 检查配置决定是否关闭浏览器
            should_close = force_close
            
            if not force_close:
                try:
                    # 尝试读取配置文件中的设置
                    should_close = self.config.get('browser', {}).get('close_after_test', True)
                except Exception as e:
                    should_close = True
            
            if should_close:
                self.driver.quit()
                self.driver = None
                return True  # 表示已关闭
            else:
                # 不关闭，但提醒用户WebDriver的限制
                print("💡 根据配置跳过浏览器关闭，但程序结束时可能仍会被系统清理")
                return False  # 表示未关闭 