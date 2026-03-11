"""
支付宝支付页面处理模块
处理完整的支付宝登录和支付流程
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.base_page import BasePage
import time
from selenium.webdriver.common.action_chains import ActionChains


class AlipayPayment(BasePage):
    """支付宝支付页面类"""
    
    # 支付宝登录页面元素定位器
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='loginId'][id='J_tLoginId']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[id='payPasswd_rsainput'][name='payPasswd_rsainput']")
    NEXT_BUTTON = (By.CSS_SELECTOR, "a[id='J_newBtn'][data-role='submitBtn']")
    NEXT_BUTTON_SPAN = (By.CSS_SELECTOR, "a[id='J_newBtn'][data-role='submitBtn'] span")
    NEXT_BUTTON_ALT = (By.ID, "J_newBtn")
    NEXT_BUTTON_CLASS = (By.CSS_SELECTOR, "a.newBtn-blue.newBtn-long")
    
    # 支付确认页面元素定位器
    PAY_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[id='payPassword_rsainput'][name='payPassword_rsainput']")
    CONFIRM_PAY_BUTTON = (By.CSS_SELECTOR, "input[id='J_authSubmit'][value='确认付款']")
    
    # 页面状态检测元素
    ALIPAY_LOGO = (By.CSS_SELECTOR, "[class*='alipay'], [alt*='支付宝'], [title*='支付宝']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.original_window = None
    
    def set_original_window(self, window_handle):
        """设置原始窗口句柄"""
        self.original_window = window_handle
    
    def wait_for_alipay_page(self):
        """等待支付宝页面加载"""
        try:
            # 等待支付宝特征元素出现
            WebDriverWait(self.driver, 15).until(
                EC.any_of(
                    EC.url_contains("alipay"),
                    EC.url_contains("pay"),
                    EC.title_contains("支付"),
                    EC.presence_of_element_located(self.EMAIL_INPUT),
                    EC.presence_of_element_located(self.ALIPAY_LOGO)
                )
            )
            print("✓ 支付宝页面已加载")
            return True
        except TimeoutException:
            print("❌ 等待支付宝页面超时")
            return False
    
    def check_alipay_input_availability(self):
        """检查支付宝页面是否可以正常填写账号和密码"""
        try:
            print("🔍 检查支付宝页面输入框是否可用...")
            
            # 检查邮箱输入框是否存在且可交互
            try:
                email_input = WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located(self.EMAIL_INPUT)
                )
                
                # 检查输入框是否可见且可编辑
                if not email_input.is_displayed():
                    print("❌ 邮箱输入框不可见")
                    return False
                
                if not email_input.is_enabled():
                    print("❌ 邮箱输入框不可编辑")
                    return False
                
                # 尝试清空并输入测试内容
                email_input.clear()
                email_input.send_keys("test@test.com")
                
                # 检查是否成功输入
                if email_input.get_attribute("value") != "test@test.com":
                    print("❌ 邮箱输入框无法正常输入内容")
                    return False
                
                # 清空测试内容
                email_input.clear()
                print("✓ 邮箱输入框检查通过")
                
            except TimeoutException:
                print("❌ 无法找到邮箱输入框")
                return False
            except Exception as e:
                print(f"❌ 邮箱输入框检查失败: {e}")
                return False
            
            # 检查密码输入框
            try:
                password_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.PASSWORD_INPUT)
                )
                
                if not password_input.is_displayed():
                    print("❌ 密码输入框不可见")
                    return False
                
                if not password_input.is_enabled():
                    print("❌ 密码输入框不可编辑")
                    return False
                
                print("✓ 密码输入框检查通过")
                
            except TimeoutException:
                print("❌ 无法找到密码输入框")
                return False
            except Exception as e:
                print(f"❌ 密码输入框检查失败: {e}")
                return False
            
            print("✅ 支付宝页面输入框检查完成，可以正常使用")
            return True
            
        except Exception as e:
            print(f"❌ 支付宝页面检查失败: {e}")
            return False
    
    def enter_email(self, email):
        """输入邮箱账号"""
        try:
            # 等待邮箱输入框可交互
            email_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.EMAIL_INPUT)
            )
            email_input.clear()
            email_input.send_keys(email)
            print(f"✓ 已输入邮箱: {email}")
            return True
        except Exception as e:
            print(f"❌ 输入邮箱失败: {e}")
            return False
    
    def enter_login_password(self, password):
        """输入登录密码"""
        try:
            # 等待密码输入框可交互
            password_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.PASSWORD_INPUT)
            )
            password_input.clear()
            password_input.send_keys(password)
            print("✓ 已输入登录密码")
            return True
        except Exception as e:
            print(f"❌ 输入登录密码失败: {e}")
            return False
    
    def click_next_button(self):
        """点击下一步按钮（超强版：多重保障机制）"""
        try:
            print("🔍 正在查找下一步按钮...")
            
            # 多种定位器尝试
            button_locators = [
                self.NEXT_BUTTON,        # a[id='J_newBtn'][data-role='submitBtn']
                self.NEXT_BUTTON_ALT,    # id='J_newBtn'
                self.NEXT_BUTTON_CLASS,  # a.newBtn-blue.newBtn-long
                (By.CSS_SELECTOR, "a[data-role='submitBtn']"),  # 更通用的定位器
                (By.CSS_SELECTOR, "a.newBtn-blue"),  # 简化的class定位器
                (By.XPATH, "//a[contains(@class,'newBtn-blue')]//span[text()='下一步']"),  # XPath定位器
            ]
            
            next_button = None
            used_locator = None
            
            for i, locator in enumerate(button_locators):
                try:
                    next_button = WebDriverWait(self.driver, 8).until(
                        EC.element_to_be_clickable(locator)
                    )
                    used_locator = locator
                    print(f"✓ 找到下一步按钮，定位器: {locator[1]}")
                    break
                except TimeoutException:
                    continue
            
            if next_button is None:
                print("❌ 无法找到下一步按钮")
                return False
            
            # 记录当前页面URL，用于检测跳转
            initial_url = self.driver.current_url
            print(f"📋 当前页面: {initial_url}")
            
            # 确保页面完全加载
            print("⏳ 等待页面完全加载...")
            time.sleep(2)
            
            # 确保元素可见并滚动到位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            time.sleep(1)
            
            # 检查按钮状态
            print(f"📋 按钮文本: {next_button.text}")
            print(f"📋 按钮可见: {next_button.is_displayed()}")
            print(f"📋 按钮启用: {next_button.is_enabled()}")
            
            # 超强重试机制（最多5次，增加成功率）
            max_attempts = 5
            for attempt in range(1, max_attempts + 1):
                print(f"🖱️ 第{attempt}次尝试点击...")
                
                # 重新获取按钮元素（确保元素新鲜）
                try:
                    next_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable(used_locator)
                    )
                except:
                    print(f"❌ 第{attempt}次重新定位按钮失败")
                    time.sleep(2)
                    continue
                
                # 6种点击方法（增加成功率）
                click_methods = [
                    ("普通点击", lambda: next_button.click()),
                    ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", next_button)),
                    ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(next_button).click().perform()),
                    ("键盘回车", lambda: next_button.send_keys(Keys.RETURN)),
                    ("JavaScript强制点击", lambda: self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", next_button)),
                    ("坐标点击", lambda: ActionChains(self.driver).move_to_element(next_button).pause(0.5).click().perform()),
                ]
                
                click_executed = False
                for method_name, click_func in click_methods:
                    try:
                        # 确保元素仍然可点击
                        if next_button.is_enabled() and next_button.is_displayed():
                            click_func()
                            print(f"✓ {method_name}执行成功")
                            click_executed = True
                            break
                        else:
                            print(f"⚠️ 按钮状态异常，跳过{method_name}")
                    except Exception as e:
                        print(f"❌ {method_name}失败: {e}")
                        continue
                
                if not click_executed:
                    print(f"❌ 第{attempt}次所有点击方法都失败")
                    time.sleep(2)
                    continue
                
                # 增强的页面跳转检测（最多等待12秒，更充分）
                print(f"⏳ 检测页面跳转（最多12秒）...")
                page_changed = False
                
                for wait_time in range(1, 13):  # 增加到12秒
                    time.sleep(1)
                    
                    # 检查多个跳转指标
                    try:
                        # 指标1：支付密码输入框出现（最可靠）
                        pay_input = self.driver.find_element(*self.PAY_PASSWORD_INPUT)
                        if pay_input.is_displayed():
                            print(f"✓ 支付密码输入框出现，页面已跳转（{wait_time}秒）")
                            page_changed = True
                            break
                    except:
                        pass
                    
                    # 指标2：URL变化
                    current_url = self.driver.current_url
                    if current_url != initial_url:
                        print(f"✓ URL已变化，页面已跳转（{wait_time}秒）")
                        print(f"📋 新URL: {current_url}")
                        page_changed = True
                        break
                    
                    # 指标3：页面标题变化
                    try:
                        current_title = self.driver.title
                        if "auth" in current_title.lower() or "确认" in current_title:
                            print(f"✓ 页面标题变化，已跳转（{wait_time}秒）")
                            page_changed = True
                            break
                    except:
                        pass
                    
                    # 指标4：确认付款按钮出现
                    try:
                        self.driver.find_element(*self.CONFIRM_PAY_BUTTON)
                        print(f"✓ 确认付款按钮出现，页面已跳转（{wait_time}秒）")
                        page_changed = True
                        break
                    except:
                        pass
                    
                    # 进度提示
                    if wait_time % 4 == 0:  # 每4秒提示一次
                        print(f"⏳ 继续等待跳转...({wait_time}/12秒)")
                
                if page_changed:
                    print(f"🎉 第{attempt}次点击成功！页面已跳转")
                    # 额外等待确保页面完全加载
                    time.sleep(2)
                    return True
                else:
                    print(f"❌ 第{attempt}次点击后页面未跳转")
                    if attempt < max_attempts:
                        print("🔄 准备重试，稍等...")
                        time.sleep(3)  # 增加重试间隔
            
            # 所有尝试都失败
            print(f"❌ 经过{max_attempts}次尝试，按钮仍未响应")
            print("💡 提示：页面可能需要手动点击下一步按钮")
            print("🤔 建议：检查是否有验证码或其他阻塞因素")
            return False
            
        except Exception as e:
            print(f"❌ 点击下一步按钮失败: {e}")
            return False
    
    def enter_pay_password(self, pay_password):
        """输入支付密码"""
        try:
            # 等待支付密码输入框出现并可交互
            pay_password_input = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.PAY_PASSWORD_INPUT)
            )
            pay_password_input.clear()
            pay_password_input.send_keys(pay_password)
            print("✓ 已输入支付密码")
            return True
        except Exception as e:
            print(f"❌ 输入支付密码失败: {e}")
            return False
    
    def click_confirm_payment(self):
        """点击确认付款按钮"""
        try:
            # 等待确认付款按钮可点击
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CONFIRM_PAY_BUTTON)
            )
            confirm_button.click()
            print("✓ 已点击确认付款按钮")
            return True
        except Exception as e:
            print(f"❌ 点击确认付款按钮失败: {e}")
            return False
    
    def close_alipay_window_immediately(self):
        """立即关闭支付宝窗口并返回原页面（用于异常情况）"""
        try:
            print("⚠️ 检测到支付宝页面异常，立即关闭并返回...")
            
            # 检查当前窗口数量和信息
            all_windows = self.driver.window_handles
            current_window = self.driver.current_window_handle
            window_count = len(all_windows)
            
            print(f"📋 当前窗口总数: {window_count}")
            
            # 分析所有窗口的信息
            window_info = {}
            for i, window_handle in enumerate(all_windows):
                try:
                    self.driver.switch_to.window(window_handle)
                    url = self.driver.current_url
                    title = self.driver.title
                    window_info[window_handle] = {
                        'url': url,
                        'title': title,
                        'index': i
                    }
                    print(f"📋 窗口{i+1}: {title} - {url[:50]}...")
                except Exception as e:
                    print(f"⚠️ 无法获取窗口{i+1}信息: {e}")
            
            # 找到支付宝窗口和IPIPGO窗口
            alipay_windows = []
            ipipgo_windows = []
            
            for handle, info in window_info.items():
                url = info['url'].lower()
                title = info['title'].lower()
                
                if 'alipay' in url or 'pay' in url or '支付宝' in title:
                    alipay_windows.append(handle)
                    print(f"🏦 识别到支付宝窗口: {info['title']}")
                elif 'ipipgo' in url or 'ipipgo' in title:
                    ipipgo_windows.append(handle)
                    print(f"🌐 识别到IPIPGO窗口: {info['title']}")
            
            # 关闭支付宝窗口
            if alipay_windows:
                for alipay_window in alipay_windows:
                    try:
                        print(f"🔄 正在关闭支付宝窗口...")
                        self.driver.switch_to.window(alipay_window)
                        self.driver.close()
                        print("✅ 支付宝窗口已关闭")
                    except Exception as e:
                        print(f"⚠️ 关闭支付宝窗口失败: {e}")
            
            # 选择合适的IPIPGO窗口切换
            time.sleep(1)
            remaining_windows = self.driver.window_handles
            print(f"📋 剩余窗口数: {len(remaining_windows)}")
            
            target_window = None
            
            # 优先选择原始窗口
            if self.original_window and self.original_window in remaining_windows:
                target_window = self.original_window
                print("✅ 选择原始IPIPGO窗口")
            # 其次选择IPIPGO窗口
            elif ipipgo_windows:
                for ipipgo_window in ipipgo_windows:
                    if ipipgo_window in remaining_windows:
                        target_window = ipipgo_window
                        print("✅ 选择IPIPGO窗口")
                        break
            # 最后选择第一个剩余窗口
            elif remaining_windows:
                target_window = remaining_windows[0]
                print("✅ 选择第一个剩余窗口")
            
            if target_window:
                self.driver.switch_to.window(target_window)
                current_url = self.driver.current_url
                current_title = self.driver.title
                print(f"✅ 已切换回窗口: {current_title}")
                print(f"📋 当前页面: {current_url[:50]}...")
                return True
            else:
                print("❌ 无法找到合适的窗口切换")
                return False
            
        except Exception as e:
            print(f"❌ 关闭支付宝窗口失败: {e}")
            return False

    def close_alipay_window(self):
        """关闭支付宝窗口并返回原页面（智能版：处理多窗口情况）"""
        try:
            print("等待10秒后处理支付宝页面...")
            time.sleep(10)
            
            # 检查当前窗口数量和信息
            all_windows = self.driver.window_handles
            current_window = self.driver.current_window_handle
            window_count = len(all_windows)
            
            print(f"📋 当前窗口总数: {window_count}")
            print(f"📋 当前窗口句柄: {current_window}")
            
            # 分析所有窗口的信息
            window_info = {}
            for i, window_handle in enumerate(all_windows):
                try:
                    self.driver.switch_to.window(window_handle)
                    url = self.driver.current_url
                    title = self.driver.title
                    window_info[window_handle] = {
                        'url': url,
                        'title': title,
                        'index': i
                    }
                    print(f"📋 窗口{i+1}: {title} - {url}")
                except Exception as e:
                    print(f"⚠️ 无法获取窗口{i+1}信息: {e}")
            
            # 找到支付宝窗口和IPIPGO窗口
            alipay_windows = []
            ipipgo_windows = []
            
            for handle, info in window_info.items():
                url = info['url'].lower()
                title = info['title'].lower()
                
                if 'alipay' in url or 'pay' in url or '支付宝' in title:
                    alipay_windows.append(handle)
                    print(f"🏦 识别到支付宝窗口: {info['title']}")
                elif 'ipipgo' in url or 'ipipgo' in title:
                    ipipgo_windows.append(handle)
                    print(f"🌐 识别到IPIPGO窗口: {info['title']}")
            
            # 关闭支付宝窗口
            if alipay_windows:
                for alipay_window in alipay_windows:
                    try:
                        print(f"🔄 正在关闭支付宝窗口...")
                        self.driver.switch_to.window(alipay_window)
                        self.driver.close()
                        print("✅ 支付宝窗口已关闭")
                    except Exception as e:
                        print(f"⚠️ 关闭支付宝窗口失败: {e}")
            else:
                print("⚠️ 未找到支付宝窗口")
            
            # 选择合适的IPIPGO窗口切换
            time.sleep(2)
            remaining_windows = self.driver.window_handles
            print(f"📋 剩余窗口数: {len(remaining_windows)}")
            
            target_window = None
            
            # 优先选择原始窗口
            if self.original_window and self.original_window in remaining_windows:
                target_window = self.original_window
                print("✅ 选择原始IPIPGO窗口")
            # 其次选择IPIPGO窗口
            elif ipipgo_windows:
                for ipipgo_window in ipipgo_windows:
                    if ipipgo_window in remaining_windows:
                        target_window = ipipgo_window
                        print("✅ 选择IPIPGO窗口")
                        break
            # 最后选择第一个剩余窗口
            elif remaining_windows:
                target_window = remaining_windows[0]
                print("✅ 选择第一个剩余窗口")
            
            if target_window:
                self.driver.switch_to.window(target_window)
                current_url = self.driver.current_url
                current_title = self.driver.title
                print(f"✅ 已切换到窗口: {current_title}")
                print(f"📋 当前页面: {current_url}")
            else:
                print("❌ 无法找到合适的窗口切换")
            
            print("✅ 支付宝页面处理完成")
            return True
            
        except Exception as e:
            print(f"❌ 关闭支付宝窗口失败: {e}")
            print("💡 继续执行后续流程")
            return False
    
    def complete_payment_process(self, email="lgipqm7573@sandbox.com", login_password="111111", pay_password="111111", max_retries=2):
        """完整的支付宝支付流程（带重试机制）"""
        
        for attempt in range(1, max_retries + 1):
            try:
                print("="*50)
                print(f"🏦 开始支付宝支付流程 (第{attempt}次尝试)")
                print("="*50)
                
                # 步骤1: 等待支付宝页面加载
                print("步骤1: 等待支付宝页面加载...")
                if not self.wait_for_alipay_page():
                    if attempt < max_retries:
                        print("⚠️ 支付宝页面加载失败，重新尝试...")
                        continue
                    else:
                        return "failed"
                
                # 步骤2: 检查支付宝页面输入框是否可用
                print("步骤2: 检查支付宝页面输入框是否可用...")
                if not self.check_alipay_input_availability():
                    print("⚠️ 支付宝页面输入框不可用，关闭窗口重试...")
                    self.close_alipay_window_immediately()
                    if attempt < max_retries:
                        print("🔄 返回购买页面重试...")
                        return "retry"
                    else:
                        print("❌ 达到最大重试次数，支付失败")
                        return "failed"
                
                # 步骤3: 输入邮箱账号
                print("步骤3: 输入支付宝账号...")
                if not self.enter_email(email):
                    if attempt < max_retries:
                        print("⚠️ 输入邮箱失败，重新尝试...")
                        continue
                    else:
                        return "failed"
                
                # 步骤4: 输入登录密码
                print("步骤4: 输入登录密码...")
                if not self.enter_login_password(login_password):
                    if attempt < max_retries:
                        print("⚠️ 输入登录密码失败，重新尝试...")
                        continue
                    else:
                        return "failed"
                
                # 步骤5: 点击下一步
                print("步骤5: 点击下一步按钮...")
                if not self.click_next_button():
                    if attempt < max_retries:
                        print("⚠️ 点击下一步失败，重新尝试...")
                        continue
                    else:
                        return "failed"
                
                # 步骤6: 输入支付密码
                print("步骤6: 输入支付密码...")
                if not self.enter_pay_password(pay_password):
                    if attempt < max_retries:
                        print("⚠️ 输入支付密码失败，重新尝试...")
                        continue
                    else:
                        return "failed"
                
                # 步骤7: 点击确认付款
                print("步骤7: 点击确认付款按钮...")
                if not self.click_confirm_payment():
                    if attempt < max_retries:
                        print("⚠️ 点击确认付款失败，重新尝试...")
                        continue
                    else:
                        return "failed"
                
                # 步骤8: 等待并关闭支付宝页面
                print("步骤8: 等待并关闭支付宝页面...")
                if not self.close_alipay_window():
                    print("⚠️ 关闭支付宝页面失败，但支付流程可能已完成")
                
                print("="*50)
                print("🎉 支付宝支付流程完成！")
                print("="*50)
                return "success"
                
            except Exception as e:
                print(f"❌ 支付宝支付流程失败 (第{attempt}次尝试): {e}")
                if attempt < max_retries:
                    print("🔄 准备下一次尝试...")
                    time.sleep(2)
                    continue
                else:
                    print("❌ 所有重试尝试均失败")
                    return "failed"
        
        return "failed"
    
    def get_current_page_info(self):
        """获取当前页面信息（调试用）"""
        try:
            current_url = self.driver.current_url
            current_title = self.driver.title
            print(f"当前URL: {current_url}")
            print(f"当前标题: {current_title}")
            return current_url, current_title
        except Exception as e:
            print(f"获取页面信息失败: {e}")
            return None, None 