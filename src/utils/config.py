import os
from dotenv import load_dotenv
from typing import Dict, Any

class Config:
    def __init__(self):
        load_dotenv()
        self.config: Dict[str, Any] = {
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
                'temperature': float(os.getenv('TEMPERATURE', '0.7')),
                'max_tokens': int(os.getenv('SUMMARY_LENGTH', '1000'))
            },
            'crawler': {
                'max_papers_per_day': int(os.getenv('MAX_PAPERS_PER_DAY', '5')),
                'days_to_crawl': int(os.getenv('DAYS_TO_CRAWL', '7'))
            },
            'schedule': {
                'time': os.getenv('SCHEDULE_TIME', '10:00')
            },
            'output': {
                'dir': os.getenv('OUTPUT_DIR', 'output'),
                'wechat_template': os.getenv('WECHAT_TEMPLATE', 'templates/wechat.md'),
                'xiaohongshu_template': os.getenv('XIAOHONGSHU_TEMPLATE', 'templates/xiaohongshu.md')
            }
        }
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        获取配置项
        :param section: 配置节
        :param key: 配置键
        :param default: 默认值
        :return: 配置值
        """
        return self.config.get(section, {}).get(key, default)
    
    def validate(self) -> bool:
        """
        验证配置是否有效
        :return: 是否有效
        """
        if not self.config['openai']['api_key']:
            raise ValueError("OpenAI API密钥未配置")
        return True 