import arxiv
import pandas as pd
from datetime import datetime, timedelta

class PaperCrawler:
    def __init__(self):
        self.client = arxiv.Client()
    
    def search_papers(self, query, max_results=10):
        """
        搜索论文
        :param query: 搜索关键词
        :param max_results: 最大结果数
        :return: 论文列表
        """
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        for result in self.client.results(search):
            paper = {
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'summary': result.summary,
                'pdf_url': result.pdf_url,
                'published': result.published,
                'updated': result.updated,
                'primary_category': result.primary_category,
                'categories': result.categories
            }
            papers.append(paper)
        
        return papers
    
    def get_recent_papers(self, days=7, max_results=20):
        """
        获取最近几天的论文
        :param days: 天数
        :param max_results: 最大结果数
        :return: 论文列表
        """
        date = datetime.now() - timedelta(days=days)
        query = f"submittedDate:[{date.strftime('%Y%m%d')} TO *]"
        return self.search_papers(query, max_results) 