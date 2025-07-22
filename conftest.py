"""
pytest配置文件
包含测试fixtures和全局配置
"""

import pytest
import os
import time
from utils.driver_manager import DriverManager
from utils.logger import logger


@pytest.fixture(scope="session")
def driver_manager():
    """WebDriver管理器fixture"""
    manager = DriverManager()
    yield manager
    manager.quit_driver()


@pytest.fixture
def driver(driver_manager):
    """WebDriver fixture"""
    driver = driver_manager.get_driver()
    yield driver
    # 由session级别的fixture处理quit


@pytest.fixture(autouse=True)
def test_setup_teardown(request):
    """测试前后处理"""
    test_name = request.node.name
    logger.info(f"开始执行测试: {test_name}")
    
    start_time = time.time()
    
    yield
    
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"测试 {test_name} 执行完成，耗时: {duration:.2f}秒")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试报告钩子"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if report.failed:
            logger.error(f"测试失败: {item.name}")
            # 可以在这里添加截图逻辑
        elif report.passed:
            logger.info(f"测试通过: {item.name}")


def pytest_configure(config):
    """pytest配置"""
    # 创建必要的目录
    directories = ["screenshots", "logs", "reports"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="指定浏览器类型: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="无头模式运行"
    )


@pytest.fixture
def browser_type(request):
    """浏览器类型fixture"""
    return request.config.getoption("--browser")


@pytest.fixture
def headless_mode(request):
    """无头模式fixture"""
    return request.config.getoption("--headless") 