# 支付重试机制修复说明

## 问题诊断

根据日志分析，发现支付重试机制存在关键问题：

### 原问题
1. ✅ **第一次尝试**：成功检测到支付宝页面输入框异常，正确关闭窗口并返回IPIPGO购买页面
2. ❌ **第二、三次重试**：直接查找"立即支付"按钮失败，因为页面状态已经改变，需要重新点击套餐的"立即购买"按钮

### 根本原因
支付宝异常关闭窗口后，页面回到了套餐选择状态，但重试逻辑直接查找"立即支付"按钮，跳过了必需的"立即购买"步骤。

## 修复方案

### 1. 优化重试逻辑
修改 `handle_payment_with_retry()` 方法：
- **第一次尝试**：跳过"立即购买"按钮（已在外部点击）
- **重试时**：自动重新点击"立即购买"按钮，然后点击"立即支付"

```python
# 关键修复代码
if buy_button_func and retry_count > 1:  # 只有重试时才需要重新点击立即购买按钮
    print(f"步骤1: 重试-点击{package_name}立即购买按钮...")
    if not buy_button_func():
        # 处理失败...
elif retry_count == 1:
    print(f"ℹ️ 第一次尝试，跳过{package_name}立即购买按钮（已在外部点击）")
```

### 2. 套餐特定修复

#### ✅ 个人套餐 (已修复)
```python
def click_pay_button_and_handle_payment(self):
    def click_second_buy_button():
        # 重试时重新点击第二个立即购买按钮
        second_buy_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.OLD_SECOND_BUY_BUTTON)
        )
        second_buy_btn.click()
    
    return self.handle_payment_with_retry(
        buy_button_func=click_second_buy_button,  # 重试时使用
        pay_button_func=click_pay_button,
        package_name="个人套餐"
    )
```

#### ✅ 企业套餐 (已修复)  
```python
def click_enterprise_pay_button_and_handle_payment(self):
    def click_enterprise_buy_button():
        # 重试时重新点击企业选项卡和购买按钮
        self.click_dynamic_enterprise_tab()
        enterprise_buy_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SECOND_BUY_BUTTON)
        )
        enterprise_buy_btn.click()
    
    return self.handle_payment_with_retry(
        buy_button_func=click_enterprise_buy_button,  # 重试时使用
        pay_button_func=click_enterprise_pay_button,
        package_name="企业套餐"
    )
```

## 预期修复效果

### 修复后的工作流程
1. **第一次尝试**
   - 跳过立即购买按钮（已点击）
   - 直接点击立即支付按钮
   - 检测到支付宝页面异常 → 关闭窗口

2. **第二次重试**
   - ✅ **重新点击立即购买按钮**
   - 点击立即支付按钮
   - 进入支付流程

3. **第三次重试**（如果第二次还失败）
   - ✅ **再次重新点击立即购买按钮**
   - 点击立即支付按钮
   - 进入支付流程

## 其他套餐修复模板

其余6个套餐可以按照相同模式修复：

```python
def click_xxx_pay_button_and_handle_payment(self):
    def click_xxx_buy_button():
        """重试时重新点击对应套餐的立即购买按钮"""
        try:
            # 1. 切换到对应选项卡（如果需要）
            # self.click_xxx_tab()
            
            # 2. 点击对应的购买按钮
            buy_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.XXX_BUY_BUTTON)
            )
            buy_btn.click()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"❌ 重试：点击XXX套餐立即购买按钮失败: {e}")
            return False
    
    def click_xxx_pay_button():
        # 原有的支付按钮点击逻辑
        pass
    
    return self.handle_payment_with_retry(
        buy_button_func=click_xxx_buy_button,  # 重试时使用
        pay_button_func=click_xxx_pay_button,
        package_name="XXX套餐"
    )
```

## 需要修复的其他套餐

1. **独享静态套餐**: `click_third_pay_button_and_handle_payment()`
2. **静态住宅套餐**: `click_fourth_pay_button_and_handle_payment()`
3. **动态住宅ISP套餐**: `click_fifth_pay_button_and_handle_payment()`
4. **动态不限量套餐**: `click_sixth_pay_button_and_handle_payment()`
5. **动态数据中心套餐**: `click_seventh_pay_button_and_handle_payment()`
6. **静态数据中心套餐**: `click_eighth_pay_button_and_handle_payment()`

## 测试建议

1. **优先测试已修复的套餐**：个人套餐和企业套餐
2. **观察日志输出**：确认重试时正确点击了立即购买按钮
3. **监控成功率**：重试机制应该显著提高支付成功率
4. **逐步修复其他套餐**：按照模板逐个更新

## 关键改进点

- ✅ **智能重试逻辑**：第一次不重复点击，重试时完整执行
- ✅ **页面状态恢复**：重试时回到正确的购买状态
- ✅ **详细日志**：清楚显示每步的执行状态
- ✅ **错误处理**：每步都有完整的异常处理
