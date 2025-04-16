from typing import Callable, Any
from functools import wraps
from .logger import Logger

logger = Logger()

class ZakaError(Exception):
    """自定义异常基类"""
    pass

class PaperCrawlError(ZakaError):
    """论文爬取错误"""
    pass

class SummaryGenerationError(ZakaError):
    """摘要生成错误"""
    pass

class ContentFormatError(ZakaError):
    """内容格式化错误"""
    pass

def error_handler(func: Callable) -> Callable:
    """
    错误处理装饰器
    :param func: 被装饰的函数
    :return: 装饰后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except PaperCrawlError as e:
            logger.error(f"论文爬取错误: {str(e)}")
            raise
        except SummaryGenerationError as e:
            logger.error(f"摘要生成错误: {str(e)}")
            raise
        except ContentFormatError as e:
            logger.error(f"内容格式化错误: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            raise ZakaError(f"未知错误: {str(e)}")
    return wrapper 