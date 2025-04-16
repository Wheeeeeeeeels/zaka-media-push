from paper_crawler import PaperCrawler
from summary_generator import SummaryGenerator
from content_formatter import ContentFormatter
import schedule
import time
import os
from typing import Dict, Any
from .utils import Logger, error_handler
from .utils.config import Config

logger = Logger()
config = Config()

class ZakaMediaPush:
    def __init__(self):
        self.crawler = PaperCrawler()
        self.generator = SummaryGenerator()
        self.formatter = ContentFormatter()
        self.config = config
    
    @error_handler
    def process_paper(self, paper: Dict[str, Any]) -> Dict[str, str]:
        """
        处理单篇论文
        :param paper: 论文信息
        :return: 生成的文件路径
        """
        try:
            # 生成摘要
            summary = self.generator.generate_comprehensive_summary(paper)
            
            # 格式化并保存内容
            file_paths = self.formatter.format_and_save(paper, summary)
            
            # 下载论文PDF
            pdf_path = self.crawler.download_paper(paper)
            
            logger.info(f"成功处理论文: {paper['title']}")
            return {
                **file_paths,
                'pdf': pdf_path
            }
        except Exception as e:
            logger.error(f"处理论文失败: {paper['title']}, 错误: {str(e)}")
            raise
    
    @error_handler
    def daily_task(self):
        """
        每日任务
        """
        try:
            logger.info("开始执行每日任务")
            
            # 获取最近论文
            days = self.config.get('crawler', 'days_to_crawl')
            max_papers = self.config.get('crawler', 'max_papers_per_day')
            papers = self.crawler.get_recent_papers(days=days, max_results=max_papers)
            
            # 处理每篇论文
            for paper in papers:
                try:
                    self.process_paper(paper)
                except Exception as e:
                    logger.error(f"处理论文失败: {paper['title']}, 错误: {str(e)}")
                    continue
            
            logger.info("每日任务执行完成")
        except Exception as e:
            logger.error(f"每日任务执行失败: {str(e)}")
            raise
    
    @error_handler
    def run(self):
        """
        运行程序
        """
        try:
            # 验证配置
            self.config.validate()
            
            # 创建必要的目录
            os.makedirs(self.config.get('output', 'dir'), exist_ok=True)
            os.makedirs('logs', exist_ok=True)
            
            # 设置定时任务
            schedule_time = self.config.get('schedule', 'time')
            schedule.every().day.at(schedule_time).do(self.daily_task)
            
            logger.info(f"程序已启动，将在每天 {schedule_time} 执行任务")
            
            # 立即执行一次
            self.daily_task()
            
            # 保持程序运行
            while True:
                schedule.run_pending()
                time.sleep(60)
        except Exception as e:
            logger.error(f"程序运行失败: {str(e)}")
            raise

def main():
    try:
        app = ZakaMediaPush()
        app.run()
    except Exception as e:
        logger.error(f"程序异常退出: {str(e)}")
        raise

if __name__ == "__main__":
    main() 