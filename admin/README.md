# IPIPGO管理后台UI自动化

## 📋 概述

这是IPIPGO管理后台的UI自动化测试框架，专门用于处理管理后台的登录及后续操作流程。

## 🏗️ 目录结构

```
admin/
├── __init__.py                 # 模块初始化文件
├── admin_main.py              # 管理后台主程序
├── pages/                     # 页面类文件夹
│   ├── __init__.py           # 页面模块初始化
│   └── admin_login_page.py   # 管理后台登录页面类
└── README.md                 # 本说明文档
```

## 🚀 使用方法

### 1. 单独运行管理后台登录测试

```bash
# 在项目根目录下运行
python admin/admin_main.py
```

### 2. 配置信息

确保 `config/config.yaml` 文件中包含管理后台配置：

```yaml
# 管理后台环境配置
admin_environment:
  login_url: "https://sso.xiaoxitech.com/login?project=lwlu63w1&cb=https%3A%2F%2Ftest-admin-ipipgo.cd.xiaoxigroup.net"
  dashboard_url: "https://test-admin-ipipgo.cd.xiaoxigroup.net"

# 管理后台登录数据
test_data:
  admin_login:
    username: "qinrenchi"
    password: "Sandog031220@"
    target_position: "秦仁驰"  # 切换到的目标职位
```

## 🔧 登录流程

管理后台登录包含以下步骤：

1. **打开登录页面** - 访问SSO登录地址
2. **点击用户名密码登录** - 点击登录方式切换按钮
3. **输入用户名** - 在用户名输入框输入账号
4. **输入密码** - 在密码输入框输入密码
5. **点击登录按钮** - 提交登录表单
6. **验证登录状态** - 检查是否成功跳转到管理后台

## 🔄 切换职位流程

登录成功后，自动执行切换职位操作：

1. **点击用户下拉箭头** - 点击右上角的下拉箭头
2. **选择切换账号** - 点击"切换账号"菜单项
3. **打开职位下拉** - 点击弹窗中的职位下拉箭头
4. **选择目标职位** - 选择指定的职位选项
5. **确认切换** - 点击"确定"按钮完成切换

## 📸 截图功能

- **成功截图**: `admin_login_completed.png` - 登录成功后的截图
- **切换截图**: `admin_position_switched.png` - 职位切换成功后的截图
- **错误截图**: `admin_error_login.png` - 登录失败时的错误截图

## 🛠️ 技术特性

### 强化的元素定位
- 多种CSS选择器策略
- XPath备用定位方案  
- 智能文本匹配

### 错误处理
- 详细的日志记录
- 多种点击方式尝试
- 失败时自动截图

### 配置灵活性
- 支持浏览器选择（Chrome、Firefox、Edge）
- 可配置是否关闭浏览器
- 自定义超时时间

## 📝 日志输出

程序运行时会输出详细的日志信息：

```
🚀 开始IPIPGO管理后台UI自动化测试
🔹 包含：管理后台登录
✓ 成功启动Edge浏览器
🌐 管理后台登录地址: https://sso.xiaoxitech.com/...
👤 管理员用户: qinrenchi
🔄 目标职位: 秦仁驰
🔐 第一阶段：管理后台登录流程
✓ 管理后台登录页面打开成功
✓ 管理后台登录成功
🔄 第二阶段：切换职位流程
✓ 职位切换成功，已切换到: 秦仁驰
🎉 IPIPGO管理后台登录自动化测试成功完成！
```

## 🔗 与主系统集成

后续可以将此模块与主系统(`main.py`)集成，实现：
- 官网购买流程 + 管理后台操作的完整自动化
- 数据验证和交叉检查
- 端到端的业务流程测试

## ⚠️ 注意事项

1. 确保网络连接正常，能够访问管理后台地址
2. 确保测试账号有效且具有相应权限
3. 首次运行时建议设置 `close_after_test: false` 以便观察结果
4. 如遇到元素定位失败，可能需要更新HTML元素选择器 