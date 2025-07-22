"""
IPIPGO完整自动化程序（离线版 - 内置WebDriver）
功能：打开浏览器 → 登录IPIPGO官网 → 获取W_TOKEN → 打开环境管理页面 → 自动填写cookie_web参数
完整工作流程，使用W_TOKEN自动填写cookie_web，无需用户输入
可独立运行，无需其他文件依赖，内置WebDriver完全离线

【离线WebDriver优化说明】
1. 内置WebDriver：程序自带WebDriver文件，无需网络下载
2. 智能路径检测：自动检测exe环境和脚本环境的WebDriver路径
3. 快速启动优化：跳过网络下载，直接启动浏览器
4. 完全离线运行：适合分发给其他用户，无网络依赖

【exe环境优化说明】
1. 浏览器启动优化：增加了重试机制，最多重试3次（主要问题点）
2. 快速执行优化：页面加载5秒，元素定位5-8秒，大幅提升速度
3. 智能重试优化：失败自动重试，2秒间隔，快速恢复
4. 用户体验优化：详细进度提示，快速执行，高效稳定

【使用说明】
- 浏览器启动无需网络，快速启动（主要优化点）
- 后续操作都很快速，元素定位即刻执行
- 遇到问题会快速重试，无需等待
- 程序总执行时间约1-2分钟（大幅优化）

【故障排除】
- 浏览器启动失败：自动重试3次（主要问题）
- 页面/元素超时：快速重试，立即执行
- WebDriver缺失：检查drivers文件夹中是否有msedgedriver.exe
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import re
import sys


class IPIPGOStandaloneLogin:
    """IPIPGO完整自动化操作类 - 包含登录、获取W_TOKEN、填写cookie_web等完整功能（离线版）"""
    
    def __init__(self, headless=False, timeout=10, enable_screenshot=False):
        """
        初始化登录操作类
        
        Args:
            headless (bool): 是否使用无头模式
            timeout (int): 默认超时时间
            enable_screenshot (bool): 是否启用截图功能，默认关闭
        """
        self.driver = None
        self.timeout = timeout
        self.headless = headless
        self.enable_screenshot = enable_screenshot
        self.w_token = None  # 存储获取到的W_TOKEN
        
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
    
    def get_webdriver_path(self):
        """
        获取WebDriver路径（完美适配exe打包环境）
        
        Returns:
            str: WebDriver文件的完整路径
        """
        print("🔍 正在检测WebDriver路径...")
        
        # 获取程序运行目录的多种方式
        possible_base_dirs = []
        
        # 方法1: PyInstaller打包后的临时目录（最重要）
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller创建的临时目录
            possible_base_dirs.append(sys._MEIPASS)
            print(f"📦 检测到PyInstaller环境，临时目录: {sys._MEIPASS}")
        
        # 方法2: 传统的exe目录检测
        if hasattr(sys, 'frozen') and sys.frozen:
            # 如果是EXE打包后的程序
            exe_dir = os.path.dirname(sys.executable)
            possible_base_dirs.append(exe_dir)
            print(f"📁 EXE程序目录: {exe_dir}")
        
        # 方法3: Python脚本目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_base_dirs.append(script_dir)
        print(f"📄 脚本目录: {script_dir}")
        
        # 尝试所有可能的路径
        for i, base_dir in enumerate(possible_base_dirs):
            # 尝试多种可能的WebDriver位置
            possible_paths = [
                os.path.join(base_dir, "drivers", "msedgedriver.exe"),              # 标准位置
                os.path.join(base_dir, "_internal", "drivers", "msedgedriver.exe"), # PyInstaller内部位置
                os.path.join(base_dir, "msedgedriver.exe"),                         # 根目录直接放置
            ]
            
            for j, driver_path in enumerate(possible_paths):
                print(f"🔍 尝试路径 {i+1}.{j+1}: {driver_path}")
                
                if os.path.exists(driver_path):
                    print(f"✅ WebDriver文件找到: {driver_path}")
                    return driver_path
                else:
                    print(f"❌ 路径不存在: {driver_path}")
        
        # 如果所有路径都失败，显示详细的调试信息
        print("\n❌ 所有路径都未找到WebDriver文件")
        print("🔍 调试信息:")
        print(f"   - sys.frozen: {getattr(sys, 'frozen', False)}")
        print(f"   - sys._MEIPASS: {getattr(sys, '_MEIPASS', 'Not found')}")
        print(f"   - sys.executable: {sys.executable}")
        print(f"   - __file__: {__file__}")
        
        print("\n💡 解决方案:")
        print("   1. 确保 msedgedriver.exe 文件存在")
        print("   2. 重新打包: pyinstaller --onedir --add-data 'drivers;drivers' IPIPGO_token.py")
        print("   3. 或将 msedgedriver.exe 直接放在exe同目录下")
        
        raise FileNotFoundError("WebDriver文件未找到，请检查打包配置或手动放置文件")
    
    def init_driver(self):
        """初始化浏览器驱动（离线版 - 使用本地WebDriver）"""
        if self.driver is None:
            print("🌐 正在初始化Edge浏览器（离线版）...")
            print("⚡ 使用本地WebDriver，无需网络下载，快速启动")
            
            # 重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"🔄 尝试启动浏览器 ({attempt + 1}/{max_retries})...")
                    
                    options = EdgeOptions()
                    
                    # 添加常用选项
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--disable-blink-features=AutomationControlled')
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    options.add_experimental_option('useAutomationExtension', False)
                    
                    # 优化启动速度的选项（保持网站功能正常）
                    options.add_argument('--disable-extensions')
                    options.add_argument('--disable-plugins')
                    options.add_argument('--disable-gpu')
                    options.add_argument('--disable-software-rasterizer')
                    options.add_argument('--disable-background-timer-throttling')
                    options.add_argument('--disable-renderer-backgrounding')
                    options.add_argument('--disable-backgrounding-occluded-windows')
                    options.add_argument('--disable-ipc-flooding-protection')
                    # 注意：不禁用图片和JavaScript，因为网站需要这些功能正常运行
                    
                    # 无头模式
                    if self.headless:
                        options.add_argument('--headless')
                    
                    # 窗口大小
                    options.add_argument('--window-size=1920,1080')
                    
                    print("📥 正在配置本地WebDriver...")
                    # 使用本地WebDriver路径
                    driver_path = self.get_webdriver_path()
                    service = EdgeService(driver_path)
                    print("✅ 本地WebDriver配置完成")
                    
                    print("🚀 正在启动浏览器进程...")
                    self.driver = webdriver.Edge(service=service, options=options)
                    
                    # 设置更长的超时时间（适配exe环境）
                    self.driver.implicitly_wait(self.timeout * 2)  # 增加隐式等待时间
                    self.driver.set_page_load_timeout(60)  # 增加到60秒
                    self.driver.set_script_timeout(60)     # 增加到60秒
                    
                    # 最大化窗口
                    print("📏 正在最大化窗口...")
                    self.driver.maximize_window()
                    
                    print("✅ Edge浏览器初始化完成（离线模式）")
                    break
                    
                except FileNotFoundError as e:
                    print(f"❌ WebDriver文件未找到: {e}")
                    print("💡 解决方案:")
                    print("   1. 确保已下载 msedgedriver.exe")
                    print("   2. 将文件放在 drivers/ 目录下")
                    print("   3. 检查文件名是否正确: msedgedriver.exe")
                    raise e
                    
                except Exception as e:
                    print(f"❌ 浏览器启动失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                    if self.driver:
                        try:
                            self.driver.quit()
                        except:
                            pass
                        self.driver = None
                    
                    if attempt < max_retries - 1:
                        print("⏳ 等待2秒后重试...")
                        time.sleep(2)
                    else:
                        print("❌ 多次尝试失败，浏览器初始化失败")
                        raise Exception(f"浏览器初始化失败: {e}")
    
    def open_homepage(self, url):
        """
        打开IPIPGO首页（优化版 - 适配exe环境）
        
        Args:
            url (str): 网站地址
        """
        self.init_driver()
        print(f"🌐 正在打开网站: {url}")
        print("⏳ 首次访问网站可能较慢，请耐心等待...")
        
        # 重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 尝试访问网站 ({attempt + 1}/{max_retries})...")
                
                # 访问网站
                self.driver.get(url)
                
                # 智能等待页面加载（优化版 - 更宽松的条件）
                print("⏳ 等待页面加载...")
                
                # 先检查页面是否可以访问
                try:
                    # 等待基本页面结构（更宽松的条件）
                    WebDriverWait(self.driver, 10).until(  # 增加到10秒
                        EC.any_of(
                            EC.presence_of_element_located((By.TAG_NAME, "body")),
                            EC.presence_of_element_located((By.TAG_NAME, "html")),
                            EC.presence_of_element_located((By.TAG_NAME, "head"))
                        )
                    )
                    print("✅ 基础页面结构加载完成")
                    
                    # 再等待页面内容（可选）
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.any_of(
                                EC.title_contains("IPIPGO"),
                                EC.presence_of_element_located(self.LOGIN_LINK),
                                EC.presence_of_element_located((By.CSS_SELECTOR, "a, button, input"))
                            )
                        )
                        print("✅ 页面内容加载完成")
                    except TimeoutException:
                        print("⚠️ 页面内容加载超时，但基础结构已就绪，继续执行")
                        
                except TimeoutException:
                    print("❌ 基础页面结构加载失败")
                    # 尝试获取当前状态
                    try:
                        current_url = self.driver.current_url
                        page_source_length = len(self.driver.page_source)
                        print(f"📋 当前URL: {current_url}")
                        print(f"📋 页面源码长度: {page_source_length}")
                        if page_source_length > 100:  # 如果有内容，继续执行
                            print("✅ 检测到页面内容，继续执行")
                        else:
                            raise TimeoutException("页面无内容")
                    except Exception as debug_e:
                        print(f"❌ 页面状态检查失败: {debug_e}")
                        raise TimeoutException("页面加载完全失败")
                
                print("✅ 网站页面加载完成")
                
                # 额外等待确保页面完全加载
                time.sleep(1)  # 减少等待时间
                
                # 验证页面是否正常加载
                page_title = self.driver.title
                current_url = self.driver.current_url
                print(f"📋 页面标题: {page_title}")
                print(f"📋 当前URL: {current_url}")
                
                # 检查是否成功到达目标页面
                if "test.ipipgo.com" in current_url or "IPIPGO" in page_title:
                    print("✅ 页面加载验证成功")
                    break
                else:
                    print("⚠️ 页面可能未正确加载，但继续执行")
                    break
                    
            except TimeoutException:
                print(f"❌ 页面加载超时 (尝试 {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    print("⏳ 等待3秒后重试...")
                    time.sleep(3)
                else:
                    print("⚠️ 多次尝试后页面加载仍然超时，继续执行（可能影响后续操作）")
                    
            except Exception as e:
                print(f"❌ 访问网站失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print("⏳ 等待2秒后重试...")
                    time.sleep(2)
                else:
                    print("❌ 多次尝试失败，网站访问失败")
                    raise Exception(f"网站访问失败: {e}")
    
    def click_login_link(self):
        """点击登录链接（优化版 - 适配exe环境）"""
        print("🔗 正在点击登录链接...")
        
        # 重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 尝试点击登录链接 ({attempt + 1}/{max_retries})...")
                
                # 等待登录链接可点击（快速定位）
                print("⏳ 等待登录链接加载...")
                login_element = WebDriverWait(self.driver, 8).until(  # 减少到8秒
                    EC.element_to_be_clickable(self.LOGIN_LINK)
                )
                
                # 确保元素完全可见
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_element)
                time.sleep(1)
                
                print("🖱️ 点击登录链接...")
                login_element.click()
                
                # 等待跳转到登录页面（等待用户名输入框出现）
                print("⏳ 等待跳转到登录页面...")
                WebDriverWait(self.driver, 8).until(  # 减少到8秒
                    EC.presence_of_element_located(self.USERNAME_INPUT)
                )
                
                print("✅ 登录链接点击成功，已跳转到登录页面")
                
                # 额外等待确保页面完全加载
                time.sleep(1)  # 减少等待时间
                break
                
            except TimeoutException:
                print(f"❌ 登录链接操作超时 (尝试 {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    print("⏳ 等待2秒后重试...")
                    time.sleep(2)
                    # 尝试刷新页面
                    try:
                        print("🔄 尝试刷新页面...")
                        self.driver.refresh()
                        time.sleep(2)
                    except:
                        pass
                else:
                    print("❌ 多次尝试后登录链接点击失败")
                    raise TimeoutException("登录链接点击失败或页面跳转超时")
                    
            except Exception as e:
                print(f"❌ 点击登录链接失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print("⏳ 等待2秒后重试...")
                    time.sleep(2)
                else:
                    print("❌ 多次尝试失败，登录链接点击失败")
                    raise
    
    def enter_username(self, username):
        """
        输入用户名（优化版 - 适配exe环境）
        
        Args:
            username (str): 用户名（手机号或邮箱）
        """
        print(f"📝 正在输入用户名: {username}")
        
        # 重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 尝试输入用户名 ({attempt + 1}/{max_retries})...")
                
                # 等待用户名输入框可交互（快速定位）
                print("⏳ 等待用户名输入框加载...")
                username_element = WebDriverWait(self.driver, 5).until(  # 减少到5秒
                    EC.element_to_be_clickable(self.USERNAME_INPUT)
                )
                
                # 确保元素完全可见
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", username_element)
                time.sleep(0.5)
                
                # 清空输入框
                username_element.clear()
                time.sleep(0.5)
                
                # 输入用户名
                username_element.send_keys(username)
                
                # 验证输入是否成功
                actual_value = username_element.get_attribute('value')
                if actual_value == username:
                    print("✅ 用户名输入完成")
                    break
                else:
                    print(f"⚠️ 用户名输入验证失败，期望: {username}, 实际: {actual_value}")
                    if attempt < max_retries - 1:
                        print("🔄 重新尝试输入...")
                        continue
                        
            except TimeoutException:
                print(f"❌ 用户名输入框超时 (尝试 {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    print("⏳ 等待2秒后重试...")
                    time.sleep(2)
                else:
                    print("❌ 多次尝试后用户名输入框仍未找到")
                    raise TimeoutException("用户名输入框未找到或不可交互")
                    
            except Exception as e:
                print(f"❌ 输入用户名失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print("⏳ 等待2秒后重试...")
                    time.sleep(2)
                else:
                    print("❌ 多次尝试失败，用户名输入失败")
                    raise
    
    def enter_password(self, password):
        """
        输入密码（优化版 - 适配exe环境）
        
        Args:
            password (str): 密码
        """
        print("🔒 正在输入密码...")
        
        # 重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 尝试输入密码 ({attempt + 1}/{max_retries})...")
                
                # 等待密码输入框可交互（快速定位）
                print("⏳ 等待密码输入框加载...")
                password_element = WebDriverWait(self.driver, 5).until(  # 减少到5秒
                    EC.element_to_be_clickable(self.PASSWORD_INPUT)
                )
                
                # 确保元素完全可见
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", password_element)
                time.sleep(0.5)
                
                # 清空输入框
                password_element.clear()
                time.sleep(0.5)
                
                # 输入密码
                password_element.send_keys(password)
                
                # 验证输入是否成功（密码框通常不显示明文，所以检查是否有值）
                actual_value = password_element.get_attribute('value')
                if actual_value and len(actual_value) > 0:
                    print("✅ 密码输入完成")
                    break
                else:
                    print("⚠️ 密码输入验证失败，输入框仍为空")
                    if attempt < max_retries - 1:
                        print("🔄 重新尝试输入...")
                        continue
                        
            except TimeoutException:
                print(f"❌ 密码输入框超时 (尝试 {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    print("⏳ 等待2秒后重试...")
                    time.sleep(2)
                else:
                    print("❌ 多次尝试后密码输入框仍未找到")
                    raise TimeoutException("密码输入框未找到或不可交互")
                    
            except Exception as e:
                print(f"❌ 输入密码失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print("⏳ 等待2秒后重试...")
                    time.sleep(2)
                else:
                    print("❌ 多次尝试失败，密码输入失败")
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
        
        # 等待页面响应（极速响应版）
        print("⏳ 等待页面响应...")
        time.sleep(0.5)  # 进一步减少基础等待时间
        current_url = self.driver.current_url
        
        try:
            # 优先检测URL变化（最快的登录成功指标）
            WebDriverWait(self.driver, 2).until(  # 缩短到2秒，极速检测
                EC.url_changes(current_url)
            )
            print("✅ 页面已跳转，登录成功")
        except TimeoutException:
            # 如果URL没变化，再检测其他成功指标
            try:
                WebDriverWait(self.driver, 1).until(  # 1秒快速检测
                    EC.any_of(
                        EC.presence_of_element_located(self.SUCCESS_INDICATOR),
                        EC.presence_of_element_located(self.USER_AVATAR)
                    )
                )
                print("✅ 页面已响应，登录请求已提交")
            except TimeoutException:
                print("⚠️ 页面响应超时，检查是否有错误信息...")
                # 检查是否有错误信息
                try:
                    error_element = self.driver.find_element(*self.ERROR_MESSAGE)
                    if error_element.is_displayed():
                        print(f"❌ 登录错误: {error_element.text}")
                except NoSuchElementException:
                    print("ℹ️ 未找到错误信息，登录可能需要人机验证或正在处理中")
        
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
    
    def take_screenshot(self, filename=None, enabled=None):
        """
        截图功能（可选）
        
        Args:
            filename (str): 截图文件名
            enabled (bool): 是否启用截图，如果None则使用类的设置
            
        Returns:
            str: 截图文件路径，如果禁用则返回None
        """
        # 如果未指定enabled，使用类的设置
        if enabled is None:
            enabled = self.enable_screenshot
            
        if not enabled:
            return None
            
        if filename is None:
            filename = f"login_screenshot_{int(time.time())}.png"
        
        try:
            # 获取程序运行目录（适配EXE打包）
            if hasattr(os.sys, 'frozen') and os.sys.frozen:
                # 如果是EXE打包后的程序
                program_dir = os.path.dirname(os.sys.executable)
            else:
                # 如果是Python脚本
                program_dir = os.path.dirname(os.path.abspath(__file__))
            
            # 确保截图目录存在
            screenshot_dir = os.path.join(program_dir, "screenshots")
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            filepath = os.path.join(screenshot_dir, filename)
            self.driver.save_screenshot(filepath)
            print(f"📸 截图已保存: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"⚠️ 截图保存失败: {e}")
            return None
    
    def get_current_url(self):
        """获取当前页面URL"""
        return self.driver.current_url if self.driver else None
    
    def get_page_title(self):
        """获取页面标题"""
        return self.driver.title if self.driver else None
    
    def get_w_token_from_cookies(self):
        """
        从浏览器cookies中获取W_TOKEN
        
        Returns:
            str: W_TOKEN值，如果未找到则返回None
        """
        try:
            print("🔍 正在从cookies中查找W_TOKEN...")
            all_cookies = self.driver.get_cookies()
            
            for cookie in all_cookies:
                if cookie.get('name') == 'W_TOKEN':
                    token = cookie.get('value')
                    print(f"✓ 从cookies中找到W_TOKEN: {token}")
                    return token
            
            print("❌ 在cookies中未找到W_TOKEN")
            return None
            
        except Exception as e:
            print(f"❌ 获取cookies失败: {e}")
            return None
    

    
    def get_w_token_from_javascript(self):
        """
        使用JavaScript从页面中获取W_TOKEN
        
        Returns:
            str: W_TOKEN值，如果未找到则返回None
        """
        try:
            print("🔍 正在使用JavaScript查找W_TOKEN...")
            
            # 尝试从document.cookie中获取
            cookie_script = "return document.cookie;"
            cookies = self.driver.execute_script(cookie_script)
            
            if cookies and 'W_TOKEN=' in cookies:
                match = re.search(r'W_TOKEN=([^;]+)', cookies)
                if match:
                    token = match.group(1)
                    print(f"✓ 从document.cookie中找到W_TOKEN: {token}")
                    return token
            
            # 尝试从window对象中获取
            window_script = """
            try {
                if (window.W_TOKEN) return window.W_TOKEN;
                if (window.token) return window.token;
                if (window.authToken) return window.authToken;
                if (window.userToken) return window.userToken;
                return null;
            } catch (e) {
                return null;
            }
            """
            
            window_token = self.driver.execute_script(window_script)
            if window_token:
                print(f"✓ 从window对象中找到token: {window_token}")
                return window_token
            
            print("❌ 在JavaScript中未找到W_TOKEN")
            return None
            
        except Exception as e:
            print(f"❌ 执行JavaScript获取token失败: {e}")
            return None
    
    def get_w_token_optimized(self):
        """
        优化后的W_TOKEN获取方法
        基于日志分析，主要使用cookies方法和持续监听
        
        Returns:
            str: W_TOKEN值，如果未找到则返回None
        """
        print("=" * 60)
        print("🔍 开始获取W_TOKEN")
        print("=" * 60)
        
        # 等待页面完全加载和API调用完成
        print("⏳ 等待页面完全加载和API调用...")
        time.sleep(2)  # 缩短等待时间
        
        # 持续监听cookies，因为根据日志分析，W_TOKEN主要出现在cookies中
        print("⏳ 持续监听cookies中的W_TOKEN...")
        for i in range(8):  # 减少到8次，每次间隔0.5秒
            time.sleep(0.5)  # 缩短监听间隔
            print(f"  监听第 {i+1}/8 次...")
            
            # 检查cookies中是否出现了W_TOKEN
            try:
                all_cookies = self.driver.get_cookies()
                for cookie in all_cookies:
                    if cookie.get('name') == 'W_TOKEN':
                        token = cookie.get('value')
                        print(f"✓ 在持续监听中从cookies找到W_TOKEN: {token}")
                        self.w_token = token  # 存储到实例变量
                        return token
            except Exception as e:
                print(f"❌ 监听cookies时发生错误: {e}")
                continue
        
        # 如果持续监听没有找到，尝试一次性获取
        print("🔍 尝试一次性从cookies获取W_TOKEN...")
        token = self.get_w_token_from_cookies()
        if token:
            self.w_token = token  # 存储到实例变量
            return token
        
        # 备用方法：从JavaScript获取
        print("🔍 备用方法：从JavaScript获取W_TOKEN...")
        token = self.get_w_token_from_javascript()
        if token:
            self.w_token = token  # 存储到实例变量
            return token
        
        # 显示调试信息
        print("\n🔍 显示cookies调试信息:")
        try:
            all_cookies = self.driver.get_cookies()
            for cookie in all_cookies:
                print(f"Cookie: {cookie.get('name')} = {cookie.get('value')[:50]}...")
        except Exception as e:
            print(f"❌ 获取cookies调试信息失败: {e}")
        
        print("\n❌ 未能获取到W_TOKEN")
        return None
    
    def get_stored_w_token(self):
        """
        获取已存储的W_TOKEN
        
        Returns:
            str: 存储的W_TOKEN值，如果未存储则返回None
        """
        return self.w_token
    
    def open_new_page(self, url):
        """
        打开新的页面（优化版 - 适配exe环境）
        
        Args:
            url (str): 要打开的页面URL
            
        Returns:
            bool: 是否成功打开页面
        """
        print(f"🌐 正在打开新页面: {url}")
        print("⏳ 页面加载可能需要较长时间，请耐心等待...")
        
        # 重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 尝试打开页面 ({attempt + 1}/{max_retries})...")
                
                # 打开页面
                self.driver.get(url)
                
                # 等待页面加载完成（快速加载）
                print("⏳ 等待页面加载...")
                WebDriverWait(self.driver, 5).until(  # 减少到5秒
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # 额外等待确保页面完全加载
                time.sleep(1)  # 快速执行
                
                # 验证页面是否正常加载
                current_url = self.driver.current_url
                page_title = self.driver.title
                print(f"📋 页面标题: {page_title}")
                print(f"📋 当前URL: {current_url}")
                
                print("✅ 新页面加载完成")
                return True
                
            except TimeoutException:
                print(f"❌ 页面加载超时 (尝试 {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    print("⏳ 等待3秒后重试...")
                    time.sleep(3)
                else:
                    print("❌ 多次尝试后页面加载仍然超时")
                    return False
                    
            except Exception as e:
                print(f"❌ 打开页面失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print("⏳ 等待2秒后重试...")
                    time.sleep(2)
                else:
                    print("❌ 多次尝试失败，页面打开失败")
                    return False
        
        return False
    
    def find_cookie_web_input(self):
        """
        查找cookie_web参数的输入框
        使用多种策略定位输入框
        
        Returns:
            WebElement: 找到的输入框元素，如果未找到则返回None
        """
        print("🔍 正在查找cookie_web输入框...")
        
        # 定位策略列表
        strategies = [
            # 策略1: 通过placeholder定位
            (By.CSS_SELECTOR, 'input[placeholder="以@开始"]'),
            
            # 策略2: 通过CSS类组合定位
            (By.CSS_SELECTOR, '.arco-input-wrapper.ms-params-input input'),
            
            # 策略3: 通过父级容器定位
            (By.CSS_SELECTOR, '.ms-params-input input.arco-input'),
            
            # 策略4: 通过input类型和占位符组合
            (By.CSS_SELECTOR, 'input.arco-input-size-medium[placeholder="以@开始"]'),
            
            # 策略5: 更宽泛的定位
            (By.CSS_SELECTOR, 'input.arco-input[type="text"]'),
        ]
        
        for i, (by, selector) in enumerate(strategies):
            try:
                print(f"🔍 尝试定位策略 {i+1}: {selector}")
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((by, selector))
                )
                
                # 验证是否是正确的输入框
                if self.verify_cookie_web_input(element):
                    print(f"✓ 找到cookie_web输入框，使用策略: {selector}")
                    return element
                else:
                    print(f"❌ 策略 {i+1} 找到的不是目标输入框")
                    
            except TimeoutException:
                print(f"❌ 策略 {i+1} 未找到元素")
                continue
            except Exception as e:
                print(f"❌ 策略 {i+1} 发生错误: {e}")
                continue
        
        print("❌ 所有策略都未找到cookie_web输入框")
        return None
    
    def verify_cookie_web_input(self, element):
        """
        验证找到的输入框是否是cookie_web的输入框
        
        Args:
            element: 要验证的输入框元素
            
        Returns:
            bool: 是否是正确的输入框
        """
        try:
            # 检查placeholder属性
            placeholder = element.get_attribute('placeholder')
            if placeholder and '以@开始' in placeholder:
                return True
            
            # 检查父级元素的class
            parent = element.find_element(By.XPATH, '..')
            parent_class = parent.get_attribute('class') or ''
            if 'ms-params-input' in parent_class:
                return True
            
            # 检查是否在cookie_web相关的上下文中
            # 向上查找几层，看是否能找到cookie_web文本
            current = element
            for _ in range(5):  # 向上查找5层
                try:
                    parent = current.find_element(By.XPATH, '..')
                    parent_text = parent.text or ''
                    if 'cookie_web' in parent_text.lower():
                        return True
                    current = parent
                except:
                    break
            
            return False
            
        except Exception as e:
            print(f"❌ 验证输入框时发生错误: {e}")
            return False
    
    def find_cookie_web_input_by_context(self):
        """
        通过上下文查找cookie_web输入框
        先找到"cookie_web"文本，然后找到相关的输入框
        
        Returns:
            WebElement: 找到的输入框元素，如果未找到则返回None
        """
        try:
            print("🔍 通过上下文查找cookie_web输入框...")
            
            # 查找包含"cookie_web"文本的元素
            text_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'cookie_web')]")
            
            if not text_elements:
                print("❌ 未找到包含'cookie_web'文本的元素")
                return None
            
            print(f"✓ 找到 {len(text_elements)} 个包含'cookie_web'的元素")
            
            # 在每个文本元素附近查找输入框
            for text_element in text_elements:
                try:
                    print("🔍 在文本元素附近查找输入框...")
                    
                    # 查找同级或子级的输入框
                    parent = text_element.find_element(By.XPATH, '..')
                    inputs = parent.find_elements(By.CSS_SELECTOR, 'input[placeholder="以@开始"]')
                    
                    if inputs:
                        print("✓ 在文本元素附近找到输入框")
                        return inputs[0]
                    
                    # 查找更广范围的输入框
                    inputs = parent.find_elements(By.CSS_SELECTOR, 'input.arco-input')
                    for input_elem in inputs:
                        if self.verify_cookie_web_input(input_elem):
                            print("✓ 通过上下文验证找到正确的输入框")
                            return input_elem
                            
                except Exception as e:
                    print(f"❌ 在文本元素附近查找输入框时发生错误: {e}")
                    continue
            
            print("❌ 通过上下文未找到cookie_web输入框")
            return None
            
        except Exception as e:
            print(f"❌ 通过上下文查找时发生错误: {e}")
            return None
    
    def login_metersphere(self, username, password):
        """
        登录MeterSphere系统
        
        Args:
            username (str): 用户名
            password (str): 密码
            
        Returns:
            bool: 是否成功登录
        """
        try:
            print("🔐 开始登录MeterSphere系统...")
            
            # 等待页面加载完成（优化：减少等待时间）
            time.sleep(1)
            
            # 用户名输入框定位器
            username_selectors = [
                (By.CSS_SELECTOR, 'input[placeholder="请输入用户名"]'),
                (By.CSS_SELECTOR, '.login-input input'),
                (By.CSS_SELECTOR, 'input.arco-input-size-large[type="text"]'),
                (By.CSS_SELECTOR, '.arco-input-wrapper input[type="text"]'),
            ]
            
            # 查找用户名输入框
            username_element = None
            for i, (by, selector) in enumerate(username_selectors):
                try:
                    print(f"🔍 尝试用户名输入框定位策略 {i+1}: {selector}")
                    username_element = WebDriverWait(self.driver, 2).until(  # 优化：减少到2秒
                        EC.element_to_be_clickable((by, selector))
                    )
                    print(f"✓ 找到用户名输入框，使用策略: {selector}")
                    break
                except TimeoutException:
                    print(f"❌ 用户名输入框策略 {i+1} 未找到")
                    continue
            
            if not username_element:
                print("❌ 无法找到用户名输入框")
                return False
            
            # 输入用户名
            print(f"📝 输入用户名: {username}")
            username_element.clear()
            username_element.send_keys(username)
            
            # 密码输入框定位器
            password_selectors = [
                (By.CSS_SELECTOR, 'input[placeholder="请输入密码"]'),
                (By.CSS_SELECTOR, '.login-password-input input'),
                (By.CSS_SELECTOR, 'input.arco-input-size-large[type="password"]'),
                (By.CSS_SELECTOR, '.arco-input-wrapper input[type="password"]'),
            ]
            
            # 查找密码输入框
            password_element = None
            for i, (by, selector) in enumerate(password_selectors):
                try:
                    print(f"🔍 尝试密码输入框定位策略 {i+1}: {selector}")
                    password_element = WebDriverWait(self.driver, 2).until(  # 优化：减少到2秒
                        EC.element_to_be_clickable((by, selector))
                    )
                    print(f"✓ 找到密码输入框，使用策略: {selector}")
                    break
                except TimeoutException:
                    print(f"❌ 密码输入框策略 {i+1} 未找到")
                    continue
            
            if not password_element:
                print("❌ 无法找到密码输入框")
                return False
            
            # 输入密码
            print("🔒 输入密码...")
            password_element.clear()
            password_element.send_keys(password)
            
            # 登录按钮定位器
            login_button_selectors = [
                (By.CSS_SELECTOR, 'button[type="submit"]'),
                (By.CSS_SELECTOR, 'button.arco-btn-primary'),
                (By.CSS_SELECTOR, 'button.arco-btn-long'),
                (By.XPATH, '//button[contains(text(), "登录")]'),
                (By.CSS_SELECTOR, '.arco-btn.arco-btn-primary.arco-btn-shape-square.arco-btn-size-large'),
            ]
            
            # 查找登录按钮
            login_button = None
            for i, (by, selector) in enumerate(login_button_selectors):
                try:
                    print(f"🔍 尝试登录按钮定位策略 {i+1}: {selector}")
                    login_button = WebDriverWait(self.driver, 2).until(  # 优化：减少到2秒
                        EC.element_to_be_clickable((by, selector))
                    )
                    print(f"✓ 找到登录按钮，使用策略: {selector}")
                    break
                except TimeoutException:
                    print(f"❌ 登录按钮策略 {i+1} 未找到")
                    continue
            
            if not login_button:
                print("❌ 无法找到登录按钮")
                return False
            
            # 点击登录按钮
            print("🚀 点击登录按钮...")
            login_button.click()
            
            # 等待登录完成（优化：减少等待时间，使用智能等待）
            print("⏳ 等待登录响应...")
            time.sleep(2)  # 基础等待时间减少到2秒
            
            # 检查登录是否成功（智能检测URL变化）
            current_url = self.driver.current_url
            
            # 方法1：检查URL是否不再包含login
            if "login" not in current_url:
                print("✅ MeterSphere登录成功（URL已跳转）")
                return True
            
            # 方法2：如果URL还是login页面，再等待一下看是否会跳转
            try:
                WebDriverWait(self.driver, 3).until(  # 等待最多3秒检测跳转
                    lambda driver: "login" not in driver.current_url
                )
                print("✅ MeterSphere登录成功（延迟跳转）")
                return True
            except TimeoutException:
                print("❌ MeterSphere登录失败，仍在登录页面")
                return False
                
        except Exception as e:
            print(f"❌ MeterSphere登录失败: {e}")
            return False
    
    def find_save_button(self):
        """
        查找保存按钮
        
        Returns:
            WebElement: 找到的保存按钮元素，如果未找到则返回None
        """
        print("🔍 正在查找保存按钮...")
        
        # 保存按钮定位策略
        save_button_selectors = [
            # 策略1: 通过完整的class定位
            (By.CSS_SELECTOR, 'button.arco-btn.arco-btn-primary.arco-btn-shape-square.arco-btn-size-medium'),
            
            # 策略2: 通过文本内容定位
            (By.XPATH, '//button[contains(text(), "保存")]'),
            
            # 策略3: 通过主要class定位
            (By.CSS_SELECTOR, 'button.arco-btn-primary[type="button"]'),
            
            # 策略4: 通过组合属性定位
            (By.CSS_SELECTOR, 'button.arco-btn.arco-btn-primary'),
            
            # 策略5: 更宽泛的定位
            (By.CSS_SELECTOR, 'button[type="button"]'),
        ]
        
        for i, (by, selector) in enumerate(save_button_selectors):
            try:
                print(f"🔍 尝试保存按钮定位策略 {i+1}: {selector}")
                
                if by == By.XPATH:
                    # 对于xpath，直接查找
                    element = WebDriverWait(self.driver, 2).until(  # 优化：减少到2秒
                        EC.element_to_be_clickable((by, selector))
                    )
                else:
                    # 对于CSS选择器，查找后验证文本
                    elements = self.driver.find_elements(by, selector)
                    element = None
                    for elem in elements:
                        if "保存" in elem.text:
                            element = elem
                            break
                    
                    if not element:
                        print(f"❌ 策略 {i+1} 未找到包含'保存'文本的按钮")
                        continue
                
                print(f"✓ 找到保存按钮，使用策略: {selector}")
                return element
                
            except TimeoutException:
                print(f"❌ 保存按钮策略 {i+1} 未找到元素")
                continue
            except Exception as e:
                print(f"❌ 保存按钮策略 {i+1} 发生错误: {e}")
                continue
        
        print("❌ 所有策略都未找到保存按钮")
        return None
    
    def click_save_button(self):
        """
        点击保存按钮
        
        Returns:
            bool: 是否成功点击保存按钮
        """
        try:
            print("💾 正在点击保存按钮...")
            
            # 查找保存按钮
            save_button = self.find_save_button()
            
            if not save_button:
                print("❌ 无法找到保存按钮")
                return False
            
            # 点击保存按钮
            save_button.click()
            print("✓ 保存按钮点击成功")
            
            # 等待保存完成（优化等待时间）
            time.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击保存按钮失败: {e}")
            return False
    
    def fill_cookie_web_value(self, value):
        """
        填写cookie_web参数值
        
        Args:
            value (str): 要填写的值（带W_TOKEN=前缀和分号后缀）
            
        Returns:
            bool: 是否成功填写
        """
        try:
            print(f"📝 正在填写cookie_web参数值: {value}")
            
            # 首先尝试直接定位
            input_element = self.find_cookie_web_input()
            
            # 如果直接定位失败，尝试通过上下文定位
            if not input_element:
                print("🔍 直接定位失败，尝试通过上下文定位...")
                input_element = self.find_cookie_web_input_by_context()
            
            if not input_element:
                print("❌ 无法找到cookie_web输入框")
                return False
            
            # 清空输入框并填写新值
            print("🧹 清空输入框...")
            
            # 使用多种方式确保完全清空
            # 方法1：使用clear()
            input_element.clear()
            time.sleep(0.3)
            
            # 方法2：使用Ctrl+A全选然后删除
            input_element.send_keys(Keys.CONTROL + "a")
            time.sleep(0.1)
            input_element.send_keys(Keys.DELETE)
            time.sleep(0.1)
            
            # 方法3：使用JavaScript直接设置值为空
            self.driver.execute_script("arguments[0].value = '';", input_element)
            time.sleep(0.1)
            
            # 验证清空是否成功
            current_value = input_element.get_attribute('value')
            if current_value:
                print(f"⚠️ 输入框未完全清空，剩余内容: {current_value[:50]}...")
                # 再次尝试清空
                input_element.clear()
                input_element.send_keys(Keys.CONTROL + "a")
                input_element.send_keys(Keys.DELETE)
                time.sleep(0.5)
            
            print(f"✏️ 输入值: {value}")
            input_element.send_keys(value)
            
            # 验证输入是否成功
            time.sleep(0.5)
            actual_value = input_element.get_attribute('value')
            if actual_value == value:
                print("✓ cookie_web参数值填写成功")
                
                # 填写成功后点击保存按钮
                save_success = self.click_save_button()
                if save_success:
                    print("✓ 参数保存成功")
                    return True
                else:
                    print("❌ 参数保存失败")
                    return False
            else:
                print(f"❌ 填写验证失败，期望: {value}, 实际: {actual_value}")
                return False
                
        except Exception as e:
            print(f"❌ 填写cookie_web参数值失败: {e}")
            return False
    

    
    def close(self, force_close=False):
        """
        关闭浏览器
        
        Args:
            force_close (bool): 强制关闭浏览器，忽略配置文件设置
        """
        if self.driver:
            # 检查配置决定是否关闭浏览器
            should_close = force_close
            
            if not force_close:
                try:
                    # 尝试读取配置文件
                    config_path = 'config/config.yaml'
                    if os.path.exists(config_path):
                        import yaml
                        with open(config_path, 'r', encoding='utf-8') as file:
                            config = yaml.safe_load(file)
                        should_close = config.get('browser', {}).get('close_after_test', True)
                    else:
                        should_close = True  # 配置文件不存在时默认关闭
                except Exception as e:
                    print(f"⚠️ 读取配置文件失败，默认关闭浏览器: {e}")
                    should_close = True
            
            if should_close:
                print("🔄 正在关闭浏览器...")
                self.driver.quit()
                self.driver = None
                print("✓ 浏览器已关闭")
            else:
                print("🌐 根据配置，浏览器将保持打开状态")
                print("💡 提示：如需关闭浏览器，可手动关闭或修改config.yaml中browser.close_after_test为true")
                # 不关闭driver，但提醒用户


def main():
    """主函数 - 执行完整工作流程"""
    print("🎯 IPIPGO自动化程序 - 完整工作流程（离线版）")
    print("=" * 60)
    print("流程：登录 → 获取W_TOKEN → 打开新页面 → 填写cookie_web")
    print("⚡ 离线优化：内置WebDriver，无需网络下载，快速启动")
    print("💡 完全离线运行，适合打包分发，总时间1-2分钟")
    print("=" * 60)
    
    # 直接执行完整工作流程
    run_full_workflow_with_token()



def run_full_workflow_with_token():
    """执行完整工作流程 - 使用W_TOKEN作为cookie_web值"""
    # 创建登录实例（优化版 - 适配exe环境）
    print("🎯 程序初始化完成，开始执行自动化流程...")
    print("📋 程序已针对离线exe环境进行优化：")
    print("   - 内置WebDriver，无需网络下载（核心优化）")
    print("   - 快速页面加载等待时间（5秒）")
    print("   - 快速元素定位等待时间（5-8秒）")
    print("   - 智能重试机制，快速执行")
    print("   - 完全离线运行，大幅缩短启动时间")
    print("=" * 60)
    
    # 使用快速响应的超时时间
    print("🔧 正在创建自动化实例...")
    login = IPIPGOStandaloneLogin(headless=False, timeout=10)  # 快速执行的超时时间
    print("✅ 自动化实例创建完成")
    
    try:
        # IPIPGO登录信息
        ipipgo_url = "https://test.ipipgo.com/zh-CN/"
        ipipgo_username = "18327166247"  # 替换为您的用户名
        ipipgo_password = "qinrenchi123"  # 替换为您的密码
        
        # MeterSphere登录信息
        metersphere_login_url = "http://10.20.51.100:8081/#/login?redirect=no-project"
        metersphere_username = "renchi.qin@xiaoxitech.com"
        metersphere_password = "renchi.qin@xiaoxitech.com"
        
        # 目标页面URL
        target_url = "http://10.20.51.100:8081/#/project-management/environmentManagement?orgId=100001&pId=49912330342924288"
        
        print("🎯 IPIPGO完整工作流程")
        print(f"IPIPGO登录地址: {ipipgo_url}")
        print(f"IPIPGO用户名: {ipipgo_username}")
        print(f"MeterSphere登录地址: {metersphere_login_url}")
        print(f"MeterSphere用户名: {metersphere_username}")
        print(f"目标页面: {target_url}")
        print("📝 cookie_web值: 将使用获取的W_TOKEN（带前缀）")
        print("=" * 60)
        
        # 第1步：登录IPIPGO
        print("第1步：登录IPIPGO...")
        login_success = login.login(ipipgo_url, ipipgo_username, ipipgo_password)
        
        if not login_success:
            print("❌ IPIPGO登录失败")
            return
        
        # 第2步：获取W_TOKEN
        print("第2步：获取W_TOKEN...")
        w_token = login.get_w_token_optimized()
        
        if not w_token:
            print("❌ W_TOKEN获取失败")
            return
        
        print(f"✅ W_TOKEN获取成功: {w_token[:50]}...")
        
        # 第3步：打开MeterSphere登录页面
        print("第3步：打开MeterSphere登录页面...")
        page_opened = login.open_new_page(metersphere_login_url)
        
        if not page_opened:
            print("❌ MeterSphere登录页面打开失败")
            return
        
        # 第4步：登录MeterSphere
        print("第4步：登录MeterSphere...")
        metersphere_login_success = login.login_metersphere(metersphere_username, metersphere_password)
        
        if not metersphere_login_success:
            print("❌ MeterSphere登录失败")
            return
        
        # 第5步：跳转到环境管理页面
        print("第5步：跳转到环境管理页面...")
        env_page_opened = login.open_new_page(target_url)
        
        if not env_page_opened:
            print("❌ 环境管理页面打开失败")
            return
        
        # 等待页面加载完成（快速加载）
        print("⏳ 等待页面加载完成...")
        time.sleep(2)  # 缩短等待时间
        
        # 可选截图：如果需要记录页面状态，可以启用
        # login.take_screenshot("env_page_loaded_before_fill.png")
        
        # 第6步：使用W_TOKEN填写cookie_web值（带前缀和分号）
        print("第6步：使用W_TOKEN填写cookie_web值...")
        cookie_web_value = f"W_TOKEN={w_token};"
        print(f"📝 将要填写的完整值: {cookie_web_value[:60]}...")
        
        cookie_filled = login.fill_cookie_web_value(cookie_web_value)
        
        # 显示结果
        print("\n🎯 工作流程执行结果：")
        print("=" * 60)
        print(f"✅ IPIPGO登录: {'成功' if login_success else '失败'}")
        print(f"🔑 W_TOKEN获取: {'成功' if w_token else '失败'}")
        print(f"🌐 MeterSphere登录页面打开: {'成功' if page_opened else '失败'}")
        print(f"🔐 MeterSphere登录: {'成功' if metersphere_login_success else '失败'}")
        print(f"🌐 环境管理页面打开: {'成功' if env_page_opened else '失败'}")
        print(f"📝 Cookie填写: {'成功' if cookie_filled else '失败'}")
        print(f"🔑 使用的W_TOKEN: {w_token[:50]}...")
        print(f"🔑 完整cookie_web值: {cookie_web_value[:60]}...")
        print("=" * 60)
        
        if cookie_filled:
            print("🎉 完整工作流程执行成功！")
            print("✅ 已成功使用W_TOKEN（带前缀和分号）填写cookie_web参数")
            # 可选截图：如果需要记录成功状态，可以启用
            # login.take_screenshot("workflow_completed.png")
        else:
            print("❌ cookie_web填写失败")
            # 可选截图：如果需要记录失败状态，可以启用
            # login.take_screenshot("workflow_failed.png")
        
        # 工作流程完成后稍等片刻再关闭浏览器
        print("\n⏳ 流程完成，2秒后自动关闭浏览器...")
        print("💡 提示：如果需要手动查看结果，请在浏览器关闭前进行操作")
        time.sleep(2)  # 给用户时间查看结果
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户取消操作")
    except Exception as e:
        print(f"\n❌ 程序执行失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭浏览器
        login.close()
        print("=" * 60)
        print("🏁 程序结束")
        print("=" * 60)


if __name__ == "__main__":
    # 程序启动提示
    print("=" * 60)
    print("🚀 IPIPGO自动化工具正在启动（离线版）...")
    print("⏳ 程序初始化中，无需网络下载（约5-10秒）")
    print("📦 正在加载依赖包和本地WebDriver...")
    print("💡 离线运行，启动速度更快")
    print("=" * 60)
    
    main() 