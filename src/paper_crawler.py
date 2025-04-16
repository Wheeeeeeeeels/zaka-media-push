import arxiv
import requests
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from .utils import error_handler, PaperCrawlError, Logger
from .utils.config import Config

logger = Logger()
config = Config()

class PaperCrawler:
    def __init__(self):
        self.client = arxiv.Client()
        self.config = config
    
    @error_handler
    def search_papers(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索论文
        :param query: 搜索关键词
        :param max_results: 最大结果数
        :return: 论文列表
        """
        try:
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
                    'categories': result.categories,
                    'doi': result.doi,
                    'comment': result.comment,
                    'journal_ref': result.journal_ref
                }
                papers.append(paper)
            
            logger.info(f"成功爬取 {len(papers)} 篇论文")
            return papers
        except Exception as e:
            raise PaperCrawlError(f"论文搜索失败: {str(e)}")
    
    @error_handler
    def get_recent_papers(self, days: int = 7, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        获取最近几天的论文
        :param days: 天数
        :param max_results: 最大结果数
        :return: 论文列表
        """
        date = datetime.now() - timedelta(days=days)
        query = f"submittedDate:[{date.strftime('%Y%m%d')} TO *]"
        return self.search_papers(query, max_results)
    
    @error_handler
    def get_paper_by_category(self, category: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        按类别获取论文
        :param category: 论文类别
        :param max_results: 最大结果数
        :return: 论文列表
        """
        query = f"cat:{category}"
        return self.search_papers(query, max_results)
    
    @error_handler
    def get_paper_by_keyword(self, keyword: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        按关键词获取论文
        :param keyword: 关键词
        :param max_results: 最大结果数
        :return: 论文列表
        """
        return self.search_papers(keyword, max_results)
    
    @error_handler
    def download_paper(self, paper: Dict[str, Any]) -> Optional[str]:
        """
        下载论文PDF
        :param paper: 论文信息
        :return: 下载的文件路径
        """
        try:
            if not paper.get('pdf_url'):
                raise PaperCrawlError("论文PDF链接不存在")
            
            response = requests.get(paper['pdf_url'], stream=True)
            if response.status_code != 200:
                raise PaperCrawlError(f"下载失败，状态码: {response.status_code}")
            
            # 创建输出目录
            output_dir = os.path.join(config.get('output', 'dir'), 'papers')
            os.makedirs(output_dir, exist_ok=True)
            
            # 生成文件名
            filename = f"{paper['title'][:50]}_{paper['published'].strftime('%Y%m%d')}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            # 保存文件
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"成功下载论文: {filename}")
            return filepath
        except Exception as e:
            raise PaperCrawlError(f"论文下载失败: {str(e)}")
    
    @error_handler
    def get_paper_metadata(self, paper_id: str) -> Dict[str, Any]:
        """
        获取论文元数据
        :param paper_id: 论文ID
        :return: 论文元数据
        """
        try:
            paper = next(self.client.results(arxiv.Search(id_list=[paper_id])))
            return {
                'title': paper.title,
                'authors': [author.name for author in paper.authors],
                'summary': paper.summary,
                'pdf_url': paper.pdf_url,
                'published': paper.published,
                'updated': paper.updated,
                'primary_category': paper.primary_category,
                'categories': paper.categories,
                'doi': paper.doi,
                'comment': paper.comment,
                'journal_ref': paper.journal_ref
            }
        except Exception as e:
            raise PaperCrawlError(f"获取论文元数据失败: {str(e)}") 