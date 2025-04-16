from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class SummaryGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def generate_summary(self, paper_content):
        """
        生成论文摘要
        :param paper_content: 论文内容
        :return: 生成的摘要
        """
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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的学术论文摘要生成助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content 