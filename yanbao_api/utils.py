import os
import logging
import logging.handlers
from datetime import datetime


def get_logger(name, path, level=logging.DEBUG):
    """
    :param name: 日志名称
    :param path: 日志路径
    """
    # 创建一个日志器。提供了应用程序接口
    logger = logging.getLogger(name)
    # 设置日志输出的最低等级,低于当前等级则会被忽略
    logger.setLevel(level)
    # 创建日志输出路径
    if not os.path.exists(path):
        os.mkdir(path)
    # 创建格式器
    formatter = logging.Formatter(
        fmt="%(levelname)s - %(asctime)s - %(filename)s[:%(lineno)d] - %(message)s",
        datefmt="%m-%d %H:%M:%S",
    )
    # 创建处理器：ch为控制台处理器，fh为文件处理器
    ch = logging.StreamHandler()
    ch.setLevel(level)

    filename = os.path.join(path, f'{name}.log')
    # 输出到文件
    fh = logging.handlers.TimedRotatingFileHandler(
        filename=filename,
        when="D",  # 间隔时间:S:秒 M:分 H:小时 D:天 W:每星期（interval==0时代表星期一） midnight: 每天凌晨
        backupCount=6,
        encoding='utf-8'
    )
    fh.setLevel(level)

    # 设置日志输出格式
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    if not logger.handlers:
        # 将处理器，添加至日志器中
        logger.addHandler(fh)
        logger.addHandler(ch)
    # print(logger.handlers)
    return logger


def get_strftime(fmt="%Y-%m-%d %H:%M:%S"):
    """
    fmt: "%Y-%m-%d %H:%M:%S", "%Y%m%d%H%M%S", "%Y-%m-%d %H:%M:%S.%f", "%Y%m%d%H%M%S%f"
    """
    return datetime.now().strftime(fmt)