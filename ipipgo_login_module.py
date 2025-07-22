"""
IPIPGO登录操作模块
独立的登录操作模块，包含完整的登录功能
使用方法：
1. 创建IPIPGOLogin实例
2. 调用login方法进行登录
3. 使用is_login_successful检查登录状态
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import os


class IPIPGOLogin:
    """IPIPGO登录操作类"""
    
    def __init__(self, headless=False, timeout=10):
        """
        初始化登录操作类
        
        Args:
            headless (bool): 是否使用无头模式
            timeout (int): 默认超时时间
        """
        self.driver = None
        self.timeout = timeout
        self.headless = headless
        
        # 页面元素定位器
        self.LOGIN_LINK = (By.CSS_SELECTOR, "a.login-a[href='/login?scene=login']")
        self.USERNAME_INPUT = (By.CSS_SELECTOR, "input.el-input__inner[placeholder='请输入手机号/邮箱']")
        self.PASSWORD_INPUT = (By.CSS_SELECTOR, "input.el-input__inner[placeholder*='请输入密码']")
        
        # 登录按钮的多种定位器
        self.LOGIN_BUTTON = (By.CSS_SELECTOR, "button.el-button.login-btn.el-button--primary")
        self.LOGIN_BUTTON_ALT1 = (By.CSS_SELECTOR, "button.login-btn.el-button--primary")
        self.LOGIN_BUTTON_ALT2 = (By.CSS_SELECTOR, "button.el-button--primary")
        self.LOGIN_BUTTON_ALT3 = (By.CSS_SELECTOR, "button[type='button'].el-button")
        self.LOGIN_BUTTON_SPAN = (By.XPATH, "//button[contains(@class,'login-btn')]//span[contains(text(),'登录')]")
        
        # 登录成功的判断元素
        self.USER_AVATAR = (By.CSS_SELECTOR, ".user-info, .avatar, .profile, .user-avatar")
        self.SUCCESS_INDICATOR = (By.CSS_SELECTOR, ".dashboard, .user-center, .my-account, .personal-center")
        
        # 错误信息元素
        self.ERROR_MESSAGE = (By.CSS_SELECTOR, ".el-message--error, .error-message, .login-error")
    
    def init_driver(self):
        """初始化浏览器驱动"""
        if self.driver is None:
            print("🌐 正在初始化Edge浏览器...")
            options = EdgeOptions()
            
            # 添加常用选项
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # 无头模式
            if self.headless:
                options.add_argument('--headless')
            
            # 窗口大小
            options.add_argument('--window-size=1920,1080')
            
            service = EdgeService(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service, options=options)
            
            # 设置超时时间
            self.driver.implicitly_wait(self.timeout)
            self.driver.set_page_load_timeout(30)
            self.driver.set_script_timeout(30)
            
            # 最大化窗口
            self.driver.maximize_window()
            
            print("✓ Edge浏览器初始化完成")
    
    def open_homepage(self, url):
        """
        打开IPIPGO首页
        
        Args:
            url (str): 网站地址
        """
        self.init_driver()
        print(f"🌐 正在打开网站: {url}")
        self.driver.get(url)
        
        # 智能等待页面加载
        try:
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.title_contains("IPIPGO"),
                    EC.presence_of_element_located(self.LOGIN_LINK)
                )
            )
            print("✓ 网站页面加载完成")
        except TimeoutException:
            print("⚠️ 页面加载超时，但继续执行")
    
    def click_login_link(self):
        """点击登录链接"""
        print("🔗 正在点击登录链接...")
        try:
            # 等待登录链接可点击
            login_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.LOGIN_LINK)
            )
            login_element.click()
            
            # 等待跳转到登录页面（等待用户名输入框出现）
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.USERNAME_INPUT)
            )
            print("✓ 登录链接点击成功，已跳转到登录页面")
        except TimeoutException:
            print("❌ 登录链接点击失败或页面跳转超时")
            raise
    
    def enter_username(self, username):
        """
        输入用户名
        
        Args:
            username (str): 用户名（手机号或邮箱）
        """
        print(f"📝 正在输入用户名: {username}")
        try:
            # 等待用户名输入框可交互
            username_element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.USERNAME_INPUT)
            )
            username_element.clear()
            username_element.send_keys(username)
            print("✓ 用户名输入完成")
        except TimeoutException:
            print("❌ 用户名输入框未找到或不可交互")
            raise
    
    def enter_password(self, password):
        """
        输入密码
        
        Args:
            password (str): 密码
        """
        print("🔒 正在输入密码...")
        try:
            # 等待密码输入框可交互
            password_element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.PASSWORD_INPUT)
            )
            password_element.clear()
            password_element.send_keys(password)
            print("✓ 密码输入完成")
        except TimeoutException:
            print("❌ 密码输入框未找到或不可交互")
            raise
    
    def click_login_button(self):
        """点击登录按钮"""
        print("🔍 正在查找登录按钮...")
        
        # 多种登录按钮定位器
        login_button_locators = [
            self.LOGIN_BUTTON,        # button.el-button.login-btn.el-button--primary
            self.LOGIN_BUTTON_ALT1,   # button.login-btn.el-button--primary
            self.LOGIN_BUTTON_ALT2,   # button.el-button--primary
            self.LOGIN_BUTTON_ALT3,   # button[type='button'].el-button
            self.LOGIN_BUTTON_SPAN    # //button[contains(@class,'login-btn')]//span[contains(text(),'登录')]
        ]
        
        login_btn = None
        
        # 尝试多种定位器找到登录按钮
        for i, locator in enumerate(login_button_locators):
            try:
                print(f"🔍 尝试登录按钮定位器 {i+1}: {locator[1]}")
                login_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(locator)
                )
                print(f"✓ 找到登录按钮，使用定位器: {locator[1]}")
                break
            except TimeoutException:
                print(f"❌ 登录按钮定位器 {i+1} 未找到按钮")
                continue
        
        if login_btn is None:
            print("❌ 所有定位器都无法找到登录按钮")
            return False
        
        # 检查按钮状态
        print(f"📋 登录按钮文本: {login_btn.text}")
        print(f"📋 登录按钮是否可见: {login_btn.is_displayed()}")
        print(f"📋 登录按钮是否启用: {login_btn.is_enabled()}")
        
        # 滚动到登录按钮位置
        print("📍 滚动到登录按钮位置...")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_btn)
        time.sleep(1)  # 等待滚动完成
        
        # 尝试多种点击方式
        print("🖱️ 正在点击登录按钮...")
        click_success = False
        
        # 方法1: 普通点击
        try:
            login_btn.click()
            print("✓ 方法1-普通点击成功")
            click_success = True
        except Exception as e:
            print(f"❌ 方法1-普通点击失败: {e}")
        
        # 方法2: JavaScript点击（如果普通点击失败）
        if not click_success:
            try:
                self.driver.execute_script("arguments[0].click();", login_btn)
                print("✓ 方法2-JavaScript点击成功")
                click_success = True
            except Exception as e:
                print(f"❌ 方法2-JavaScript点击失败: {e}")
        
        # 方法3: ActionChains点击（如果前两种都失败）
        if not click_success:
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(login_btn).click().perform()
                print("✓ 方法3-ActionChains点击成功")
                click_success = True
            except Exception as e:
                print(f"❌ 方法3-ActionChains点击失败: {e}")
        
        if not click_success:
            print("❌ 所有点击方式都失败了")
            return False
        
        # 等待页面响应
        print("⏳ 等待页面响应...")
        time.sleep(2)
        current_url = self.driver.current_url
        
        try:
            WebDriverWait(self.driver, 8).until(
                EC.any_of(
                    EC.url_changes(current_url),
                    EC.presence_of_element_located(self.SUCCESS_INDICATOR),
                    EC.presence_of_element_located(self.USER_AVATAR)
                )
            )
            print("✓ 页面已响应，登录请求已提交")
        except TimeoutException:
            print("⚠️ 页面响应超时，检查是否有错误信息...")
            # 检查是否有错误信息
            try:
                error_element = self.driver.find_element(*self.ERROR_MESSAGE)
                if error_element.is_displayed():
                    print(f"❌ 登录错误: {error_element.text}")
            except NoSuchElementException:
                print("ℹ️ 未找到错误信息，可能登录正在处理中")
        
        return True
    
    def login(self, url, username, password):
        """
        完整的登录流程
        
        Args:
            url (str): 网站地址
            username (str): 用户名
            password (str): 密码
            
        Returns:
            bool: 登录是否成功
        """
        try:
            print("=" * 60)
            print("🚀 开始IPIPGO登录流程")
            print("=" * 60)
            
            # 1. 打开网站
            self.open_homepage(url)
            
            # 2. 点击登录链接
            self.click_login_link()
            
            # 3. 输入用户名
            self.enter_username(username)
            
            # 4. 输入密码
            self.enter_password(password)
            
            # 5. 点击登录按钮
            success = self.click_login_button()
            
            if success:
                print("✓ 登录流程完成")
                return True
            else:
                print("❌ 登录流程失败")
                return False
                
        except Exception as e:
            print(f"❌ 登录过程中发生错误: {e}")
            return False
    
    def is_login_successful(self):
        """
        检查是否登录成功
        
        Returns:
            bool: 登录是否成功
        """
        try:
            current_url = self.driver.current_url
            
            # 方法1：检查URL是否不再包含login
            if "/login" not in current_url:
                print("✓ 登录成功（URL检查）")
                return True
            
            # 方法2：检查是否有登录成功的元素
            success_elements = [self.SUCCESS_INDICATOR, self.USER_AVATAR]
            for locator in success_elements:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located(locator)
                    )
                    if element.is_displayed():
                        print("✓ 登录成功（元素检查）")
                        return True
                except TimeoutException:
                    continue
            
            print("❌ 登录状态未确认")
            return False
            
        except Exception as e:
            print(f"❌ 登录状态检查失败: {e}")
            return False
    
    def take_screenshot(self, filename=None):
        """
        截图
        
        Args:
            filename (str): 截图文件名
            
        Returns:
            str: 截图文件路径
        """
        if filename is None:
            filename = f"login_screenshot_{int(time.time())}.png"
        
        # 确保截图目录存在
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        filepath = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        print(f"📸 截图已保存: {filepath}")
        return filepath
    
    def get_current_url(self):
        """获取当前页面URL"""
        return self.driver.current_url if self.driver else None
    
    def get_page_title(self):
        """获取页面标题"""
        return self.driver.title if self.driver else None
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            print("🔄 正在关闭浏览器...")
            self.driver.quit()
            self.driver = None
            print("✓ 浏览器已关闭")


# 使用示例
if __name__ == "__main__":
    # 创建登录实例
    login = IPIPGOLogin(headless=False)  # headless=True为无头模式
    
    try:
        # 登录信息
        url = "https://test.ipipgo.com/zh-CN/"
        username = "18327166247"
        password = "qinrenchi123"
        
        # 执行登录
        login_success = login.login(url, username, password)
        
        if login_success:
            # 等待一段时间让页面完全加载
            time.sleep(3)
            
            # 检查登录状态
            if login.is_login_successful():
                print("🎉 登录成功！")
            else:
                print("⚠️ 登录状态未确认")
            
            # 截图保存结果
            login.take_screenshot("login_result.png")
            
            # 显示当前页面信息
            print(f"📋 当前页面URL: {login.get_current_url()}")
            print(f"📋 页面标题: {login.get_page_title()}")
            
            # 等待用户观察结果
            print("按回车键继续...")
            input()
        else:
            print("❌ 登录失败")
            login.take_screenshot("login_failure.png")
    
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")
        login.take_screenshot("login_error.png")
    
    finally:
        # 关闭浏览器
        login.close()
        print("=" * 60)
        print("🏁 程序结束")
        print("=" * 60) 