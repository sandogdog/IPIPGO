"""
IPIPGO登录页面
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.base_page import BasePage
import time


class LoginPage(BasePage):
    """登录页面类"""
    
    # 页面元素定位器
    LOGIN_LINK = (By.CSS_SELECTOR, "a.login-a[href='/login?scene=login']")
    USERNAME_INPUT = (By.CSS_SELECTOR, "input.el-input__inner[placeholder='请输入手机号/邮箱']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input.el-input__inner[placeholder*='请输入密码']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.el-button.login-btn.el-button--primary")
    LOGIN_BUTTON_ALT1 = (By.CSS_SELECTOR, "button.login-btn.el-button--primary")
    LOGIN_BUTTON_ALT2 = (By.CSS_SELECTOR, "button.el-button--primary")
    LOGIN_BUTTON_ALT3 = (By.CSS_SELECTOR, "button[type='button'].el-button")
    LOGIN_BUTTON_SPAN = (By.XPATH, "//button[contains(@class,'login-btn')]//span[contains(text(),'登录')]")
    
    # 登录后的页面元素（用于判断登录是否成功）
    USER_AVATAR = (By.CSS_SELECTOR, ".user-info, .avatar, .profile, .user-avatar")
    SUCCESS_INDICATOR = (By.CSS_SELECTOR, ".dashboard, .user-center, .my-account, .personal-center")
    
    # 可能的错误信息元素
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".el-message--error, .error-message, .login-error")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_homepage(self, url):
        """打开首页"""
        self.driver.get(url)
        # 智能等待页面标题包含关键词或等待登录链接出现
        try:
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.title_contains("IPIPGO"),
                    EC.presence_of_element_located(self.LOGIN_LINK)
                )
            )
        except:
            pass  # 如果等待失败，继续执行
    
    def click_login_link(self):
        """点击登录链接"""
        # 等待登录链接可点击
        login_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGIN_LINK)
        )
        login_element.click()
        
        # 等待跳转到登录页面（等待用户名输入框出现）
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )
    
    def enter_username(self, username):
        """输入用户名"""
        # 等待用户名输入框可交互
        username_element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.USERNAME_INPUT)
        )
        username_element.clear()
        username_element.send_keys(username)
    
    def enter_password(self, password):
        """输入密码"""
        # 等待密码输入框可交互
        password_element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.PASSWORD_INPUT)
        )
        password_element.clear()
        password_element.send_keys(password)
    
    def click_login_button(self):
        """点击登录按钮"""
        try:
            print("🔍 正在查找登录按钮...")
            
            # 多种定位器尝试
            login_button_locators = [
                self.LOGIN_BUTTON,        # button.el-button.login-btn.el-button--primary
                self.LOGIN_BUTTON_ALT1,   # button.login-btn.el-button--primary
                self.LOGIN_BUTTON_ALT2,   # button.el-button--primary
                self.LOGIN_BUTTON_ALT3,   # button[type='button'].el-button
                self.LOGIN_BUTTON_SPAN    # //button[contains(@class,'login-btn')]//span[contains(text(),'登录')]
            ]
            
            login_btn = None
            used_locator = None
            
            for i, locator in enumerate(login_button_locators):
                try:
                    print(f"🔍 尝试登录按钮定位器 {i+1}: {locator[1]}")
                    login_btn = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable(locator)
                    )
                    used_locator = locator
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
            
            # 确保元素完全可见和可点击
            print("📍 滚动到登录按钮位置...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_btn)
            time.sleep(1)  # 等待滚动完成
            
            # 多种点击方式尝试
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
            
            # 方法3: 强制点击（如果前两种都失败）
            if not click_success:
                try:
                    # 移动到元素并点击
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.move_to_element(login_btn).click().perform()
                    print("✓ 方法3-ActionChains点击成功")
                    click_success = True
                except Exception as e:
                    print(f"❌ 方法3-ActionChains点击失败: {e}")
            
            if not click_success:
                print("❌ 所有点击方式都失败了")
                return False
            
            # 等待一下确保点击生效
            time.sleep(2)
            print("✓ 登录按钮点击完成，等待页面响应...")
            
            # 等待页面响应（等待URL变化或出现登录后元素）
            print("⏳ 等待页面响应...")
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
            
        except Exception as e:
            print(f"❌ 点击登录按钮失败: {e}")
            # 打印页面信息用于调试
            try:
                print(f"📋 当前页面URL: {self.driver.current_url}")
                print(f"📋 当前页面标题: {self.driver.title}")
            except:
                pass
            return False
    
    def login(self, username, password):
        """完整的登录流程"""
        try:
            print("📱 开始登录流程...")
            self.click_login_link()
            print("✓ 登录链接点击完成")
            
            self.enter_username(username)
            print("✓ 用户名输入完成")
            
            self.enter_password(password)
            print("✓ 密码输入完成")
            
            success = self.click_login_button()
            if success:
                print("✓ 登录按钮点击完成")
                return True
            else:
                print("❌ 登录按钮点击失败")
                return False
        except Exception as e:
            print(f"❌ 登录流程失败: {e}")
            return False
    
    def is_login_successful(self):
        """检查是否登录成功"""
        try:
            current_url = self.get_current_url()
            
            # 方法1：检查URL是否不再包含login
            if "/login" not in current_url:
                return True
            
            # 方法2：检查是否有登录成功的元素
            success_elements = [self.SUCCESS_INDICATOR, self.USER_AVATAR]
            for locator in success_elements:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located(locator)
                    )
                    if element.is_displayed():
                        return True
                except TimeoutException:
                    continue
            
            return False
            
        except Exception as e:
            return False 