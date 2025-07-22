"""
日志管理器
用于记录测试执行过程中的日志信息
"""

import logging
import colorlog
import os
from datetime import datetime


class Logger:
    """日志管理器类"""
    
    def __init__(self, name=__name__, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_console_handler()
            self._setup_file_handler()
    
    def _setup_console_handler(self):
        """设置控制台处理器"""
        console_handler = colorlog.StreamHandler()
        console_format = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self):
        """设置文件处理器"""
        # 创建日志目录
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建日志文件名（按日期）
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(log_dir, f"test_{today}.log")
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """调试日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """信息日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """警告日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """错误日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """严重错误日志"""
        self.logger.critical(message)


# 创建全局日志实例
logger = Logger().logger 