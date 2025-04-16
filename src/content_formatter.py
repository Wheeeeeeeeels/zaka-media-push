import os
import jinja2
from typing import Dict, Any
from .utils import error_handler, ContentFormatError, Logger
from .utils.config import Config

logger = Logger()
config = Config()

class ContentFormatter:
    def __init__(self):
        self.template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        self.template_env = jinja2.Environment(loader=self.template_loader)
    
    @error_handler
    def format_wechat_article(self, paper: Dict[str, Any], summary: Dict[str, str]) -> str:
        """
        格式化微信公众号文章
        :param paper: 论文信息
        :param summary: 论文摘要
        :return: 格式化后的文章
        """
        try:
            template = self.template_env.get_template('wechat.md')
            content = template.render(
                title=paper['title'],
                authors=', '.join(paper['authors']),
                pdf_url=paper['pdf_url'],
                summary=paper['summary'],
                detailed_summary=summary['summary'],
                significance=summary['implications'],
                categories=', '.join(paper['categories']),
                publish_date=paper['published'].strftime('%Y-%m-%d')
            )
            logger.info("成功生成微信公众号文章")
            return content
        except Exception as e:
            raise ContentFormatError(f"微信公众号文章格式化失败: {str(e)}")
    
    @error_handler
    def format_xiaohongshu(self, paper: Dict[str, Any], summary: Dict[str, str]) -> str:
        """
        格式化小红书内容
        :param paper: 论文信息
        :param summary: 论文摘要
        :return: 格式化后的内容
        """
        try:
            template = self.template_env.get_template('xiaohongshu.md')
            content = template.render(
                title=paper['title'],
                authors=', '.join(paper['authors']),
                summary=summary['highlights'],
                significance=summary['implications'],
                results=summary['technical_details'],
                primary_category=paper['primary_category']
            )
            logger.info("成功生成小红书内容")
            return content
        except Exception as e:
            raise ContentFormatError(f"小红书内容格式化失败: {str(e)}")
    
    @error_handler
    def save_content(self, content: str, filename: str) -> str:
        """
        保存内容到文件
        :param content: 内容
        :param filename: 文件名
        :return: 文件路径
        """
        try:
            output_dir = config.get('output', 'dir')
            os.makedirs(output_dir, exist_ok=True)
            
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"成功保存内容到文件: {filepath}")
            return filepath
        except Exception as e:
            raise ContentFormatError(f"内容保存失败: {str(e)}")
    
    @error_handler
    def format_and_save(self, paper: Dict[str, Any], summary: Dict[str, str]) -> Dict[str, str]:
        """
        格式化并保存内容
        :param paper: 论文信息
        :param summary: 论文摘要
        :return: 保存的文件路径
        """
        try:
            # 生成内容
            wechat_content = self.format_wechat_article(paper, summary)
            xiaohongshu_content = self.format_xiaohongshu(paper, summary)
            
            # 生成文件名
            base_filename = f"{paper['title'][:20]}_{paper['published'].strftime('%Y%m%d')}"
            wechat_filename = f"wechat_{base_filename}.md"
            xiaohongshu_filename = f"xiaohongshu_{base_filename}.md"
            
            # 保存文件
            wechat_path = self.save_content(wechat_content, wechat_filename)
            xiaohongshu_path = self.save_content(xiaohongshu_content, xiaohongshu_filename)
            
            return {
                'wechat': wechat_path,
                'xiaohongshu': xiaohongshu_path
            }
        except Exception as e:
            raise ContentFormatError(f"内容格式化并保存失败: {str(e)}")
    
    @error_handler
    def format_for_platform(self, platform: str, paper: Dict[str, Any], summary: Dict[str, str]) -> str:
        """
        为指定平台格式化内容
        :param platform: 平台名称
        :param paper: 论文信息
        :param summary: 论文摘要
        :return: 格式化后的内容
        """
        try:
            if platform.lower() == 'wechat':
                return self.format_wechat_article(paper, summary)
            elif platform.lower() == 'xiaohongshu':
                return self.format_xiaohongshu(paper, summary)
            else:
                raise ContentFormatError(f"不支持的平台: {platform}")
        except Exception as e:
            raise ContentFormatError(f"平台内容格式化失败: {str(e)}") 