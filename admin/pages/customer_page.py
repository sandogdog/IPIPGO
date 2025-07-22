"""
IPIPGO管理后台客户页面
处理客户相关的操作
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


class CustomerPage(BasePage):
    """管理后台客户页面类"""
    
    # 页面元素定位器
    CUSTOMER_MENU_ITEM = (By.CSS_SELECTOR, "li[role='menuitem'][base-path='/customer']")
    USER_ID_INPUT = (By.CSS_SELECTOR, "input[type='text'][placeholder='输入用户ID']")
    QUERY_BUTTON = (By.CSS_SELECTOR, "button.el-button.query.el-button--primary.el-button--medium")
    CUSTOMER_TABLE_ROW = (By.CSS_SELECTOR, "tr.el-table__row")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_customer_menu(self):
        """点击客户菜单项"""
        try:
            print("🔍 正在查找客户菜单项...")
            
            # 多种定位策略
            selectors = [
                "li[role='menuitem'][base-path='/customer']",
                "li.el-menu-item.main-menu-item[base-path='/customer']",
                "li[class*='menu-item'][base-path='/customer']",
                "li[base-path='/customer']"
            ]
            
            customer_menu = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试客户菜单定位器: {selector}")
                    menu_items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for menu_item in menu_items:
                        try:
                            menu_text = menu_item.text.strip()
                            print(f"   找到菜单项文本: '{menu_text}'")
                            
                            if '客户' in menu_text and menu_item.is_displayed():
                                customer_menu = menu_item
                                used_selector = selector
                                print(f"✅ 找到客户菜单项: '{menu_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取菜单项文本: {e}")
                            continue
                    
                    if customer_menu:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not customer_menu:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//li[@role='menuitem' and @base-path='/customer']",
                    "//li[contains(@class,'menu-item') and @base-path='/customer']",
                    "//li[contains(text(),'客户')]",
                    "//*[contains(@class,'menu') and contains(text(),'客户')]"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        customer_menu = self.driver.find_element(By.XPATH, xpath)
                        if customer_menu.is_displayed():
                            used_selector = xpath
                            print(f"✅ 通过XPath找到客户菜单项")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not customer_menu:
                print("❌ 无法找到客户菜单项")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", customer_menu)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: customer_menu.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", customer_menu)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(customer_menu).click().perform()),
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
            
            # 等待页面加载
            print("⏳ 等待客户页面加载...")
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击客户菜单项失败: {e}")
            return False
    
    def enter_user_id(self, user_id):
        """输入用户ID"""
        try:
            print(f"📝 正在输入用户ID: {user_id}")
            
            # 多种定位策略
            selectors = [
                "input[type='text'][placeholder='输入用户ID']",
                "input[placeholder='输入用户ID']",
                "input[class*='el-input__inner'][placeholder='输入用户ID']",
                "input.el-input__inner[type='text']"
            ]
            
            user_id_input = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试用户ID输入框定位器: {selector}")
                    user_id_input = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    used_selector = selector
                    print(f"✅ 找到用户ID输入框: {selector}")
                    break
                except:
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not user_id_input:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//input[@type='text' and @placeholder='输入用户ID']",
                    "//input[@placeholder='输入用户ID']",
                    "//input[contains(@class,'el-input__inner') and @placeholder='输入用户ID']"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        user_id_input = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        used_selector = xpath
                        print(f"✅ 通过XPath找到用户ID输入框")
                        break
                    except:
                        continue
            
            if not user_id_input:
                print("❌ 无法找到用户ID输入框")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 清空并输入用户ID
            user_id_input.clear()
            user_id_input.send_keys(str(user_id))
            print("✅ 用户ID输入完成")
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"❌ 输入用户ID失败: {e}")
            return False
    
    def click_query_button(self):
        """点击查询按钮"""
        try:
            print("🔍 正在查找查询按钮...")
            
            # 多种定位策略
            selectors = [
                "button.el-button.query.el-button--primary.el-button--medium",
                "button[class*='query'][class*='el-button--primary']",
                "button.el-button--primary",
                "button[class*='el-button--primary']"
            ]
            
            query_btn = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试查询按钮定位器: {selector}")
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for button in buttons:
                        try:
                            button_text = button.text.strip()
                            print(f"   找到按钮文本: '{button_text}'")
                            
                            if '查询' in button_text and button.is_displayed() and button.is_enabled():
                                query_btn = button
                                used_selector = selector
                                print(f"✅ 找到查询按钮: '{button_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取按钮文本: {e}")
                            continue
                    
                    if query_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not query_btn:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//button[contains(@class,'query') and contains(@class,'el-button--primary')]",
                    "//button[contains(@class,'el-button--primary') and contains(text(),'查询')]",
                    "//button[contains(text(),'查询')]",
                    "//span[contains(text(),'查询')]/parent::button",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        query_btn = self.driver.find_element(By.XPATH, xpath)
                        if query_btn.is_displayed() and query_btn.is_enabled():
                            used_selector = xpath
                            print(f"✅ 通过XPath找到查询按钮")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not query_btn:
                print("❌ 无法找到查询按钮")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", query_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: query_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", query_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(query_btn).click().perform()),
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
            
            # 等待查询结果加载
            print("⏳ 等待查询结果加载...")
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击查询按钮失败: {e}")
            return False
    
    def click_customer_record(self, user_id="7156"):
        """点击查询列表中的客户记录"""
        try:
            print(f"🔍 正在查找用户ID为 {user_id} 的客户记录...")
            
            # 多种定位策略
            selectors = [
                "tr.el-table__row",
                "tr[class*='el-table__row']",
                "[class*='table'] tr",
                "tbody tr"
            ]
            
            target_row = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试表格行定位器: {selector}")
                    table_rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for row in table_rows:
                        try:
                            row_text = row.text.strip()
                            print(f"   检查行内容: '{row_text[:100]}...'")  # 只显示前100个字符
                            
                            # 检查行是否包含目标用户ID并且行是可见的
                            if (str(user_id) in row_text and 
                                row.is_displayed() and 
                                '7156' in row_text and  # 确保包含完整的7156
                                '183****6247' in row_text):  # 进一步确认是正确的记录
                                target_row = row
                                used_selector = selector
                                print(f"✅ 找到目标客户记录行")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取行文本: {e}")
                            continue
                    
                    if target_row:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not target_row:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    f"//tr[contains(@class,'el-table__row') and contains(text(),'{user_id}')]",
                    f"//tr[contains(text(),'{user_id}')]",
                    f"//tr[contains(text(),'183****6247')]",  # 使用手机号定位
                    f"//*[contains(@class,'table') and contains(text(),'{user_id}')]/ancestor::tr"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        target_row = self.driver.find_element(By.XPATH, xpath)
                        if target_row.is_displayed():
                            used_selector = xpath
                            print(f"✅ 通过XPath找到目标客户记录行")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not target_row:
                print(f"❌ 无法找到用户ID为 {user_id} 的客户记录")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_row)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: target_row.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", target_row)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(target_row).click().perform()),
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
            
            # 等待可能的页面响应
            print("⏳ 等待页面响应...")
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击客户记录失败: {e}")
            return False
    
    def navigate_to_customer_and_query(self, user_id="7156"):
        """完整的客户查询流程"""
        try:
            print("\n" + "="*50)
            print("👥 开始客户查询流程")
            print("="*50)
            
            # 步骤1: 点击客户菜单项
            print("步骤1: 点击客户菜单项...")
            if not self.click_customer_menu():
                print("❌ 客户菜单项点击失败")
                return False
            
            # 步骤2: 输入用户ID
            print(f"步骤2: 输入用户ID {user_id}...")
            if not self.enter_user_id(user_id):
                print("❌ 用户ID输入失败")
                return False
            
            # 步骤3: 点击查询按钮
            print("步骤3: 点击查询按钮...")
            if not self.click_query_button():
                print("❌ 查询按钮点击失败")
                return False
            
            # 步骤4: 点击查询结果中的客户记录
            print("步骤4: 点击查询结果中的客户记录...")
            if not self.click_customer_record(user_id):
                print("❌ 客户记录点击失败")
                return False
            
            print("="*50)
            print(f"🎉 客户查询流程成功完成！用户ID: {user_id}")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 客户查询流程失败: {e}")
            return False
    
    def click_open_package_button(self):
        """点击开套餐按钮"""
        try:
            print("🔍 正在查找开套餐按钮...")
            
            # 多种定位策略
            selectors = [
                "button.el-button.el-icon-plus.el-button--default.el-button--medium",
                "button[class*='el-icon-plus'][class*='el-button--default']",
                "button.el-button--default",
                "button[class*='el-button--default']"
            ]
            
            package_btn = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试开套餐按钮定位器: {selector}")
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for button in buttons:
                        try:
                            button_text = button.text.strip()
                            print(f"   找到按钮文本: '{button_text}'")
                            
                            if '开套餐' in button_text and button.is_displayed() and button.is_enabled():
                                package_btn = button
                                used_selector = selector
                                print(f"✅ 找到开套餐按钮: '{button_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取按钮文本: {e}")
                            continue
                    
                    if package_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not package_btn:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//button[contains(@class,'el-icon-plus') and contains(@class,'el-button--default')]",
                    "//button[contains(@class,'el-button--default') and contains(text(),'开套餐')]",
                    "//button[contains(text(),'开套餐')]",
                    "//span[contains(text(),'开套餐')]/parent::button",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        package_btn = self.driver.find_element(By.XPATH, xpath)
                        if package_btn.is_displayed() and package_btn.is_enabled():
                            used_selector = xpath
                            print(f"✅ 通过XPath找到开套餐按钮")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not package_btn:
                print("❌ 无法找到开套餐按钮")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", package_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: package_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", package_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(package_btn).click().perform()),
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
            
            # 等待开套餐弹窗出现
            print("⏳ 等待开套餐弹窗显示...")
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击开套餐按钮失败: {e}")
            return False
    
    def select_all_dropdowns_in_sequence(self):
        """按顺序选择开套餐面板中的下拉框"""
        try:
            print("🔍 开始按顺序选择下拉框...")
            
            # 第一步：选择第一个下拉框（placeholder="选择套餐"）→ 选择"动态住宅"
            print("步骤1: 选择第一个下拉框 placeholder='选择套餐' → 动态住宅")
            if not self.select_first_dropdown_package_type():
                print("❌ 第一个下拉框选择失败")
                return False
            
            # 第二步：跳过第二个下拉框（IP类型已默认选中"标准"）
            print("步骤2: 跳过第二个下拉框（IP类型已默认选中'标准'）")
            print("✅ 第二个下拉框已默认选中，无需操作")
            
            # 第三步：选择第三个下拉框（placeholder="选择套餐"，最终的套餐选择）→ 随便选一项
            print("步骤3: 选择第三个下拉框（套餐选择）→ 随便选一项")
            if not self.select_third_dropdown_package():
                print("❌ 第三个下拉框选择失败")
                return False
            
            print("✅ 所有下拉框选择完成！")
            return True
            
        except Exception as e:
            print(f"❌ 按顺序选择下拉框失败: {e}")
            return False
    
    def select_first_dropdown_package_type(self):
        """选择第一个下拉框：placeholder='选择套餐' → 动态住宅"""
        try:
            print("🔍 正在选择第一个下拉框...")
            
            # 找到第一个 placeholder="选择套餐" 的下拉框
            container = self.driver.find_element(By.XPATH, "//div[contains(@class,'el-input') and .//input[@placeholder='选择套餐']]")
            dropdown_arrow = container.find_element(By.CSS_SELECTOR, "i.el-select__caret")
            
            print("   点击第一个下拉箭头...")
            dropdown_arrow.click()
            time.sleep(2)
            
            # 选择"动态住宅"选项
            print("   查找'动态住宅'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li[data-v-8548a9c6].el-select-dropdown__item")
            
            for option in options:
                if "动态住宅" in option.text:
                    print("   找到'动态住宅'选项，点击...")
                    option.click()
                    time.sleep(1)
                    print("✅ 第一个下拉框选择完成：动态住宅")
                    return True
            
            print("❌ 未找到'动态住宅'选项")
            return False
            
        except Exception as e:
            print(f"❌ 选择第一个下拉框失败: {e}")
            return False
    

    
    def select_third_dropdown_package(self):
        """选择第三个下拉框：具体套餐选择 → 随便选一项"""
        try:
            print("🔍 正在选择第三个下拉框...")
            
            # 等待一下，让页面状态稳定
            time.sleep(2)
            
            # 找到所有 placeholder="选择套餐" 的下拉框，选择第二个（第三个下拉框）
            containers = self.driver.find_elements(By.XPATH, "//div[contains(@class,'el-input') and .//input[@placeholder='选择套餐']]")
            
            if len(containers) >= 2:
                # 选择第二个下拉框（因为第一个是套餐类型，第二个是具体套餐）
                container = containers[1]
                print(f"   找到 {len(containers)} 个套餐下拉框，选择第 2 个")
            else:
                print(f"   只找到 {len(containers)} 个套餐下拉框，使用第一个")
                container = containers[0]
            
            dropdown_arrow = container.find_element(By.CSS_SELECTOR, "i.el-select__caret")
            
            print("   点击第三个下拉箭头...")
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_arrow)
            time.sleep(1)
            
            # 尝试点击
            dropdown_arrow.click()
            time.sleep(2)
            
            # 随便选择第一个可用选项
            print("   查找可用选项，随便选一个...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li[data-v-8548a9c6].el-select-dropdown__item")
            
            for option in options:
                option_text = option.text.strip()
                if option_text and len(option_text) > 3:  # 确保不是空选项
                    print(f"   选择选项: '{option_text[:30]}...'")
                    option.click()
                    time.sleep(1)
                    print("✅ 第三个下拉框选择完成")
                    return True
            
            print("❌ 未找到可用选项")
            return False
            
        except Exception as e:
            print(f"❌ 选择第三个下拉框失败: {e}")
            return False
    

    
    def enter_remark_info(self, remark="IPIPGO UI自动化测试"):
        """输入备注信息"""
        try:
            print(f"📝 正在输入备注信息: {remark}")
            
            # 多种定位策略
            selectors = [
                "div.el-textarea.el-input--medium textarea.el-textarea__inner",
                "textarea.el-textarea__inner",
                "div[class*='el-textarea'] textarea",
                "textarea[class*='el-textarea__inner']"
            ]
            
            remark_textarea = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试备注输入框定位器: {selector}")
                    remark_textarea = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    used_selector = selector
                    print(f"✅ 找到备注输入框: {selector}")
                    break
                except:
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not remark_textarea:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//div[contains(@class,'el-textarea')]//textarea",
                    "//textarea[contains(@class,'el-textarea__inner')]",
                    "//div[@data-v-8548a9c6 and contains(@class,'el-textarea')]//textarea"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        remark_textarea = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        used_selector = xpath
                        print(f"✅ 通过XPath找到备注输入框")
                        break
                    except:
                        continue
            
            if not remark_textarea:
                print("❌ 无法找到备注输入框")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", remark_textarea)
            time.sleep(1)
            
            # 清空并输入备注信息
            remark_textarea.clear()
            remark_textarea.send_keys(remark)
            print("✅ 备注信息输入完成")
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"❌ 输入备注信息失败: {e}")
            return False
    
    def click_confirm_button_in_package_dialog(self):
        """点击开套餐弹窗中的确定按钮"""
        try:
            print("🔍 正在查找开套餐弹窗中的确定按钮...")
            
            # 多种定位策略
            selectors = [
                "button[data-v-8548a9c6].el-button.el-button--primary.el-button--medium",
                "button.el-button--primary",
                "button[class*='el-button--primary']"
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
                    "//button[@data-v-8548a9c6 and contains(@class,'el-button--primary') and contains(text(),'确定')]",
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
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: confirm_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", confirm_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(confirm_btn).click().perform()),
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
            
            # 等待弹窗关闭或页面跳转
            print("⏳ 等待开套餐确认...")
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击确定按钮失败: {e}")
            return False
    
    def open_package_flow(self, remark="IPIPGO UI自动化测试"):
        """完整的开套餐流程"""
        try:
            print("\n" + "="*50)
            print("📦 开始开套餐流程")
            print("="*50)
            
            # 步骤1: 点击开套餐按钮
            print("步骤1: 点击开套餐按钮...")
            if not self.click_open_package_button():
                print("❌ 开套餐按钮点击失败")
                return False
            
            # 步骤2: 按顺序选择所有下拉框
            print("步骤2: 按顺序选择所有下拉框...")
            if not self.select_all_dropdowns_in_sequence():
                print("❌ 下拉框选择失败")
                return False
            
            # 步骤3: 输入备注信息
            print("步骤3: 输入备注信息...")
            if not self.enter_remark_info(remark):
                print("❌ 备注信息输入失败")
                return False
            
            # 步骤4: 点击确定按钮
            print("步骤4: 点击确定按钮...")
            if not self.click_confirm_button_in_package_dialog():
                print("❌ 确定按钮点击失败")
                return False
            
            # 步骤5: 支付操作
            print("步骤5: 开始支付操作...")
            if not self.complete_payment_flow():
                print("❌ 支付操作失败")
                return False
            
            print("="*50)
            print("🎉 开套餐+支付流程成功完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 开套餐流程失败: {e}")
            return False
    
    def click_payment_button(self):
        """点击支付按钮"""
        try:
            print("🔍 正在查找支付按钮...")
            
            # 多种定位策略
            selectors = [
                "button[data-v-39737d7c].el-button.el-button--primary.el-button--medium.is-plain",
                "button.el-button.el-button--primary.el-button--medium.is-plain",
                "button[class*='el-button--primary'][class*='is-plain']"
            ]
            
            payment_button = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试支付按钮定位器: {selector}")
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for button in buttons:
                        try:
                            button_text = button.text.strip()
                            print(f"   找到按钮文本: '{button_text}'")
                            
                            if "支付" in button_text and button.is_displayed() and button.is_enabled():
                                payment_button = button
                                used_selector = selector
                                print(f"✅ 找到支付按钮: '{button_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取按钮文本: {e}")
                            continue
                    
                    if payment_button:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not payment_button:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//button[contains(@class,'el-button--primary') and contains(@class,'is-plain') and contains(text(),'支付')]",
                    "//button[contains(text(),'支付')]"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        payment_button = self.driver.find_element(By.XPATH, xpath)
                        used_selector = xpath
                        print(f"✅ 通过XPath找到支付按钮")
                        break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not payment_button:
                print("❌ 无法找到支付按钮")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payment_button)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: payment_button.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", payment_button)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(payment_button).click().perform()),
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
            
            # 等待支付弹窗显示
            print("⏳ 等待支付弹窗显示...")
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击支付按钮失败: {e}")
            return False
    
    def click_payment_confirm_button(self):
        """点击支付确定按钮"""
        try:
            print("🔍 正在查找支付确定按钮...")
            
            # 多种定位策略
            selectors = [
                "button[data-v-2f43041c].el-button.el-button--primary.el-button--medium",
                "button.el-button.el-button--primary.el-button--medium",
                "button[class*='el-button--primary'][class*='el-button--medium']"
            ]
            
            confirm_button = None
            used_selector = None
            
            for selector in selectors:
                try:
                    print(f"🔍 尝试支付确定按钮定位器: {selector}")
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for button in buttons:
                        try:
                            button_text = button.text.strip()
                            print(f"   找到按钮文本: '{button_text}'")
                            
                            if "确定" in button_text and button.is_displayed() and button.is_enabled():
                                confirm_button = button
                                used_selector = selector
                                print(f"✅ 找到支付确定按钮: '{button_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取按钮文本: {e}")
                            continue
                    
                    if confirm_button:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果CSS选择器失败，尝试XPath
            if not confirm_button:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//button[contains(@class,'el-button--primary') and contains(text(),'确定')]",
                    "//button[contains(text(),'确定')]"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        confirm_button = self.driver.find_element(By.XPATH, xpath)
                        used_selector = xpath
                        print(f"✅ 通过XPath找到支付确定按钮")
                        break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not confirm_button:
                print("❌ 无法找到支付确定按钮")
                return False
            
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_button)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: confirm_button.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", confirm_button)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(confirm_button).click().perform()),
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
            
            # 等待支付完成
            print("⏳ 等待支付处理完成...")
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 点击支付确定按钮失败: {e}")
            return False
    
    def complete_payment_flow(self):
        """完整的支付流程"""
        try:
            print("\n" + "="*50)
            print("💳 开始支付流程")
            print("="*50)
            
            # 步骤1: 点击支付按钮
            print("步骤1: 点击支付按钮...")
            if not self.click_payment_button():
                print("❌ 支付按钮点击失败")
                return False
            
            # 步骤2: 点击支付确定按钮
            print("步骤2: 点击支付确定按钮...")
            if not self.click_payment_confirm_button():
                print("❌ 支付确定按钮点击失败")
                return False
            
            print("="*50)
            print("🎉 支付流程成功完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 支付流程失败: {e}")
            return False
    
    def select_enterprise_ip_type(self):
        """选择企业IP类型（点击输入框方式）"""
        try:
            print("🔍 正在选择企业IP类型...")
            
            # 步骤1: 等待弹窗完全加载并稳定
            print("步骤1: 等待开套餐弹窗完全加载...")
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-8548a9c6]")))
            time.sleep(2)  # 等待弹窗稳定
            print("✅ 开套餐弹窗已稳定加载")
            
            # 步骤2: 先调试所有输入框，然后查找IP类型输入框
            print("步骤2: 查找IP类型输入框...")
            self.debug_dialog_inputs()
            
            # 查找所有可能的IP类型输入框
            all_inputs = self.driver.find_elements(By.CSS_SELECTOR, "div[data-v-8548a9c6] input.el-input__inner")
            ip_input = None
            
            # 根据调试信息手动指定IP类型输入框（通常是第二个，placeholder="请选择"）
            for i, input_elem in enumerate(all_inputs):
                try:
                    placeholder = input_elem.get_attribute("placeholder")
                    value = input_elem.get_attribute("value")
                    if placeholder == "请选择" and input_elem.is_displayed():
                        ip_input = input_elem
                        print(f"✅ 选择输入框 {i+1} 作为IP类型输入框，当前值: '{value}'")
                        break
                except Exception as e:
                    continue
            
            if not ip_input:
                print("❌ 未找到placeholder='请选择'的IP类型输入框")
                return False
            
            # 步骤3: 使用JavaScript点击IP类型输入框避免遮挡
            print("步骤3: 点击IP类型输入框中间...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ip_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", ip_input)
            print("✅ IP类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤4: 查找并选择"企业"选项
            print("步骤4: 查找并选择'企业'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li[data-v-8548a9c6].el-select-dropdown__item")
            print(f"   找到 {len(options)} 个选项")
            
            enterprise_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    print(f"   选项 {i+1}: '{option_text}'")
                    if "企业" in option_text and option.is_displayed():
                        enterprise_option = option
                        print(f"✅ 找到企业选项: '{option_text}'")
                        break
                except Exception as e:
                    print(f"   选项 {i+1}: 读取文本失败 - {e}")
                    continue
            
            if not enterprise_option:
                print("❌ 未找到企业选项")
                return False
            
            # 步骤5: 点击企业选项
            print("步骤5: 点击企业选项...")
            enterprise_option.click()
            print("✅ 企业选项选择完成")
            time.sleep(2)
            
            print("🎉 IP类型成功选择为企业！")
            return True
            
        except Exception as e:
            print(f"❌ 选择企业IP类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_enterprise_package(self):
        """选择企业套餐（点击输入框方式）"""
        try:
            print("🔍 正在选择企业套餐...")
            
            # 步骤1: 查找第三个下拉框（具体套餐选择）
            print("步骤1: 查找第三个下拉框（具体套餐选择）...")
            
            # 找到所有 placeholder="选择套餐" 的下拉框容器
            containers = self.driver.find_elements(By.XPATH, "//div[contains(@class,'el-input') and .//input[@placeholder='选择套餐']]")
            print(f"   找到 {len(containers)} 个'选择套餐'下拉框")
            
            if len(containers) >= 2:
                # 选择第二个下拉框（因为第一个是套餐类型，第二个是具体套餐）
                container = containers[1]
                package_input = container.find_element(By.CSS_SELECTOR, "input.el-input__inner")
                print(f"✅ 选择第 2 个'选择套餐'下拉框作为具体套餐选择")
            else:
                print(f"❌ 只找到 {len(containers)} 个'选择套餐'下拉框，无法确定第三个")
                return False
            
            # 步骤2: 使用JavaScript点击选择套餐输入框避免遮挡
            print("步骤2: 点击选择套餐输入框中间...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", package_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", package_input)
            print("✅ 选择套餐输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 随便选择一个套餐选项
            print("步骤3: 查找并选择套餐选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li[data-v-8548a9c6].el-select-dropdown__item")
            print(f"   找到 {len(options)} 个选项")
            
            selected_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    if option_text and option.is_displayed() and "标准" in option_text:
                        selected_option = option
                        print(f"✅ 选择套餐选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            # 如果没找到包含"标准"的，就选第一个可见的
            if not selected_option:
                for i, option in enumerate(options):
                    try:
                        option_text = option.text.strip()
                        if option_text and option.is_displayed():
                            selected_option = option
                            print(f"✅ 选择套餐选项: '{option_text}'")
                            break
                    except Exception as e:
                        continue
            
            if not selected_option:
                print("❌ 未找到可选择的套餐选项")
                return False
            
            # 步骤4: 点击选择的套餐选项
            print("步骤4: 点击选择的套餐选项...")
            selected_option.click()
            print("✅ 套餐选项选择完成")
            time.sleep(2)
            
            print("🎉 企业套餐选择完成！")
            return True
            
        except Exception as e:
            print(f"❌ 选择企业套餐失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_basic_ip_type(self):
        """选择基础IP类型（点击输入框方式）"""
        try:
            print("🔍 正在选择基础IP类型...")
            
            # 步骤1: 等待弹窗完全加载并稳定
            print("步骤1: 等待开套餐弹窗完全加载...")
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-8548a9c6]")))
            time.sleep(2)  # 等待弹窗稳定
            print("✅ 开套餐弹窗已稳定加载")
            
            # 步骤2: 查找IP类型输入框
            print("步骤2: 查找IP类型输入框...")
            
            # 查找所有可能的IP类型输入框
            all_inputs = self.driver.find_elements(By.CSS_SELECTOR, "div[data-v-8548a9c6] input.el-input__inner")
            ip_input = None
            
            # 找到 placeholder="请选择" 的IP类型输入框
            for i, input_elem in enumerate(all_inputs):
                try:
                    placeholder = input_elem.get_attribute("placeholder")
                    value = input_elem.get_attribute("value")
                    if placeholder == "请选择" and input_elem.is_displayed():
                        ip_input = input_elem
                        print(f"✅ 找到IP类型输入框，当前值: '{value}'")
                        break
                except Exception as e:
                    continue
            
            if not ip_input:
                print("❌ 未找到placeholder='请选择'的IP类型输入框")
                return False
            
            # 步骤3: 使用JavaScript点击IP类型输入框避免遮挡
            print("步骤3: 点击IP类型输入框中间...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ip_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", ip_input)
            print("✅ IP类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤4: 查找并选择"基础"选项
            print("步骤4: 查找并选择'基础'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li[data-v-8548a9c6].el-select-dropdown__item")
            print(f"   找到 {len(options)} 个选项")
            
            basic_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    if "基础" in option_text and option.is_displayed():
                        basic_option = option
                        print(f"✅ 找到基础选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not basic_option:
                print("❌ 未找到基础选项")
                return False
            
            # 步骤5: 点击基础选项
            print("步骤5: 点击基础选项...")
            basic_option.click()
            print("✅ 基础选项选择完成")
            time.sleep(2)
            
            print("🎉 IP类型成功选择为基础！")
            return True
            
        except Exception as e:
            print(f"❌ 选择基础IP类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_basic_package(self):
        """选择基础套餐（点击输入框方式）"""
        try:
            print("🔍 正在选择基础套餐...")
            
            # 步骤1: 查找第三个下拉框（具体套餐选择）
            print("步骤1: 查找第三个下拉框（具体套餐选择）...")
            
            # 找到所有 placeholder="选择套餐" 的下拉框容器
            containers = self.driver.find_elements(By.XPATH, "//div[contains(@class,'el-input') and .//input[@placeholder='选择套餐']]")
            print(f"   找到 {len(containers)} 个'选择套餐'下拉框")
            
            if len(containers) >= 2:
                # 选择第二个下拉框（因为第一个是套餐类型，第二个是具体套餐）
                container = containers[1]
                package_input = container.find_element(By.CSS_SELECTOR, "input.el-input__inner")
                print(f"✅ 选择第 2 个'选择套餐'下拉框作为具体套餐选择")
            else:
                print(f"❌ 只找到 {len(containers)} 个'选择套餐'下拉框，无法确定第三个")
                return False
            
            # 步骤2: 使用JavaScript点击选择套餐输入框避免遮挡
            print("步骤2: 点击选择套餐输入框中间...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", package_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", package_input)
            print("✅ 选择套餐输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 随便选择一个套餐选项
            print("步骤3: 查找并选择套餐选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li[data-v-8548a9c6].el-select-dropdown__item")
            print(f"   找到 {len(options)} 个选项")
            
            selected_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    if option_text and option.is_displayed() and "基础" in option_text:
                        selected_option = option
                        print(f"✅ 选择套餐选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            # 如果没找到包含"基础"的，就选第一个可见的
            if not selected_option:
                for i, option in enumerate(options):
                    try:
                        option_text = option.text.strip()
                        if option_text and option.is_displayed():
                            selected_option = option
                            print(f"✅ 选择套餐选项: '{option_text}'")
                            break
                    except Exception as e:
                        continue
            
            if not selected_option:
                print("❌ 未找到可选择的套餐选项")
                return False
            
            # 步骤4: 点击选择的套餐选项
            print("步骤4: 点击选择的套餐选项...")
            selected_option.click()
            print("✅ 套餐选项选择完成")
            time.sleep(2)
            
            print("🎉 基础套餐选择完成！")
            return True
            
        except Exception as e:
            print(f"❌ 选择基础套餐失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def open_enterprise_package_flow(self, remark="IPIPGO UI自动化测试"):
        """开企业套餐的完整流程（简化版 - 直接点击输入框）"""
        try:
            print("\n" + "="*50)
            print("📦 开始开企业套餐流程")
            print("="*50)
            
            # 步骤1: 点击开套餐按钮
            print("步骤1: 点击开套餐按钮...")
            if not self.click_open_package_button():
                print("❌ 开套餐按钮点击失败")
                return False
            
            # 步骤2: 第一个【套餐类型】保持不变（默认动态住宅）
            print("步骤2: 套餐类型保持默认（动态住宅）...")
            print("✅ 套餐类型无需修改，保持动态住宅")
            time.sleep(1)
            
            # 步骤3: 第二个【IP类型】选择企业
            print("步骤3: 选择IP类型为企业...")
            if not self.select_enterprise_ip_type():
                print("❌ IP类型选择失败，开始调试...")
                self.debug_dialog_inputs()
                return False
            
            # 步骤4: 第三个【选择套餐】随便选一项
            print("步骤4: 选择具体套餐...")
            if not self.select_enterprise_package():
                print("❌ 具体套餐选择失败")
                return False
            
            # 步骤5: 输入备注信息
            print("步骤5: 输入备注信息...")
            if not self.enter_remark_info(remark):
                print("❌ 备注信息输入失败")
                return False
            
            # 步骤6: 点击确定按钮
            print("步骤6: 点击确定按钮...")
            if not self.click_confirm_button_in_package_dialog():
                print("❌ 确定按钮点击失败")
                return False
            
            # 步骤7: 支付操作
            print("步骤7: 开始支付操作...")
            if not self.complete_payment_flow():
                print("❌ 支付操作失败")
                return False
            
            print("="*50)
            print("🎉 企业套餐+支付流程成功完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 开企业套餐流程失败: {e}")
            return False
    
    def open_basic_package_flow(self, remark="IPIPGO UI自动化测试"):
        """开基础套餐的完整流程（简化版 - 直接点击输入框）"""
        try:
            print("\n" + "="*50)
            print("📦 开始开基础套餐流程")
            print("="*50)
            
            # 步骤1: 点击开套餐按钮
            print("步骤1: 点击开套餐按钮...")
            if not self.click_open_package_button():
                print("❌ 开套餐按钮点击失败")
                return False
            
            # 步骤2: 第一个【套餐类型】保持不变（默认动态住宅）
            print("步骤2: 套餐类型保持默认（动态住宅）...")
            print("✅ 套餐类型无需修改，保持动态住宅")
            time.sleep(1)
            
            # 步骤3: 第二个【IP类型】选择基础
            print("步骤3: 选择IP类型为基础...")
            if not self.select_basic_ip_type():
                print("❌ IP类型选择失败")
                return False
            
            # 步骤4: 第三个【选择套餐】随便选一项
            print("步骤4: 选择具体套餐...")
            if not self.select_basic_package():
                print("❌ 具体套餐选择失败")
                return False
            
            # 步骤5: 输入备注信息
            print("步骤5: 输入备注信息...")
            if not self.enter_remark_info(remark):
                print("❌ 备注信息输入失败")
                return False
            
            # 步骤6: 点击确定按钮
            print("步骤6: 点击确定按钮...")
            if not self.click_confirm_button_in_package_dialog():
                print("❌ 确定按钮点击失败")
                return False
            
            # 步骤7: 支付操作
            print("步骤7: 开始支付操作...")
            if not self.complete_payment_flow():
                print("❌ 支付操作失败")
                return False
            
            print("="*50)
            print("🎉 基础套餐+支付流程成功完成！")
            print("="*50)
            return True
        except Exception as e:
            print(f"❌ 开基础套餐流程失败: {e}")
            return False
    
    def select_unlimited_ip_type(self):
        """选择不限量IP类型（点击输入框方式）"""
        try:
            print("🔍 正在选择不限量IP类型...")
            
            # 步骤1: 等待弹窗完全加载并稳定
            print("步骤1: 等待开套餐弹窗完全加载...")
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-8548a9c6]")))
            time.sleep(2)  # 等待弹窗稳定
            print("✅ 开套餐弹窗已稳定加载")
            
            # 步骤2: 查找IP类型输入框
            print("步骤2: 查找IP类型输入框...")
            
            # 查找所有可能的IP类型输入框
            all_inputs = self.driver.find_elements(By.CSS_SELECTOR, "div[data-v-8548a9c6] input.el-input__inner")
            ip_input = None
            
            # 找到 placeholder="请选择" 的IP类型输入框
            for i, input_elem in enumerate(all_inputs):
                try:
                    placeholder = input_elem.get_attribute("placeholder")
                    value = input_elem.get_attribute("value")
                    if placeholder == "请选择" and input_elem.is_displayed():
                        ip_input = input_elem
                        print(f"✅ 找到IP类型输入框，当前值: '{value}'")
                        break
                except Exception as e:
                    continue
            
            if not ip_input:
                print("❌ 未找到placeholder='请选择'的IP类型输入框")
                return False
            
            # 步骤3: 使用JavaScript点击IP类型输入框避免遮挡
            print("步骤3: 点击IP类型输入框中间...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ip_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", ip_input)
            print("✅ IP类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤4: 查找并选择"不限量"选项
            print("步骤4: 查找并选择'不限量'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li[data-v-8548a9c6].el-select-dropdown__item")
            print(f"   找到 {len(options)} 个选项")
            
            unlimited_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    if "不限量" in option_text and option.is_displayed():
                        unlimited_option = option
                        print(f"✅ 找到不限量选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not unlimited_option:
                print("❌ 未找到不限量选项")
                return False
            
            # 步骤5: 点击不限量选项
            print("步骤5: 点击不限量选项...")
            unlimited_option.click()
            print("✅ 不限量选项选择完成")
            time.sleep(3)  # 等待页面更新，显示时长和带宽下拉框
            
            print("🎉 IP类型成功选择为不限量！")
            return True
            
        except Exception as e:
            print(f"❌ 选择不限量IP类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_unlimited_duration(self):
        """选择不限量套餐时长（点击输入框方式）"""
        try:
            print("🔍 正在选择套餐时长...")
            
            # 步骤1: 查找套餐时长输入框
            print("步骤1: 查找套餐时长输入框...")
            duration_input = None
            duration_selectors = [
                "input[placeholder='请选择套餐时长'].el-input__inner",
                "div[data-v-8548a9c6] input[placeholder='请选择套餐时长']"
            ]
            
            for selector in duration_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "请选择套餐时长":
                            duration_input = input_elem
                            print("✅ 找到套餐时长输入框")
                            break
                    if duration_input:
                        break
                except Exception as e:
                    continue
            
            if not duration_input:
                print("❌ 未找到套餐时长输入框")
                return False
            
            # 步骤2: 使用JavaScript点击时长输入框避免遮挡
            print("步骤2: 点击套餐时长输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", duration_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", duration_input)
            print("✅ 套餐时长输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 随便选择一个时长选项
            print("步骤3: 选择套餐时长选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li[data-v-8548a9c6].el-select-dropdown__item")
            print(f"   找到 {len(options)} 个时长选项")
            
            selected_option = None
            for option in options:
                try:
                    option_text = option.text.strip()
                    if option_text and option.is_displayed():
                        selected_option = option
                        print(f"✅ 选择时长选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not selected_option:
                print("❌ 未找到可选择的时长选项")
                return False
            
            # 步骤4: 点击选择的时长选项
            print("步骤4: 点击选择的时长选项...")
            selected_option.click()
            print("✅ 套餐时长选择完成")
            time.sleep(2)
            
            print("🎉 套餐时长选择完成！")
            return True
            
        except Exception as e:
            print(f"❌ 选择套餐时长失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_unlimited_bandwidth(self):
        """选择不限量套餐带宽（点击输入框方式）"""
        try:
            print("🔍 正在选择套餐带宽...")
            
            # 步骤1: 查找套餐带宽输入框
            print("步骤1: 查找套餐带宽输入框...")
            bandwidth_input = None
            bandwidth_selectors = [
                "input[placeholder='请选择套餐带宽'].el-input__inner",
                "div[data-v-8548a9c6] input[placeholder='请选择套餐带宽']"
            ]
            
            for selector in bandwidth_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "请选择套餐带宽":
                            bandwidth_input = input_elem
                            print("✅ 找到套餐带宽输入框")
                            break
                    if bandwidth_input:
                        break
                except Exception as e:
                    continue
            
            if not bandwidth_input:
                print("❌ 未找到套餐带宽输入框")
                return False
            
            # 步骤2: 使用JavaScript点击带宽输入框避免遮挡
            print("步骤2: 点击套餐带宽输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bandwidth_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", bandwidth_input)
            print("✅ 套餐带宽输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 随便选择一个带宽选项
            print("步骤3: 选择套餐带宽选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li[data-v-8548a9c6].el-select-dropdown__item")
            print(f"   找到 {len(options)} 个带宽选项")
            
            selected_option = None
            for option in options:
                try:
                    option_text = option.text.strip()
                    if option_text and option.is_displayed():
                        selected_option = option
                        print(f"✅ 选择带宽选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not selected_option:
                print("❌ 未找到可选择的带宽选项")
                return False
            
            # 步骤4: 点击选择的带宽选项
            print("步骤4: 点击选择的带宽选项...")
            selected_option.click()
            print("✅ 套餐带宽选择完成")
            time.sleep(2)
            
            print("🎉 套餐带宽选择完成！")
            return True
            
        except Exception as e:
            print(f"❌ 选择套餐带宽失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def open_unlimited_package_flow(self, remark="IPIPGO UI自动化测试"):
        """开不限量套餐的完整流程（特殊流程 - 时长和带宽选择）"""
        try:
            print("\n" + "="*50)
            print("📦 开始开不限量套餐流程")
            print("="*50)
            
            # 步骤1: 点击开套餐按钮
            print("步骤1: 点击开套餐按钮...")
            if not self.click_open_package_button():
                print("❌ 开套餐按钮点击失败")
                return False
            
            # 步骤2: 第一个【套餐类型】保持不变（默认动态住宅）
            print("步骤2: 套餐类型保持默认（动态住宅）...")
            print("✅ 套餐类型无需修改，保持动态住宅")
            time.sleep(1)
            
            # 步骤3: 第二个【IP类型】选择不限量
            print("步骤3: 选择IP类型为不限量...")
            if not self.select_unlimited_ip_type():
                print("❌ IP类型选择失败")
                return False
            
            # 步骤4: 选择套餐时长
            print("步骤4: 选择套餐时长...")
            if not self.select_unlimited_duration():
                print("❌ 套餐时长选择失败")
                return False
            
            # 步骤5: 选择套餐带宽
            print("步骤5: 选择套餐带宽...")
            if not self.select_unlimited_bandwidth():
                print("❌ 套餐带宽选择失败")
                return False
            
            # 步骤6: 输入备注信息
            print("步骤6: 输入备注信息...")
            if not self.enter_remark_info(remark):
                print("❌ 备注信息输入失败")
                return False
            
            # 步骤7: 点击确定按钮
            print("步骤7: 点击确定按钮...")
            if not self.click_confirm_button_in_package_dialog():
                print("❌ 确定按钮点击失败")
                return False
            
            # 步骤8: 支付操作
            print("步骤8: 开始支付操作...")
            if not self.complete_payment_flow():
                print("❌ 支付操作失败")
                return False
            
            print("="*50)
            print("🎉 不限量套餐+支付流程成功完成！")
            print("="*50)
            return True
        except Exception as e:
            print(f"❌ 开不限量套餐流程失败: {e}")
            return False
    
    def test_locate_ip_type_dropdown(self):
        """测试定位IP类型下拉箭头的方法"""
        try:
            print("🔍 开始测试定位IP类型下拉箭头...")
            
            # 等待弹窗加载
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-8548a9c6]")))
            time.sleep(2)
            
            # 查找所有可能的下拉容器
            print("\n📋 查找所有下拉容器...")
            all_selects = self.driver.find_elements(By.CSS_SELECTOR, "div[data-v-8548a9c6].el-select")
            print(f"找到 {len(all_selects)} 个下拉容器")
            
            for i, select in enumerate(all_selects):
                try:
                    input_elem = select.find_element(By.CSS_SELECTOR, "input.el-input__inner")
                    placeholder = input_elem.get_attribute("placeholder")
                    value = input_elem.get_attribute("value")
                    print(f"容器 {i+1}: placeholder='{placeholder}', value='{value}'")
                    
                    # 查找下拉箭头
                    try:
                        arrow = select.find_element(By.CSS_SELECTOR, "i.el-select__caret")
                        arrow_classes = arrow.get_attribute("class")
                        print(f"   箭头类名: {arrow_classes}")
                        
                        # 检查是否是IP类型（placeholder="请选择"且有默认值）
                        if placeholder == "请选择" and value:
                            print(f"   ⭐ 这可能是IP类型下拉框！值='{value}'")
                            return select, arrow
                    except:
                        print(f"   ❌ 容器 {i+1} 没有找到下拉箭头")
                        
                except Exception as e:
                    print(f"   ❌ 容器 {i+1} 解析失败: {e}")
                    
            print("❌ 未找到IP类型下拉箭头")
            return None, None
            
        except Exception as e:
            print(f"❌ 测试定位失败: {e}")
            return None, None 

    def debug_dialog_inputs(self):
        """调试弹窗中的所有输入框"""
        try:
            print("🔍 开始调试弹窗中的所有输入框...")
            
            # 等待弹窗加载
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-8548a9c6]")))
            time.sleep(2)
            
            # 查找所有输入框
            all_inputs = self.driver.find_elements(By.CSS_SELECTOR, "div[data-v-8548a9c6] input.el-input__inner")
            print(f"📋 找到 {len(all_inputs)} 个输入框:")
            
            for i, input_elem in enumerate(all_inputs):
                try:
                    placeholder = input_elem.get_attribute("placeholder") or "无"
                    value = input_elem.get_attribute("value") or "空"
                    readonly = input_elem.get_attribute("readonly")
                    display = input_elem.is_displayed()
                    
                    print(f"输入框 {i+1}:")
                    print(f"  placeholder: '{placeholder}'")
                    print(f"  value: '{value}'")
                    print(f"  readonly: {readonly}")
                    print(f"  显示状态: {display}")
                    print(f"  位置: {input_elem.location}")
                    print("---")
                    
                except Exception as e:
                    print(f"输入框 {i+1}: 读取失败 - {e}")
                    
            return True
            
        except Exception as e:
            print(f"❌ 调试失败: {e}")
            return False 
    
    def select_static_package_type(self):
        """选择静态代理套餐类型（第一个下拉框）"""
        try:
            print("🔍 正在选择静态代理套餐类型...")
            
            # 步骤1: 等待弹窗完全加载并稳定
            print("步骤1: 等待开套餐弹窗完全加载...")
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-8548a9c6], div[data-v-78b06e16]")))
            time.sleep(2)  # 等待弹窗稳定
            print("✅ 开套餐弹窗已稳定加载")
            
            # 步骤2: 查找套餐类型输入框（第一个下拉框）
            print("步骤2: 查找套餐类型输入框...")
            package_type_input = None
            
            # 查找所有可能的套餐类型输入框
            type_selectors = [
                "input[placeholder='选择套餐'].el-input__inner",
                "div[data-v-8548a9c6] input[placeholder='选择套餐']",
                "div[data-v-78b06e16] input[placeholder='选择套餐']"
            ]
            
            for selector in type_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    # 获取第一个匹配的输入框（套餐类型）
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "选择套餐":
                            package_type_input = input_elem
                            current_value = input_elem.get_attribute("value")
                            print(f"✅ 找到套餐类型输入框，当前值: '{current_value}'")
                            break
                    if package_type_input:
                        break
                except Exception as e:
                    continue
            
            if not package_type_input:
                print("❌ 未找到套餐类型输入框")
                return False
            
            # 步骤3: 使用JavaScript点击套餐类型输入框避免遮挡
            print("步骤3: 点击套餐类型输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", package_type_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", package_type_input)
            print("✅ 套餐类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤4: 查找并选择"静态代理"选项
            print("步骤4: 查找并选择'静态代理'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个套餐类型选项")
            
            static_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    print(f"   选项 {i+1}: '{option_text}'")
                    if "静态代理" in option_text and option.is_displayed():
                        static_option = option
                        print(f"✅ 找到静态代理选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not static_option:
                print("❌ 未找到静态代理选项")
                return False
            
            # 步骤5: 点击静态代理选项
            print("步骤5: 点击静态代理选项...")
            static_option.click()
            print("✅ 静态代理选项选择完成")
            time.sleep(3)  # 等待页面更新，显示对应的IP类型选项
            
            print("🎉 套餐类型成功选择为静态代理！")
            return True
            
        except Exception as e:
            print(f"❌ 选择静态代理套餐类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_hosting_ip_type(self):
        """选择Hosting IP类型（第二个下拉框）"""
        try:
            print("🔍 正在选择Hosting IP类型...")
            
            # 步骤1: 查找IP类型输入框
            print("步骤1: 查找IP类型输入框...")
            ip_type_input = None
            
            # 查找IP类型输入框
            ip_selectors = [
                "input[placeholder='选择IP类型'].el-input__inner",
                "div[data-v-78b06e16] input[placeholder='选择IP类型']",
                "div[data-v-8548a9c6] input[placeholder='选择IP类型']"
            ]
            
            for selector in ip_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "选择IP类型":
                            ip_type_input = input_elem
                            print("✅ 找到IP类型输入框")
                            break
                    if ip_type_input:
                        break
                except Exception as e:
                    continue
            
            if not ip_type_input:
                print("❌ 未找到IP类型输入框")
                return False
            
            # 步骤2: 使用JavaScript点击IP类型输入框避免遮挡
            print("步骤2: 点击IP类型输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ip_type_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", ip_type_input)
            print("✅ IP类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 查找并选择"Hosting"选项
            print("步骤3: 查找并选择'Hosting'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个IP类型选项")
            
            hosting_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    print(f"   选项 {i+1}: '{option_text}'")
                    if "Hosting" in option_text and option.is_displayed():
                        hosting_option = option
                        print(f"✅ 找到Hosting选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not hosting_option:
                print("❌ 未找到Hosting选项")
                return False
            
            # 步骤4: 点击Hosting选项
            print("步骤4: 点击Hosting选项...")
            hosting_option.click()
            print("✅ Hosting选项选择完成")
            time.sleep(2)
            
            print("🎉 IP类型成功选择为Hosting！")
            return True
            
        except Exception as e:
            print(f"❌ 选择Hosting IP类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_static_package(self):
        """选择静态套餐（第三个下拉框）"""
        try:
            print("🔍 正在选择静态套餐...")
            
            # 步骤1: 查找选择套餐输入框（第三个下拉框）
            print("步骤1: 查找选择套餐输入框...")
            package_input = None
            
            # 方法1: 先尝试查找所有placeholder="选择套餐"的输入框
            package_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder='选择套餐'].el-input__inner")
            print(f"   找到 {len(package_inputs)} 个'选择套餐'输入框")
            
            if len(package_inputs) >= 2:
                package_input = package_inputs[1]  # 第二个"选择套餐"输入框（第三个下拉框）
                print("✅ 找到静态套餐选择输入框（第三个下拉框 - 多套餐模式）")
            elif len(package_inputs) == 1:
                # 静态代理模式下，只有一个"选择套餐"输入框，就是第三个下拉框
                package_input = package_inputs[0]  # 唯一的"选择套餐"输入框
                print("✅ 找到静态套餐选择输入框（静态代理模式 - 单套餐模式）")
            else:
                print(f"❌ 只找到 {len(package_inputs)} 个'选择套餐'输入框，无法确定第三个")
                return False
            
            # 步骤2: 使用JavaScript点击套餐输入框避免遮挡
            print("步骤2: 点击静态套餐输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", package_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", package_input)
            print("✅ 静态套餐输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 随便选择一个静态套餐选项
            print("步骤3: 选择静态套餐选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个静态套餐选项")
            
            selected_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    if option_text and option.is_displayed():
                        selected_option = option
                        print(f"✅ 选择静态套餐选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not selected_option:
                print("❌ 未找到可选择的静态套餐选项")
                return False
            
            # 步骤4: 点击选择的静态套餐选项
            print("步骤4: 点击选择的静态套餐选项...")
            selected_option.click()
            print("✅ 静态套餐选择完成")
            time.sleep(2)
            
            print("🎉 静态套餐选择完成！")
            return True
            
        except Exception as e:
            print(f"❌ 选择静态套餐失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def click_add_region_button(self):
        """点击添加地区按钮（加号按钮）"""
        try:
            print("🔍 正在查找并点击添加地区按钮...")
            
            # 步骤1: 等待静态套餐选择完成后，页面状态稳定
            print("步骤1: 等待页面状态稳定...")
            time.sleep(3)
            
            # 步骤2: 打印当前页面状态用于调试
            print("步骤2: 调试当前页面状态...")
            
            # 查找所有加号按钮
            all_plus_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".el-icon-plus, em[class*='plus'], i[class*='plus']")
            print(f"   找到 {len(all_plus_buttons)} 个加号按钮")
            
            for i, btn in enumerate(all_plus_buttons):
                try:
                    btn_class = btn.get_attribute("class")
                    btn_tag = btn.tag_name
                    btn_visible = btn.is_displayed()
                    btn_location = btn.location
                    
                    # 获取按钮周围的文本内容
                    try:
                        parent_element = btn.find_element(By.XPATH, "./..")
                        surrounding_text = parent_element.text[:100]
                    except:
                        surrounding_text = "无法获取"
                    
                    print(f"   加号按钮 {i+1}: tag={btn_tag}, class='{btn_class}', visible={btn_visible}")
                    print(f"     位置: x={btn_location['x']}, y={btn_location['y']}")
                    print(f"     周围文本: '{surrounding_text}'")
                    print("     ---")
                except Exception as e:
                    print(f"   加号按钮 {i+1}: 分析失败 - {e}")
            
            # 步骤3: 更精确地查找地区加号按钮
            print("步骤3: 查找地区加号按钮...")
            add_button = None
            
            # 优先查找在静态代理弹窗内的特定加号按钮
            specific_selectors = [
                "em[data-v-78b06e16].el-icon-plus.add-first",
                "div[data-v-78b06e16] em.el-icon-plus.add-first",
                "em.el-icon-plus.add-first"
            ]
            
            for i, selector in enumerate(specific_selectors):
                try:
                    print(f"   尝试选择器 {i+1}: {selector}")
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"   找到 {len(buttons)} 个匹配的按钮")
                    
                    for j, button in enumerate(buttons):
                        try:
                            if button.is_displayed() and button.is_enabled():
                                button_classes = button.get_attribute("class")
                                button_tag = button.tag_name
                                button_location = button.location
                                
                                print(f"     按钮 {j+1}: tag={button_tag}, classes='{button_classes}'")
                                print(f"     位置: x={button_location['x']}, y={button_location['y']}")
                                
                                # 获取按钮周围的上下文，确认这是地区相关的按钮
                                try:
                                    # 查找按钮的容器，看是否包含地区相关信息
                                    container = button
                                    for _ in range(5):  # 向上查找5层
                                        container = container.find_element(By.XPATH, "./..")
                                        container_text = container.text
                                        if "地区" in container_text or "区域" in container_text:
                                            print(f"     ✅ 确认为地区相关按钮")
                                            add_button = button
                                            break
                                        elif len(container_text) > 200:  # 如果文本太长，说明可能是整个弹窗
                                            break
                                except:
                                    pass
                                
                                # 如果上面的方法没找到，但按钮符合基本条件，也可以作为候选
                                if not add_button and button_tag == "em" and "el-icon-plus" in button_classes and "add-first" in button_classes:
                                    add_button = button
                                    print(f"     候选地区按钮: {selector}")
                        except Exception as e:
                            print(f"     按钮 {j+1} 分析失败: {e}")
                            continue
                    
                    if add_button:
                        print(f"✅ 选定地区加号按钮: {selector}")
                        break
                except Exception as e:
                    print(f"   选择器 {selector} 失败: {e}")
                    continue
            
            if not add_button:
                print("❌ 未找到地区加号按钮")
                return False
            
            # 步骤4: 点击地区加号按钮
            print("步骤4: 点击地区加号按钮...")
            
            # 滚动到按钮位置
            print("   滚动到按钮位置...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
            time.sleep(1)
            
            # 点击前记录按钮状态
            btn_location = add_button.location
            print(f"   点击前按钮位置: x={btn_location['x']}, y={btn_location['y']}")
            
            # 使用JavaScript点击
            print("   使用JavaScript点击地区加号按钮...")
            self.driver.execute_script("arguments[0].click();", add_button)
            print("✅ 地区加号按钮点击完成")
            
            # 步骤5: 验证地区选择区域是否出现
            print("步骤5: 验证地区选择区域是否出现...")
            time.sleep(3)  # 等待地区选择区域出现
            
            # 检查是否有新的输入框出现
            before_inputs = len(self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder='请选择']"))
            print(f"   当前 placeholder='请选择' 的输入框数量: {before_inputs}")
            
            # 检查是否有地区相关的文本出现
            page_text = self.driver.page_source
            region_keywords = ["地区", "区域", "IP数量", "选择地区"]
            found_keywords = [keyword for keyword in region_keywords if keyword in page_text]
            print(f"   找到地区相关关键词: {found_keywords}")
            
            # 检查弹窗内容是否发生变化
            dialog_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-v-78b06e16]")
            if dialog_elements:
                dialog_text = dialog_elements[0].text
                print(f"   弹窗当前内容: '{dialog_text[:200]}...'")
                
                if any(keyword in dialog_text for keyword in region_keywords):
                    print("✅ 地区选择区域已出现")
                    return True
                else:
                    print("⚠️ 弹窗内容未包含地区相关信息")
            
            # 如果上面的验证都没通过，但有新输入框出现，也认为成功
            if before_inputs > 0:
                print("✅ 有新的输入框出现，认为地区选择区域已出现")
                return True
            else:
                print("❌ 地区选择区域可能未出现")
                return False
            
        except Exception as e:
            print(f"❌ 点击地区加号按钮失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_available_region(self):
        """选择可用地区（括号里数字不为0的地区）"""
        try:
            print("🔍 正在选择可用地区...")
            
            # 步骤1: 使用特殊类名精确定位地区选择输入框
            print("步骤1: 查找地区选择输入框...")
            region_input = None
            
            # 等待页面稳定
            time.sleep(2)
            
            # 使用contry-select类名精确定位地区选择框
            region_selectors = [
                ".el-select.contry-select input[placeholder='请选择']",
                "div.contry-select input.el-input__inner",
                ".contry-select input[placeholder='请选择']"
            ]
            
            print("   使用contry-select类名定位地区选择框...")
            for i, selector in enumerate(region_selectors):
                try:
                    print(f"   尝试选择器 {i+1}: {selector}")
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"   找到 {len(inputs)} 个匹配的输入框")
                    
                    for j, input_elem in enumerate(inputs):
                        try:
                            if input_elem.is_displayed():
                                placeholder = input_elem.get_attribute("placeholder")
                                parent_classes = input_elem.find_element(By.XPATH, "../..").get_attribute("class")
                                print(f"     输入框 {j+1}: placeholder='{placeholder}'")
                                print(f"     父容器类: '{parent_classes}'")
                                
                                if placeholder == "请选择" and "contry-select" in parent_classes:
                                    region_input = input_elem
                                    print(f"✅ 找到地区选择输入框: {selector}")
                                    break
                        except Exception as e:
                            print(f"     输入框 {j+1} 分析失败: {e}")
                            continue
                    
                    if region_input:
                        break
                except Exception as e:
                    print(f"   选择器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，显示所有contry-select相关的元素
            if not region_input:
                print("⚠️ 未找到地区选择输入框，调试所有contry-select相关元素...")
                contry_elements = self.driver.find_elements(By.CSS_SELECTOR, ".contry-select, [class*='contry']")
                print(f"   找到 {len(contry_elements)} 个contry相关元素")
                
                for i, elem in enumerate(contry_elements):
                    try:
                        elem_classes = elem.get_attribute("class")
                        elem_tag = elem.tag_name
                        elem_visible = elem.is_displayed()
                        print(f"   contry元素 {i+1}: tag={elem_tag}, class='{elem_classes}', visible={elem_visible}")
                        
                        # 查找该元素内的输入框
                        inputs_in_elem = elem.find_elements(By.CSS_SELECTOR, "input")
                        for input_elem in inputs_in_elem:
                            if input_elem.is_displayed():
                                placeholder = input_elem.get_attribute("placeholder")
                                if placeholder == "请选择":
                                    region_input = input_elem
                                    print(f"✅ 在contry元素内找到地区选择输入框")
                                    break
                        if region_input:
                            break
                    except Exception as e:
                        print(f"   contry元素 {i+1} 分析失败: {e}")
                        continue
            
            if not region_input:
                print("❌ 未找到地区选择输入框")
                return False
            
            # 步骤2: 验证这是正确的地区选择框
            print("步骤2: 验证地区选择框...")
            try:
                parent_container = region_input.find_element(By.XPATH, "../..")
                container_classes = parent_container.get_attribute("class")
                print(f"   父容器类名: '{container_classes}'")
                
                if "contry-select" in container_classes:
                    print("✅ 确认这是地区选择框（包含contry-select类）")
                else:
                    print("⚠️ 警告：父容器不包含contry-select类")
            except:
                print("   无法验证父容器类名")
            
            # 步骤3: 点击地区选择输入框打开下拉选项
            print("步骤3: 点击地区选择输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_input)
            time.sleep(1)
            print("   使用JavaScript点击地区选择输入框...")
            self.driver.execute_script("arguments[0].click();", region_input)
            print("✅ 地区选择输入框点击完成，下拉选项应该已打开")
            time.sleep(3)  # 等待下拉选项完全显示
            
            # 步骤4: 查找地区选项（优先查找data-v-78b06e16的选项）
            print("步骤4: 查找地区选项...")
            
            option_selectors = [
                "li[data-v-78b06e16].el-select-dropdown__item",  # 优先选择器：静态代理弹窗的选项
                "li.el-select-dropdown__item",  # 标准选择器
                ".el-select-dropdown__item"    # 类选择器
            ]
            
            options = []
            for selector in option_selectors:
                try:
                    found_options = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found_options:
                        options = found_options
                        print(f"✅ 使用选择器 '{selector}' 找到 {len(options)} 个地区选项")
                        break
                except Exception as e:
                    continue
            
            if not options:
                print("❌ 未找到任何地区选项")
                return False
            
            # 步骤5: 分析并选择可用地区
            print("步骤5: 分析地区选项...")
            available_option = None
            
            for i, option in enumerate(options):
                try:
                    if not option.is_displayed():
                        continue
                        
                    option_text = option.text.strip()
                    print(f"   地区选项 {i+1}: '{option_text}'")
                    
                    if not option_text:
                        continue
                    
                    # 检查括号里的数字是否不为0
                    import re
                    match = re.search(r'\((\d+)\)', option_text)
                    if match:
                        count = int(match.group(1))
                        if count > 0:
                            available_option = option
                            print(f"✅ 找到可用地区: '{option_text}' (可用数量: {count})")
                            break
                        else:
                            print(f"   跳过地区: '{option_text}' (数量为0)")
                    else:
                        # 如果没有括号，检查是否是有用的地区名称
                        if option_text and len(option_text) > 1:
                            available_option = option
                            print(f"✅ 找到地区选项: '{option_text}' (无数量限制)")
                            break
                except Exception as e:
                    print(f"   分析选项 {i+1} 时出错: {e}")
                    continue
            
            if not available_option:
                print("❌ 未找到可用的地区选项")
                return False
            
            # 步骤6: 点击选择的地区选项
            print("步骤6: 点击选择的地区选项...")
            selected_text = available_option.text.strip()
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", available_option)
            time.sleep(1)
            
            print(f"   使用JavaScript点击地区选项: '{selected_text}'")
            self.driver.execute_script("arguments[0].click();", available_option)
            print("✅ 地区选择完成")
            time.sleep(2)
            
            print(f"🎉 可用地区选择完成: {selected_text}")
            return True
            
        except Exception as e:
            print(f"❌ 选择可用地区失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def enter_static_remark_info(self, remark="IPIPGO UI自动化测试"):
        """在静态代理套餐的备注信息输入框中输入内容"""
        try:
            print(f"🔍 正在输入静态代理套餐备注信息: '{remark}'...")
            
            # 步骤1: 查找备注信息输入框
            print("步骤1: 查找备注信息输入框...")
            remark_textarea = None
            
            # 查找备注输入框（针对静态代理套餐的data-v-78b06e16）
            remark_selectors = [
                "div[data-v-78b06e16] textarea.el-textarea__inner",
                "textarea.el-textarea__inner",
                "div.el-textarea textarea"
            ]
            
            for selector in remark_selectors:
                try:
                    textareas = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for textarea in textareas:
                        if textarea.is_displayed():
                            remark_textarea = textarea
                            print("✅ 找到静态代理套餐备注信息输入框")
                            break
                    if remark_textarea:
                        break
                except Exception as e:
                    continue
            
            if not remark_textarea:
                print("❌ 未找到静态代理套餐备注信息输入框")
                return False
            
            # 步骤2: 清空并输入备注信息
            print("步骤2: 清空并输入备注信息...")
            remark_textarea.clear()
            time.sleep(0.5)
            remark_textarea.send_keys(remark)
            print(f"✅ 备注信息输入完成: '{remark}'")
            time.sleep(1)
            
            print("🎉 静态代理套餐备注信息输入成功！")
            return True
            
        except Exception as e:
            print(f"❌ 输入静态代理套餐备注信息失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def click_static_confirm_button(self):
        """点击静态代理套餐的确定按钮"""
        try:
            print("🔍 正在查找并点击静态代理套餐确定按钮...")
            
            # 步骤1: 查找确定按钮
            print("步骤1: 查找确定按钮...")
            confirm_button = None
            
            # 查找确定按钮（针对静态代理套餐的data-v-78b06e16）
            confirm_selectors = [
                "button[data-v-78b06e16].el-button.el-button--primary.el-button--medium",
                "div[data-v-78b06e16] button.el-button--primary",
                "button.el-button--primary span:contains('确定')",
                "button.el-button--primary"
            ]
            
            for selector in confirm_selectors:
                try:
                    if ":contains" in selector:
                        # 使用xpath查找包含"确定"文本的按钮
                        buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'el-button--primary')]//span[text()='确定']/..")
                    else:
                        buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for button in buttons:
                        if button.is_displayed():
                            button_text = button.text.strip()
                            if "确定" in button_text:
                                confirm_button = button
                                print(f"✅ 找到静态代理套餐确定按钮: '{button_text}'")
                                break
                    if confirm_button:
                        break
                except Exception as e:
                    continue
            
            if not confirm_button:
                print("❌ 未找到静态代理套餐确定按钮")
                return False
            
            # 步骤2: 使用JavaScript点击确定按钮避免遮挡
            print("步骤2: 点击静态代理套餐确定按钮...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_button)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", confirm_button)
            print("✅ 静态代理套餐确定按钮点击完成")
            time.sleep(3)  # 等待弹窗关闭，跳转到支付页面
            
            print("🎉 静态代理套餐确定按钮点击成功！")
            return True
            
        except Exception as e:
            print(f"❌ 点击静态代理套餐确定按钮失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def open_static_package_flow(self, remark="IPIPGO UI自动化测试"):
        """开静态代理套餐的完整流程（特殊流程 - 包含地区选择）"""
        try:
            print("\n" + "="*50)
            print("📦 开始开静态代理套餐流程")
            print("="*50)
            
            # 步骤1: 点击开套餐按钮
            print("步骤1: 点击开套餐按钮...")
            if not self.click_open_package_button():
                print("❌ 开套餐按钮点击失败")
                return False
            
            # 步骤2: 选择套餐类型为"静态代理"
            print("步骤2: 选择套餐类型为静态代理...")
            if not self.select_static_package_type():
                print("❌ 静态代理套餐类型选择失败")
                return False
            
            # 步骤3: 选择IP类型为"Hosting"
            print("步骤3: 选择IP类型为Hosting...")
            if not self.select_hosting_ip_type():
                print("❌ Hosting IP类型选择失败")
                return False
            
            # 步骤4: 选择静态套餐
            print("步骤4: 选择静态套餐...")
            if not self.select_static_package():
                print("❌ 静态套餐选择失败")
                return False
            
            # 步骤5: 点击添加地区按钮
            print("步骤5: 点击添加地区按钮...")
            if not self.click_add_region_button():
                print("❌ 添加地区按钮点击失败")
                return False
            
            # 步骤6: 选择可用地区
            print("步骤6: 选择可用地区...")
            if not self.select_available_region():
                print("❌ 可用地区选择失败")
                return False
            
            # 步骤7: 输入备注信息
            print("步骤7: 输入备注信息...")
            if not self.enter_static_remark_info(remark):
                print("❌ 备注信息输入失败")
                return False
            
            # 步骤8: 点击确定按钮
            print("步骤8: 点击确定按钮...")
            if not self.click_static_confirm_button():
                print("❌ 确定按钮点击失败")
                return False
            
            # 步骤9: 支付操作
            print("步骤9: 开始支付操作...")
            if not self.complete_payment_flow():
                print("❌ 支付操作失败")
                return False
            
            print("="*50)
            print("🎉 静态代理套餐+支付流程成功完成！")
            print("="*50)
            return True
        except Exception as e:
            print(f"❌ 开静态代理套餐流程失败: {e}")
            return False
    
    def select_isp_ip_type(self):
        """选择ISP IP类型（第二个下拉框）"""
        try:
            print("🔍 正在选择ISP IP类型...")
            
            # 步骤1: 查找IP类型输入框
            print("步骤1: 查找IP类型输入框...")
            ip_type_input = None
            
            # 查找IP类型输入框
            ip_selectors = [
                "input[placeholder='选择IP类型'].el-input__inner",
                "div[data-v-78b06e16] input[placeholder='选择IP类型']",
                "div[data-v-8548a9c6] input[placeholder='选择IP类型']"
            ]
            
            for selector in ip_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "选择IP类型":
                            ip_type_input = input_elem
                            print("✅ 找到IP类型输入框")
                            break
                    if ip_type_input:
                        break
                except Exception as e:
                    continue
            
            if not ip_type_input:
                print("❌ 未找到IP类型输入框")
                return False
            
            # 步骤2: 使用JavaScript点击IP类型输入框避免遮挡
            print("步骤2: 点击IP类型输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ip_type_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", ip_type_input)
            print("✅ IP类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 查找并选择"ISP"选项
            print("步骤3: 查找并选择'ISP'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个IP类型选项")
            
            isp_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    print(f"   选项 {i+1}: '{option_text}'")
                    if "ISP" in option_text and option.is_displayed():
                        isp_option = option
                        print(f"✅ 找到ISP选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not isp_option:
                print("❌ 未找到ISP选项")
                return False
            
            # 步骤4: 点击ISP选项
            print("步骤4: 点击ISP选项...")
            isp_option.click()
            print("✅ ISP选项选择完成")
            time.sleep(2)
            
            print("🎉 IP类型成功选择为ISP！")
            return True
            
        except Exception as e:
            print(f"❌ 选择ISP IP类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def open_static_isp_package_flow(self, remark="IPIPGO UI自动化测试"):
        """开静态代理ISP套餐的完整流程（特殊流程 - 包含地区选择）"""
        try:
            print("\n" + "="*50)
            print("📦 开始开静态代理ISP套餐流程")
            print("="*50)
            
            # 步骤1: 点击开套餐按钮
            print("步骤1: 点击开套餐按钮...")
            if not self.click_open_package_button():
                print("❌ 开套餐按钮点击失败")
                return False
            
            # 步骤2: 选择套餐类型为"静态代理"
            print("步骤2: 选择套餐类型为静态代理...")
            if not self.select_static_package_type():
                print("❌ 静态代理套餐类型选择失败")
                return False
            
            # 步骤3: 选择IP类型为"ISP"
            print("步骤3: 选择IP类型为ISP...")
            if not self.select_isp_ip_type():
                print("❌ ISP IP类型选择失败")
                return False
            
            # 步骤4: 选择静态套餐
            print("步骤4: 选择静态套餐...")
            if not self.select_static_package():
                print("❌ 静态套餐选择失败")
                return False
            
            # 步骤5: 点击添加地区按钮
            print("步骤5: 点击添加地区按钮...")
            if not self.click_add_region_button():
                print("❌ 添加地区按钮点击失败")
                return False
            
            # 步骤6: 选择可用地区
            print("步骤6: 选择可用地区...")
            if not self.select_available_region():
                print("❌ 可用地区选择失败")
                return False
            
            # 步骤7: 输入备注信息
            print("步骤7: 输入备注信息...")
            if not self.enter_static_remark_info(remark):
                print("❌ 备注信息输入失败")
                return False
            
            # 步骤8: 点击确定按钮
            print("步骤8: 点击确定按钮...")
            if not self.click_static_confirm_button():
                print("❌ 确定按钮点击失败")
                return False
            
            # 步骤9: 支付操作
            print("步骤9: 开始支付操作...")
            if not self.complete_payment_flow():
                print("❌ 支付操作失败")
                return False
            
            print("="*50)
            print("🎉 静态代理ISP套餐+支付流程成功完成！")
            print("="*50)
            return True
        except Exception as e:
            print(f"❌ 开静态代理ISP套餐流程失败: {e}")
            return False
    
    def select_dual_isp_ip_type(self):
        """选择双ISP IP类型（第二个下拉框）"""
        try:
            print("🔍 正在选择双ISP IP类型...")
            
            # 步骤1: 查找IP类型输入框
            print("步骤1: 查找IP类型输入框...")
            ip_type_input = None
            
            # 查找IP类型输入框
            ip_selectors = [
                "input[placeholder='选择IP类型'].el-input__inner",
                "div[data-v-78b06e16] input[placeholder='选择IP类型']",
                "div[data-v-8548a9c6] input[placeholder='选择IP类型']"
            ]
            
            for selector in ip_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "选择IP类型":
                            ip_type_input = input_elem
                            print("✅ 找到IP类型输入框")
                            break
                    if ip_type_input:
                        break
                except Exception as e:
                    continue
            
            if not ip_type_input:
                print("❌ 未找到IP类型输入框")
                return False
            
            # 步骤2: 使用JavaScript点击IP类型输入框避免遮挡
            print("步骤2: 点击IP类型输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ip_type_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", ip_type_input)
            print("✅ IP类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 查找并选择"双ISP"选项
            print("步骤3: 查找并选择'双ISP'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个IP类型选项")
            
            dual_isp_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    print(f"   选项 {i+1}: '{option_text}'")
                    if "双ISP" in option_text and option.is_displayed():
                        dual_isp_option = option
                        print(f"✅ 找到双ISP选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not dual_isp_option:
                print("❌ 未找到双ISP选项")
                return False
            
            # 步骤4: 点击双ISP选项
            print("步骤4: 点击双ISP选项...")
            dual_isp_option.click()
            print("✅ 双ISP选项选择完成")
            time.sleep(2)
            
            print("🎉 IP类型成功选择为双ISP！")
            return True
            
        except Exception as e:
            print(f"❌ 选择双ISP IP类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def open_static_dual_isp_package_flow(self, remark="IPIPGO UI自动化测试"):
        """开静态代理双ISP套餐的完整流程（特殊流程 - 包含地区选择）"""
        try:
            print("\n" + "="*50)
            print("📦 开始开静态代理双ISP套餐流程")
            print("="*50)
            
            # 步骤1: 点击开套餐按钮
            print("步骤1: 点击开套餐按钮...")
            if not self.click_open_package_button():
                print("❌ 开套餐按钮点击失败")
                return False
            
            # 步骤2: 选择套餐类型为"静态代理"
            print("步骤2: 选择套餐类型为静态代理...")
            if not self.select_static_package_type():
                print("❌ 静态代理套餐类型选择失败")
                return False
            
            # 步骤3: 选择IP类型为"双ISP"
            print("步骤3: 选择IP类型为双ISP...")
            if not self.select_dual_isp_ip_type():
                print("❌ 双ISP IP类型选择失败")
                return False
            
            # 步骤4: 选择静态套餐
            print("步骤4: 选择静态套餐...")
            if not self.select_static_package():
                print("❌ 静态套餐选择失败")
                return False
            
            # 步骤5: 点击添加地区按钮
            print("步骤5: 点击添加地区按钮...")
            if not self.click_add_region_button():
                print("❌ 添加地区按钮点击失败")
                return False
            
            # 步骤6: 选择可用地区
            print("步骤6: 选择可用地区...")
            if not self.select_available_region():
                print("❌ 可用地区选择失败")
                return False
            
            # 步骤7: 输入备注信息
            print("步骤7: 输入备注信息...")
            if not self.enter_static_remark_info(remark):
                print("❌ 备注信息输入失败")
                return False
            
            # 步骤8: 点击确定按钮
            print("步骤8: 点击确定按钮...")
            if not self.click_static_confirm_button():
                print("❌ 确定按钮点击失败")
                return False
            
            # 步骤9: 支付操作
            print("步骤9: 开始支付操作...")
            if not self.complete_payment_flow():
                print("❌ 支付操作失败")
                return False
            
            print("="*50)
            print("🎉 静态代理双ISP套餐+支付流程成功完成！")
            print("="*50)
            return True
        except Exception as e:
            print(f"❌ 开静态代理双ISP套餐流程失败: {e}")
            return False
    
    def select_exclusive_static_package_type(self):
        """选择独享静态套餐类型（第一个下拉框）"""
        try:
            print("🔍 正在选择独享静态套餐类型...")
            
            # 步骤1: 查找套餐类型输入框
            print("步骤1: 查找套餐类型输入框...")
            package_type_input = None
            
            # 多种选择器尝试查找套餐类型输入框
            type_selectors = [
                "input[placeholder='选择套餐'].el-input__inner",
                "div[data-v-8548a9c6] input[placeholder='选择套餐']",
                "div[data-v-78b06e16] input[placeholder='选择套餐']"
            ]
            
            for selector in type_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "选择套餐":
                            package_type_input = input_elem
                            print("✅ 找到套餐类型输入框")
                            break
                    if package_type_input:
                        break
                except Exception as e:
                    continue
            
            if not package_type_input:
                print("❌ 未找到套餐类型输入框")
                return False
            
            # 步骤2: 点击套餐类型输入框
            print("步骤2: 点击套餐类型输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", package_type_input)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", package_type_input)
            print("✅ 套餐类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 查找并选择"独享静态"选项
            print("步骤3: 查找并选择'独享静态'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个套餐类型选项")
            
            exclusive_static_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    print(f"   选项 {i+1}: '{option_text}'")
                    if "独享静态" in option_text and option.is_displayed():
                        exclusive_static_option = option
                        print(f"✅ 找到独享静态选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not exclusive_static_option:
                print("❌ 未找到独享静态选项")
                return False
            
            # 步骤4: 点击独享静态选项
            print("步骤4: 点击独享静态选项...")
            exclusive_static_option.click()
            print("✅ 独享静态选项选择完成")
            time.sleep(2)
            
            print("🎉 套餐类型成功选择为独享静态！")
            return True
            
        except Exception as e:
            print(f"❌ 选择独享静态套餐类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_tiktok_solution_ip_type(self):
        """选择TikTok解决方案IP类型（第二个下拉框）"""
        try:
            print("🔍 正在选择TikTok解决方案IP类型...")
            
            # 步骤1: 查找IP类型输入框
            print("步骤1: 查找IP类型输入框...")
            ip_type_input = None
            
            # 查找IP类型输入框
            ip_selectors = [
                "input[placeholder='选择IP类型'].el-input__inner",
                "div[data-v-78b06e16] input[placeholder='选择IP类型']",
                "div[data-v-8548a9c6] input[placeholder='选择IP类型']"
            ]
            
            for selector in ip_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "选择IP类型":
                            ip_type_input = input_elem
                            print("✅ 找到IP类型输入框")
                            break
                    if ip_type_input:
                        break
                except Exception as e:
                    continue
            
            if not ip_type_input:
                print("❌ 未找到IP类型输入框")
                return False
            
            # 步骤2: 使用JavaScript点击IP类型输入框避免遮挡
            print("步骤2: 点击IP类型输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ip_type_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", ip_type_input)
            print("✅ IP类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 查找并选择"TikTok解决方案"选项
            print("步骤3: 查找并选择'TikTok解决方案'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个IP类型选项")
            
            tiktok_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    print(f"   选项 {i+1}: '{option_text}'")
                    if "TikTok解决方案" in option_text and option.is_displayed():
                        tiktok_option = option
                        print(f"✅ 找到TikTok解决方案选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not tiktok_option:
                print("❌ 未找到TikTok解决方案选项")
                return False
            
            # 步骤4: 点击TikTok解决方案选项
            print("步骤4: 点击TikTok解决方案选项...")
            tiktok_option.click()
            print("✅ TikTok解决方案选项选择完成")
            time.sleep(2)
            
            print("🎉 IP类型成功选择为TikTok解决方案！")
            return True
            
        except Exception as e:
            print(f"❌ 选择TikTok解决方案IP类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_exclusive_static_package(self):
        """选择独享静态套餐（第三个下拉框）"""
        try:
            print("🔍 正在选择独享静态套餐...")
            
            # 步骤1: 查找选择套餐输入框
            print("步骤1: 查找选择套餐输入框...")
            package_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder='选择套餐'].el-input__inner")
            print(f"   找到 {len(package_inputs)} 个'选择套餐'输入框")
            
            # 对于独享静态，通常有两个"选择套餐"输入框，我们需要第二个
            if len(package_inputs) >= 2:
                package_input = package_inputs[1]  # 第二个"选择套餐"输入框
                print("✅ 选择第二个'选择套餐'输入框（独享静态套餐）")
            elif len(package_inputs) == 1:
                package_input = package_inputs[0]  # 只有一个"选择套餐"输入框
                print("✅ 选择唯一的'选择套餐'输入框")
            else:
                print("❌ 未找到足够的'选择套餐'输入框")
                return False
            
            # 步骤2: 点击选择套餐输入框
            print("步骤2: 点击选择套餐输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", package_input)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", package_input)
            print("✅ 选择套餐输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 查找并选择可用套餐选项
            print("步骤3: 查找并选择可用套餐选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个套餐选项")
            
            # 筛选可见且非空的选项
            available_options = []
            for i, option in enumerate(options):
                try:
                    if option.is_displayed():
                        option_text = option.text.strip()
                        print(f"   选项 {i+1}: '{option_text}'")
                        if option_text and option_text != "":
                            available_options.append(option)
                except Exception as e:
                    continue
            
            if not available_options:
                print("❌ 未找到可用的套餐选项")
                return False
            
            # 步骤4: 选择第一个可用选项
            selected_option = available_options[0]
            selected_text = selected_option.text.strip()
            print(f"步骤4: 选择套餐选项: '{selected_text}'...")
            selected_option.click()
            print(f"✅ 套餐选择完成: '{selected_text}'")
            time.sleep(2)
            
            print("🎉 独享静态套餐选择成功！")
            return True
            
        except Exception as e:
            print(f"❌ 选择独享静态套餐失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_ip_bandwidth(self):
        """选择IP带宽（第四个下拉框）"""
        try:
            print("🔍 正在选择IP带宽...")
            
            # 步骤1: 查找IP带宽输入框
            print("步骤1: 查找IP带宽输入框...")
            bandwidth_input = None
            
            # 首先获取所有"请选择"的输入框，然后按照顺序选择
            all_please_select_inputs = []
            bandwidth_selectors = [
                "div[data-v-78b06e16] input[placeholder='请选择'].el-input__inner",
                "input[placeholder='请选择'].el-input__inner"
            ]
            
            for selector in bandwidth_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "请选择":
                            # 检查这个输入框的父元素，避免选择到套餐类型相关的
                            parent_html = input_elem.find_element(By.XPATH, "..").get_attribute("outerHTML")
                            print(f"   找到'请选择'输入框，父元素: {parent_html[:200]}...")
                            all_please_select_inputs.append(input_elem)
                except Exception as e:
                    continue
            
            print(f"   总共找到 {len(all_please_select_inputs)} 个'请选择'输入框")
            
            # 对于独享静态TikTok套餐，IP带宽应该是第一个"请选择"输入框
            if len(all_please_select_inputs) >= 1:
                bandwidth_input = all_please_select_inputs[0]  # 第一个"请选择"输入框应该是IP带宽
                print("✅ 选择第一个'请选择'输入框作为IP带宽输入框")
            else:
                print("❌ 未找到IP带宽输入框")
                return False
            
            # 验证这个输入框确实是IP带宽（通过检查周围元素或位置）
            try:
                # 检查输入框的值，确保不是套餐类型
                current_value = bandwidth_input.get_attribute("value")
                print(f"   当前输入框的值: '{current_value}'")
                
                # 如果值是套餐类型相关的，说明选错了
                if current_value in ["动态住宅", "静态代理", "独享静态"]:
                    print("   警告：当前选择的输入框似乎是套餐类型输入框，尝试选择其他输入框...")
                    if len(all_please_select_inputs) >= 2:
                        bandwidth_input = all_please_select_inputs[1]  # 尝试第二个
                        print("   改为选择第二个'请选择'输入框")
                    else:
                        print("❌ 无法找到正确的IP带宽输入框")
                        return False
            except Exception as e:
                print(f"   无法检查输入框值: {e}")
            
            # 步骤2: 点击IP带宽输入框
            print("步骤2: 点击IP带宽输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bandwidth_input)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", bandwidth_input)
            print("✅ IP带宽输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 查找并选择IP带宽选项
            print("步骤3: 查找并选择IP带宽选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个IP带宽选项")
            
            # 验证选项内容，确保这些是IP带宽选项而不是套餐类型选项
            sample_options = []
            for i, option in enumerate(options[:5]):  # 只检查前5个选项
                try:
                    if option.is_displayed():
                        option_text = option.text.strip()
                        sample_options.append(option_text)
                        print(f"   样本选项 {i+1}: '{option_text}'")
                except Exception as e:
                    continue
            
            # 如果选项包含套餐类型，说明还是选错了
            package_type_keywords = ["动态住宅", "静态代理", "独享静态"]
            if any(keyword in " ".join(sample_options) for keyword in package_type_keywords):
                print("❌ 检测到套餐类型选项，当前选择的不是IP带宽下拉框")
                print("   可能需要重新定位IP带宽输入框")
                return False
            
            # 筛选可见且非空的选项
            available_options = []
            for i, option in enumerate(options):
                try:
                    if option.is_displayed():
                        option_text = option.text.strip()
                        print(f"   选项 {i+1}: '{option_text}'")
                        if option_text and option_text != "":
                            available_options.append(option)
                except Exception as e:
                    continue
            
            if not available_options:
                print("❌ 未找到可用的IP带宽选项")
                return False
            
            # 步骤4: 选择第一个可用选项
            selected_option = available_options[0]
            selected_text = selected_option.text.strip()
            print(f"步骤4: 选择IP带宽选项: '{selected_text}'...")
            selected_option.click()
            print(f"✅ IP带宽选择完成: '{selected_text}'")
            time.sleep(2)
            
            print("🎉 IP带宽选择成功！")
            return True
            
        except Exception as e:
            print(f"❌ 选择IP带宽失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def select_country_region(self):
        """选择国家地区（第五个下拉框）- 选择括号数字不为0的地区"""
        try:
            print("🔍 正在选择国家地区...")
            
            # 步骤1: 查找国家地区输入框
            print("步骤1: 查找国家地区输入框...")
            region_input = None
            
            # 获取所有"请选择"的输入框
            all_region_inputs = []
            region_selectors = [
                "div[data-v-78b06e16] input[placeholder='请选择'].el-input__inner",
                "input[placeholder='请选择'].el-input__inner"
            ]
            
            for selector in region_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "请选择":
                            current_value = input_elem.get_attribute("value")
                            print(f"   找到'请选择'输入框，当前值: '{current_value}'")
                            all_region_inputs.append((input_elem, current_value))
                except Exception as e:
                    continue
            
            print(f"   总共找到 {len(all_region_inputs)} 个'请选择'输入框")
            
            # 智能选择国家地区输入框：
            # 1. 排除套餐类型相关的（值为：独享静态、动态住宅、静态代理）
            # 2. 排除IP带宽相关的（值包含：M、Mbps、带宽等）
            # 3. 优先选择空值的输入框
            # 4. 避免选择'全部'、分页相关的输入框
            
            exclude_keywords = ["独享静态", "动态住宅", "静态代理", "M", "Mbps", "带宽", "全部", "条/页"]
            
            # 首先尝试找空值的输入框（最可能是国家地区）
            candidate_inputs = []
            for input_elem, current_value in all_region_inputs:
                # 排除明显不是地区的输入框
                is_excluded = False
                for keyword in exclude_keywords:
                    if keyword in current_value:
                        is_excluded = True
                        break
                
                if not is_excluded:
                    candidate_inputs.append((input_elem, current_value))
                    print(f"   候选国家地区输入框，当前值: '{current_value}'")
            
            if not candidate_inputs:
                print("❌ 未找到合适的国家地区输入框候选")
                return False
            
            # 优先选择空值的输入框
            empty_inputs = [(elem, val) for elem, val in candidate_inputs if val == ""]
            if empty_inputs:
                region_input = empty_inputs[0][0]
                print("✅ 选择空值的'请选择'输入框作为国家地区输入框")
            else:
                # 如果没有空值的，选择第一个候选
                region_input = candidate_inputs[0][0]
                selected_value = candidate_inputs[0][1]
                print(f"✅ 选择候选输入框作为国家地区输入框，当前值: '{selected_value}'")
            
            # 最终验证这个输入框确实不是带宽相关的
            try:
                final_value = region_input.get_attribute("value")
                print(f"   最终选择的国家地区输入框当前值: '{final_value}'")
                
                # 如果值包含明显的带宽相关内容，报错
                bandwidth_keywords = ["M", "Mbps", "带宽", "bandwidth"]
                if any(keyword in final_value for keyword in bandwidth_keywords):
                    print("❌ 最终选择的输入框仍然是带宽相关的，无法继续")
                    return False
            except Exception as e:
                print(f"   无法检查最终输入框值: {e}")
            
            # 步骤2: 点击国家地区输入框
            print("步骤2: 点击国家地区输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_input)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", region_input)
            print("✅ 国家地区输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 查找并选择可用地区（括号数字>0）
            print("步骤3: 查找并选择可用地区（括号数字>0）...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个地区选项")
            
            # 验证选项内容，确保这些是地区选项而不是其他类型的选项
            sample_options = []
            for i, option in enumerate(options[:5]):  # 只检查前5个选项
                try:
                    if option.is_displayed():
                        option_text = option.text.strip()
                        sample_options.append(option_text)
                        print(f"   样本选项 {i+1}: '{option_text}'")
                except Exception as e:
                    continue
            
            # 检查是否是套餐类型、IP带宽或其他错误选项
            wrong_keywords = ["动态住宅", "静态代理", "独享静态", "M", "Mbps", "带宽"]
            if any(keyword in " ".join(sample_options) for keyword in wrong_keywords):
                print("❌ 检测到非地区选项，当前选择的不是国家地区下拉框")
                print(f"   样本选项: {sample_options}")
                print("   可能需要重新定位国家地区输入框")
                return False
            
            # 使用正则表达式匹配括号中的数字
            import re
            available_regions = []
            for i, option in enumerate(options):
                try:
                    if option.is_displayed():
                        option_text = option.text.strip()
                        print(f"   选项 {i+1}: '{option_text}'")
                        
                        # 使用正则表达式查找括号中的数字
                        match = re.search(r'\((\d+)\)', option_text)
                        if match:
                            count = int(match.group(1))
                            print(f"      括号中的数字: {count}")
                            if count > 0:
                                available_regions.append((option, option_text, count))
                                print(f"      ✅ 可用地区: '{option_text}' (数量: {count})")
                except Exception as e:
                    continue
            
            if not available_regions:
                print("❌ 未找到可用的地区选项（括号数字>0）")
                # 如果没有找到数字>0的选项，选择第一个看起来像地区名的选项作为备选
                fallback_options = []
                for option in options:
                    try:
                        if option.is_displayed():
                            option_text = option.text.strip()
                            # 检查是否看起来像地区名（包含常见地区词汇）
                            region_indicators = ["国", "州", "省", "市", "区", "-", "美国", "中国", "日本", "韩国", "新加坡", "香港", "台湾"]
                            if option_text and any(indicator in option_text for indicator in region_indicators):
                                fallback_options.append(option)
                                print(f"   找到疑似地区选项: '{option_text}'")
                                break
                    except Exception as e:
                        continue
                
                if fallback_options:
                    selected_option = fallback_options[0]
                    selected_text = selected_option.text.strip()
                    print(f"   使用备选方案，选择疑似地区选项: '{selected_text}'")
                else:
                    print("❌ 无法找到任何合适的地区选项")
                    return False
            else:
                # 选择第一个可用地区（数字>0）
                selected_option, selected_text, count = available_regions[0]
                print(f"步骤4: 选择地区: '{selected_text}' (数量: {count})...")
            
            # 步骤4: 点击选择的地区选项
            selected_option.click()
            print(f"✅ 地区选择完成: '{selected_text}'")
            time.sleep(2)
            
            print("🎉 国家地区选择成功！")
            return True
            
        except Exception as e:
            print(f"❌ 选择国家地区失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def open_exclusive_static_tiktok_package_flow(self, remark="IPIPGO UI自动化测试"):
        """开独享静态TikTok解决方案套餐的完整流程"""
        try:
            print("\n" + "="*50)
            print("📦 开始开独享静态TikTok解决方案套餐流程")
            print("="*50)
            
            # 步骤1: 点击开套餐按钮
            print("步骤1: 点击开套餐按钮...")
            if not self.click_open_package_button():
                print("❌ 开套餐按钮点击失败")
                return False
            
            # 步骤2: 选择套餐类型为"独享静态"
            print("步骤2: 选择套餐类型为独享静态...")
            if not self.select_exclusive_static_package_type():
                print("❌ 独享静态套餐类型选择失败")
                return False
            
            # 步骤3: 选择IP类型为"TikTok解决方案"
            print("步骤3: 选择IP类型为TikTok解决方案...")
            if not self.select_tiktok_solution_ip_type():
                print("❌ TikTok解决方案IP类型选择失败")
                return False
            
            # 步骤4: 选择独享静态套餐
            print("步骤4: 选择独享静态套餐...")
            if not self.select_exclusive_static_package():
                print("❌ 独享静态套餐选择失败")
                return False
            
            # 步骤5: 选择IP带宽
            print("步骤5: 选择IP带宽...")
            if not self.select_ip_bandwidth():
                print("❌ IP带宽选择失败")
                return False
            
            # 步骤6: 选择国家地区
            print("步骤6: 选择国家地区...")
            if not self.select_country_region():
                print("❌ 国家地区选择失败")
                return False
            
            # 步骤7: 输入备注信息
            print("步骤7: 输入备注信息...")
            if not self.enter_static_remark_info(remark):
                print("❌ 备注信息输入失败")
                return False
            
            # 步骤8: 点击确定按钮
            print("步骤8: 点击确定按钮...")
            if not self.click_static_confirm_button():
                print("❌ 确定按钮点击失败")
                return False
            
            # 步骤9: 支付操作
            print("步骤9: 开始支付操作...")
            if not self.complete_payment_flow():
                print("❌ 支付操作失败")
                return False
            
            print("="*50)
            print("🎉 独享静态TikTok解决方案套餐+支付流程成功完成！")
            print("="*50)
            return True
        except Exception as e:
            print(f"❌ 开独享静态TikTok解决方案套餐流程失败: {e}")
            return False
    
    def select_exclusive_static_ip_type(self):
        """选择独享静态IP类型（第二个下拉框）- 注意这里选择的是"独享静态"而不是"TikTok解决方案" """
        try:
            print("🔍 正在选择独享静态IP类型...")
            
            # 步骤1: 查找IP类型输入框
            print("步骤1: 查找IP类型输入框...")
            ip_type_input = None
            
            # 查找IP类型输入框
            ip_selectors = [
                "input[placeholder='选择IP类型'].el-input__inner",
                "div[data-v-78b06e16] input[placeholder='选择IP类型']",
                "div[data-v-8548a9c6] input[placeholder='选择IP类型']"
            ]
            
            for selector in ip_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.get_attribute("placeholder") == "选择IP类型":
                            ip_type_input = input_elem
                            print("✅ 找到IP类型输入框")
                            break
                    if ip_type_input:
                        break
                except Exception as e:
                    continue
            
            if not ip_type_input:
                print("❌ 未找到IP类型输入框")
                return False
            
            # 步骤2: 使用JavaScript点击IP类型输入框避免遮挡
            print("步骤2: 点击IP类型输入框...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ip_type_input)
            time.sleep(1)
            print("   使用JavaScript点击避免弹窗遮挡...")
            self.driver.execute_script("arguments[0].click();", ip_type_input)
            print("✅ IP类型输入框点击完成，下拉选项已打开")
            time.sleep(2)
            
            # 步骤3: 查找并选择"独享静态"选项
            print("步骤3: 查找并选择'独享静态'选项...")
            options = self.driver.find_elements(By.CSS_SELECTOR, "li.el-select-dropdown__item")
            print(f"   找到 {len(options)} 个IP类型选项")
            
            exclusive_static_option = None
            for i, option in enumerate(options):
                try:
                    option_text = option.text.strip()
                    print(f"   选项 {i+1}: '{option_text}'")
                    if "独享静态" in option_text and option.is_displayed():
                        exclusive_static_option = option
                        print(f"✅ 找到独享静态选项: '{option_text}'")
                        break
                except Exception as e:
                    continue
            
            if not exclusive_static_option:
                print("❌ 未找到独享静态选项")
                return False
            
            # 步骤4: 点击独享静态选项
            print("步骤4: 点击独享静态选项...")
            exclusive_static_option.click()
            print("✅ 独享静态选项选择完成")
            time.sleep(2)
            
            print("🎉 IP类型成功选择为独享静态！")
            return True
            
        except Exception as e:
            print(f"❌ 选择独享静态IP类型失败: {e}")
            print(f"   详细错误信息: {str(e)}")
            return False
    
    def open_exclusive_static_package_flow(self, remark="IPIPGO UI自动化测试"):
        """开独享静态套餐的完整流程（IP类型为独享静态，后续流程和静态代理一样）"""
        try:
            print("\n" + "="*50)
            print("📦 开始开独享静态套餐流程")
            print("="*50)
            
            # 步骤1: 点击开套餐按钮
            print("步骤1: 点击开套餐按钮...")
            if not self.click_open_package_button():
                print("❌ 开套餐按钮点击失败")
                return False
            
            # 步骤2: 选择套餐类型为"独享静态"
            print("步骤2: 选择套餐类型为独享静态...")
            if not self.select_exclusive_static_package_type():
                print("❌ 独享静态套餐类型选择失败")
                return False
            
            # 步骤3: 选择IP类型为"独享静态"
            print("步骤3: 选择IP类型为独享静态...")
            if not self.select_exclusive_static_ip_type():
                print("❌ 独享静态IP类型选择失败")
                return False
            
            # 步骤4: 选择独享静态套餐（复用静态代理的选择套餐方法）
            print("步骤4: 选择独享静态套餐...")
            if not self.select_static_package():
                print("❌ 独享静态套餐选择失败")
                return False
            
            # 步骤5: 点击添加地区按钮（复用静态代理的方法）
            print("步骤5: 点击添加地区按钮...")
            if not self.click_add_region_button():
                print("❌ 添加地区按钮点击失败")
                return False
            
            # 步骤6: 选择可用地区（复用静态代理的方法）
            print("步骤6: 选择可用地区...")
            if not self.select_available_region():
                print("❌ 可用地区选择失败")
                return False
            
            # 步骤7: 输入备注信息（复用静态代理的方法）
            print("步骤7: 输入备注信息...")
            if not self.enter_static_remark_info(remark):
                print("❌ 备注信息输入失败")
                return False
            
            # 步骤8: 点击确定按钮（复用静态代理的方法）
            print("步骤8: 点击确定按钮...")
            if not self.click_static_confirm_button():
                print("❌ 确定按钮点击失败")
                return False
            
            # 步骤9: 支付操作（复用通用的支付方法）
            print("步骤9: 开始支付操作...")
            if not self.complete_payment_flow():
                print("❌ 支付操作失败")
                return False
            
            print("="*50)
            print("🎉 独享静态套餐+支付流程成功完成！")
            print("="*50)
            return True
        except Exception as e:
            print(f"❌ 开独享静态套餐流程失败: {e}")
            return False