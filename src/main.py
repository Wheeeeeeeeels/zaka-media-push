from paper_crawler import PaperCrawler
from summary_generator import SummaryGenerator
from content_formatter import ContentFormatter
import schedule
import time
import os
from dotenv import load_dotenv

load_dotenv()

def daily_task():
    # 初始化各个模块
    crawler = PaperCrawler()
    generator = SummaryGenerator()
    formatter = ContentFormatter()
    
    # 获取最近7天的论文
    papers = crawler.get_recent_papers(days=7, max_results=5)
    
    for paper in papers:
        # 生成摘要
        summary = generator.generate_summary(paper['summary'])
        
        # 生成微信公众号文章
        wechat_article = formatter.format_wechat_article(paper, summary)
        
        # 生成小红书内容
        xiaohongshu_content = formatter.format_xiaohongshu(paper, summary)
        
        # 保存到文件
        with open(f"output/wechat_{paper['title'][:20]}.md", "w", encoding="utf-8") as f:
            f.write(wechat_article)
        
        with open(f"output/xiaohongshu_{paper['title'][:20]}.md", "w", encoding="utf-8") as f:
            f.write(xiaohongshu_content)

def main():
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 设置定时任务，每天上午10点执行
    schedule.every().day.at("10:00").do(daily_task)
    
    # 立即执行一次
    daily_task()
    
    # 保持程序运行
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 