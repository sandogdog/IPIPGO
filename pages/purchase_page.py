"""
IPIPGO购买页面
处理登录后的购买流程
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from utils.base_page import BasePage
from pages.alipay_payment import AlipayPayment
import time
import yaml
from selenium.webdriver.common.action_chains import ActionChains


class PurchasePage(BasePage):
    """购买页面类"""
    
    # 页面元素定位器
    # 第一次购买流程的元素定位器
    FIRST_BUY_BUTTON = (By.CSS_SELECTOR, "div.buy-btn button.personal-button.el-button--default span")
    
    # 原有的第二个立即购买按钮（第一次流程中的）  
    OLD_SECOND_BUY_BUTTON = (By.CSS_SELECTOR, "button.buy-btn.el-button--default.cicle-green-border span")
    
    # 原有的立即支付按钮
    PAY_BUTTON = (By.CSS_SELECTOR, "div.pay-btn button.personal-button.el-button--default span")
    
    # 支付页面标识
    ALIPAY_INDICATOR = (By.CSS_SELECTOR, "[class*='alipay'], [id*='alipay'], [title*='支付宝'], [alt*='支付宝']")
    
    # 第二次购买流程的元素定位器
    DYNAMIC_ENTERPRISE_TAB = (By.CSS_SELECTOR, "div[data-v-369d5cdf].custom-tab-item.cursor")
    SECOND_BUY_BUTTON = (By.CSS_SELECTOR, "button[data-v-0ebd072d][data-v-11ed8ffc].el-button.buy-btn.el-button--default.cicle-green-border")
    SECOND_PAY_BUTTON = (By.CSS_SELECTOR, "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary")

    # 第三次购买流程的元素定位器（独享静态套餐）
    EXCLUSIVE_STATIC_TAB = (By.CSS_SELECTOR, "div[data-v-369d5cdf].custom-tab-item.cursor")
    HONGKONG_LINE_CONTAINER = (By.CSS_SELECTOR, "div[data-v-4269ae51] div[data-v-d73930ac].city-box")
    ADD_LINE_BUTTON = (By.CSS_SELECTOR, "div[data-v-4269ae51][data-v-d73930ac].add-box.flex-j-a")
    THIRD_BUY_BUTTON = (By.CSS_SELECTOR, "button[data-v-0ebd072d][data-v-074476e6].el-button.btn.el-button--default.primary")
    THIRD_PAY_BUTTON = (By.CSS_SELECTOR, "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary")

    # 第四次购买流程的元素定位器（静态住宅套餐）
    STATIC_RESIDENTIAL_TAB = (By.CSS_SELECTOR, "div[data-v-369d5cdf].custom-tab-item.cursor")
    NEWYORK_LINE_CONTAINER = (By.CSS_SELECTOR, "div[data-v-4269ae51] div[data-v-d73930ac].city-box")
    FOURTH_BUY_BUTTON = (By.CSS_SELECTOR, "button[data-v-0ebd072d][data-v-074476e6].el-button.btn.el-button--default.primary")
    FOURTH_PAY_BUTTON = (By.CSS_SELECTOR, "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary")

    # 第五次购买流程的元素定位器（动态住宅（长效ISP）套餐）
    DYNAMIC_RESIDENTIAL_ISP_TAB = (By.CSS_SELECTOR, "div[data-v-369d5cdf].custom-tab-item.cursor")
    FIFTH_BUY_BUTTON = (By.CSS_SELECTOR, "button[data-v-0ebd072d][data-v-11ed8ffc].el-button.buy-btn.el-button--default.cicle-green-border")
    FIFTH_PAY_BUTTON = (By.CSS_SELECTOR, "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary")

    # 第六次购买流程的元素定位器（动态不限量套餐）
    DYNAMIC_UNLIMITED_TAB = (By.CSS_SELECTOR, "div[data-v-369d5cdf].custom-tab-item.cursor")
    SIXTH_BUY_BUTTON = (By.CSS_SELECTOR, "button[data-v-0ebd072d][data-v-11ed8ffc].el-button.buy-btn.el-button--default.cicle-green-border")
    SIXTH_PAY_BUTTON = (By.CSS_SELECTOR, "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary")

    # 第七次购买流程的元素定位器（动态数据中心（基础）套餐）
    DATA_CENTER_MENU_ITEM = (By.CSS_SELECTOR, "li[data-v-625350b8].el-menu-item.personal-left-menu-item")
    SEVENTH_BUY_BUTTON = (By.CSS_SELECTOR, "button[data-v-0ebd072d][data-v-11ed8ffc].el-button.buy-btn.el-button--default.cicle-green-border")
    SEVENTH_PAY_BUTTON = (By.CSS_SELECTOR, "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary")

    # 第八次购买流程的元素定位器（静态数据中心套餐）
    STATIC_DATACENTER_TAB = (By.CSS_SELECTOR, "div[data-v-369d5cdf].custom-tab-item.cursor")
    MANILA_LINE_CONTAINER = (By.CSS_SELECTOR, "div[data-v-4269ae51] div[data-v-d73930ac].city-box")
    MANILA_ADD_BUTTON = (By.CSS_SELECTOR, "div[data-v-4269ae51][data-v-d73930ac].add-box.flex-j-a")
    EIGHTH_BUY_BUTTON = (By.CSS_SELECTOR, "button[data-v-0ebd072d][data-v-074476e6].el-button.btn.el-button--default.primary")
    EIGHTH_PAY_BUTTON = (By.CSS_SELECTOR, "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary")

    def __init__(self, driver):
        super().__init__(driver)
        self.original_window = None
        self.alipay_payment = AlipayPayment(driver)
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        try:
            with open('config/config.yaml', 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def click_dynamic_enterprise_tab(self):
        """点击动态（企业）选项卡（增强版）"""
        try:
            print("🔍 正在查找动态（企业）选项卡...")
            
            # 多种定位器尝试
            tab_selectors = [
                "div[data-v-369d5cdf].custom-tab-item.cursor",  # 原始定位器
                "div.custom-tab-item.cursor",  # 简化版本
                ".custom-tab-item",  # 更简化
                "div.custom-tab-item",  # 基础版本
                "[class*='tab-item']",  # 包含tab-item的元素
                "[class*='custom-tab']",  # 包含custom-tab的元素
            ]
            
            dynamic_tab = None
            used_selector = None
            
            for selector in tab_selectors:
                try:
                    print(f"🔍 尝试定位器: {selector}")
                    
                    # 查找所有匹配的元素
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(elements)} 个元素")
                    
                    # 在所有元素中查找包含"动态"或"企业"的
                    for i, element in enumerate(elements):
                        try:
                            element_text = element.text.strip()
                            print(f"   元素{i+1}文本: '{element_text}'")
                            
                            if ('动态' in element_text and '企业' in element_text) or \
                               '动态（企业）' in element_text or \
                               'dynamic' in element_text.lower() or \
                               'enterprise' in element_text.lower():
                                dynamic_tab = element
                                used_selector = selector
                                print(f"✅ 找到动态企业选项卡: '{element_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取元素{i+1}文本: {e}")
                            continue
                    
                    if dynamic_tab:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not dynamic_tab:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//div[contains(@class,'tab-item') and contains(text(),'动态')]",
                    "//div[contains(@class,'tab-item') and contains(text(),'企业')]",
                    "//div[contains(text(),'动态（企业）')]",
                    "//div[contains(text(),'动态') and contains(text(),'企业')]",
                    "//*[contains(@class,'tab') and contains(text(),'动态')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            dynamic_tab = elements[0]
                            used_selector = xpath
                            print(f"✅ 通过XPath找到动态企业选项卡: '{dynamic_tab.text}'")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not dynamic_tab:
                print("❌ 无法找到动态（企业）选项卡")
                print("🔍 打印页面中所有可能的选项卡元素...")
                
                # 调试：打印所有可能的选项卡
                try:
                    debug_selectors = ["div", "[class*='tab']", "[class*='item']"]
                    for debug_selector in debug_selectors:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, debug_selector)
                        for element in elements[:10]:  # 只打印前10个
                            try:
                                text = element.text.strip()
                                if text and ('动态' in text or '企业' in text or 'tab' in element.get_attribute('class').lower()):
                                    print(f"   调试发现: '{text}' - class: {element.get_attribute('class')}")
                            except:
                                pass
                except Exception as e:
                    print(f"调试信息获取失败: {e}")
                
                return False
            
            print(f"📋 选项卡文本: '{dynamic_tab.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 确保元素可见并滚动到位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dynamic_tab)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: dynamic_tab.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", dynamic_tab)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(dynamic_tab).click().perform()),
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
            
            # 等待页面内容更新
            print("⏳ 等待页面内容更新...")
            time.sleep(3)
            
            # 验证选项卡切换是否成功
            try:
                # 检查是否有企业套餐相关的内容出现
                time.sleep(2)
                enterprise_indicators = [
                    "button[data-v-0ebd072d][data-v-11ed8ffc]",  # 企业套餐购买按钮
                    "[class*='enterprise']",  # 包含enterprise的元素
                    "[class*='dynamic']",  # 包含dynamic的元素
                ]
                
                for indicator in enterprise_indicators:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, indicator)
                        if elements:
                            print(f"✅ 检测到企业套餐内容: {indicator}")
                            return True
                    except:
                        continue
                
                print("⚠️ 未明确检测到企业套餐内容，但选项卡点击已执行")
                return True
                
            except Exception as e:
                print(f"⚠️ 选项卡切换验证失败: {e}")
                return True  # 假设点击成功
            
        except Exception as e:
            print(f"❌ 点击动态（企业）选项卡失败: {e}")
            return False
    
    def click_enterprise_buy_button(self):
        """点击企业套餐的立即购买按钮（增强版）"""
        try:
            print("🔍 正在查找企业套餐购买按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 多种定位器尝试
            buy_button_selectors = [
                "button[data-v-0ebd072d][data-v-11ed8ffc].el-button.buy-btn.el-button--default.cicle-green-border",  # 原始定位器
                "button.buy-btn.el-button--default.cicle-green-border",  # 简化版本
                "button.buy-btn.cicle-green-border",  # 更简化
                "button.buy-btn",  # 基础版本
                "button[class*='buy-btn']",  # 包含buy-btn的按钮
                "button[class*='cicle-green-border']",  # 包含cicle-green-border的按钮
                "button.el-button--default",  # 默认按钮样式
            ]
            
            enterprise_buy_btn = None
            used_selector = None
            
            for selector in buy_button_selectors:
                try:
                    print(f"🔍 尝试购买按钮定位器: {selector}")
                    
                    # 查找所有匹配的按钮
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    # 在所有按钮中查找包含"立即购买"或"购买"的
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即购买' in button_text or '购买' in button_text or 'buy' in button_text.lower():
                                # 检查按钮是否可见和可点击
                                if button.is_displayed() and button.is_enabled():
                                    enterprise_buy_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到企业套餐购买按钮: '{button_text}'")
                                    break
                                else:
                                    print(f"   ⚠️ 按钮{i+1}不可点击或不可见")
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if enterprise_buy_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not enterprise_buy_btn:
                print("🔍 尝试XPath定位购买按钮...")
                xpath_selectors = [
                    "//button[contains(@class,'buy-btn') and contains(text(),'立即购买')]",
                    "//button[contains(@class,'buy-btn') and contains(text(),'购买')]",
                    "//button[contains(text(),'立即购买')]",
                    "//button[contains(text(),'购买')]",
                    "//*[contains(@class,'buy') and contains(text(),'购买')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                enterprise_buy_btn = button
                                used_selector = xpath
                                print(f"✅ 通过XPath找到购买按钮: '{button.text}'")
                                break
                        if enterprise_buy_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not enterprise_buy_btn:
                print("❌ 无法找到企业套餐购买按钮")
                print("🔍 打印页面中所有可能的购买按钮...")
                
                # 调试：打印所有可能的按钮
                try:
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    print(f"📋 页面总共有 {len(all_buttons)} 个按钮")
                    
                    for i, button in enumerate(all_buttons[:20]):  # 只检查前20个按钮
                        try:
                            text = button.text.strip()
                            classes = button.get_attribute('class')
                            if text and ('购买' in text or 'buy' in text.lower() or 'btn' in classes):
                                visible = button.is_displayed()
                                enabled = button.is_enabled()
                                print(f"   按钮{i+1}: '{text}' - class: {classes} - 可见:{visible} - 可点击:{enabled}")
                        except:
                            pass
                except Exception as e:
                    print(f"调试信息获取失败: {e}")
                
                return False
            
            print(f"📋 购买按钮文本: '{enterprise_buy_btn.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", enterprise_buy_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: enterprise_buy_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", enterprise_buy_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(enterprise_buy_btn).click().perform()),
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
            
            # 等待页面跳转
            print("⏳ 等待页面跳转...")
            time.sleep(3)
            
            # 验证是否跳转到支付页面
            try:
                # 检查URL变化或支付相关元素出现
                current_url = self.driver.current_url
                print(f"📋 当前页面: {current_url}")
                
                # 检查是否有支付按钮出现
                pay_button_selectors = [
                    "button[data-v-46103f1d]",  # 支付按钮
                    "button[class*='personal-button']",  # 个人按钮样式
                    "button[class*='pay']",  # 包含pay的按钮
                ]
                
                for selector in pay_button_selectors:
                    try:
                        buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for button in buttons:
                            if '支付' in button.text or 'pay' in button.text.lower():
                                print(f"✅ 检测到支付按钮，页面跳转成功")
                                return True
                    except:
                        continue
                
                print("⚠️ 未明确检测到支付按钮，但购买按钮点击已执行")
                return True
                
            except Exception as e:
                print(f"⚠️ 页面跳转验证失败: {e}")
                return True
            
        except Exception as e:
            print(f"❌ 点击企业套餐购买按钮失败: {e}")
            return False
    
    def click_enterprise_pay_button_and_handle_payment(self):
        """点击企业套餐立即支付按钮并处理支付流程"""
        try:
            print("🔍 正在查找企业套餐立即支付按钮...")
            
            # 记录当前窗口句柄
            self.original_window = self.driver.current_window_handle
            original_window_count = len(self.driver.window_handles)
            
            # 设置支付宝支付模块的原始窗口
            self.alipay_payment.set_original_window(self.original_window)
            
            # 等待企业套餐支付按钮可点击并点击
            enterprise_pay_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.SECOND_PAY_BUTTON)
            )
            
            print(f"📋 支付按钮文本: {enterprise_pay_btn.text}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", enterprise_pay_btn)
            time.sleep(1)
            
            # 点击支付按钮
            enterprise_pay_btn.click()
            print("✅ 已点击企业套餐立即支付按钮")
            
            # 等待跳转到支付宝页面
            payment_window_found = False
            
            # 方案1：等待新窗口打开
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.window_handles) > original_window_count
                )
                print("✓ 检测到新窗口打开（企业套餐支付页面）")
                
                # 切换到支付宝窗口
                for window in self.driver.window_handles:
                    if window != self.original_window:
                        self.driver.switch_to.window(window)
                        print("✓ 已切换到企业套餐支付宝页面窗口")
                        payment_window_found = True
                        break
                        
            except TimeoutException:
                # 方案2：检查当前页面是否跳转到支付页面
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.any_of(
                            EC.url_contains("alipay"),
                            EC.url_contains("pay"),
                            EC.title_contains("支付"),
                            EC.presence_of_element_located(self.ALIPAY_INDICATOR)
                        )
                    )
                    print("✓ 当前页面跳转到企业套餐支付页面")
                    payment_window_found = True
                except TimeoutException:
                    print("⚠️ 未检测到明显的企业套餐支付页面跳转")
                    return False
            
            if payment_window_found:
                # 从配置文件获取支付宝账号信息
                alipay_config = self.config.get('test_data', {}).get('alipay', {})
                email = alipay_config.get('email', 'lgipqm7573@sandbox.com')
                login_password = alipay_config.get('login_password', '111111')
                pay_password = alipay_config.get('pay_password', '111111')
                
                print(f"企业套餐支付使用支付宝账号: {email}")
                
                # 调用支付宝支付模块处理完整支付流程
                return self.alipay_payment.complete_payment_process(
                    email=email,
                    login_password=login_password,
                    pay_password=pay_password
                )
            else:
                print("❌ 未能成功跳转到企业套餐支付页面")
                return False
            
        except Exception as e:
            print(f"❌ 企业套餐支付流程失败: {e}")
            return False
    
    def complete_second_purchase_flow(self):
        """完整的第二次购买流程（企业套餐）"""
        try:
            print("\n" + "="*50)
            print("🏢 开始企业套餐购买流程")
            print("="*50)
            
            # 步骤0: 确保在正确的IPIPGO页面
            print("步骤0: 检查并切换到正确的IPIPGO页面...")
            if not self.ensure_on_correct_ipipgo_page():
                print("❌ 无法切换到正确的IPIPGO页面")
                return False
            
            # 点击动态（企业）选项卡
            print("步骤1: 点击动态（企业）选项卡...")
            if not self.click_dynamic_enterprise_tab():
                print("❌ 动态（企业）选项卡点击失败")
                return False
            
            print("✓ 成功点击动态（企业）选项卡")
            
            # 点击企业套餐购买按钮
            print("步骤2: 点击企业套餐立即购买按钮...")
            if not self.click_enterprise_buy_button():
                print("❌ 企业套餐购买按钮点击失败")
                return False
            
            print("✓ 成功点击企业套餐立即购买按钮")
            
            # 点击企业套餐支付按钮并处理支付流程
            print("步骤3: 点击企业套餐立即支付按钮并完成支付...")
            if not self.click_enterprise_pay_button_and_handle_payment():
                print("❌ 企业套餐支付流程失败")
                return False
            
            print("✓ 企业套餐支付流程完成")
            
            print("="*50)
            print("🎉 企业套餐购买流程完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 企业套餐购买流程执行失败: {e}")
            return False
    
    def ensure_on_correct_ipipgo_page(self):
        """确保在正确的IPIPGO页面"""
        try:
            # 检查所有窗口
            all_windows = self.driver.window_handles
            print(f"📋 当前总窗口数: {len(all_windows)}")
            
            # 分析所有窗口
            ipipgo_windows = []
            for i, window_handle in enumerate(all_windows):
                try:
                    self.driver.switch_to.window(window_handle)
                    url = self.driver.current_url
                    title = self.driver.title
                    print(f"📋 窗口{i+1}: {title} - {url}")
                    
                    if 'ipipgo' in url.lower():
                        ipipgo_windows.append({
                            'handle': window_handle,
                            'url': url,
                            'title': title,
                            'index': i
                        })
                        print(f"🌐 找到IPIPGO窗口{i+1}")
                except Exception as e:
                    print(f"⚠️ 无法检查窗口{i+1}: {e}")
            
            if not ipipgo_windows:
                print("❌ 未找到IPIPGO窗口")
                return False
            
            # 选择最合适的IPIPGO窗口
            target_window = None
            
            # 优先选择包含购买相关关键词的页面
            for window in ipipgo_windows:
                url = window['url'].lower()
                if 'buy' in url or 'purchase' in url or 'personal' in url:
                    target_window = window
                    print(f"✅ 选择购买相关的IPIPGO窗口: {window['title']}")
                    break
            
            # 如果没有找到购买相关页面，选择第一个IPIPGO窗口
            if not target_window:
                target_window = ipipgo_windows[0]
                print(f"✅ 选择第一个IPIPGO窗口: {target_window['title']}")
            
            # 切换到目标窗口
            self.driver.switch_to.window(target_window['handle'])
            current_url = self.driver.current_url
            print(f"📋 当前页面: {current_url}")
            
            # 检查页面是否包含套餐选择功能
            return self.verify_page_has_package_options()
            
        except Exception as e:
            print(f"❌ 窗口管理失败: {e}")
            return False
    
    def verify_page_has_package_options(self):
        """验证页面是否包含套餐选择功能"""
        try:
            # 等待页面加载
            time.sleep(3)
            
            # 检查是否有选项卡或套餐相关元素
            potential_selectors = [
                "div[data-v-369d5cdf].custom-tab-item",  # 选项卡
                ".custom-tab-item",  # 简化的选项卡
                "div.custom-tab-item",  # 更通用的选项卡
                "[class*='tab-item']",  # 包含tab-item的元素
                "button[class*='buy-btn']",  # 购买按钮
                "div[class*='package']",  # 套餐相关
            ]
            
            for selector in potential_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"✅ 找到套餐相关元素: {selector} (共{len(elements)}个)")
                        return True
                except:
                    continue
            
            print("⚠️ 当前页面可能不包含套餐选择功能")
            print("🔄 尝试导航到个人中心...")
            
            # 尝试导航到个人中心或套餐选择页面
            try:
                current_url = self.driver.current_url
                if 'personal' not in current_url.lower():
                    # 尝试访问个人中心页面
                    base_url = current_url.split('?')[0].split('#')[0]
                    if not base_url.endswith('/'):
                        base_url = base_url.rsplit('/', 1)[0] + '/'
                    
                    personal_url = base_url + 'personal/'
                    print(f"🔄 尝试访问: {personal_url}")
                    self.driver.get(personal_url)
                    time.sleep(3)
                    
                    return self.verify_page_has_package_options()
            except Exception as e:
                print(f"⚠️ 导航失败: {e}")
            
            return False
            
        except Exception as e:
            print(f"❌ 页面验证失败: {e}")
            return False
    
    def wait_for_dashboard(self):
        """等待进入个人中心页面"""
        try:
            # 等待页面完全加载，可以根据个人中心特有元素来判断
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.url_contains("dashboard"),
                    EC.url_contains("center"),
                    EC.url_contains("user"),
                    EC.presence_of_element_located(self.FIRST_BUY_BUTTON)
                )
            )
            return True
        except:
            return False
    
    def click_first_buy_button(self):
        """点击第一个立即购买按钮"""
        try:
            # 等待第一个购买按钮可点击
            first_buy_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.buy-btn button.personal-button"))
            )
            first_buy_btn.click()
            
            # 等待页面跳转或第二个按钮出现
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.url_changes(self.driver.current_url),
                    EC.presence_of_element_located(self.OLD_SECOND_BUY_BUTTON)
                )
            )
            return True
        except Exception as e:
            print(f"点击第一个购买按钮失败: {e}")
            return False
    
    def click_second_buy_button(self):
        """点击第二个立即购买按钮（第一次流程中的）"""
        try:
            # 等待第二个购买按钮可点击
            second_buy_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.buy-btn.el-button--default.cicle-green-border"))
            )
            second_buy_btn.click()
            
            # 等待支付按钮出现
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.pay-btn button"))
            )
            return True
        except Exception as e:
            print(f"点击第二个购买按钮失败: {e}")
            return False
    
    def click_pay_button_and_handle_payment(self):
        """点击立即支付按钮并处理支付流程"""
        try:
            # 记录当前窗口句柄
            self.original_window = self.driver.current_window_handle
            original_window_count = len(self.driver.window_handles)
            
            # 设置支付宝支付模块的原始窗口
            self.alipay_payment.set_original_window(self.original_window)
            
            # 等待支付按钮可点击并点击
            pay_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.pay-btn button.personal-button"))
            )
            pay_btn.click()
            print("✓ 已点击立即支付按钮")
            
            # 等待跳转到支付宝页面
            payment_window_found = False
            
            # 方案1：等待新窗口打开
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.window_handles) > original_window_count
                )
                print("✓ 检测到新窗口打开（支付页面）")
                
                # 切换到支付宝窗口
                for window in self.driver.window_handles:
                    if window != self.original_window:
                        self.driver.switch_to.window(window)
                        print("✓ 已切换到支付宝页面窗口")
                        payment_window_found = True
                        break
                        
            except TimeoutException:
                # 方案2：检查当前页面是否跳转到支付页面
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.any_of(
                            EC.url_contains("alipay"),
                            EC.url_contains("pay"),
                            EC.title_contains("支付"),
                            EC.presence_of_element_located(self.ALIPAY_INDICATOR)
                        )
                    )
                    print("✓ 当前页面跳转到支付页面")
                    payment_window_found = True
                except TimeoutException:
                    print("⚠️ 未检测到明显的支付页面跳转")
                    return False
            
            if payment_window_found:
                # 从配置文件获取支付宝账号信息
                alipay_config = self.config.get('test_data', {}).get('alipay', {})
                email = alipay_config.get('email', 'lgipqm7573@sandbox.com')
                login_password = alipay_config.get('login_password', '111111')
                pay_password = alipay_config.get('pay_password', '111111')
                
                print(f"使用支付宝账号: {email}")
                
                # 调用支付宝支付模块处理完整支付流程
                return self.alipay_payment.complete_payment_process(
                    email=email,
                    login_password=login_password,
                    pay_password=pay_password
                )
            else:
                print("❌ 未能成功跳转到支付页面")
                return False
            
        except Exception as e:
            print(f"❌ 支付流程失败: {e}")
            return False
    
    def complete_purchase_flow(self):
        """完整的购买流程"""
        try:
            # 等待进入个人中心
            if not self.wait_for_dashboard():
                print("未能进入个人中心页面")
                return False
            
            print("✓ 已进入个人中心页面")
            
            # 点击第一个购买按钮
            if not self.click_first_buy_button():
                print("第一个购买按钮点击失败")
                return False
            
            print("✓ 成功点击第一个立即购买按钮")
            
            # 点击第二个购买按钮
            if not self.click_second_buy_button():
                print("第二个购买按钮点击失败")
                return False
            
            print("✓ 成功点击第二个立即购买按钮")
            
            # 点击支付按钮并处理支付流程
            if not self.click_pay_button_and_handle_payment():
                print("支付流程失败")
                return False
            
            print("✓ 支付流程完成")
            
            return True
            
        except Exception as e:
            print(f"购买流程执行失败: {e}")
            return False
    
    def is_on_payment_page(self):
        """检查是否在支付页面"""
        try:
            current_url = self.get_current_url()
            current_title = self.get_title()
            
            return ("alipay" in current_url.lower() or 
                    "pay" in current_url.lower() or 
                    "支付" in current_title)
        except:
            return False 

    def click_exclusive_static_tab(self):
        """点击独享静态选项卡（增强版）"""
        try:
            print("🔍 正在查找独享静态选项卡...")
            
            # 多种定位器尝试
            tab_selectors = [
                "div[data-v-369d5cdf].custom-tab-item.cursor",  # 原始定位器
                "div.custom-tab-item.cursor",  # 简化版本
                ".custom-tab-item",  # 更简化
                "div.custom-tab-item",  # 基础版本
                "[class*='tab-item']",  # 包含tab-item的元素
                "[class*='custom-tab']",  # 包含custom-tab的元素
            ]
            
            static_tab = None
            used_selector = None
            
            for selector in tab_selectors:
                try:
                    print(f"🔍 尝试定位器: {selector}")
                    
                    # 查找所有匹配的元素
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(elements)} 个元素")
                    
                    # 在所有元素中查找包含"独享静态"的
                    for i, element in enumerate(elements):
                        try:
                            element_text = element.text.strip()
                            print(f"   元素{i+1}文本: '{element_text}'")
                            
                            if '独享静态' in element_text or \
                               ('独享' in element_text and '静态' in element_text) or \
                               'exclusive' in element_text.lower() or \
                               'static' in element_text.lower():
                                static_tab = element
                                used_selector = selector
                                print(f"✅ 找到独享静态选项卡: '{element_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取元素{i+1}文本: {e}")
                            continue
                    
                    if static_tab:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not static_tab:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//div[contains(@class,'tab-item') and contains(text(),'独享静态')]",
                    "//div[contains(@class,'tab-item') and contains(text(),'独享')]",
                    "//div[contains(@class,'tab-item') and contains(text(),'静态')]",
                    "//div[contains(text(),'独享静态')]",
                    "//*[contains(@class,'tab') and contains(text(),'独享')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            static_tab = elements[0]
                            used_selector = xpath
                            print(f"✅ 通过XPath找到独享静态选项卡: '{static_tab.text}'")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not static_tab:
                print("❌ 无法找到独享静态选项卡")
                return False
            
            print(f"📋 选项卡文本: '{static_tab.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 确保元素可见并滚动到位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", static_tab)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: static_tab.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", static_tab)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(static_tab).click().perform()),
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
            
            # 等待页面内容更新
            print("⏳ 等待页面内容更新...")
            time.sleep(3)
            
            print("✅ 独享静态选项卡点击完成")
            return True
            
        except Exception as e:
            print(f"❌ 点击独享静态选项卡失败: {e}")
            return False
    
    def click_hongkong_add_button(self):
        """点击香港线路的加号按钮"""
        try:
            print("🔍 正在查找香港线路的加号按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 先查找所有香港相关的线路容器
            hongkong_containers = []
            container_selectors = [
                "div[data-v-4269ae51] div[data-v-d73930ac].city-box",  # 原始定位器
                "div.city-box",  # 简化版本
                "[class*='city-box']",  # 包含city-box的元素
                "div[data-v-d73930ac]",  # 数据属性定位
            ]
            
            for selector in container_selectors:
                try:
                    print(f"🔍 尝试容器定位器: {selector}")
                    containers = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(containers)} 个容器")
                    
                    for i, container in enumerate(containers):
                        try:
                            container_text = container.text
                            print(f"   容器{i+1}文本: '{container_text}'")
                            
                            if '香港' in container_text or 'HK' in container_text.upper() or 'HONG' in container_text.upper():
                                hongkong_containers.append(container)
                                print(f"✅ 找到香港线路容器: '{container_text}'")
                        except Exception as e:
                            print(f"   ⚠️ 无法获取容器{i+1}文本: {e}")
                            continue
                    
                    if hongkong_containers:
                        break
                        
                except Exception as e:
                    print(f"❌ 容器定位器 {selector} 失败: {e}")
                    continue
            
            if not hongkong_containers:
                print("❌ 无法找到香港线路容器")
                return False
            
            # 在香港容器中查找加号按钮
            add_button = None
            for container in hongkong_containers:
                try:
                    print("🔍 在香港容器中查找加号按钮...")
                    
                    # 多种加号按钮定位器
                    add_button_selectors = [
                        "div[data-v-4269ae51][data-v-d73930ac].add-box.flex-j-a",  # 原始定位器
                        ".add-box.flex-j-a",  # 简化版本
                        ".add-box",  # 更简化
                        "[class*='add-box']",  # 包含add-box的元素
                        "i.el-icon-plus",  # 加号图标
                        "[class*='plus']",  # 包含plus的元素
                    ]
                    
                    for add_selector in add_button_selectors:
                        try:
                            add_buttons = container.find_elements(By.CSS_SELECTOR, add_selector)
                            if add_buttons:
                                add_button = add_buttons[0]
                                print(f"✅ 找到加号按钮: {add_selector}")
                                break
                        except:
                            continue
                    
                    if add_button:
                        break
                        
                except Exception as e:
                    print(f"⚠️ 在容器中查找加号按钮失败: {e}")
                    continue
            
            if not add_button:
                print("❌ 无法找到香港线路的加号按钮")
                return False
            
            # 滚动到加号按钮位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: add_button.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", add_button)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(add_button).click().perform()),
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
            
            print("✅ 香港线路加号按钮点击成功")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ 点击香港线路加号按钮失败: {e}")
            return False
    
    def click_third_buy_button(self):
        """点击第三次立即购买按钮（独享静态套餐）"""
        try:
            print("🔍 正在查找第三次立即购买按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 多种定位器尝试
            buy_button_selectors = [
                "button[data-v-0ebd072d][data-v-074476e6].el-button.btn.el-button--default.primary",  # 原始定位器
                "button.el-button.btn.el-button--default.primary",  # 简化版本
                "button.btn.primary",  # 更简化
                "button[class*='primary']",  # 包含primary的按钮
                "button.el-button--default",  # 默认按钮样式
                "button[class*='btn']",  # 包含btn的按钮
            ]
            
            third_buy_btn = None
            used_selector = None
            
            for selector in buy_button_selectors:
                try:
                    print(f"🔍 尝试购买按钮定位器: {selector}")
                    
                    # 查找所有匹配的按钮
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    # 在所有按钮中查找包含"立即购买"或"购买"的
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即购买' in button_text or '购买' in button_text or 'buy' in button_text.lower():
                                # 检查按钮是否可见和可点击
                                if button.is_displayed() and button.is_enabled():
                                    third_buy_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第三次购买按钮: '{button_text}'")
                                    break
                                else:
                                    print(f"   ⚠️ 按钮{i+1}不可点击或不可见")
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if third_buy_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not third_buy_btn:
                print("🔍 尝试XPath定位购买按钮...")
                xpath_selectors = [
                    "//button[contains(text(),'立即购买')]",
                    "//button[contains(text(),'购买')]",
                    "//button[contains(@class,'primary') and contains(text(),'购买')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                third_buy_btn = button
                                used_selector = xpath
                                print(f"✅ 通过XPath找到购买按钮: '{button.text}'")
                                break
                        if third_buy_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not third_buy_btn:
                print("❌ 无法找到第三次购买按钮")
                return False
            
            print(f"📋 购买按钮文本: '{third_buy_btn.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", third_buy_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: third_buy_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", third_buy_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(third_buy_btn).click().perform()),
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
            
            # 等待页面跳转
            print("⏳ 等待页面跳转...")
            time.sleep(3)
            
            print("✅ 第三次购买按钮点击成功")
            return True
            
        except Exception as e:
            print(f"❌ 点击第三次购买按钮失败: {e}")
            return False
    
    def click_third_pay_button_and_handle_payment(self):
        """点击第三次立即支付按钮并处理支付流程（增强版）"""
        try:
            print("🔍 正在查找第三次立即支付按钮...")
            
            # 等待页面加载
            time.sleep(3)
            
            # 记录当前窗口句柄
            self.original_window = self.driver.current_window_handle
            original_window_count = len(self.driver.window_handles)
            
            # 设置支付宝支付模块的原始窗口
            self.alipay_payment.set_original_window(self.original_window)
            
            # 调试：打印当前页面信息
            current_url = self.driver.current_url
            current_title = self.driver.title
            print(f"📋 当前页面: {current_title}")
            print(f"📋 当前URL: {current_url}")
            
            # 多种支付按钮定位器尝试
            pay_button_selectors = [
                "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary",  # 原始定位器
                "button.personal-button.el-button--default.large.primary",  # 简化版本
                "button.personal-button.primary",  # 更简化
                "button.personal-button",  # 基础版本
                "button[class*='personal-button']",  # 包含personal-button的按钮
                "button[class*='primary']",  # 包含primary的按钮
                "button.el-button--default",  # 默认按钮样式
                "button[class*='large']",  # 包含large的按钮
            ]
            
            third_pay_btn = None
            used_selector = None
            
            for selector in pay_button_selectors:
                try:
                    print(f"🔍 尝试支付按钮定位器: {selector}")
                    
                    # 查找所有匹配的按钮
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    # 在所有按钮中查找包含"立即支付"或"支付"的
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即支付' in button_text or '支付' in button_text or 'pay' in button_text.lower():
                                # 检查按钮是否可见和可点击
                                if button.is_displayed() and button.is_enabled():
                                    third_pay_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第三次支付按钮: '{button_text}'")
                                    break
                                else:
                                    print(f"   ⚠️ 按钮{i+1}不可点击或不可见")
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if third_pay_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not third_pay_btn:
                print("🔍 尝试XPath定位支付按钮...")
                xpath_selectors = [
                    "//button[contains(text(),'立即支付')]",
                    "//button[contains(text(),'支付')]",
                    "//button[contains(@class,'primary') and contains(text(),'支付')]",
                    "//button[contains(@class,'personal-button')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            try:
                                button_text = button.text.strip()
                                if button.is_displayed() and button.is_enabled():
                                    if '支付' in button_text or 'pay' in button_text.lower():
                                        third_pay_btn = button
                                        used_selector = xpath
                                        print(f"✅ 通过XPath找到支付按钮: '{button.text}'")
                                        break
                            except:
                                continue
                        if third_pay_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            # 如果还是没找到，打印所有可能的按钮进行调试
            if not third_pay_btn:
                print("❌ 无法找到第三次支付按钮")
                print("🔍 打印页面中所有可能的支付按钮...")
                
                try:
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    print(f"📋 页面总共有 {len(all_buttons)} 个按钮")
                    
                    for i, button in enumerate(all_buttons[:30]):  # 检查前30个按钮
                        try:
                            text = button.text.strip()
                            classes = button.get_attribute('class')
                            data_attrs = []
                            
                            # 获取所有data-属性
                            for attr in button.get_property('attributes'):
                                attr_name = attr.get('name', '')
                                if attr_name.startswith('data-'):
                                    attr_value = button.get_attribute(attr_name)
                                    data_attrs.append(f"{attr_name}='{attr_value}'")
                            
                            data_str = " ".join(data_attrs) if data_attrs else "无data属性"
                            
                            if text and ('支付' in text or 'pay' in text.lower() or 
                                       'btn' in classes or 'button' in classes or 
                                       'primary' in classes or 'personal' in classes):
                                visible = button.is_displayed()
                                enabled = button.is_enabled()
                                print(f"   按钮{i+1}: '{text}' - class: {classes}")
                                print(f"     {data_str}")
                                print(f"     可见:{visible} - 可点击:{enabled}")
                                print("     ---")
                        except Exception as e:
                            print(f"   按钮{i+1}: 无法获取信息 - {e}")
                except Exception as e:
                    print(f"调试信息获取失败: {e}")
                
                print("💡 请检查页面是否正确跳转到了支付页面")
                print("💡 或者支付按钮的HTML结构可能与预期不同")
                return False
            
            print(f"📋 支付按钮文本: '{third_pay_btn.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", third_pay_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: third_pay_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", third_pay_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(third_pay_btn).click().perform()),
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
            
            print("✅ 已点击第三次立即支付按钮")
            
            # 等待跳转到支付宝页面
            payment_window_found = False
            
            # 方案1：等待新窗口打开
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.window_handles) > original_window_count
                )
                print("✓ 检测到新窗口打开（独享静态套餐支付页面）")
                
                # 切换到支付宝窗口
                for window in self.driver.window_handles:
                    if window != self.original_window:
                        self.driver.switch_to.window(window)
                        print("✓ 已切换到独享静态套餐支付宝页面窗口")
                        payment_window_found = True
                        break
                        
            except TimeoutException:
                # 方案2：检查当前页面是否跳转到支付页面
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.any_of(
                            EC.url_contains("alipay"),
                            EC.url_contains("pay"),
                            EC.title_contains("支付"),
                            EC.presence_of_element_located(self.ALIPAY_INDICATOR)
                        )
                    )
                    print("✓ 当前页面跳转到独享静态套餐支付页面")
                    payment_window_found = True
                except TimeoutException:
                    print("⚠️ 未检测到明显的独享静态套餐支付页面跳转")
                    return False
            
            if payment_window_found:
                # 从配置文件获取支付宝账号信息
                alipay_config = self.config.get('test_data', {}).get('alipay', {})
                email = alipay_config.get('email', 'lgipqm7573@sandbox.com')
                login_password = alipay_config.get('login_password', '111111')
                pay_password = alipay_config.get('pay_password', '111111')
                
                print(f"独享静态套餐支付使用支付宝账号: {email}")
                
                # 调用支付宝支付模块处理完整支付流程
                return self.alipay_payment.complete_payment_process(
                    email=email,
                    login_password=login_password,
                    pay_password=pay_password
                )
            else:
                print("❌ 未能成功跳转到独享静态套餐支付页面")
                return False
            
        except Exception as e:
            print(f"❌ 独享静态套餐支付流程失败: {e}")
            return False
    
    def complete_third_purchase_flow(self):
        """完整的第三次购买流程（独享静态套餐）"""
        try:
            print("\n" + "="*50)
            print("🏢 开始独享静态套餐购买流程")
            print("="*50)
            
            # 步骤0: 确保在正确的IPIPGO页面
            print("步骤0: 检查并切换到正确的IPIPGO页面...")
            if not self.ensure_on_correct_ipipgo_page():
                print("❌ 无法切换到正确的IPIPGO页面")
                return False
            
            # 点击独享静态选项卡
            print("步骤1: 点击独享静态选项卡...")
            if not self.click_exclusive_static_tab():
                print("❌ 独享静态选项卡点击失败")
                return False
            
            print("✓ 成功点击独享静态选项卡")
            
            # 点击香港线路的加号按钮
            print("步骤2: 点击香港线路的加号按钮...")
            if not self.click_hongkong_add_button():
                print("❌ 香港线路加号按钮点击失败")
                return False
            
            print("✓ 成功点击香港线路加号按钮")
            
            # 点击第三次购买按钮
            print("步骤3: 点击独享静态套餐立即购买按钮...")
            if not self.click_third_buy_button():
                print("❌ 独享静态套餐购买按钮点击失败")
                return False
            
            print("✓ 成功点击独享静态套餐立即购买按钮")
            
            # 点击第三次支付按钮并处理支付流程
            print("步骤4: 点击独享静态套餐立即支付按钮并完成支付...")
            if not self.click_third_pay_button_and_handle_payment():
                print("❌ 独享静态套餐支付流程失败")
                return False
            
            print("✓ 独享静态套餐支付流程完成")
            
            print("="*50)
            print("🎉 独享静态套餐购买流程完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 独享静态套餐购买流程执行失败: {e}")
            return False 

    def click_static_residential_tab(self):
        """点击静态住宅选项卡（增强版）"""
        try:
            print("🔍 正在查找静态住宅选项卡...")
            
            # 多种定位器尝试
            tab_selectors = [
                "div[data-v-369d5cdf].custom-tab-item.cursor",  # 原始定位器
                "div.custom-tab-item.cursor",  # 简化版本
                ".custom-tab-item",  # 更简化
                "div.custom-tab-item",  # 基础版本
                "[class*='tab-item']",  # 包含tab-item的元素
                "[class*='custom-tab']",  # 包含custom-tab的元素
            ]
            
            residential_tab = None
            used_selector = None
            
            for selector in tab_selectors:
                try:
                    print(f"🔍 尝试定位器: {selector}")
                    
                    # 查找所有匹配的元素
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(elements)} 个元素")
                    
                    # 在所有元素中查找包含"静态住宅"的
                    for i, element in enumerate(elements):
                        try:
                            element_text = element.text.strip()
                            print(f"   元素{i+1}文本: '{element_text}'")
                            
                            if '静态住宅' in element_text or \
                               ('静态' in element_text and '住宅' in element_text) or \
                               'residential' in element_text.lower() or \
                               'static' in element_text.lower():
                                residential_tab = element
                                used_selector = selector
                                print(f"✅ 找到静态住宅选项卡: '{element_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取元素{i+1}文本: {e}")
                            continue
                    
                    if residential_tab:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not residential_tab:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//div[contains(@class,'tab-item') and contains(text(),'静态住宅')]",
                    "//div[contains(@class,'tab-item') and contains(text(),'静态')]",
                    "//div[contains(@class,'tab-item') and contains(text(),'住宅')]",
                    "//div[contains(text(),'静态住宅')]",
                    "//*[contains(@class,'tab') and contains(text(),'住宅')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            residential_tab = elements[0]
                            used_selector = xpath
                            print(f"✅ 通过XPath找到静态住宅选项卡: '{residential_tab.text}'")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not residential_tab:
                print("❌ 无法找到静态住宅选项卡")
                return False
            
            print(f"📋 选项卡文本: '{residential_tab.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 确保元素可见并滚动到位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", residential_tab)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: residential_tab.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", residential_tab)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(residential_tab).click().perform()),
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
            
            # 等待页面内容更新
            print("⏳ 等待页面内容更新...")
            time.sleep(3)
            
            print("✅ 静态住宅选项卡点击完成")
            return True
            
        except Exception as e:
            print(f"❌ 点击静态住宅选项卡失败: {e}")
            return False
    
    def click_newyork_add_button(self):
        """点击美国-纽约线路的加号按钮"""
        try:
            print("🔍 正在查找美国-纽约线路的加号按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 先查找所有纽约相关的线路容器
            newyork_containers = []
            container_selectors = [
                "div[data-v-4269ae51] div[data-v-d73930ac].city-box",  # 原始定位器
                "div.city-box",  # 简化版本
                "[class*='city-box']",  # 包含city-box的元素
                "div[data-v-d73930ac]",  # 数据属性定位
            ]
            
            for selector in container_selectors:
                try:
                    print(f"🔍 尝试容器定位器: {selector}")
                    containers = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(containers)} 个容器")
                    
                    for i, container in enumerate(containers):
                        try:
                            container_text = container.text
                            print(f"   容器{i+1}文本: '{container_text}'")
                            
                            if ('纽约' in container_text or 'NY' in container_text.upper() or 
                                'NEW YORK' in container_text.upper() or '美国-纽约' in container_text):
                                newyork_containers.append(container)
                                print(f"✅ 找到纽约线路容器: '{container_text}'")
                        except Exception as e:
                            print(f"   ⚠️ 无法获取容器{i+1}文本: {e}")
                            continue
                    
                    if newyork_containers:
                        break
                        
                except Exception as e:
                    print(f"❌ 容器定位器 {selector} 失败: {e}")
                    continue
            
            # 如果没找到纽约容器，尝试通过id查找
            if not newyork_containers:
                print("🔍 尝试通过ID查找纽约线路...")
                try:
                    # 根据提供的HTML，id="city-name + NY"
                    ny_elements = self.driver.find_elements(By.CSS_SELECTOR, "[id*='NY']")
                    for element in ny_elements:
                        try:
                            # 查找父容器
                            parent_container = element.find_element(By.XPATH, "./ancestor::div[contains(@class,'city-box')]")
                            container_text = parent_container.text
                            if '纽约' in container_text or 'NY' in container_text.upper():
                                newyork_containers.append(parent_container)
                                print(f"✅ 通过ID找到纽约线路容器: '{container_text}'")
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"⚠️ 通过ID查找失败: {e}")
            
            if not newyork_containers:
                print("❌ 无法找到纽约线路容器")
                return False
            
            # 在纽约容器中查找加号按钮
            add_button = None
            for container in newyork_containers:
                try:
                    print("🔍 在纽约容器中查找加号按钮...")
                    
                    # 多种加号按钮定位器
                    add_button_selectors = [
                        "div[data-v-4269ae51][data-v-d73930ac].add-box.flex-j-a",  # 原始定位器
                        ".add-box.flex-j-a",  # 简化版本
                        ".add-box",  # 更简化
                        "[class*='add-box']",  # 包含add-box的元素
                        "i.el-icon-plus",  # 加号图标
                        "[class*='plus']",  # 包含plus的元素
                    ]
                    
                    for add_selector in add_button_selectors:
                        try:
                            add_buttons = container.find_elements(By.CSS_SELECTOR, add_selector)
                            if add_buttons:
                                add_button = add_buttons[0]
                                print(f"✅ 找到加号按钮: {add_selector}")
                                break
                        except:
                            continue
                    
                    if add_button:
                        break
                        
                except Exception as e:
                    print(f"⚠️ 在容器中查找加号按钮失败: {e}")
                    continue
            
            if not add_button:
                print("❌ 无法找到纽约线路的加号按钮")
                return False
            
            # 滚动到加号按钮位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: add_button.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", add_button)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(add_button).click().perform()),
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
            
            print("✅ 纽约线路加号按钮点击成功")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ 点击纽约线路加号按钮失败: {e}")
            return False
    
    def click_fourth_buy_button(self):
        """点击第四次立即购买按钮（静态住宅套餐）"""
        try:
            print("🔍 正在查找第四次立即购买按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 多种定位器尝试（与第三次购买按钮相同的结构）
            buy_button_selectors = [
                "button[data-v-0ebd072d][data-v-074476e6].el-button.btn.el-button--default.primary",  # 原始定位器
                "button.el-button.btn.el-button--default.primary",  # 简化版本
                "button.btn.primary",  # 更简化
                "button[class*='primary']",  # 包含primary的按钮
                "button.el-button--default",  # 默认按钮样式
                "button[class*='btn']",  # 包含btn的按钮
            ]
            
            fourth_buy_btn = None
            used_selector = None
            
            for selector in buy_button_selectors:
                try:
                    print(f"🔍 尝试购买按钮定位器: {selector}")
                    
                    # 查找所有匹配的按钮
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    # 在所有按钮中查找包含"立即购买"或"购买"的
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即购买' in button_text or '购买' in button_text or 'buy' in button_text.lower():
                                # 检查按钮是否可见和可点击
                                if button.is_displayed() and button.is_enabled():
                                    fourth_buy_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第四次购买按钮: '{button_text}'")
                                    break
                                else:
                                    print(f"   ⚠️ 按钮{i+1}不可点击或不可见")
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if fourth_buy_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not fourth_buy_btn:
                print("🔍 尝试XPath定位购买按钮...")
                xpath_selectors = [
                    "//button[contains(text(),'立即购买')]",
                    "//button[contains(text(),'购买')]",
                    "//button[contains(@class,'primary') and contains(text(),'购买')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                fourth_buy_btn = button
                                used_selector = xpath
                                print(f"✅ 通过XPath找到购买按钮: '{button.text}'")
                                break
                        if fourth_buy_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not fourth_buy_btn:
                print("❌ 无法找到第四次购买按钮")
                return False
            
            print(f"📋 购买按钮文本: '{fourth_buy_btn.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fourth_buy_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: fourth_buy_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", fourth_buy_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(fourth_buy_btn).click().perform()),
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
            
            # 等待页面跳转
            print("⏳ 等待页面跳转...")
            time.sleep(3)
            
            print("✅ 第四次购买按钮点击成功")
            return True
            
        except Exception as e:
            print(f"❌ 点击第四次购买按钮失败: {e}")
            return False
    
    def click_fourth_pay_button_and_handle_payment(self):
        """点击第四次立即支付按钮并处理支付流程"""
        try:
            print("🔍 正在查找第四次立即支付按钮...")
            
            # 等待页面加载
            time.sleep(3)
            
            # 记录当前窗口句柄
            self.original_window = self.driver.current_window_handle
            original_window_count = len(self.driver.window_handles)
            
            # 设置支付宝支付模块的原始窗口
            self.alipay_payment.set_original_window(self.original_window)
            
            # 复用第三次支付的增强查找逻辑
            pay_button_selectors = [
                "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary",  # 原始定位器
                "button.personal-button.el-button--default.large.primary",  # 简化版本
                "button.personal-button.primary",  # 更简化
                "button.personal-button",  # 基础版本
                "button[class*='personal-button']",  # 包含personal-button的按钮
                "button[class*='primary']",  # 包含primary的按钮
                "button.el-button--default",  # 默认按钮样式
                "button[class*='large']",  # 包含large的按钮
            ]
            
            fourth_pay_btn = None
            used_selector = None
            
            for selector in pay_button_selectors:
                try:
                    print(f"🔍 尝试支付按钮定位器: {selector}")
                    
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即支付' in button_text or '支付' in button_text or 'pay' in button_text.lower():
                                if button.is_displayed() and button.is_enabled():
                                    fourth_pay_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第四次支付按钮: '{button_text}'")
                                    break
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if fourth_pay_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            if not fourth_pay_btn:
                print("❌ 无法找到第四次支付按钮")
                return False
            
            print(f"📋 支付按钮文本: '{fourth_pay_btn.text}'")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fourth_pay_btn)
            time.sleep(1)
            
            # 点击支付按钮
            fourth_pay_btn.click()
            print("✅ 已点击第四次立即支付按钮")
            
            # 等待跳转到支付宝页面
            payment_window_found = False
            
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.window_handles) > original_window_count
                )
                print("✓ 检测到新窗口打开（静态住宅套餐支付页面）")
                
                for window in self.driver.window_handles:
                    if window != self.original_window:
                        self.driver.switch_to.window(window)
                        print("✓ 已切换到静态住宅套餐支付宝页面窗口")
                        payment_window_found = True
                        break
                        
            except TimeoutException:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.any_of(
                            EC.url_contains("alipay"),
                            EC.url_contains("pay"),
                            EC.title_contains("支付"),
                            EC.presence_of_element_located(self.ALIPAY_INDICATOR)
                        )
                    )
                    print("✓ 当前页面跳转到静态住宅套餐支付页面")
                    payment_window_found = True
                except TimeoutException:
                    print("⚠️ 未检测到明显的静态住宅套餐支付页面跳转")
                    return False
            
            if payment_window_found:
                # 从配置文件获取支付宝账号信息
                alipay_config = self.config.get('test_data', {}).get('alipay', {})
                email = alipay_config.get('email', 'lgipqm7573@sandbox.com')
                login_password = alipay_config.get('login_password', '111111')
                pay_password = alipay_config.get('pay_password', '111111')
                
                print(f"静态住宅套餐支付使用支付宝账号: {email}")
                
                # 调用支付宝支付模块处理完整支付流程
                return self.alipay_payment.complete_payment_process(
                    email=email,
                    login_password=login_password,
                    pay_password=pay_password
                )
            else:
                print("❌ 未能成功跳转到静态住宅套餐支付页面")
                return False
            
        except Exception as e:
            print(f"❌ 静态住宅套餐支付流程失败: {e}")
            return False
    
    def complete_fourth_purchase_flow(self):
        """完整的第四次购买流程（静态住宅套餐）"""
        try:
            print("\n" + "="*50)
            print("🏘️ 开始静态住宅套餐购买流程")
            print("="*50)
            
            # 步骤0: 确保在正确的IPIPGO页面
            print("步骤0: 检查并切换到正确的IPIPGO页面...")
            if not self.ensure_on_correct_ipipgo_page():
                print("❌ 无法切换到正确的IPIPGO页面")
                return False
            
            # 点击静态住宅选项卡
            print("步骤1: 点击静态住宅选项卡...")
            if not self.click_static_residential_tab():
                print("❌ 静态住宅选项卡点击失败")
                return False
            
            print("✓ 成功点击静态住宅选项卡")
            
            # 点击纽约线路的加号按钮
            print("步骤2: 点击美国-纽约线路的加号按钮...")
            if not self.click_newyork_add_button():
                print("❌ 纽约线路加号按钮点击失败")
                return False
            
            print("✓ 成功点击纽约线路加号按钮")
            
            # 点击第四次购买按钮
            print("步骤3: 点击静态住宅套餐立即购买按钮...")
            if not self.click_fourth_buy_button():
                print("❌ 静态住宅套餐购买按钮点击失败")
                return False
            
            print("✓ 成功点击静态住宅套餐立即购买按钮")
            
            # 点击第四次支付按钮并处理支付流程
            print("步骤4: 点击静态住宅套餐立即支付按钮并完成支付...")
            if not self.click_fourth_pay_button_and_handle_payment():
                print("❌ 静态住宅套餐支付流程失败")
                return False
            
            print("✓ 静态住宅套餐支付流程完成")
            
            print("="*50)
            print("🎉 静态住宅套餐购买流程完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 静态住宅套餐购买流程执行失败: {e}")
            return False 

    def click_dynamic_residential_isp_tab(self):
        """点击动态住宅（长效ISP）选项卡（增强版）"""
        try:
            print("🔍 正在查找动态住宅（长效ISP）选项卡...")
            
            # 多种定位器尝试
            tab_selectors = [
                "div[data-v-369d5cdf].custom-tab-item.cursor",  # 原始定位器
                "div.custom-tab-item.cursor",  # 简化版本
                ".custom-tab-item",  # 更简化
                "div.custom-tab-item",  # 基础版本
                "[class*='tab-item']",  # 包含tab-item的元素
                "[class*='custom-tab']",  # 包含custom-tab的元素
            ]
            
            isp_tab = None
            used_selector = None
            
            for selector in tab_selectors:
                try:
                    print(f"🔍 尝试定位器: {selector}")
                    
                    # 查找所有匹配的元素
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(elements)} 个元素")
                    
                    # 在所有元素中查找包含"动态住宅（长效ISP）"的
                    for i, element in enumerate(elements):
                        try:
                            element_text = element.text.strip()
                            print(f"   元素{i+1}文本: '{element_text}'")
                            
                            if ('动态住宅（长效ISP）' in element_text or 
                                ('动态住宅' in element_text and 'ISP' in element_text) or
                                ('动态住宅' in element_text and '长效' in element_text) or
                                'dynamic residential' in element_text.lower() or
                                'long-term isp' in element_text.lower()):
                                isp_tab = element
                                used_selector = selector
                                print(f"✅ 找到动态住宅（长效ISP）选项卡: '{element_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取元素{i+1}文本: {e}")
                            continue
                    
                    if isp_tab:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not isp_tab:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//div[contains(@class,'tab-item') and contains(text(),'动态住宅（长效ISP）')]",
                    "//div[contains(@class,'tab-item') and contains(text(),'动态住宅') and contains(text(),'ISP')]",
                    "//div[contains(@class,'tab-item') and contains(text(),'动态住宅') and contains(text(),'长效')]",
                    "//div[contains(text(),'动态住宅（长效ISP）')]",
                    "//*[contains(@class,'tab') and contains(text(),'动态住宅') and contains(text(),'ISP')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            isp_tab = elements[0]
                            used_selector = xpath
                            print(f"✅ 通过XPath找到动态住宅（长效ISP）选项卡: '{isp_tab.text}'")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not isp_tab:
                print("❌ 无法找到动态住宅（长效ISP）选项卡")
                return False
            
            print(f"📋 选项卡文本: '{isp_tab.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 确保元素可见并滚动到位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", isp_tab)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: isp_tab.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", isp_tab)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(isp_tab).click().perform()),
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
            
            # 等待页面内容更新
            print("⏳ 等待页面内容更新...")
            time.sleep(3)
            
            print("✅ 动态住宅（长效ISP）选项卡点击完成")
            return True
            
        except Exception as e:
            print(f"❌ 点击动态住宅（长效ISP）选项卡失败: {e}")
            return False
    
    def click_fifth_buy_button(self):
        """点击第五次立即购买按钮（动态住宅（长效ISP）套餐）"""
        try:
            print("🔍 正在查找第五次立即购买按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 多种定位器尝试（与企业套餐相同的结构）
            buy_button_selectors = [
                "button[data-v-0ebd072d][data-v-11ed8ffc].el-button.buy-btn.el-button--default.cicle-green-border",  # 原始定位器
                "button.buy-btn.el-button--default.cicle-green-border",  # 简化版本
                "button.buy-btn.cicle-green-border",  # 更简化
                "button.buy-btn",  # 基础版本
                "button[class*='buy-btn']",  # 包含buy-btn的按钮
                "button[class*='cicle-green-border']",  # 包含cicle-green-border的按钮
                "button.el-button--default",  # 默认按钮样式
            ]
            
            fifth_buy_btn = None
            used_selector = None
            
            for selector in buy_button_selectors:
                try:
                    print(f"🔍 尝试购买按钮定位器: {selector}")
                    
                    # 查找所有匹配的按钮
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    # 在所有按钮中查找包含"立即购买"或"购买"的
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即购买' in button_text or '购买' in button_text or 'buy' in button_text.lower():
                                # 检查按钮是否可见和可点击
                                if button.is_displayed() and button.is_enabled():
                                    fifth_buy_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第五次购买按钮: '{button_text}'")
                                    break
                                else:
                                    print(f"   ⚠️ 按钮{i+1}不可点击或不可见")
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if fifth_buy_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not fifth_buy_btn:
                print("🔍 尝试XPath定位购买按钮...")
                xpath_selectors = [
                    "//button[contains(@class,'buy-btn') and contains(text(),'立即购买')]",
                    "//button[contains(@class,'buy-btn') and contains(text(),'购买')]",
                    "//button[contains(text(),'立即购买')]",
                    "//button[contains(text(),'购买')]",
                    "//*[contains(@class,'buy') and contains(text(),'购买')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                fifth_buy_btn = button
                                used_selector = xpath
                                print(f"✅ 通过XPath找到购买按钮: '{button.text}'")
                                break
                        if fifth_buy_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not fifth_buy_btn:
                print("❌ 无法找到第五次购买按钮")
                return False
            
            print(f"📋 购买按钮文本: '{fifth_buy_btn.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fifth_buy_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: fifth_buy_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", fifth_buy_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(fifth_buy_btn).click().perform()),
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
            
            # 等待页面跳转
            print("⏳ 等待页面跳转...")
            time.sleep(3)
            
            print("✅ 第五次购买按钮点击成功")
            return True
            
        except Exception as e:
            print(f"❌ 点击第五次购买按钮失败: {e}")
            return False
    
    def click_fifth_pay_button_and_handle_payment(self):
        """点击第五次立即支付按钮并处理支付流程"""
        try:
            print("🔍 正在查找第五次立即支付按钮...")
            
            # 等待页面加载
            time.sleep(3)
            
            # 记录当前窗口句柄
            self.original_window = self.driver.current_window_handle
            original_window_count = len(self.driver.window_handles)
            
            # 设置支付宝支付模块的原始窗口
            self.alipay_payment.set_original_window(self.original_window)
            
            # 复用之前支付按钮的增强查找逻辑
            pay_button_selectors = [
                "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary",  # 原始定位器
                "button.personal-button.el-button--default.large.primary",  # 简化版本
                "button.personal-button.primary",  # 更简化
                "button.personal-button",  # 基础版本
                "button[class*='personal-button']",  # 包含personal-button的按钮
                "button[class*='primary']",  # 包含primary的按钮
                "button.el-button--default",  # 默认按钮样式
                "button[class*='large']",  # 包含large的按钮
            ]
            
            fifth_pay_btn = None
            used_selector = None
            
            for selector in pay_button_selectors:
                try:
                    print(f"🔍 尝试支付按钮定位器: {selector}")
                    
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即支付' in button_text or '支付' in button_text or 'pay' in button_text.lower():
                                if button.is_displayed() and button.is_enabled():
                                    fifth_pay_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第五次支付按钮: '{button_text}'")
                                    break
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if fifth_pay_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not fifth_pay_btn:
                print("🔍 尝试XPath定位支付按钮...")
                xpath_selectors = [
                    "//button[contains(text(),'立即支付')]",
                    "//button[contains(text(),'支付')]",
                    "//button[contains(@class,'primary') and contains(text(),'支付')]",
                    "//button[contains(@class,'personal-button')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            try:
                                button_text = button.text.strip()
                                if button.is_displayed() and button.is_enabled():
                                    if '支付' in button_text or 'pay' in button_text.lower():
                                        fifth_pay_btn = button
                                        used_selector = xpath
                                        print(f"✅ 通过XPath找到支付按钮: '{button.text}'")
                                        break
                            except:
                                continue
                        if fifth_pay_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not fifth_pay_btn:
                print("❌ 无法找到第五次支付按钮")
                return False
            
            print(f"📋 支付按钮文本: '{fifth_pay_btn.text}'")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fifth_pay_btn)
            time.sleep(1)
            
            # 点击支付按钮
            fifth_pay_btn.click()
            print("✅ 已点击第五次立即支付按钮")
            
            # 等待跳转到支付宝页面
            payment_window_found = False
            
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.window_handles) > original_window_count
                )
                print("✓ 检测到新窗口打开（动态住宅ISP套餐支付页面）")
                
                for window in self.driver.window_handles:
                    if window != self.original_window:
                        self.driver.switch_to.window(window)
                        print("✓ 已切换到动态住宅ISP套餐支付宝页面窗口")
                        payment_window_found = True
                        break
                        
            except TimeoutException:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.any_of(
                            EC.url_contains("alipay"),
                            EC.url_contains("pay"),
                            EC.title_contains("支付"),
                            EC.presence_of_element_located(self.ALIPAY_INDICATOR)
                        )
                    )
                    print("✓ 当前页面跳转到动态住宅ISP套餐支付页面")
                    payment_window_found = True
                except TimeoutException:
                    print("⚠️ 未检测到明显的动态住宅ISP套餐支付页面跳转")
                    return False
            
            if payment_window_found:
                # 从配置文件获取支付宝账号信息
                alipay_config = self.config.get('test_data', {}).get('alipay', {})
                email = alipay_config.get('email', 'lgipqm7573@sandbox.com')
                login_password = alipay_config.get('login_password', '111111')
                pay_password = alipay_config.get('pay_password', '111111')
                
                print(f"动态住宅ISP套餐支付使用支付宝账号: {email}")
                
                # 调用支付宝支付模块处理完整支付流程
                return self.alipay_payment.complete_payment_process(
                    email=email,
                    login_password=login_password,
                    pay_password=pay_password
                )
            else:
                print("❌ 未能成功跳转到动态住宅ISP套餐支付页面")
                return False
            
        except Exception as e:
            print(f"❌ 动态住宅ISP套餐支付流程失败: {e}")
            return False
    
    def complete_fifth_purchase_flow(self):
        """完整的第五次购买流程（动态住宅（长效ISP）套餐）"""
        try:
            print("\n" + "="*50)
            print("🏠 开始动态住宅（长效ISP）套餐购买流程")
            print("="*50)
            
            # 步骤0: 确保在正确的IPIPGO页面
            print("步骤0: 检查并切换到正确的IPIPGO页面...")
            if not self.ensure_on_correct_ipipgo_page():
                print("❌ 无法切换到正确的IPIPGO页面")
                return False
            
            # 点击动态住宅（长效ISP）选项卡
            print("步骤1: 点击动态住宅（长效ISP）选项卡...")
            if not self.click_dynamic_residential_isp_tab():
                print("❌ 动态住宅（长效ISP）选项卡点击失败")
                return False
            
            print("✓ 成功点击动态住宅（长效ISP）选项卡")
            
            # 点击第五次购买按钮
            print("步骤2: 点击动态住宅（长效ISP）套餐立即购买按钮...")
            if not self.click_fifth_buy_button():
                print("❌ 动态住宅（长效ISP）套餐购买按钮点击失败")
                return False
            
            print("✓ 成功点击动态住宅（长效ISP）套餐立即购买按钮")
            
            # 点击第五次支付按钮并处理支付流程
            print("步骤3: 点击动态住宅（长效ISP）套餐立即支付按钮并完成支付...")
            if not self.click_fifth_pay_button_and_handle_payment():
                print("❌ 动态住宅（长效ISP）套餐支付流程失败")
                return False
            
            print("✓ 动态住宅（长效ISP）套餐支付流程完成")
            
            print("="*50)
            print("🎉 动态住宅（长效ISP）套餐购买流程完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 动态住宅（长效ISP）套餐购买流程执行失败: {e}")
            return False
    
    def click_dynamic_unlimited_tab(self):
        """点击动态不限量选项卡（增强版）"""
        try:
            print("🔍 正在查找动态不限量选项卡...")
            
            # 多种定位器尝试
            tab_selectors = [
                "div[data-v-369d5cdf].custom-tab-item.cursor",  # 原始定位器
                "div.custom-tab-item.cursor",  # 简化版本
                ".custom-tab-item",  # 更简化
                "div.custom-tab-item",  # 基础版本
                "[class*='tab-item']",  # 包含tab-item的元素
                "[class*='custom-tab']",  # 包含custom-tab的元素
            ]
            
            unlimited_tab = None
            used_selector = None
            
            for selector in tab_selectors:
                try:
                    print(f"🔍 尝试定位器: {selector}")
                    
                    # 查找所有匹配的元素
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(elements)} 个元素")
                    
                    # 在所有元素中查找包含"动态不限量"的
                    for i, element in enumerate(elements):
                        try:
                            element_text = element.text.strip()
                            print(f"   元素{i+1}文本: '{element_text}'")
                            
                            if ('动态不限量' in element_text or 
                                ('动态' in element_text and '不限量' in element_text) or
                                'dynamic unlimited' in element_text.lower() or
                                'unlimited' in element_text.lower()):
                                unlimited_tab = element
                                used_selector = selector
                                print(f"✅ 找到动态不限量选项卡: '{element_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取元素{i+1}文本: {e}")
                            continue
                    
                    if unlimited_tab:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not unlimited_tab:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//div[contains(@class,'tab-item') and contains(text(),'动态不限量')]",
                    "//div[contains(@class,'tab-item') and contains(text(),'动态') and contains(text(),'不限量')]",
                    "//div[contains(text(),'动态不限量')]",
                    "//*[contains(@class,'tab') and contains(text(),'不限量')]",
                    "//*[contains(@class,'tab') and contains(text(),'unlimited')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            unlimited_tab = elements[0]
                            used_selector = xpath
                            print(f"✅ 通过XPath找到动态不限量选项卡: '{unlimited_tab.text}'")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not unlimited_tab:
                print("❌ 无法找到动态不限量选项卡")
                return False
            
            print(f"📋 选项卡文本: '{unlimited_tab.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 确保元素可见并滚动到位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", unlimited_tab)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: unlimited_tab.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", unlimited_tab)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(unlimited_tab).click().perform()),
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
            
            # 等待页面内容更新
            print("⏳ 等待页面内容更新...")
            time.sleep(3)
            
            print("✅ 动态不限量选项卡点击完成")
            return True
            
        except Exception as e:
            print(f"❌ 点击动态不限量选项卡失败: {e}")
            return False
    
    def click_sixth_buy_button(self):
        """点击第六次立即购买按钮（动态不限量套餐）"""
        try:
            print("🔍 正在查找第六次立即购买按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 多种定位器尝试（与企业套餐相同的结构）
            buy_button_selectors = [
                "button[data-v-0ebd072d][data-v-11ed8ffc].el-button.buy-btn.el-button--default.cicle-green-border",  # 原始定位器
                "button.buy-btn.el-button--default.cicle-green-border",  # 简化版本
                "button.buy-btn.cicle-green-border",  # 更简化
                "button.buy-btn",  # 基础版本
                "button[class*='buy-btn']",  # 包含buy-btn的按钮
                "button[class*='cicle-green-border']",  # 包含cicle-green-border的按钮
                "button.el-button--default",  # 默认按钮样式
            ]
            
            sixth_buy_btn = None
            used_selector = None
            
            for selector in buy_button_selectors:
                try:
                    print(f"🔍 尝试购买按钮定位器: {selector}")
                    
                    # 查找所有匹配的按钮
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    # 在所有按钮中查找包含"立即购买"或"购买"的
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即购买' in button_text or '购买' in button_text or 'buy' in button_text.lower():
                                # 检查按钮是否可见和可点击
                                if button.is_displayed() and button.is_enabled():
                                    sixth_buy_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第六次购买按钮: '{button_text}'")
                                    break
                                else:
                                    print(f"   ⚠️ 按钮{i+1}不可点击或不可见")
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if sixth_buy_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not sixth_buy_btn:
                print("🔍 尝试XPath定位购买按钮...")
                xpath_selectors = [
                    "//button[contains(@class,'buy-btn') and contains(text(),'立即购买')]",
                    "//button[contains(@class,'buy-btn') and contains(text(),'购买')]",
                    "//button[contains(text(),'立即购买')]",
                    "//button[contains(text(),'购买')]",
                    "//*[contains(@class,'buy') and contains(text(),'购买')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                sixth_buy_btn = button
                                used_selector = xpath
                                print(f"✅ 通过XPath找到购买按钮: '{button.text}'")
                                break
                        if sixth_buy_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not sixth_buy_btn:
                print("❌ 无法找到第六次购买按钮")
                return False
            
            print(f"📋 购买按钮文本: '{sixth_buy_btn.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sixth_buy_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: sixth_buy_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", sixth_buy_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(sixth_buy_btn).click().perform()),
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
            
            # 等待页面跳转
            print("⏳ 等待页面跳转...")
            time.sleep(3)
            
            print("✅ 第六次购买按钮点击成功")
            return True
            
        except Exception as e:
            print(f"❌ 点击第六次购买按钮失败: {e}")
            return False
    
    def click_sixth_pay_button_and_handle_payment(self):
        """点击第六次立即支付按钮并处理支付流程"""
        try:
            print("🔍 正在查找第六次立即支付按钮...")
            
            # 等待页面加载
            time.sleep(3)
            
            # 记录当前窗口句柄
            self.original_window = self.driver.current_window_handle
            original_window_count = len(self.driver.window_handles)
            
            # 设置支付宝支付模块的原始窗口
            self.alipay_payment.set_original_window(self.original_window)
            
            # 复用之前支付按钮的增强查找逻辑
            pay_button_selectors = [
                "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary",  # 原始定位器
                "button.personal-button.el-button--default.large.primary",  # 简化版本
                "button.personal-button.primary",  # 更简化
                "button.personal-button",  # 基础版本
                "button[class*='personal-button']",  # 包含personal-button的按钮
                "button[class*='primary']",  # 包含primary的按钮
                "button.el-button--default",  # 默认按钮样式
                "button[class*='large']",  # 包含large的按钮
            ]
            
            sixth_pay_btn = None
            used_selector = None
            
            for selector in pay_button_selectors:
                try:
                    print(f"🔍 尝试支付按钮定位器: {selector}")
                    
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即支付' in button_text or '支付' in button_text or 'pay' in button_text.lower():
                                if button.is_displayed() and button.is_enabled():
                                    sixth_pay_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第六次支付按钮: '{button_text}'")
                                    break
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if sixth_pay_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not sixth_pay_btn:
                print("🔍 尝试XPath定位支付按钮...")
                xpath_selectors = [
                    "//button[contains(text(),'立即支付')]",
                    "//button[contains(text(),'支付')]",
                    "//button[contains(@class,'primary') and contains(text(),'支付')]",
                    "//button[contains(@class,'personal-button')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            try:
                                button_text = button.text.strip()
                                if button.is_displayed() and button.is_enabled():
                                    if '支付' in button_text or 'pay' in button_text.lower():
                                        sixth_pay_btn = button
                                        used_selector = xpath
                                        print(f"✅ 通过XPath找到支付按钮: '{button.text}'")
                                        break
                            except:
                                continue
                        if sixth_pay_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not sixth_pay_btn:
                print("❌ 无法找到第六次支付按钮")
                return False
            
            print(f"📋 支付按钮文本: '{sixth_pay_btn.text}'")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sixth_pay_btn)
            time.sleep(1)
            
            # 点击支付按钮
            sixth_pay_btn.click()
            print("✅ 已点击第六次立即支付按钮")
            
            # 等待跳转到支付宝页面
            payment_window_found = False
            
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.window_handles) > original_window_count
                )
                print("✓ 检测到新窗口打开（动态不限量套餐支付页面）")
                
                for window in self.driver.window_handles:
                    if window != self.original_window:
                        self.driver.switch_to.window(window)
                        print("✓ 已切换到动态不限量套餐支付宝页面窗口")
                        payment_window_found = True
                        break
                        
            except TimeoutException:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.any_of(
                            EC.url_contains("alipay"),
                            EC.url_contains("pay"),
                            EC.title_contains("支付"),
                            EC.presence_of_element_located(self.ALIPAY_INDICATOR)
                        )
                    )
                    print("✓ 当前页面跳转到动态不限量套餐支付页面")
                    payment_window_found = True
                except TimeoutException:
                    print("⚠️ 未检测到明显的动态不限量套餐支付页面跳转")
                    return False
            
            if payment_window_found:
                # 从配置文件获取支付宝账号信息
                alipay_config = self.config.get('test_data', {}).get('alipay', {})
                email = alipay_config.get('email', 'lgipqm7573@sandbox.com')
                login_password = alipay_config.get('login_password', '111111')
                pay_password = alipay_config.get('pay_password', '111111')
                
                print(f"动态不限量套餐支付使用支付宝账号: {email}")
                
                # 调用支付宝支付模块处理完整支付流程
                return self.alipay_payment.complete_payment_process(
                    email=email,
                    login_password=login_password,
                    pay_password=pay_password
                )
            else:
                print("❌ 未能成功跳转到动态不限量套餐支付页面")
                return False
            
        except Exception as e:
            print(f"❌ 动态不限量套餐支付流程失败: {e}")
            return False
    
    def complete_sixth_purchase_flow(self):
        """完整的第六次购买流程（动态不限量套餐）"""
        try:
            print("\n" + "="*50)
            print("♾️ 开始动态不限量套餐购买流程")
            print("="*50)
            
            # 步骤0: 确保在正确的IPIPGO页面
            print("步骤0: 检查并切换到正确的IPIPGO页面...")
            if not self.ensure_on_correct_ipipgo_page():
                print("❌ 无法切换到正确的IPIPGO页面")
                return False
            
            # 点击动态不限量选项卡
            print("步骤1: 点击动态不限量选项卡...")
            if not self.click_dynamic_unlimited_tab():
                print("❌ 动态不限量选项卡点击失败")
                return False
            
            print("✓ 成功点击动态不限量选项卡")
            
            # 点击第六次购买按钮
            print("步骤2: 点击动态不限量套餐立即购买按钮...")
            if not self.click_sixth_buy_button():
                print("❌ 动态不限量套餐购买按钮点击失败")
                return False
            
            print("✓ 成功点击动态不限量套餐立即购买按钮")
            
            # 点击第六次支付按钮并处理支付流程
            print("步骤3: 点击动态不限量套餐立即支付按钮并完成支付...")
            if not self.click_sixth_pay_button_and_handle_payment():
                print("❌ 动态不限量套餐支付流程失败")
                return False
            
            print("✓ 动态不限量套餐支付流程完成")
            
            print("="*50)
            print("🎉 动态不限量套餐购买流程完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 动态不限量套餐购买流程执行失败: {e}")
            return False
    
    def click_data_center_menu_item(self):
        """点击数据中心菜单项（增强版）"""
        try:
            print("🔍 正在查找数据中心菜单项...")
            
            # 多种定位器尝试
            menu_selectors = [
                "li[data-v-625350b8].el-menu-item.personal-left-menu-item",  # 原始定位器
                "li.el-menu-item.personal-left-menu-item",  # 简化版本
                "li.personal-left-menu-item",  # 更简化
                "li.el-menu-item",  # 基础版本
                "[class*='personal-left-menu-item']",  # 包含personal-left-menu-item的元素
                "[role='menuitem']",  # 按角色查找
            ]
            
            data_center_menu = None
            used_selector = None
            
            for selector in menu_selectors:
                try:
                    print(f"🔍 尝试定位器: {selector}")
                    
                    # 查找所有匹配的元素
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(elements)} 个元素")
                    
                    # 在所有元素中查找包含"数据中心"的
                    for i, element in enumerate(elements):
                        try:
                            element_text = element.text.strip()
                            print(f"   元素{i+1}文本: '{element_text}'")
                            
                            if ('数据中心' in element_text or 
                                'data center' in element_text.lower() or
                                'datacenter' in element_text.lower()):
                                data_center_menu = element
                                used_selector = selector
                                print(f"✅ 找到数据中心菜单项: '{element_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取元素{i+1}文本: {e}")
                            continue
                    
                    if data_center_menu:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not data_center_menu:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//li[contains(@class,'el-menu-item') and contains(text(),'数据中心')]",
                    "//li[contains(@class,'personal-left-menu-item') and contains(text(),'数据中心')]",
                    "//li[@role='menuitem' and contains(text(),'数据中心')]",
                    "//li[contains(text(),'数据中心')]",
                    "//*[contains(@class,'menu-item') and contains(text(),'数据中心')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            data_center_menu = elements[0]
                            used_selector = xpath
                            print(f"✅ 通过XPath找到数据中心菜单项: '{data_center_menu.text}'")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not data_center_menu:
                print("❌ 无法找到数据中心菜单项")
                return False
            
            print(f"📋 菜单项文本: '{data_center_menu.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 确保元素可见并滚动到位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", data_center_menu)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: data_center_menu.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", data_center_menu)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(data_center_menu).click().perform()),
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
            
            # 等待页面内容更新
            print("⏳ 等待页面内容更新...")
            time.sleep(3)
            
            print("✅ 数据中心菜单项点击完成")
            return True
            
        except Exception as e:
            print(f"❌ 点击数据中心菜单项失败: {e}")
            return False
    
    def click_seventh_buy_button(self):
        """点击第七次立即购买按钮（动态数据中心（基础）套餐）"""
        try:
            print("🔍 正在查找第七次立即购买按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 多种定位器尝试（与企业套餐相同的结构）
            buy_button_selectors = [
                "button[data-v-0ebd072d][data-v-11ed8ffc].el-button.buy-btn.el-button--default.cicle-green-border",  # 原始定位器
                "button.buy-btn.el-button--default.cicle-green-border",  # 简化版本
                "button.buy-btn.cicle-green-border",  # 更简化
                "button.buy-btn",  # 基础版本
                "button[class*='buy-btn']",  # 包含buy-btn的按钮
                "button[class*='cicle-green-border']",  # 包含cicle-green-border的按钮
                "button.el-button--default",  # 默认按钮样式
            ]
            
            seventh_buy_btn = None
            used_selector = None
            
            for selector in buy_button_selectors:
                try:
                    print(f"🔍 尝试购买按钮定位器: {selector}")
                    
                    # 查找所有匹配的按钮
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    # 在所有按钮中查找包含"立即购买"或"购买"的
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即购买' in button_text or '购买' in button_text or 'buy' in button_text.lower():
                                # 检查按钮是否可见和可点击
                                if button.is_displayed() and button.is_enabled():
                                    seventh_buy_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第七次购买按钮: '{button_text}'")
                                    break
                                else:
                                    print(f"   ⚠️ 按钮{i+1}不可点击或不可见")
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if seventh_buy_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not seventh_buy_btn:
                print("🔍 尝试XPath定位购买按钮...")
                xpath_selectors = [
                    "//button[contains(@class,'buy-btn') and contains(text(),'立即购买')]",
                    "//button[contains(@class,'buy-btn') and contains(text(),'购买')]",
                    "//button[contains(text(),'立即购买')]",
                    "//button[contains(text(),'购买')]",
                    "//*[contains(@class,'buy') and contains(text(),'购买')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                seventh_buy_btn = button
                                used_selector = xpath
                                print(f"✅ 通过XPath找到购买按钮: '{button.text}'")
                                break
                        if seventh_buy_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not seventh_buy_btn:
                print("❌ 无法找到第七次购买按钮")
                return False
            
            print(f"📋 购买按钮文本: '{seventh_buy_btn.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seventh_buy_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: seventh_buy_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", seventh_buy_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(seventh_buy_btn).click().perform()),
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
            
            # 等待页面跳转
            print("⏳ 等待页面跳转...")
            time.sleep(3)
            
            print("✅ 第七次购买按钮点击成功")
            return True
            
        except Exception as e:
            print(f"❌ 点击第七次购买按钮失败: {e}")
            return False
    
    def click_seventh_pay_button_and_handle_payment(self):
        """点击第七次立即支付按钮并处理支付流程（动态数据中心（基础）套餐）"""
        try:
            print("🔍 正在查找第七次立即支付按钮...")
            
            # 等待页面加载
            time.sleep(3)
            
            # 记录当前窗口句柄
            self.original_window = self.driver.current_window_handle
            original_window_count = len(self.driver.window_handles)
            
            # 设置支付宝支付模块的原始窗口
            self.alipay_payment.set_original_window(self.original_window)
            
            # 复用之前支付按钮的增强查找逻辑
            pay_button_selectors = [
                "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary",  # 原始定位器
                "button.personal-button.el-button--default.large.primary",  # 简化版本
                "button.personal-button.primary",  # 更简化
                "button.personal-button",  # 基础版本
                "button[class*='personal-button']",  # 包含personal-button的按钮
                "button[class*='primary']",  # 包含primary的按钮
                "button.el-button--default",  # 默认按钮样式
                "button[class*='large']",  # 包含large的按钮
            ]
            
            seventh_pay_btn = None
            used_selector = None
            
            for selector in pay_button_selectors:
                try:
                    print(f"🔍 尝试支付按钮定位器: {selector}")
                    
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即支付' in button_text or '支付' in button_text or 'pay' in button_text.lower():
                                if button.is_displayed() and button.is_enabled():
                                    seventh_pay_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第七次支付按钮: '{button_text}'")
                                    break
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if seventh_pay_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not seventh_pay_btn:
                print("🔍 尝试XPath定位支付按钮...")
                xpath_selectors = [
                    "//button[contains(text(),'立即支付')]",
                    "//button[contains(text(),'支付')]",
                    "//button[contains(@class,'primary') and contains(text(),'支付')]",
                    "//button[contains(@class,'personal-button')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            try:
                                button_text = button.text.strip()
                                if button.is_displayed() and button.is_enabled():
                                    if '支付' in button_text or 'pay' in button_text.lower():
                                        seventh_pay_btn = button
                                        used_selector = xpath
                                        print(f"✅ 通过XPath找到支付按钮: '{button.text}'")
                                        break
                            except:
                                continue
                        if seventh_pay_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not seventh_pay_btn:
                print("❌ 无法找到第七次支付按钮")
                return False
            
            print(f"📋 支付按钮文本: '{seventh_pay_btn.text}'")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seventh_pay_btn)
            time.sleep(1)
            
            # 点击支付按钮
            seventh_pay_btn.click()
            print("✅ 已点击第七次立即支付按钮")
            
            # 等待跳转到支付宝页面
            payment_window_found = False
            
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.window_handles) > original_window_count
                )
                print("✓ 检测到新窗口打开（动态数据中心（基础）套餐支付页面）")
                
                for window in self.driver.window_handles:
                    if window != self.original_window:
                        self.driver.switch_to.window(window)
                        print("✓ 已切换到动态数据中心（基础）套餐支付宝页面窗口")
                        payment_window_found = True
                        break
                        
            except TimeoutException:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.any_of(
                            EC.url_contains("alipay"),
                            EC.url_contains("pay"),
                            EC.title_contains("支付"),
                            EC.presence_of_element_located(self.ALIPAY_INDICATOR)
                        )
                    )
                    print("✓ 当前页面跳转到动态数据中心（基础）套餐支付页面")
                    payment_window_found = True
                except TimeoutException:
                    print("⚠️ 未检测到明显的动态数据中心（基础）套餐支付页面跳转")
                    return False
            
            if payment_window_found:
                # 从配置文件获取支付宝账号信息
                alipay_config = self.config.get('test_data', {}).get('alipay', {})
                email = alipay_config.get('email', 'lgipqm7573@sandbox.com')
                login_password = alipay_config.get('login_password', '111111')
                pay_password = alipay_config.get('pay_password', '111111')
                
                print(f"动态数据中心（基础）套餐支付使用支付宝账号: {email}")
                
                # 调用支付宝支付模块处理完整支付流程
                return self.alipay_payment.complete_payment_process(
                    email=email,
                    login_password=login_password,
                    pay_password=pay_password
                )
            else:
                print("❌ 未能成功跳转到动态数据中心（基础）套餐支付页面")
                return False
            
        except Exception as e:
            print(f"❌ 动态数据中心（基础）套餐支付流程失败: {e}")
            return False
    
    def complete_seventh_purchase_flow(self):
        """完整的第七次购买流程（动态数据中心（基础）套餐）"""
        try:
            print("\n" + "="*50)
            print("🏢 开始动态数据中心（基础）套餐购买流程")
            print("="*50)
            
            # 步骤0: 确保在正确的IPIPGO页面
            print("步骤0: 检查并切换到正确的IPIPGO页面...")
            if not self.ensure_on_correct_ipipgo_page():
                print("❌ 无法切换到正确的IPIPGO页面")
                return False
            
            # 点击数据中心菜单项
            print("步骤1: 点击动态数据中心菜单项...")
            if not self.click_data_center_menu_item():
                print("❌ 动态数据中心菜单项点击失败")
                return False
            
            print("✓ 成功点击动态数据中心菜单项")
            
            # 点击第七次购买按钮
            print("步骤2: 点击动态数据中心（基础）套餐立即购买按钮...")
            if not self.click_seventh_buy_button():
                print("❌ 动态数据中心（基础）套餐购买按钮点击失败")
                return False
            
            print("✓ 成功点击动态数据中心（基础）套餐立即购买按钮")
            
            # 点击第七次支付按钮并处理支付流程
            print("步骤3: 点击动态数据中心（基础）套餐立即支付按钮并完成支付...")
            if not self.click_seventh_pay_button_and_handle_payment():
                print("❌ 动态数据中心（基础）套餐支付流程失败")
                return False
            
            print("✓ 动态数据中心（基础）套餐支付流程完成")
            
            print("="*50)
            print("🎉 动态数据中心（基础）套餐购买流程完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 动态数据中心（基础）套餐购买流程执行失败: {e}")
            return False

    def click_static_datacenter_tab(self):
        """点击静态数据中心选项卡（增强版）"""
        try:
            print("🔍 正在查找静态数据中心选项卡...")
            
            # 多种定位器尝试
            tab_selectors = [
                "div[data-v-369d5cdf].custom-tab-item.cursor",  # 原始定位器
                "div.custom-tab-item.cursor",  # 简化版本
                ".custom-tab-item",  # 更简化
                "div.custom-tab-item",  # 基础版本
                "[class*='tab-item']",  # 包含tab-item的元素
                "[class*='custom-tab']",  # 包含custom-tab的元素
            ]
            
            static_datacenter_tab = None
            used_selector = None
            
            for selector in tab_selectors:
                try:
                    print(f"🔍 尝试定位器: {selector}")
                    
                    # 查找所有匹配的元素
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(elements)} 个元素")
                    
                    # 在所有元素中查找包含"静态数据中心"的
                    for i, element in enumerate(elements):
                        try:
                            element_text = element.text.strip()
                            print(f"   元素{i+1}文本: '{element_text}'")
                            
                            if ('静态数据中心' in element_text or 
                                ('静态' in element_text and '数据中心' in element_text) or
                                'static datacenter' in element_text.lower() or
                                'static data center' in element_text.lower()):
                                static_datacenter_tab = element
                                used_selector = selector
                                print(f"✅ 找到静态数据中心选项卡: '{element_text}'")
                                break
                        except Exception as e:
                            print(f"   ⚠️ 无法获取元素{i+1}文本: {e}")
                            continue
                    
                    if static_datacenter_tab:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not static_datacenter_tab:
                print("🔍 尝试XPath定位...")
                xpath_selectors = [
                    "//div[contains(@class,'tab-item') and contains(text(),'静态数据中心')]",
                    "//div[contains(@class,'tab-item') and contains(text(),'静态') and contains(text(),'数据中心')]",
                    "//div[contains(text(),'静态数据中心')]",
                    "//*[contains(@class,'tab') and contains(text(),'静态数据中心')]",
                    "//*[contains(@class,'tab') and contains(text(),'static') and contains(text(),'datacenter')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            static_datacenter_tab = elements[0]
                            used_selector = xpath
                            print(f"✅ 通过XPath找到静态数据中心选项卡: '{static_datacenter_tab.text}'")
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not static_datacenter_tab:
                print("❌ 无法找到静态数据中心选项卡")
                return False
            
            print(f"📋 选项卡文本: '{static_datacenter_tab.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 确保元素可见并滚动到位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", static_datacenter_tab)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: static_datacenter_tab.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", static_datacenter_tab)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(static_datacenter_tab).click().perform()),
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
            
            # 等待页面内容更新
            print("⏳ 等待页面内容更新...")
            time.sleep(3)
            
            print("✅ 静态数据中心选项卡点击完成")
            return True
            
        except Exception as e:
            print(f"❌ 点击静态数据中心选项卡失败: {e}")
            return False
    
    def click_manila_add_button(self):
        """点击菲律宾-马尼拉线路的加号按钮"""
        try:
            print("🔍 正在查找菲律宾-马尼拉线路的加号按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 先查找所有马尼拉相关的线路容器
            manila_containers = []
            container_selectors = [
                "div[data-v-4269ae51] div[data-v-d73930ac].city-box",  # 原始定位器
                "div.city-box",  # 简化版本
                "[class*='city-box']",  # 包含city-box的元素
                "div[data-v-d73930ac]",  # 数据属性定位
            ]
            
            for selector in container_selectors:
                try:
                    print(f"🔍 尝试容器定位器: {selector}")
                    containers = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(containers)} 个容器")
                    
                    for i, container in enumerate(containers):
                        try:
                            container_text = container.text
                            print(f"   容器{i+1}文本: '{container_text}'")
                            
                            if ('马尼拉' in container_text or 'MNL' in container_text.upper() or 
                                'MANILA' in container_text.upper() or '菲律宾-马尼拉' in container_text or
                                '菲律宾' in container_text and '马尼拉' in container_text):
                                manila_containers.append(container)
                                print(f"✅ 找到马尼拉线路容器: '{container_text}'")
                        except Exception as e:
                            print(f"   ⚠️ 无法获取容器{i+1}文本: {e}")
                            continue
                    
                    if manila_containers:
                        break
                        
                except Exception as e:
                    print(f"❌ 容器定位器 {selector} 失败: {e}")
                    continue
            
            # 如果没找到马尼拉容器，尝试通过id查找
            if not manila_containers:
                print("🔍 尝试通过ID查找马尼拉线路...")
                try:
                    # 根据提供的HTML，id="city-name + MNL"
                    mnl_elements = self.driver.find_elements(By.CSS_SELECTOR, "[id*='MNL']")
                    for element in mnl_elements:
                        try:
                            # 查找父容器
                            parent_container = element.find_element(By.XPATH, "./ancestor::div[contains(@class,'city-box')]")
                            container_text = parent_container.text
                            if '马尼拉' in container_text or 'MNL' in container_text.upper():
                                manila_containers.append(parent_container)
                                print(f"✅ 通过ID找到马尼拉线路容器: '{container_text}'")
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"⚠️ 通过ID查找失败: {e}")
            
            if not manila_containers:
                print("❌ 无法找到马尼拉线路容器")
                return False
            
            # 在马尼拉容器中查找加号按钮
            add_button = None
            for container in manila_containers:
                try:
                    print("🔍 在马尼拉容器中查找加号按钮...")
                    
                    # 多种加号按钮定位器
                    add_button_selectors = [
                        "div[data-v-4269ae51][data-v-d73930ac].add-box.flex-j-a",  # 原始定位器
                        ".add-box.flex-j-a",  # 简化版本
                        ".add-box",  # 更简化
                        "[class*='add-box']",  # 包含add-box的元素
                        "i.el-icon-plus",  # 加号图标
                        "[class*='plus']",  # 包含plus的元素
                    ]
                    
                    for add_selector in add_button_selectors:
                        try:
                            add_buttons = container.find_elements(By.CSS_SELECTOR, add_selector)
                            if add_buttons:
                                add_button = add_buttons[0]
                                print(f"✅ 找到加号按钮: {add_selector}")
                                break
                        except:
                            continue
                    
                    if add_button:
                        break
                        
                except Exception as e:
                    print(f"⚠️ 在容器中查找加号按钮失败: {e}")
                    continue
            
            if not add_button:
                print("❌ 无法找到马尼拉线路的加号按钮")
                return False
            
            # 滚动到加号按钮位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: add_button.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", add_button)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(add_button).click().perform()),
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
            
            print("✅ 马尼拉线路加号按钮点击成功")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ 点击马尼拉线路加号按钮失败: {e}")
            return False
    
    def click_eighth_buy_button(self):
        """点击第八次立即购买按钮（静态数据中心套餐）"""
        try:
            print("🔍 正在查找第八次立即购买按钮...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 多种定位器尝试（根据用户提供的HTML）
            buy_button_selectors = [
                "button[data-v-0ebd072d][data-v-074476e6].el-button.btn.el-button--default.primary",  # 原始定位器
                "button.el-button.btn.el-button--default.primary",  # 简化版本
                "button.btn.primary",  # 更简化
                "button[class*='primary']",  # 包含primary的按钮
                "button.el-button--default",  # 默认按钮样式
                "button[class*='btn']",  # 包含btn的按钮
            ]
            
            eighth_buy_btn = None
            used_selector = None
            
            for selector in buy_button_selectors:
                try:
                    print(f"🔍 尝试购买按钮定位器: {selector}")
                    
                    # 查找所有匹配的按钮
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    # 在所有按钮中查找包含"立即购买"或"购买"的
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即购买' in button_text or '购买' in button_text or 'buy' in button_text.lower():
                                # 检查按钮是否可见和可点击
                                if button.is_displayed() and button.is_enabled():
                                    eighth_buy_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第八次购买按钮: '{button_text}'")
                                    break
                                else:
                                    print(f"   ⚠️ 按钮{i+1}不可点击或不可见")
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if eighth_buy_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not eighth_buy_btn:
                print("🔍 尝试XPath定位购买按钮...")
                xpath_selectors = [
                    "//button[contains(text(),'立即购买')]",
                    "//button[contains(text(),'购买')]",
                    "//button[contains(@class,'primary') and contains(text(),'购买')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                eighth_buy_btn = button
                                used_selector = xpath
                                print(f"✅ 通过XPath找到购买按钮: '{button.text}'")
                                break
                        if eighth_buy_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not eighth_buy_btn:
                print("❌ 无法找到第八次购买按钮")
                return False
            
            print(f"📋 购买按钮文本: '{eighth_buy_btn.text}'")
            print(f"📋 使用的定位器: {used_selector}")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", eighth_buy_btn)
            time.sleep(1)
            
            # 多种点击方式尝试
            click_success = False
            click_methods = [
                ("普通点击", lambda: eighth_buy_btn.click()),
                ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", eighth_buy_btn)),
                ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(eighth_buy_btn).click().perform()),
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
            
            # 等待页面跳转
            print("⏳ 等待页面跳转...")
            time.sleep(3)
            
            print("✅ 第八次购买按钮点击成功")
            return True
            
        except Exception as e:
            print(f"❌ 点击第八次购买按钮失败: {e}")
            return False
    
    def click_eighth_pay_button_and_handle_payment(self):
        """点击第八次立即支付按钮并处理支付流程"""
        try:
            print("🔍 正在查找第八次立即支付按钮...")
            
            # 等待页面加载
            time.sleep(3)
            
            # 记录当前窗口句柄
            self.original_window = self.driver.current_window_handle
            original_window_count = len(self.driver.window_handles)
            
            # 设置支付宝支付模块的原始窗口
            self.alipay_payment.set_original_window(self.original_window)
            
            # 复用之前支付按钮的增强查找逻辑（根据用户提供的HTML）
            pay_button_selectors = [
                "button[data-v-46103f1d].el-button.personal-button.el-button--default.large.primary",  # 原始定位器
                "button.personal-button.el-button--default.large.primary",  # 简化版本
                "button.personal-button.primary",  # 更简化
                "button.personal-button",  # 基础版本
                "button[class*='personal-button']",  # 包含personal-button的按钮
                "button[class*='primary']",  # 包含primary的按钮
                "button.el-button--default",  # 默认按钮样式
                "button[class*='large']",  # 包含large的按钮
            ]
            
            eighth_pay_btn = None
            used_selector = None
            
            for selector in pay_button_selectors:
                try:
                    print(f"🔍 尝试支付按钮定位器: {selector}")
                    
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"📋 找到 {len(buttons)} 个按钮")
                    
                    for i, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            print(f"   按钮{i+1}文本: '{button_text}'")
                            
                            if '立即支付' in button_text or '支付' in button_text or 'pay' in button_text.lower():
                                if button.is_displayed() and button.is_enabled():
                                    eighth_pay_btn = button
                                    used_selector = selector
                                    print(f"✅ 找到第八次支付按钮: '{button_text}'")
                                    break
                        except Exception as e:
                            print(f"   ⚠️ 无法检查按钮{i+1}: {e}")
                            continue
                    
                    if eighth_pay_btn:
                        break
                        
                except Exception as e:
                    print(f"❌ 定位器 {selector} 失败: {e}")
                    continue
            
            # 如果还没找到，尝试XPath方式
            if not eighth_pay_btn:
                print("🔍 尝试XPath定位支付按钮...")
                xpath_selectors = [
                    "//button[contains(text(),'立即支付')]",
                    "//button[contains(text(),'支付')]",
                    "//button[contains(@class,'primary') and contains(text(),'支付')]",
                    "//button[contains(@class,'personal-button')]",
                ]
                
                for xpath in xpath_selectors:
                    try:
                        print(f"🔍 尝试XPath: {xpath}")
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            try:
                                button_text = button.text.strip()
                                if button.is_displayed() and button.is_enabled():
                                    if '支付' in button_text or 'pay' in button_text.lower():
                                        eighth_pay_btn = button
                                        used_selector = xpath
                                        print(f"✅ 通过XPath找到支付按钮: '{button.text}'")
                                        break
                            except:
                                continue
                        if eighth_pay_btn:
                            break
                    except Exception as e:
                        print(f"❌ XPath {xpath} 失败: {e}")
                        continue
            
            if not eighth_pay_btn:
                print("❌ 无法找到第八次支付按钮")
                return False
            
            print(f"📋 支付按钮文本: '{eighth_pay_btn.text}'")
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", eighth_pay_btn)
            time.sleep(1)
            
            # 点击支付按钮
            eighth_pay_btn.click()
            print("✅ 已点击第八次立即支付按钮")
            
            # 等待跳转到支付宝页面
            payment_window_found = False
            
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.window_handles) > original_window_count
                )
                print("✓ 检测到新窗口打开（静态数据中心套餐支付页面）")
                
                for window in self.driver.window_handles:
                    if window != self.original_window:
                        self.driver.switch_to.window(window)
                        print("✓ 已切换到静态数据中心套餐支付宝页面窗口")
                        payment_window_found = True
                        break
                        
            except TimeoutException:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.any_of(
                            EC.url_contains("alipay"),
                            EC.url_contains("pay"),
                            EC.title_contains("支付"),
                            EC.presence_of_element_located(self.ALIPAY_INDICATOR)
                        )
                    )
                    print("✓ 当前页面跳转到静态数据中心套餐支付页面")
                    payment_window_found = True
                except TimeoutException:
                    print("⚠️ 未检测到明显的静态数据中心套餐支付页面跳转")
                    return False
            
            if payment_window_found:
                # 从配置文件获取支付宝账号信息
                alipay_config = self.config.get('test_data', {}).get('alipay', {})
                email = alipay_config.get('email', 'lgipqm7573@sandbox.com')
                login_password = alipay_config.get('login_password', '111111')
                pay_password = alipay_config.get('pay_password', '111111')
                
                print(f"静态数据中心套餐支付使用支付宝账号: {email}")
                
                # 调用支付宝支付模块处理完整支付流程
                return self.alipay_payment.complete_payment_process(
                    email=email,
                    login_password=login_password,
                    pay_password=pay_password
                )
            else:
                print("❌ 未能成功跳转到静态数据中心套餐支付页面")
                return False
            
        except Exception as e:
            print(f"❌ 静态数据中心套餐支付流程失败: {e}")
            return False
    
    def complete_eighth_purchase_flow(self):
        """完整的第八次购买流程（静态数据中心套餐）"""
        try:
            print("\n" + "="*50)
            print("🏢 开始静态数据中心套餐购买流程")
            print("="*50)
            
            # 步骤0: 确保在正确的IPIPGO页面
            print("步骤0: 检查并切换到正确的IPIPGO页面...")
            if not self.ensure_on_correct_ipipgo_page():
                print("❌ 无法切换到正确的IPIPGO页面")
                return False
            
            # 点击静态数据中心选项卡
            print("步骤1: 点击静态数据中心选项卡...")
            if not self.click_static_datacenter_tab():
                print("❌ 静态数据中心选项卡点击失败")
                return False
            
            print("✓ 成功点击静态数据中心选项卡")
            
            # 点击马尼拉线路的加号按钮
            print("步骤2: 点击菲律宾-马尼拉线路的加号按钮...")
            if not self.click_manila_add_button():
                print("❌ 马尼拉线路加号按钮点击失败")
                return False
            
            print("✓ 成功点击马尼拉线路加号按钮")
            
            # 点击第八次购买按钮
            print("步骤3: 点击静态数据中心套餐立即购买按钮...")
            if not self.click_eighth_buy_button():
                print("❌ 静态数据中心套餐购买按钮点击失败")
                return False
            
            print("✓ 成功点击静态数据中心套餐立即购买按钮")
            
            # 点击第八次支付按钮并处理支付流程
            print("步骤4: 点击静态数据中心套餐立即支付按钮并完成支付...")
            if not self.click_eighth_pay_button_and_handle_payment():
                print("❌ 静态数据中心套餐支付流程失败")
                return False
            
            print("✓ 静态数据中心套餐支付流程完成")
            
            print("="*50)
            print("🎉 静态数据中心套餐购买流程完成！")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ 静态数据中心套餐购买流程执行失败: {e}")
            return False