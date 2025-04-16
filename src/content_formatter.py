class ContentFormatter:
    def format_wechat_article(self, paper, summary):
        """
        格式化微信公众号文章
        :param paper: 论文信息
        :param summary: 论文摘要
        :return: 格式化后的文章
        """
        article = f"""
# {paper['title']}

## 作者
{', '.join(paper['authors'])}

## 论文链接
[点击查看原文]({paper['pdf_url']})

## 论文摘要
{paper['summary']}

## 详细解读
{summary}

## 研究意义
本文的创新点在于...（由AI生成的具体分析）

## 相关领域
{', '.join(paper['categories'])}
"""
        return article
    
    def format_xiaohongshu(self, paper, summary):
        """
        格式化小红书内容
        :param paper: 论文信息
        :param summary: 论文摘要
        :return: 格式化后的内容
        """
        content = f"""
📚 今日论文推荐：《{paper['title']}》

👨‍🏫 作者：{', '.join(paper['authors'])}

🔍 研究亮点：
{summary}

💡 创新点：
（由AI生成的具体分析）

#学术 #论文 #科研 #AI
"""
        return content 