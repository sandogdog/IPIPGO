"""
IPIPGO管理后台登录页面
处理管理后台的登录流程
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import sys

# 添加父目录到路径，以便导入utils模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.base_page import BasePage


class AdminLoginPage(BasePage):
    """管理后台登录页面类"""
    
    # 页面元素定位器
    USERNAME_PASSWORD_LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-v-0695f084].el-button.el-button--text.el-button--medium span")
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[type='text'][placeholder='用户名'].el-input__inner")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password'][placeholder='密码'].el-input__inner")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-v-6f5962bb].el-button.el-button--primary.el-button--medium span")
    
    # 切换职位相关元素定位器
    USER_MENU_CONTAINER = (By.CSS_SELECTOR, "div.topbar-right-menu-wrapper.el-dropdown-selfdefine")
    USER_DROPDOWN_ARROW = (By.CSS_SELECTOR, "i.el-icon-arrow-down")
    SWITCH_ACCOUNT_MENU_ITEM = (By.CSS_SELECTOR, "li.el-dropdown-menu__item")
    POSITION_DROPDOWN_ARROW = (By.CSS_SELECTOR, "i.el-select__caret.el-input__icon.el-icon-arrow-up")
    POSITION_OPTION = (By.CSS_SELECTOR, "li.el-select-dropdown__item")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "button.el-button.el-button--primary.el-button--medium")
    
    # 登录成功标识符
    DASHBOARD_INDICATOR = (By.CSS_SELECTOR, "[class*='dashboard'], [class*='admin'], [class*='menu']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_admin_login_page(self, login_url):
        """打开管理后台登录页面"""
        try:
            print(f"📱 正在打开管理后台登录页面: {login_url}")
            self.driver.get(login_url)
            
            # 等待页面加载完成
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ 管理后台登录页面加载完成")
            time.sleep(2)  # 额外等待页面完全渲染
            return True
            
        except Exception as e:
            print(f"❌ 打开管理后台登录页面失败: {e}")
            return False
    
    def click_username_password_login(self):
        """点击用户名密码登录按钮"""
        try:
            print("🔍 正在查找用户名密码登录按钮...")
            
            # 多种定位策略
            selectors = [
                "button[data-v-0695f084].el-button.el-button--text.el-button--medium",
                "button.el-button--text",
                "button[class*='el-button--text']"
            ]
            
            username_login_btn = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试定位器: {selector}")
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for button in buttons:
                        button_text = button.text.strip()
                        print(f"   找到按钮文本: '{button_text}'")
                        
                        if '用户名密码登录' in button_text or '用户名' in button_text:
                            username_login_btn = button
                            used_selector = selector
                            print(f"✅ 找到用户名密码登录按钮: '{button_text}'")
                            break
                    
                    if username_login_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not username_login_btn:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//button[contains(text(),'用户名密码登录')]",
                    "//button[contains(@class,'el-button--text') and contains(text(),'用户名')]",
                    "//span[contains(text(),'用户名密码登录')]/parent::button",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        username_login_btn = self.driver.find_element(By.XPATH, xpath)
                        used_selector = xpath
                        print(f"✅ 通过XPath找到用户名密码登录按钮")
                        break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not username_login_btn:
                print("❌ 无法找到用户名密码登录按钮")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", username_login_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: username_login_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", username_login_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(username_login_btn).click().perform()),
            ]
            
            for method_name, click_func in click_methods:
                try:
                    print(f"🖱️ 尝试{method_name}...")
                    click_func()
                    print(f"✅ {method_name}执行成功")
                    click_success = True
                    break
                except Exception as e:
                    print(f"❌ {method_name}失败: {e}")
                    continue
            
            if not click_success:
                print("❌ 所有点击方式都失败")
                return False
            
            # 等待页面切换到用户名密码登录表单
            print("⏳ 等待登录表单加载...")
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击用户名密码登录按钮失败: {e}")
            return False
    
    def enter_username(self, username):
        """输入用户名"""
        try:
            print(f"📝 正在输入用户名: {username}")
            
            # 多种定位策略
            selectors = [
                "input[type='text'][placeholder='用户名'].el-input__inner",
                "input[placeholder='用户名']",
                "input[type='text'].el-input__inner",
                "input.el-input__inner[type='text']"
            ]
            
            username_input = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试用户名输入框定位器: {selector}")
                    username_input = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ 找到用户名输入框: {selector}")
                    break
                except:
                    continue
            
            if not username_input:
                print("❌ 无法找到用户名输入框")
                return False
            
            # 清空并输入用户名
            username_input.clear()
            username_input.send_keys(username)
            print("✅ 用户名输入完成")
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"❌ 输入用户名失败: {e}")
            return False
    
    def enter_password(self, password):
        """输入密码"""
        try:
            print("🔑 正在输入密码...")
            
            # 多种定位策略
            selectors = [
                "input[type='password'][placeholder='密码'].el-input__inner",
                "input[placeholder='密码']",
                "input[type='password'].el-input__inner",
                "input.el-input__inner[type='password']"
            ]
            
            password_input = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试密码输入框定位器: {selector}")
                    password_input = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ 找到密码输入框: {selector}")
                    break
                except:
                    continue
            
            if not password_input:
                print("❌ 无法找到密码输入框")
                return False
            
            # 清空并输入密码
            password_input.clear()
            password_input.send_keys(password)
            print("✅ 密码输入完成")
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"❌ 输入密码失败: {e}")
            return False
    
    def click_login_button(self):
        """点击登录按钮"""
        try:
            print("🔍 正在查找登录按钮...")
            
            # 多种定位策略
            selectors = [
                "button[data-v-6f5962bb].el-button.el-button--primary.el-button--medium",
                "button.el-button--primary",
                "button[class*='el-button--primary']"
            ]
            
            login_btn = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试登录按钮定位器: {selector}")
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for button in buttons:
                        button_text = button.text.strip()
                        print(f"   找到按钮文本: '{button_text}'")
                        
                        if '登录' in button_text and button.is_displayed() and button.is_enabled():
                            login_btn = button
                            used_selector = selector
                            print(f"✅ 找到登录按钮: '{button_text}'")
                            break
                    
                    if login_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not login_btn:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//button[contains(text(),'登录')]",
                    "//button[contains(@class,'el-button--primary') and contains(text(),'登录')]",
                    "//span[contains(text(),'登录')]/parent::button",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        login_btn = self.driver.find_element(By.XPATH, xpath)
                        if login_btn.is_displayed() and login_btn.is_enabled():
                            used_selector = xpath
                            print(f"✅ 通过XPath找到登录按钮")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not login_btn:
                print("❌ 无法找到登录按钮")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_btn)
            time.sleep(1)
            
            # 点击登录按钮
            login_btn.click()
            print("✅ 登录按钮点击完成")
            
            # 等待页面跳转
            print("⏳ 等待登录跳转...")
            time.sleep(5)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击登录按钮失败: {e}")
            return False
    
    def is_login_successful(self):
        """检查是否登录成功"""
        try:
            print("🔍 正在检查登录状态...")
            
            # 检查URL变化
            current_url = self.driver.current_url
            print(f"📋 当前URL: {current_url}")
            
            # 检查是否跳转到管理后台
            success_indicators = [
                "admin" in current_url.lower(),
                "dashboard" in current_url.lower(),
                "test-admin-ipipgo" in current_url.lower()
            ]
            
            if any(success_indicators):
                print("✅ URL检查：已跳转到管理后台")
                return True
            
            # 检查页面元素
            dashboard_selectors = [
                "[class*='dashboard']",
                "[class*='admin']",
                "[class*='menu']",
                "[class*='sidebar']",
                ".el-menu",
                ".layout"
            ]
            
            for selector in dashboard_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"✅ 元素检查：找到管理后台元素 {selector}")
                        return True
                except:
                    continue
            
            # 检查页面标题
            title = self.driver.title
            print(f"📋 页面标题: {title}")
            
            if any(keyword in title.lower() for keyword in ['admin', 'dashboard', 'ipipgo', '管理']):
                print("✅ 标题检查：页面标题包含管理后台关键词")
                return True
            
            print("⚠️ 登录状态检查：未发现明确的成功标识")
            return False
            
        except Exception as e:
            print(f"❌ 检查登录状态失败: {e}")
            return False
    
    def admin_login(self, username, password):
        """完整的管理后台登录流程"""
        try:
            print("\n" + "="*50)
            print("🔐 开始管理后台登录流程")
            print("="*50)
            
            # 步骤1: 点击用户名密码登录按钮
            print("步骤1: 点击用户名密码登录按钮...")
            if not self.click_username_password_login():
                print("❌ 用户名密码登录按钮点击失败")
                return False
            
            # 步骤2: 输入用户名
            print("步骤2: 输入用户名...")
            if not self.enter_username(username):
                print("❌ 用户名输入失败")
                return False
            
            # 步骤3: 输入密码
            print("步骤3: 输入密码...")
            if not self.enter_password(password):
                print("❌ 密码输入失败")
                return False
            
            # 步骤4: 自动点击登录按钮（现在无需验证码）
            print("步骤4: 准备点击登录按钮...")
            print("💡 提示：现在没有验证码，将自动点击登录")
            
            # 等待几秒让页面稳定
            time.sleep(2)
            
            # 自动点击登录按钮
            if not self.click_login_button():
                print("❌ 登录按钮点击失败")
                return False
            
            print("✅ 登录按钮已点击，等待页面跳转...")
            
            # 步骤5: 检查登录结果
            print("步骤5: 检查登录结果...")
            if self.is_login_successful():
                print("🎉 管理后台登录成功！")
                return True
            else:
                print("⚠️ 管理后台登录状态未确认")
                print("💡 提示：登录按钮已点击，请稍等片刻让页面完成跳转")
                
                # 额外等待5秒再次检查
                print("⏳ 额外等待5秒后再次检查登录状态...")
                time.sleep(5)
                
                if self.is_login_successful():
                    print("🎉 管理后台登录成功！（延迟确认）")
                    return True
                else:
                    print("❌ 登录状态仍未确认，请检查验证码是否正确")
                    return False
            
        except Exception as e:
            print(f"❌ 管理后台登录流程失败: {e}")
            return False
    
    def click_user_dropdown_arrow(self):
        """点击右上角的用户下拉箭头"""
        try:
            print("🔍 正在查找用户菜单容器...")
            
            # 先定位到用户菜单容器
            container_selectors = [
                "div.topbar-right-menu-wrapper.el-dropdown-selfdefine",
                ".topbar-right-menu-wrapper",
                "[class*='topbar-right-menu-wrapper']",
                "div[class*='el-dropdown-selfdefine']"
            ]
            
            user_menu_container = None
            used_container_selector = None
            
            for selector in container_selectors:
                try:
                    print(f"🔍 尝试容器定位器: {selector}")
                    containers = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for container in containers:
                        try:
                            container_text = container.text.strip()
                            print(f"   找到容器文本: '{container_text}'")
                            
                            # 检查容器是否包含用户信息文本
                            if ('管理员' in container_text or '秦仁驰' in container_text) and container.is_displayed():
                                user_menu_container = container
                                used_container_selector = selector
                                print(f"✅ 找到用户菜单容器: '{container_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取容器文本: {e}")
                            continue
                    
                    if user_menu_container:
                        break
                        
                except Exception as e:
                    print(f"❌ 容器定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not user_menu_container:
                print("🔍 尝试XPath定位容器...")
                xpath_selectors = [
                    "//div[contains(@class,'topbar-right-menu-wrapper') and contains(@class,'el-dropdown-selfdefine')]",
                    "//div[contains(@class,'topbar-right-menu-wrapper')]",
                    "//div[contains(text(),'管理员') and contains(text(),'秦仁驰')]",
                    "//*[contains(@class,'dropdown') and contains(text(),'管理员')]"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        user_menu_container = self.driver.find_element(By.XPATH, xpath)
                        if user_menu_container.is_displayed():
                            used_container_selector = xpath
                            print(f"✅ 通过XPath找到用户菜单容器")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not user_menu_container:
                print("❌ 无法找到用户菜单容器")
                return False
            
            print(f"📋 使用的容器定位器: {used_container_selector}")
            
            # 在用户菜单容器内查找下拉箭头
            print("🔍 在用户菜单容器内查找下拉箭头...")
            dropdown_arrow = None
            
            # 在容器内查找下拉箭头
            arrow_selectors = [
                "i.el-icon-arrow-down",
                "i[class*='arrow-down']",
                "i[class*='el-icon-arrow']"
            ]
            
            for arrow_selector in arrow_selectors:
                try:
                    print(f"🔍 在容器内尝试箭头定位器: {arrow_selector}")
                    arrows = user_menu_container.find_elements(By.CSS_SELECTOR, arrow_selector)
                    
                    for arrow in arrows:
                        if arrow.is_displayed() and arrow.is_enabled():
                            dropdown_arrow = arrow
                            print(f"✅ 在用户菜单容器内找到下拉箭头")
                            break
                    
                    if dropdown_arrow:
                        break
                        
                except Exception as e:
                    print(f"❌ 容器内箭头定位器 {arrow_selector} 失败: {e}")
                    continue
            
            if not dropdown_arrow:
                print("❌ 在用户菜单容器内无法找到下拉箭头")
                return False
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_arrow)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: dropdown_arrow.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", dropdown_arrow)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(dropdown_arrow).click().perform()),
                ("点击容器", lambda: user_menu_container.click()),  # 备用方案：点击整个容器
            ]
            
            for method_name, click_func in click_methods:
                try:
                    print(f"🖱️ 尝试{method_name}...")
                    click_func()
                    print(f"✅ {method_name}执行成功")
                    click_success = True
                    break
                except Exception as e:
                    print(f"❌ {method_name}失败: {e}")
                    continue
            
            if not click_success:
                print("❌ 所有点击方式都失败")
                return False
            
            # 等待下拉菜单出现
            print("⏳ 等待下拉菜单显示...")
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击用户下拉箭头失败: {e}")
            return False
    
    def click_switch_account_menu(self):
        """点击切换账号菜单项"""
        try:
            print("🔍 正在查找切换账号菜单项...")
            
            # 等待下拉菜单完全显示
            time.sleep(1)
            
            # 多种定位策略
            selectors = [
                "li.el-dropdown-menu__item",
                "li[class*='dropdown-menu__item']",
                "[class*='dropdown-menu'] li"
            ]
            
            switch_menu_item = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试菜单项定位器: {selector}")
                    menu_items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for item in menu_items:
                        try:
                            item_text = item.text.strip()
                            print(f"   找到菜单项文本: '{item_text}'")
                            
                            if ('切换账号' in item_text or '切换' in item_text) and item.is_displayed():
                                switch_menu_item = item
                                used_selector = selector
                                print(f"✅ 找到切换账号菜单项: '{item_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取菜单项文本: {e}")
                            continue
                    
                    if switch_menu_item:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not switch_menu_item:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//li[contains(@class,'dropdown-menu__item') and contains(text(),'切换账号')]",
                    "//li[contains(text(),'切换账号')]",
                    "//*[contains(@class,'dropdown') and contains(text(),'切换')]"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        switch_menu_item = self.driver.find_element(By.XPATH, xpath)
                        if switch_menu_item.is_displayed():
                            used_selector = xpath
                            print(f"✅ 通过XPath找到切换账号菜单项")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not switch_menu_item:
                print("❌ 无法找到切换账号菜单项")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 点击切换账号菜单项
            switch_menu_item.click()
            print("✅ 切换账号菜单项点击完成")
            
            # 等待弹窗出现
            print("⏳ 等待切换账号弹窗显示...")
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击切换账号菜单项失败: {e}")
            return False
    
    def click_position_dropdown_arrow(self):
        """点击职位下拉箭头"""
        try:
            print("🔍 正在查找职位下拉箭头...")
            
            # 多种定位策略
            selectors = [
                "i.el-select__caret.el-input__icon.el-icon-arrow-up",
                "i.el-select__caret",
                "i[class*='select__caret']",
                "i[class*='arrow-up']"
            ]
            
            position_arrow = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试职位下拉箭头定位器: {selector}")
                    arrows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for arrow in arrows:
                        if arrow.is_displayed() and arrow.is_enabled():
                            position_arrow = arrow
                            used_selector = selector
                            print(f"✅ 找到职位下拉箭头")
                            break
                    
                    if position_arrow:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            if not position_arrow:
                print("❌ 无法找到职位下拉箭头")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", position_arrow)
            time.sleep(1)
            
            # 点击职位下拉箭头
            position_arrow.click()
            print("✅ 职位下拉箭头点击完成")
            
            # 等待职位选项显示
            print("⏳ 等待职位选项显示...")
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击职位下拉箭头失败: {e}")
            return False
    
    def select_position_option(self, target_position_name="秦仁驰"):
        """选择指定的职位选项"""
        try:
            print(f"🔍 正在查找职位选项: {target_position_name}...")
            
            # 多种定位策略
            selectors = [
                "li.el-select-dropdown__item",
                "li[class*='select-dropdown__item']",
                "[class*='select-dropdown'] li"
            ]
            
            target_option = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试职位选项定位器: {selector}")
                    options = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for option in options:
                        try:
                            option_text = option.text.strip()
                            print(f"   找到职位选项文本: '{option_text}'")
                            
                            if (target_position_name in option_text and 
                                option.is_displayed() and option.is_enabled()):
                                target_option = option
                                used_selector = selector
                                print(f"✅ 找到目标职位选项: '{option_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取选项文本: {e}")
                            continue
                    
                    if target_option:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not target_option:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    f"//li[contains(@class,'select-dropdown__item') and contains(text(),'{target_position_name}')]",
                    f"//li[contains(text(),'{target_position_name}')]",
                    f"//*[contains(@class,'dropdown') and contains(text(),'{target_position_name}')]"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        target_option = self.driver.find_element(By.XPATH, xpath)
                        if target_option.is_displayed():
                            used_selector = xpath
                            print(f"✅ 通过XPath找到目标职位选项")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not target_option:
                print(f"❌ 无法找到职位选项: {target_position_name}")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 点击目标职位选项
            target_option.click()
            print(f"✅ 职位选项点击完成: {target_position_name}")
            
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ 选择职位选项失败: {e}")
            return False
    
    def click_confirm_button(self):
        """点击确定按钮"""
        try:
            print("🔍 正在查找确定按钮...")
            
            # 多种定位策略
            selectors = [
                "button.el-button.el-button--primary.el-button--medium",
                "button[class*='el-button--primary']",
                "button.el-button--primary"
            ]
            
            confirm_btn = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试确定按钮定位器: {selector}")
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for button in buttons:
                        try:
                            button_text = button.text.strip()
                            print(f"   找到按钮文本: '{button_text}'")
                            
                            if ('确定' in button_text or 'OK' in button_text.upper()) and button.is_displayed() and button.is_enabled():
                                confirm_btn = button
                                used_selector = selector
                                print(f"✅ 找到确定按钮: '{button_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取按钮文本: {e}")
                            continue
                    
                    if confirm_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not confirm_btn:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//button[contains(@class,'el-button--primary') and contains(text(),'确定')]",
                    "//button[contains(text(),'确定')]",
                    "//span[contains(text(),'确定')]/parent::button",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        confirm_btn = self.driver.find_element(By.XPATH, xpath)
                        if confirm_btn.is_displayed() and confirm_btn.is_enabled():
                            used_selector = xpath
                            print(f"✅ 通过XPath找到确定按钮")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not confirm_btn:
                print("❌ 无法找到确定按钮")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_btn)
            time.sleep(1)
            
            # 点击确定按钮
            confirm_btn.click()
            print("✅ 确定按钮点击完成")
            
            # 等待页面刷新
            print("⏳ 等待页面刷新...")
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击确定按钮失败: {e}")
            return False
    
    def switch_position(self, target_position_name="秦仁驰"):
        """完整的切换职位流程"""
        try:
            print("\n" + "="*50)
            print("🔄 开始切换职位流程")
            print("="*50)
            
            # 步骤1: 点击右上角用户下拉箭头
            print("步骤1: 点击右上角用户下拉箭头...")
            if not self.click_user_dropdown_arrow():
                print("❌ 用户下拉箭头点击失败")
                return False
            
            # 步骤2: 点击切换账号菜单项
            print("步骤2: 点击切换账号菜单项...")
            if not self.click_switch_account_menu():
                print("❌ 切换账号菜单项点击失败")
                return False
            
            # 步骤3: 点击职位下拉箭头
            print("步骤3: 点击职位下拉箭头...")
            if not self.click_position_dropdown_arrow():
                print("❌ 职位下拉箭头点击失败")
                return False
            
            # 步骤4: 选择目标职位
            print(f"步骤4: 选择目标职位 {target_position_name}...")
            if not self.select_position_option(target_position_name):
                print(f"❌ 选择职位 {target_position_name} 失败")
                return False
            
            # 步骤5: 点击确定按钮
            print("步骤5: 点击确定按钮...")
            if not self.click_confirm_button():
                print("❌ 确定按钮点击失败")
                return False
            
            print("="*50)
            print(f"🎉 职位切换成功！已切换到: {target_position_name}")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 切换职位流程失败: {e}")
            return False 