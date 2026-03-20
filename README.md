# IPIPGO Selenium 自动化测试项目

## 🌟 项目概述

IPIPGO Selenium 自动化测试项目是一个专为 IPIPGO 代理服务网站设计的端到端自动化测试解决方案。该项目采用 Python + Selenium 技术栈，实现了用户端和管理后台的完整自动化测试流程。

## 📁 脚本文件与功能模块对应表

### 用户端脚本

| 脚本文件 | 覆盖功能模块 |
|---|---|
| `main.py` | 用户端主程序 — 完整流程调度（登录 + 9种套餐购买 + 支付宝支付） |
| `pages/login_page.py` | 用户端登录 — 打开网站 / 输入账号密码 / 验证登录结果 |
| `pages/purchase_page.py` | 用户端购买 — 9种套餐选择与下单（点击立即购买 / 选型 / 确认订单） |
| `pages/alipay_payment.py` | 支付宝支付 — 跳转支付宝沙盒 / 账号登录 / 确认付款 / 返回结果 |

### 管理后台脚本

| 脚本文件 | 覆盖功能模块 |
|---|---|
| `admin/admin_main.py` | 管理后台主程序 — 完整流程调度（登录 + 切换职位 + 客户查询 + 8种套餐开通） |
| `admin/pages/admin_login_page.py` | 管理后台登录 — 打开登录页 / 输入用户名密码 / 切换职位（角色切换） |
| `admin/pages/customer_page.py` | 客户管理 — 导航至客户页 / 按用户ID查询 / 8种套餐开通 + 支付确认 |

### 公共工具脚本

| 脚本文件 | 覆盖功能模块 |
|---|---|
| `utils/base_page.py` | 页面基类 — 元素定位 / 显式等待 / 截图封装 / 通用操作 |
| `utils/driver_manager.py` | 浏览器驱动管理 — 启动 / 配置 / 关闭 Edge 浏览器 |
| `utils/logger.py` | 日志工具 — 彩色输出 / 文件记录 / 分级日志 |

---

## 🔄 完整业务流程执行顺序

### 用户端流程（`main.py`）

```
登录（login_page.py）
    ↓
1. 个人套餐购买 → 立即购买 → 支付宝支付
    ↓
2. 企业套餐购买 → 立即购买 → 支付宝支付
    ↓
3. 独享静态套餐购买 → 选择线路（香港） → 立即购买 → 支付宝支付
    ↓
4. 静态住宅套餐购买 → 选择线路（纽约） → 立即购买 → 支付宝支付
    ↓
5. 动态住宅（长效ISP）套餐购买 → 立即购买 → 支付宝支付
    ↓
6. 动态不限量套餐购买 → 立即购买 → 支付宝支付
    ↓
7. 动态数据中心（基础）套餐购买 → 立即购买 → 支付宝支付
    ↓
8. 静态数据中心套餐购买 → 选择线路（马尼拉） → 立即购买 → 支付宝支付
```

### 管理后台流程（`admin/admin_main.py`）

```
管理后台登录 + 切换职位（admin_login_page.py）
    ↓
客户查询（按用户ID搜索，customer_page.py）
    ↓
1. 开标准套餐 → 填写备注 → 确认支付
    ↓
2. 开企业套餐 → 填写备注 → 确认支付
    ↓
3. 开基础套餐 → 填写备注 → 确认支付
    ↓
4. 开不限量套餐 → 填写备注 → 确认支付
    ↓
5. 开静态代理Hosting套餐 → 填写备注 → 确认支付
    ↓
6. 开静态代理ISP套餐 → 填写备注 → 确认支付
    ↓
7. 开静态代理双ISP套餐 → 填写备注 → 确认支付
    ↓
8. 开独享静态套餐 → 填写备注 → 确认支付
```

---

## 🎯 主要功能

### 用户端自动化测试
- ✅ **完整登录流程**：用户登录验证
- 💰 **多套餐购买测试**：支持8种不同代理套餐的自动化购买
- 💳 **支付流程验证**：集成支付宝沙盒环境，实现完整支付流程测试
- 📊 **购买结果验证**：自动验证套餐购买成功状态

### 管理后台自动化测试
- 🔐 **管理员登录**：支持用户名密码登录
- 👥 **职位切换**：自动切换到指定管理职位
- 🔍 **客户查询**：按用户ID检索客户信息
- 📦 **套餐管理测试**：涵盖8种套餐类型的开通与支付测试

### 支持的套餐类型

**用户端购买（purchase_page.py）：**
1. **个人套餐** - 基础动态住宅代理
2. **企业套餐** - 企业级动态住宅代理
3. **独享静态套餐** - 专属静态代理（香港线路）
4. **静态住宅套餐** - 静态住宅代理（纽约线路）
5. **动态住宅（长效ISP）套餐** - 长效ISP代理
6. **动态不限量套餐** - 无流量限制代理
7. **动态数据中心（基础）套餐** - 数据中心动态代理
8. **静态数据中心套餐** - 数据中心静态代理（马尼拉线路）

**管理后台开通（customer_page.py）：**
1. **标准套餐** - 动态住宅标准套餐
2. **企业套餐** - 动态住宅企业套餐
3. **基础套餐** - 动态住宅基础套餐
4. **不限量套餐** - 动态住宅不限量套餐
5. **静态代理Hosting** - 静态主机代理
6. **静态代理ISP** - ISP级静态代理
7. **静态代理双ISP** - 双ISP静态代理
8. **独享静态套餐** - 专属静态代理

## 🏗️ 项目架构

```
IPIPGO/
├── admin/                          # 管理后台测试模块
│   ├── pages/                      # 管理后台页面对象
│   │   ├── admin_login_page.py     # 管理后台登录 + 职位切换
│   │   └── customer_page.py        # 客户查询 + 8种套餐开通
│   ├── screenshots/                # 管理后台截图目录
│   └── admin_main.py               # 管理后台主程序（入口）
├── config/                         # 配置文件
│   └── config.yaml                 # 主配置文件（URL / 账号 / 浏览器）
├── pages/                          # 用户端页面对象
│   ├── login_page.py               # 用户端登录页面
│   ├── purchase_page.py            # 购买页面（8种套餐下单）
│   └── alipay_payment.py           # 支付宝沙盒支付页面
├── tests/                          # pytest 测试用例
│   ├── test_complete_flow.py       # 完整流程测试
│   ├── test_ipipgo_login.py        # 登录单项测试
│   └── test_example.py             # 示例测试
├── utils/                          # 公共工具类
│   ├── base_page.py                # 页面基类（等待 / 截图 / 定位）
│   ├── driver_manager.py           # 浏览器驱动管理
│   └── logger.py                   # 彩色日志工具
├── logs/                           # 日志文件目录
├── screenshots/                    # 用户端截图目录
├── drivers/                        # WebDriver 文件目录
├── main.py                         # 用户端主程序（入口）
└── requirements.txt                # 项目依赖
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Windows 10/11 (已针对Windows环境优化)
- Microsoft Edge 浏览器 (推荐) / Chrome / Firefox

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd IPIPGO
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置测试环境**
编辑 `config/config.yaml` 文件，设置：
- 测试网站URL
- 测试账号信息
- 浏览器配置
- 支付宝沙盒账号

### 运行测试

#### 用户端完整流程测试
```bash
# 运行完整的9个套餐购买流程
python main.py

# 运行静态数据中心套餐单独测试
python main.py --static-datacenter
```

#### 管理后台测试
```bash
python admin/admin_main.py
```

#### 使用pytest运行测试
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_complete_flow.py -v

# 生成HTML报告
pytest tests/ --html=reports/report.html
```

## ⚙️ 配置说明

### 主配置文件 (`config/config.yaml`)

```yaml
# 浏览器配置
browser:
  default: edge              # 默认浏览器
  headless: false           # 是否无头模式
  window_size: "1920,1080"  # 窗口大小
  close_after_test: false   # 测试后是否关闭浏览器

# 测试环境
environment:
  base_url: "https://test.ipipgo.com/zh-CN/"

# 测试数据
test_data:
  login:
    username: "your_username"
    password: "your_password"
  admin_login:
    username: "admin_username"
    password: "admin_password"
  alipay:
    email: "sandbox_email"
    login_password: "sandbox_password"
    pay_password: "pay_password"
```

## 📋 测试用例说明

### 用户端测试流程
1. **登录验证** - 验证用户登录功能
2. **套餐浏览** - 测试套餐展示页面
3. **购买流程** - 测试添加到购物车、确认订单
4. **支付流程** - 验证支付宝支付集成
5. **结果验证** - 确认购买成功状态

### 管理后台测试流程
1. **SSO登录** - 验证单点登录功能
2. **职位切换** - 测试管理员权限切换
3. **客户管理** - 验证客户信息查询和管理
4. **套餐管理** - 测试套餐配置和管理功能

## 📊 测试报告

- **自动截图**：关键步骤自动截图，保存至 `screenshots/` 目录
- **详细日志**：完整的测试执行日志，保存至 `logs/` 目录
- **HTML报告**：使用pytest-html生成详细的测试报告

## 🛠️ 技术栈

- **核心框架**：Selenium WebDriver 4.15.2
- **测试框架**：pytest 7.4.3
- **编程语言**：Python 3.8+
- **驱动管理**：webdriver-manager 4.0.1
- **日志系统**：colorlog 6.7.0
- **配置管理**：PyYAML 6.0.1
- **报告生成**：pytest-html 4.1.1

## 🔧 开发指南

### 页面对象模式 (POM)
项目采用页面对象模式，每个页面对应一个类：
- 所有页面类继承自 `BasePage`
- 元素定位统一管理
- 页面操作方法封装

### 添加新测试用例
1. 在 `tests/` 目录创建新的测试文件
2. 继承测试基类，使用已有的页面对象
3. 遵循现有的命名规范和代码结构

### 扩展页面对象
1. 在相应的 `pages/` 目录添加新页面类
2. 继承 `BasePage` 类
3. 定义页面元素定位器和操作方法

## 🐛 故障排除

### 常见问题

1. **WebDriver版本不匹配**
   - 解决方案：webdriver-manager会自动下载匹配的驱动版本

2. **元素定位失败**
   - 检查页面加载是否完成
   - 验证元素定位器是否正确
   - 增加等待时间

3. **支付流程失败**
   - 确认支付宝沙盒账号配置正确
   - 检查网络连接状态
   - 验证支付页面加载情况

4. **截图保存失败**
   - 检查 `screenshots/` 目录权限
   - 确认磁盘空间充足

## 📝 更新日志

### v1.0.0
- ✅ 实现用户端完整购买流程自动化
- ✅ 支持9种代理套餐类型测试
- ✅ 集成支付宝沙盒支付测试
- ✅ 实现管理后台自动化测试
- ✅ 添加完整的日志和截图功能
- ✅ 支持多浏览器测试 (Chrome/Firefox/Edge)

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目遵循 MIT 许可证。详情请查看 [LICENSE](LICENSE) 文件。

## 📧 联系信息

- 项目维护者：[您的姓名]
- 邮箱：[您的邮箱]
- 项目地址：[项目仓库地址]

---

**注意**：本项目仅用于测试目的，请勿在生产环境中使用真实的支付信息。 