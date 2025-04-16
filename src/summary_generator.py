from openai import OpenAI
import os
from typing import Dict, Any, Optional
from .utils import error_handler, SummaryGenerationError, Logger
from .utils.config import Config
from dotenv import load_dotenv

logger = Logger()
config = Config()

class SummaryGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=config.get('openai', 'api_key'))
        self.model = config.get('openai', 'model')
        self.temperature = config.get('openai', 'temperature')
        self.max_tokens = config.get('openai', 'max_tokens')
    
    @error_handler
    def generate_summary(self, paper_content: str) -> str:
        """
        生成论文摘要
        :param paper_content: 论文内容
        :return: 生成的摘要
        """
        try:
            prompt = f"""
            请为以下论文生成一个简洁的摘要，包含主要观点和创新点：
            
            {paper_content}
            
            请用中文回答，并按照以下格式组织：
            1. 研究背景
            2. 主要方法
            3. 创新点
            4. 实验结果
            5. 研究意义
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术论文摘要生成助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            summary = response.choices[0].message.content
            logger.info("成功生成论文摘要")
            return summary
        except Exception as e:
            raise SummaryGenerationError(f"摘要生成失败: {str(e)}")
    
    @error_handler
    def generate_highlights(self, paper_content: str) -> str:
        """
        生成论文亮点
        :param paper_content: 论文内容
        :return: 生成的亮点
        """
        try:
            prompt = f"""
            请为以下论文生成3-5个主要亮点：
            
            {paper_content}
            
            请用中文回答，每个亮点用一句话概括。
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术论文亮点提取助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=500
            )
            
            highlights = response.choices[0].message.content
            logger.info("成功生成论文亮点")
            return highlights
        except Exception as e:
            raise SummaryGenerationError(f"亮点生成失败: {str(e)}")
    
    @error_handler
    def generate_implications(self, paper_content: str) -> str:
        """
        生成研究意义
        :param paper_content: 论文内容
        :return: 生成的研究意义
        """
        try:
            prompt = f"""
            请分析以下论文的研究意义和潜在影响：
            
            {paper_content}
            
            请用中文回答，从学术和实际应用两个角度进行分析。
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术论文意义分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=500
            )
            
            implications = response.choices[0].message.content
            logger.info("成功生成研究意义")
            return implications
        except Exception as e:
            raise SummaryGenerationError(f"研究意义生成失败: {str(e)}")
    
    @error_handler
    def generate_technical_details(self, paper_content: str) -> str:
        """
        生成技术细节
        :param paper_content: 论文内容
        :return: 生成的技术细节
        """
        try:
            prompt = f"""
            请提取以下论文中的关键技术细节：
            
            {paper_content}
            
            请用中文回答，重点说明论文中使用的技术方法和创新点。
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的技术细节提取助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=500
            )
            
            technical_details = response.choices[0].message.content
            logger.info("成功生成技术细节")
            return technical_details
        except Exception as e:
            raise SummaryGenerationError(f"技术细节生成失败: {str(e)}")
    
    @error_handler
    def generate_comprehensive_summary(self, paper: Dict[str, Any]) -> Dict[str, str]:
        """
        生成完整的论文摘要
        :param paper: 论文信息
        :return: 包含各种摘要的字典
        """
        try:
            content = f"""
            标题: {paper['title']}
            作者: {', '.join(paper['authors'])}
            摘要: {paper['summary']}
            """
            
            return {
                'summary': self.generate_summary(content),
                'highlights': self.generate_highlights(content),
                'implications': self.generate_implications(content),
                'technical_details': self.generate_technical_details(content)
            }
        except Exception as e:
            raise SummaryGenerationError(f"完整摘要生成失败: {str(e)}") 